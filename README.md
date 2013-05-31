[fabrician.org](http://fabrician.org/)
==========================================================================
Apache ActiveMQ Enabler Guide
==========================================================================

Introduction
--------------------------------------
A Silver Fabric Enabler allows an external application or application platform, such as a J2EE application server to run in a TIBCO Silver Fabric software environment. The Apache ActiveMQ Enabler for Silver Fabric provides integration between Silver Fabric and Apache ActiveMQ. The Enabler automatically provisions, orchestrates, controls and manages an Apache ActiveMQ environment. 

Supported Platforms
--------------------------------------
* Silver Fabric 5
* Windows, Linux

Installation
--------------------------------------
The Apache ActiveMQ Enabler consists of an Enabler Runtime Grid Library and a Distribution 
Grid Library. The Enabler Runtime contains information specific to a Silver Fabric version that is used to integrate the Enabler, and the Distribution contains the application server or program used for the 
Enabler. Installation of the Apache ActiveMQ Enabler involves copying these Grid 
Libraries to the SF_HOME/webapps/livecluster/deploy/resources/gridlib directory on the Silver Fabric Broker. 

Testing the Deployment
--------------------------------------
* Start an ActiveMQ Component on Silver Fabric.  See the TIBCO Silver Fabric documentation for more information.
* Connect to the Engine machine. Using a cmd (Windows) or a shell (Linux).
* cd to: [SF Engine installation dir]/work/[hostname-instance]/fabric/apache-activemq/example
* modify the build.xml there so that the property "url" is set to "discovery://(multicast://default)"
* type: ant producer
* You need Apache Ant installed in the box. This should create the example queue and send 2000 messages to it. If you've left the example JMX_OBJECT_NAME, you'll see the "Queue Size" statistics increase to 2000.

Runtime Grid Library
--------------------------------------
The Enabler Runtime Grid Library is created by building the maven project:
```bash
mvn package
```
The version of the distribution can be optionally overridden:
```bash
mvn package -Ddistribution.version=5.7.0
```

Distribution Grid Library
--------------------------------------
The Distribution Grid Library is created by performing the following steps:
* Download the Apache ActiveMG binaries from http://activemq.apache.org/activemq-570-release.html.
* The Windows (.zip) and Linux (tar.gz) archives can be combined into one distribution or created separately.
* Build the maven project with the location of the archive, operating system target and optionally the version.  Operating system is typically 'all', 'win32,win64' or 'linux,linux64'.

```bash
mvn package -Ddistribution.location=/home/you/Downloads/apache-activemq-5.7.0-bin.tar.gz -Ddistribution.version=5.7.0 -Ddistribution.os=linux,linux64
```

Statistics
--------------------------------------
<table>
    <tr>
        <th>Name</th>
        <th>Description</th>
        <th>Units</th>
    </tr>
    <tr>
        <td>Queue Size</td>
        <td>Size of the Message Queue.</td>
        <td>messages</td>
    </tr>
</table>


Runtime Context Variables
--------------------------------------
<table>
    <tr>
        <th>Variable</th>
        <th>Type</th>
        <th>Description</th>
        <th>Default Value</th>
    </tr>
    <tr>
        <td>JDK_VERSION</td>
        <td>String</td>
        <td>The Java SDK version used by Active MQ.</td>
        <td>1.6.0.23</td>
    </tr>
    <tr>
        <td>NIO_PORT</td>
        <td>String</td>
        <td>The NIO port used by Active MQ.</td>
        <td>8162</td>
    </tr>
    <tr>
        <td>JMX_PORT</td>
        <td>Environment</td>
        <td>The JMX port opened by Active MQ, one can for instance, connect to it using jconsole.</td>
        <td>1099</td>
    </tr>
    <tr>
        <td>TCP_PORT</td>
        <td>String</td>
        <td>The TCP port used by Active MQ.</td>
        <td>61616</td>
    </tr>
    <tr>
        <td>BROKER_NAME</td>
        <td>String</td>
        <td>The name of the Active MQ broker, anything is valid, but make sure all brokers in a network have different names.</td>
        <td>${ENGINE_USERNAME}-${ENGINE_INSTANCE}</td>
    </tr>
    <tr>
        <td>HOST_JMX_PORT</td>
        <td>String</td>
        <td>The HOST JMX port.</td>
        <td>2011</td>
    </tr>
    <tr>
        <td>JMX_DOMAIN_NAME</td>
        <td>String</td>
        <td>The JMX domain name.</td>
        <td>testdomain</td>
    </tr>
    <tr>
        <td>JMX_OBJECT_NAME</td>
        <td>String</td>
        <td>This is a reasonable object to check for statistics in the examples that come with ActiveMQ, please change this to anything that suits your environemnt.</td>
        <td>testdomain:BrokerName=${ENGINE_USERNAME}-${ENGINE_INSTANCE},Type=Queue,Destination=TEST.FOO</td>
    </tr>
    <tr>
        <td>JMX_ATTRIBUTE</td>
        <td>String</td>
        <td>Together with the previous variable, this defines the statistics to be used with this component.</td>
        <td>QueueSize</td>
    </tr>
</table>
