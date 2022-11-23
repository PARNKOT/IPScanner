#!/usr/bin/python3

import asyncio
import socket
import sys
import re
import typing
from concurrent.futures import ThreadPoolExecutor
from ipaddress import IPv4Address


available_ip = set()


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def read_ip_range() -> set:
    if len(sys.argv) > 1:
        return parse_ip(sys.argv[1].replace(' ', ''))
    else:
        return parse_ip(input("IP range to scan: ").replace(' ', ''))


def parse_ip(ip: str) -> set:
    ip_set = set()

    if '-' in ip:
        ip_set = ip_range_to_list(*ip.split('-'))
    elif ',' in ip:
        ip_set = set([IPv4Address(ip) for ip in ip.split(',')])
    else:
        ip_set.add(IPv4Address(ip))

    if validate_ip(ip_set):
        return ip_set
    raise ValueError("Some ip addresses are incorrect")


def ip_range_to_list(ip_min: str, ip_max: str) -> set:
    ip1 = IPv4Address(ip_min)
    ip2 = IPv4Address(ip_max)
    ip_set = set()

    while ip1 != ip2:
        ip_set.add(ip1)
        ip1 += 1
    ip_set.add(ip2)

    return ip_set


def validate_ip(ip_list: typing.Iterable) -> bool:
    for ip in ip_list:
        if not re.fullmatch("([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})", str(ip)):
            return False
    return True


def is_ip_available(ip: IPv4Address) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = sock.connect_ex((str(ip), 22))
    return not result


def check_ip_availability(ip: IPv4Address):
    if is_ip_available(ip):
        available_ip.add(ip)


def main_threading():
    ip_range = read_ip_range()
    print("Scanning...")

    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_ip_availability, ip_range)

    if available_ip:
        print("\nHost\t\tstatus")
        for ip in sorted(available_ip):
            print(f"{Colors.OKGREEN}{ip}\tok {Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}Thera are not available hosts {Colors.ENDC}")
    print()


if __name__ == '__main__':
    main_threading()

