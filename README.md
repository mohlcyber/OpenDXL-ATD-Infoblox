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

<img width="395" alt="screen shot 2018-04-08 at 16 50 28" src="https://user-images.githubusercontent.com/25227268/38468918-07628742-3b4d-11e8-98fd-e5c821c04836.png">

Create Certificates for OpenDXL ([Link](https://opendxl.github.io/opendxl-client-python/pydoc/epoexternalcertissuance.html)). 

Make sure that the FULL PATH to the config file is entered in line 17 (atd_subscriber.py).
