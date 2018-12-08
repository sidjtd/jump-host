# Jump Host File

This repo contains the following files that allow SSH access into a user-provided IP address by the following steps:

* Create password list using criteria set in config.cfg file and running pass-brute-gen.py

* Run ssh-commands.py (currently defaulting to address 104.248.191.147

* Result should result in execution returning additional IP addresses affilicated with given address should SSH be successful.

Currently being implemented: Using REGEX, validate all IP addresses that are private by evaluating if first set of IP Octet start with 10, 172, or 192.

Those IP Addresses that fit the above criteria but lack a valid MAC address (ie: like 10.138.178.147 in exercise) will be marked as a non-applicable IP addresses 
