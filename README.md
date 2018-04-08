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
