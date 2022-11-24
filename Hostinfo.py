from ipaddress import IPv4Address


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


class Hostinfo:
    def __init__(self, ipv4: IPv4Address = "", name: str = "<unknown>", mac: str = "<unknown>"):
        self.ipv4 = ipv4
        self.name = name
        self.mac = mac
        self.manufacturer = "<unknown>"
        self.ports = set()
        self.status = None

    def print(self):
        color_header = Colors.HEADER
        print(f"{color_header}Host{Colors.ENDC}: {self.ipv4},  "
              f"{color_header}Port{Colors.ENDC}: {self.ports},  "
              f"{color_header}name{Colors.ENDC}: {self.name},  "
              f"{color_header}MAC{Colors.ENDC}: {self.mac},  "
              f"{color_header}Vendor{Colors.ENDC}: {self.manufacturer[:20]},  "
              f"{color_header}Status{Colors.ENDC}: {Colors.OKGREEN}{self.status}{Colors.ENDC}")

    def __str__(self):
        if self.status.lower() == "ok":
            return f"{self.ipv4}\t{self.ports}\t\t{self.name}\t\t{self.mac}\t{self.manufacturer[:20]}\t" \
                   f"{Colors.OKGREEN}{self.status}{Colors.ENDC}"
        else:
            return f"{self.ipv4}, {self.name}, {self.mac}, {self.manufacturer}, {Colors.FAIL}{self.status}{Colors.ENDC}"

    def __gt__(self, other):
        return self.ipv4 > other.ipv4

    def __eq__(self, other):
        return self.ipv4 == other.ipv4

    def __hash__(self):
        return hash(self.ipv4)
