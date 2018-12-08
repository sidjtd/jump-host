#!/usr/bin/env python

import re
import sys
import socket
import paramiko
import csv

the_usr = 'jason'
the_port = '22'
the_host = '104.248.191.147'
ip_pattern = '\(*\d{2,3}(\.\d{1,3}){3}\)*'
mac_pattern = '[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$'
private_pattern = '\(*(?:10|172|192)(\.\d{3}){3}\)*'

# Sort arp results into usable data that analyzes results in digestable format
def sort_list(arr):
    results = {}
    for each in arr:
        sections = each.split(' ')
        
        # If list is too short, disregard this set
        if(len(sections) < 4):
            return
            
        ip = sections[1]
        mac = sections[3]

        # If address is valid but not a private address, continue
        if(not re.match(private_pattern, ip) and re.match(ip_pattern, ip)):
    
            if(re.match(mac_pattern, mac)):

            # results.private

def proxy_connect(host, port, usr, pw, remote_host, remote_port, remote_usr):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=usr, password=pw)
        print('Connected to client')

        ssh_session = client.get_transport().open_session()
        ssh_session.exec_command('arp -a -n')   
        output = ssh_session.recv(1024)
        res_by_line = output.decode().split('\n')
        sort_list(res_by_line)


        while(True):
            print('this is the status of active', ssh_session.active)
            if ssh_session.active:
                command = input(" >>> Input: ")
                client.invoke_shell()

            cmd = str(command).strip().lower()
            if (cmd == 'exit' or cmd == 'clear'):
                print('Goodbye')
                client.close()
                exit(0)
                return
            
            # full_command = 'ssh -t {}@{} {}'.format(remote_usr, remote_host, command)
            # ssh_session.exec_command(full_command)
        
    except(paramiko.AuthenticationException) as e:
        print('Login to jumphost{} failed. \nError: {}'.format(host, e))
        return

    except(paramiko.BadHostKeyException) as e:
        print('Error with bad host key'.format(host, e))
        return

# proxy_connect(the_host, the_port, the_usr, 'jason1977', '10.138.178.218', 22, 'jason')

def main():
    try:
        HOST = '104.248.191.147'
        PORT = 22
        USER = 'jason'
        PASSWORD = 'jason1977'
        TARGET_HOST = '10.138.178.218'
        TARGET_PORT = 22
        TARGET_USER = 'jason'
        proxy_connect(HOST, PORT, USER, PASSWORD, TARGET_HOST, TARGET_PORT, TARGET_USER)
    
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit()

if __name__ == "__main__":
    main()