#!/usr/bin/env python3
import socket
import argparse
import contextlib
import sys
import os
import re
import netaddr
import dns.resolver
from timeout import timeout

parser = argparse.ArgumentParser(description="Python program that snatches banners of accessible ports")

subparsers = parser.add_subparsers(help='sub-command help', dest='command')

## Init subparser
parser_scan = subparsers.add_parser('scan', help='scan host')
parser_scan.add_argument('--host', help='host(s) to scan', nargs='+', metavar='HOST', required='true')
parser_scan.add_argument('-p', '--port', help='port(s) to scan', nargs='+', metavar='PORT', required='true')
parser_scan.add_argument('-o', '--outfile', help='output to file', metavar='FILE')
parser_scan.add_argument('-q', '--quiet', help='suppress output', action="store_true")

args = parser.parse_args()

    
def port_check(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global port_result
    port_result = sock.connect_ex((host,int(port)))
    return port_result


def banner_grab(host, port):
    s = socket.socket()  
    s.connect((host,port))  
    global banner_results
    try:
        global banner
        banner = s.recv(4096)
        banner = banner.decode("utf-8")
        banner_results = 'True'
    except:
        banner_results = 'False'
    s.close()


@timeout(1)
def port_timed_check(host, port, file_write):
    if port_check(host, int(port)) == 0:
        banner_grab(host, int(port))
        if banner_results == 'True':
            if file_write == 'True':
                if non_ip == 'True':
                    f.write(domain_name + ': ' + banner)
                else:
                    f.write(host + ': ' + banner)
            if not args.quiet:
                if non_ip == 'True':
                    print(domain_name + ': ' + banner)
                else:
                    print(host + ': ' + str(banner))

    
def dig(host):
    try:
        for ip in dns.resolver.query(host, 'A'):
            return str(ip)
        dig_error = 'False'
    except dns.resolver.NXDOMAIN:
        if not args.quiet:
            print('Unable to resolve domain ' + host)
        dig_error = 'True'


def port_scan(host, port, file_write):
    try:
        port_timed_check(host, port, file_write)
    except:
        if not args.quiet:
            print('Port ' + str(port) + ' on host ' + str(host) + ' timed out.')


def main():
    if args.outfile:
        outfile = args.outfile
        global f
        f = open(outfile, "a+")
        file_write = 'True'
    else:
        file_write = 'False'
    for host in args.host:
        global non_ip
        if re.match("(?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?)?", host):
            non_ip = 'False'
            ip = netaddr.IPNetwork(host)
            for host in ip:
                host = str(host)
                for port in args.port:
                    port_scan(host, port, file_write)
        else:
            non_ip = 'True'
            global domain_name
            domain_name = host
            ip = dig(host)
            for port in args.port:
                port_scan(ip, port, file_write)

if __name__ == '__main__':
    main()
