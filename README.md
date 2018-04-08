# OpenDXL-ATD-Infoblox
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This integration is focusing on the automated threat response with McAfee ATD, OpenDXL and Infobox. McAfee Advanced Threat Defense (ATD) will produce local threat intelligence that will be pushed via DXL. An OpenDXL wrapper will subscribe and parse IP and URL indicators ATD produced and will automatically update Infoblox RPZ rules.

## Component Description

**McAfee Advanced Threat Defense (ATD)** is a malware analytics solution combining signatures and behavioral analysis techniques to rapidly identify malicious content and provides local threat intelligence. ATD exports IOC data in STIX format and DXL.
https://www.mcafee.com/in/products/advanced-threat-defense.aspx

**Infoblox Grid** empowers you to control and secure next generation data centers, hybrid cloud deployments, and on premises infrastructure centrally and seamlessly. With Infoblox, you gain capabilities that enhance every aspect of network agility, visibility, security, and cost control.
https://www.infoblox.com/

## Prerequisites
McAfee ATD solution (tested with ATD 4.0.4)

Infoblox Grid (tested with NIOS 8.2.4 - IB-V1415)

Requests ([Link](http://docs.python-requests.org/en/master/user/install/#install))

OpenDXL SDK ([Link](https://github.com/opendxl/opendxl-client-python))
```sh
git clone https://github.com/opendxl/opendxl-client-python.git
cd opendxl-client-python/
python setup.py install
```

McAfee ePolicy Orchestrator, DXL Broker

## Configuration
Enter the Infoblox ip, username and password in the ib_push.py file (line 113, 114, 115).

Enter a Local Response Policy Zone groupname that should be used for malicious IP and Domains (ib_push.py - line 118).

<img width="328" alt="screen shot 2018-04-08 at 16 52 49" src="https://user-images.githubusercontent.com/25227268/38468937-4dc502aa-3b4d-11e8-9e65-12ff5e488116.png">

Create Certificates for OpenDXL ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epoexternalcertissuance.html)). 

Make sure that the FULL PATH to the config file is entered in line 17 (atd_subscriber.py).

## Process Description
McAfee ATD receives files from multiple sensors like Endpoints, Web Gateways, Network IPS or via Rest API. 
ATD will perform malware analytics and produce local threat intelligence. After an analysis every IOC will be published via the Data Exchange Layer (topic: /mcafee/event/atd/file/report). 

### atd_subscriber.py
The atd_subscriber.py receives DXL messages from ATD, filters out discovered IP's and URL's and loads ib_push.py.

### ib_push.py
The ib_push.py receives the discovered malicious IP's and URL's and will use the Infoblox API's to update the Local Response Policy Zone.

The script will:

1. create a new api session 
2. check if the RPZ group exist already and create it if it doesn't
3. check if IP or URL / domain exist already and create it if it doesn't
4. logout

<img width="957" alt="screen shot 2018-04-08 at 19 31 57" src="https://user-images.githubusercontent.com/25227268/38470455-8cdeb31c-3b63-11e8-8c7a-165e5564ec98.png">

## Run the OpenDXL wrapper
> python atd_subscriber.py

or

> nohup python atd_subscriber.py &

## Summary
With this use case, ATD produces local intelligence that is immediatly updating policy enforcement points like the 
DNS blackholing solutions with malicious IP's and URL's.
