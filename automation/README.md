# SNMP RSU Configuration Automation for Message Forwarding
This directory contains a script that is used for configuring a large number of CDOT Kapsch RSUs autonomously by providing it a list of RSU IPs and some other arguments.

## What the script does
The current script can be run manually from a command line shell. This script needs to be ran externally from an RSU on a separate machine.

The script can currently perform two main tasks:
- Configure an RSU's operate mode. "Standby" and "Operate" are currently the only two supported states.
- Create and overwrite the configuration of an index on the forward message table of an RSU using SNMP.
  - The script currently is only supporting UDP message forwarding

## Running the script
To run the `configrsu_msgfwd.py` script you must provide it some information so that it can do its job and run it on a machine that is configured to use SNMP, specifically `snmpwalk` and `snmpset`. This involves both environment variables and arguments that are provided directly to the script.

- Environment variables os.environ['SNMP_USERNAME'] and os.environ['SNMP_PASSWORD'] must be set. These must be set to the CDOT RSU's SNMP credentials

- A one column CSV or text file containing a list of RSU IP addresses this can look like the following:
```
10.0.0.1
10.0.0.2
10.0.0.3
10.0.0.4
```
- The destination IP. Example: `10.0.1.5`
- The UDP port the RSU should forward the packets to at the destination IP. Example: `46800`
- The RSU index the SNMP configuration should be written to on the RSU. Example: `20`
- Endian type. Little endian = 0. Big endian = 1. Any number outside of these will default to big endian.

These will be provided to the script in the form of arguments.

Check out the example shell command to run the script in a terminal:
```
python3 configrsu_msgfwd.py /home/user/RSU_Management/tests/test_files/snmp_test.csv 10.0.1.5 46800 20 0
```

## Setting up SNMP on external machine
Setting up new VM with SNMP capabilities for CDOT for remote RSU configuration

### Debian Installation Guide
Note: This should work for other Linux distributions (Ubuntu, etc.) just have to use a different package installer

```
sudo apt update
sudo apt install snmpd
sudo apt install snmp
```
Now create or copy the correct MIB profiles in the `/usr/share/snmp/mibs` directory

List of required MIB profiles:
```
IPV6-TC.txt
RSU-MIB.txt
SNMPv2-TC.txt
```

The main MIB profile used for Kapsch RSUs is the `RSU-MIB.txt`. This MIB contains all of the standard methods defined by the USDOT requirements for SNMP standards for RSUs. However, Kapsch has some unique functionality to those standard methods that requires the usage of two other MIB profiles. `IPV6-TC.txt` provides IPV6 address manipulation and reading functionality. `SNMPv2-TC.txt` provides other functionality that the RSU-MIB profile requires. This is specifically for the Kapsch RSUs. Other manufactures may have implemented different MIB profiles to follow the USDOT standard and may require other MIB profiles are just the RSU-MIB.

Running snmpwalk and snmpset commands should now work after this.
