# Copyright 2012 TIBCO Software Inc. All rights reserved.

from java.lang import Class
from java.lang import System
from java.util import Properties
from java.sql import Statement, ResultSet
from jarray import array

import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;
import java.lang.management.ManagementFactory;
import sys, socket, time

from com.datasynapse.fabric.admin.info import GridlibInfo
from com.datasynapse.fabric.container import LifecycleCommand


###
# Initialize the container
###
def doInit(additionalVariables):

    logger.info("Setting life-cycle commands for the Container")
    
    windowsCommand = LifecycleCommand()
    windowsCommand.startupCommand = '"${CONTAINER_WORK_DIR}/apache-activemq/bin/activemq.bat"'
    windowsCommand.shutdownCommand = '"${CONTAINER_WORK_DIR}/apache-activemq/bin/activemq.bat"'
    
    unixCommand = LifecycleCommand()
    unixCommand.startupCommand = "${CONTAINER_WORK_DIR}/apache-activemq/bin/activemq start"
    unixCommand.shutdownCommand = "${CONTAINER_WORK_DIR}/apache-activemq/bin/activemq stop"

    proxy.container.blocking = False
    proxy.container.windowsCommand = windowsCommand
    proxy.container.unixCommand = unixCommand

###
# Shutdown and wait for the container to gracefully shutdown
###
def doShutdown():

    host="localhost"
    portv=proxy.container.getRuntimeContext().getVariable("JMX_PORT").getValue();
    port=int(portv)
    connector = getJMXConnection(host,portv)
    
    brokername=proxy.container.getRuntimeContext().getVariable("BROKER_NAME").getValue()
    domainname=proxy.container.getRuntimeContext().getVariable("JMX_DOMAIN_NAME").getValue()
    objn=domainname+":BrokerName="+brokername+",Type=Broker"
    obn = javax.management.ObjectName(objn);

    invokeJMXObject(connector, obn, "stop")

###
# Retrieve container metrics
###
def getStatistic(statName):

    logger.info("Getting stats")
    logger.info("Name: "+statName)
    if statName == "Custom JMX Object":
        statValue = 0.0
        host="localhost"
        portv=proxy.container.getRuntimeContext().getVariable("JMX_PORT").getValue();
        objn=proxy.container.getRuntimeContext().getVariable("JMX_OBJECT_NAME").getValue();
        attribute=proxy.container.getRuntimeContext().getVariable("JMX_ATTRIBUTE").getValue();
        obn = javax.management.ObjectName(objn);

        connector = getJMXConnection(host,portv)
        default = "0.0"
        result = getJMXAttribute(connector, obn, attribute, default)
        statValue = float(result)
        return statValue

###
# Check if it worked
###
def hasContainerStarted():
    time.sleep(60)
    host="localhost"
    portv=proxy.container.getRuntimeContext().getVariable("JMX_PORT").getValue();
    brokername=proxy.container.getRuntimeContext().getVariable("BROKER_NAME").getValue();
    domainname=proxy.container.getRuntimeContext().getVariable("JMX_DOMAIN_NAME").getValue();

    connector = getJMXConnection(host,portv)
 
    try:
  
        objn=domainname+":BrokerName="+brokername+",Type=Broker";
        obn = javax.management.ObjectName(objn);
        attribute="BrokerName"
        default="0"
        result = getJMXAttribute(connector, obn, attribute, default)
        if result == "0":
            logger.severe("ActiveMQ is not running.")
            return False
    except Exception, value:
        logger.severe("ActiveMQ is not running.")
        logger.severe(value)
        return False
    return True

###
# Check if it's running
###
def isContainerRunning():

    host="localhost"
    portv=proxy.container.getRuntimeContext().getVariable("JMX_PORT").getValue();
    brokername=proxy.container.getRuntimeContext().getVariable("BROKER_NAME").getValue();
    domainname=proxy.container.getRuntimeContext().getVariable("JMX_DOMAIN_NAME").getValue();

    connector = getJMXConnection(host,portv)
 
    try:
        objn=domainname+":BrokerName="+brokername+",Type=Broker";
        obn = javax.management.ObjectName(objn);
        attribute="BrokerName"
        default="0"
        result = getJMXAttribute(connector, obn, attribute, default)
        if result == "0":
            logger.severe("ActiveMQ is not running.")
            return False
    except Exception, value:
        logger.severe("ActiveMQ is not running.")
        logger.severe(value)
        return False
    return True

###############
# Some JMX utilities
#################
def getJMXConnection(host,portv):
    
    port=int(portv)
    connectionArgs = (host, port)


    serviceURL = str()
    serviceURL = "service:jmx:rmi:///jndi/rmi://"
    serviceURL = serviceURL + host + ":" + str(port) + "/jmxrmi"

    url = javax.management.remote.JMXServiceURL(serviceURL);
    connector = javax.management.remote.JMXConnectorFactory.connect(url);
    return connector

def getJMXAttribute(connector, obn, attribute, default):    
    result = default
    remote = connector.getMBeanServerConnection();
    exists = remote.isRegistered(obn);
    if exists:
        result = str(remote.getAttribute(obn, attribute))
    else:
        result = default
    return result

def invokeJMXObject(connector, obn, action):
    remote = connector.getMBeanServerConnection();
    remote.invoke(obn,action,None,None)
