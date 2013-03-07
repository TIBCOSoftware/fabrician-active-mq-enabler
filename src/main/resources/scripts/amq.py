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
    connectionArgs = (host, port)

    #Establish Connection to JMX Server
    serviceURL = str()
    serviceURL = "service:jmx:rmi:///jndi/rmi://"
    serviceURL = serviceURL + host + ":" + str(port) + "/jmxrmi"       

    url = javax.management.remote.JMXServiceURL(serviceURL);
    connector = javax.management.remote.JMXConnectorFactory.connect(url);
    global remote
    remote = connector.getMBeanServerConnection();
    brokername=proxy.container.getRuntimeContext().getVariable("BROKER_NAME").getValue()
    domainname=proxy.container.getRuntimeContext().getVariable("JMX_DOMAIN_NAME").getValue()
    objn=domainname+":BrokerName="+brokername+",Type=Broker"
    obn = javax.management.ObjectName(objn);
    result = remote.invoke(obn,"stop",None,None)
 #   begin = System.currentTimeMillis()
 #  proxy.doShutdown()
 #  proxy.getContainer().waitForShutdown(begin)

###
# Retrieve container metrics
###
def getStatistic(statName):
    statValue = 0.0

    host="localhost"
    portv=proxy.container.getRuntimeContext().getVariable("JMX_PORT").getValue();
    port=int(portv)
    connectionArgs = (host, port)

    #Establish Connection to JMX Server
    serviceURL = str()
    serviceURL = "service:jmx:rmi:///jndi/rmi://"
    serviceURL = serviceURL + host + ":" + str(port) + "/jmxrmi"       

    url = javax.management.remote.JMXServiceURL(serviceURL);
    connector = javax.management.remote.JMXConnectorFactory.connect(url);
    global result
    result = "0.0"
    global remote
    remote = connector.getMBeanServerConnection();
    objn=proxy.container.getRuntimeContext().getVariable("JMX_OBJECT_NAME").getValue();
    attribute=proxy.container.getRuntimeContext().getVariable("JMX_ATTRIBUTE").getValue();
    obn = javax.management.ObjectName(objn);
    exists = remote.isRegistered(obn);
    if exists:
        result = str(remote.getAttribute(obn, attribute))
    statValue = float(result)
    return statValue

###
# Check if it worked
###
def hasContainerStarted():
    time.sleep(60)
    host="localhost"
    portv=proxy.container.getRuntimeContext().getVariable("JMX_PORT").getValue();
    port=int(portv)
    connectionArgs = (host, port)

    #Establish Connection to JMX Server
    serviceURL = str()
    serviceURL = "service:jmx:rmi:///jndi/rmi://"
    serviceURL = serviceURL + host + ":" + str(port) + "/jmxrmi"       
    try:
      url = javax.management.remote.JMXServiceURL(serviceURL);
      connector = javax.management.remote.JMXConnectorFactory.connect(url);
      global remote
      remote = connector.getMBeanServerConnection()
      brokername=proxy.container.getRuntimeContext().getVariable("BROKER_NAME").getValue()
      domainname=proxy.container.getRuntimeContext().getVariable("JMX_DOMAIN_NAME").getValue()
      objn=domainname+":BrokerName="+brokername+",Type=Broker"
      obn = javax.management.ObjectName(objn)
      attribute="BrokerName";
      result = remote.getAttribute(obn, attribute)

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
    port=int(portv)
    connectionArgs = (host, port)

    #Establish Connection to JMX Server
    serviceURL = str()
    serviceURL = "service:jmx:rmi:///jndi/rmi://"
    serviceURL = serviceURL + host + ":" + str(port) + "/jmxrmi"       
    try:
      url = javax.management.remote.JMXServiceURL(serviceURL);
      connector = javax.management.remote.JMXConnectorFactory.connect(url);
      global remote
      remote = connector.getMBeanServerConnection();
      brokername=proxy.container.getRuntimeContext().getVariable("BROKER_NAME").getValue();
      domainname=proxy.container.getRuntimeContext().getVariable("JMX_DOMAIN_NAME").getValue();
      objn=domainname+":BrokerName="+brokername+",Type=Broker";
      obn = javax.management.ObjectName(objn);
      attribute="BrokerName";
      result = remote.getAttribute(obn, attribute);

    except Exception, value:
      logger.severe("ActiveMQ is not running.")
      logger.severe(value)
      return False
    return True
