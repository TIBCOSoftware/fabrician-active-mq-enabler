[fabrician.org](http://fabrician.org/) - Apache ActiveMQ Enabler Guide
==========================================================================

Introduction
--------------------------------------
A Silver Fabric Enabler allows an external application or application platform, such as a J2EE application server to run in a TIBCO Silver Fabric software environment. The Apache ActiveMQ Enabler for Silver Fabric provides integration between Silver Fabric and Apache ActiveMQ. The Enabler automatically provisions, orchestrates, controls and manages an Apache ActiveMQ environment. 

Installation
--------------------------------------
The Apache ActiveMQ Enabler consists of an Enabler Runtime Grid Library and a Distribution 
Grid Library. The Enabler Runtime contains information specific to a Silver Fabric version that is used to integrate the Enabler, and the Distribution contains the application server or program used for the 
Enabler. Installation of the Apache ActiveMQ Enabler involves copying these Grid 
Libraries to the SF_HOME/webapps/livecluster/deploy/resources/gridlib directory on the Silver Fabric Broker. 

Runtime Grid Library
--------------------------------------
The Enabler Runtime Grid Library is created by building the maven project.

Distribution Grid Library
--------------------------------------
The Distribution Grid Library is created by performing the following steps for each platform:
* Download and extract the Apache ActiveMG binaries from http://activemq.apache.org/activemq-570-release.html.
* TBD
* Create a grid-library.xml file and place it next to the root directory.
* Create a tar.gz or zip of the contents.

```XML
    <?xml version="1.0" encoding="windows-1250"?>
    <grid-library os="all">
        <grid-library-name>activemq-distribution</grid-library-name>
        <grid-library-version>5.7.0</grid-library-version>
    </grid-library>
```
Statistics
--------------------------------------
* **Queue Size** - Size of the Message Queue.

Runtime Context Variables
--------------------------------------
* **JDK_VERSION** - The Java SDK version used by Active MQ.
    * Type: String
    * Default value: 1.6.0.23
* **NIO_PORT** - The NIO port used by Active MQ.
    * Type: String
    * Default value: 8162
* **JMX_PORT** - The JMX port opened by Active MQ, one can for instance, connect to it using jconsole.
    * Type: Environment
    * Default value: 1099
* **TCP_PORT** - The TCP port used by Active MQ.
    * Type: String
    * Default value: 61616
* **BROKER_NAME** - The name of the Active MQ broker, anything is valid, but make sure all brokers in a network have different names.
    * Type: String
    * Default value: ${ENGINE_USERNAME}-${ENGINE_INSTANCE}
* **HOST_JMX_PORT** - 
    * Type: String
    * Default value: 2011
* **JMX_DOMAIN_NAME** - 
    * Type: String
    * Default value: testdomain
* **JMX_OBJECT_NAME** - This is a reasonable object to check for statistics in the examples that come with ActiveMQ, please change this to anything that suits your environemnt.
    * Type: String
    * Default value: "testdomain:BrokerName=${ENGINE_USERNAME}-${ENGINE_INSTANCE},Type=Queue,Destination=TEST.FOO"
* **JMX_ATTRIBUTE** - Together with the previous variable, this defines the statistics to be used with this component.
    * Type: String
    * Default value: QueueSize