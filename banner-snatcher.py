#!/usr/bin/env python3
import socket
import argparse
import contextlib
import sys
import os
from timeout import timeout

parser = argparse.ArgumentParser(description="Python program that snatches banners of accessible ports")

subparsers = parser.add_subparsers(help='sub-command help', dest='command')

## Init subparser
parser_scan = subparsers.add_parser('scan', help='scan host')
parser_scan.add_argument('--host', help='host(s) to scan', nargs='+', metavar='HOST', required='True')
parser_scan.add_argument('-p', '--port', help='port(s) to scan', nargs='+', metavar='PORT', required='True')
parser_scan.add_argument('-o', '--outfile', help='output to file', metavar='FILE')
parser_scan.add_argument('-q', '--quiet', help='suppress output', action="store_true")

args = parser.parse_args()


def check_host(host):
    socket.gethostbyname(host)

    
def port_check(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global port_result
    port_result = sock.connect_ex((host,port))
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

@timeout(1)
def port_timed_check(host, port, file_write):
    if port_check(host, int(port)) == 0:
        banner_grab(host, int(port))
        if banner_results == 'True':
            if file_write == 'True':
                f.write(host + ': ' + banner)
            if not args.quiet:
                print(host + ': ' + str(banner))
    


def main():
    if args.outfile:
        outfile = args.outfile
        global f
        f = open(outfile, "a+")
        file_write = 'True'
    else:
        file_write = 'False'
    for host in args.host:
        try:
            check_host(host)
            for port in args.port:
                try:
                    port_timed_check(host, port, file_write)
                except:
                    print('Port ' + port + ' on host ' + host + ' timed out.')
                
        except socket.gaierror:
            print(host + ' is an invalid host.')
     

if __name__ == '__main__':
    main()
