#!/usr/bin/python3

import socket
import re
import typing
import optparse
from concurrent.futures import ThreadPoolExecutor
from ipaddress import IPv4Address

import getmac
from mac_vendor_lookup import MacLookup
from Hostinfo import Hostinfo

hosts = set()
is_continuous = False
port_to_scan = 22


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


def read_ip_range(args) -> set:
    if args:
        return parse_ip(args[0].replace(' ', ''))
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
    global port_to_scan
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = sock.connect_ex((str(ip), port_to_scan))
    return not result


def process(ip: IPv4Address):
    try:
        if is_continuous:
            host = get_host_info(ip)
            if host not in hosts:
                host.print()
                hosts.add(host)
        else:
            hosts.add(get_host_info(ip))
    except:
        pass


def get_host_info(ip: IPv4Address):
    if is_ip_available(ip):
        host = Hostinfo(ip)
        try:
            host.name = socket.gethostbyaddr(str(ip))[0]
        except Exception as e:
            pass
        host.mac = get_mac_by_addr(ip)
        host.manufacturer = get_manufacturer_by_addr(host.mac)
        host.ports.add(port_to_scan)
        host.status = "ok"

        return host

    raise Exception(f"Host {ip} is not available")


def get_mac_by_addr(ip: IPv4Address) -> str:
    mac = getmac.get_mac_address(ip=str(ip))
    return mac if mac else "<unknown>"


def get_manufacturer_by_addr(mac: str) -> str:
    if re.findall("[\w]{2}:[\w]{2}:[\w]{2}:[\w]{2}:[\w]{2}:[\w]{2}", mac):
        return MacLookup().lookup(mac)
    else:
        return "<unknown>"


def parse_options():
    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="PORT", type="int", help="Port to scan on hosts")
    parser.add_option("-c", "--continuous", dest="is_continuous", action="store_true", help="continuous print")
    parser.set_defaults(PORT=[22, 80])
    return parser.parse_args()


def main_threading():
    global port_to_scan, is_continuous

    opts, args = parse_options()
    ports = [opts.PORT] if isinstance(opts.PORT, int) else opts.PORT
    is_continuous = opts.is_continuous

    ip_range = read_ip_range(args)
    print("Scanning...")

    for port in ports:
        port_to_scan = port
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(process, ip_range)

    if not is_continuous:
        if hosts:
            print("\n\033[95mHost\t\tPort\t\tName\t\t\tMAC\t\t\tManufacturer\t\tStatus\033[0m")
            for host in sorted(hosts):
                print(host)
        else:
            print(f"\n{Colors.FAIL}Thera are not available hosts {Colors.ENDC}")
        print()


if __name__ == '__main__':
    main_threading()

