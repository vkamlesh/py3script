#!/usr/bin/env python3
import netaddr
import argparse
import fileinput
import sys, re

# Extract only IPv4 addresses by default
default_proto = 4

parser = argparse.ArgumentParser(
    description='''If invoked with one or more filenames as arguments, ipx reads the named files.
It may also be invoked with no arguments, in which case it will read from
standard input.  In either case, it searches through the input data and prints
out all of the IP addresses that it finds, one per line.  There is no guarantee
that the same IP address won't be printed more than once; if you need that
guarantee, pipe the results through sort and uniq.'''
)
parser.add_argument('file', nargs='*', help="file(s) to parse",
                    )
addr_group = parser.add_mutually_exclusive_group()
addr_group.add_argument('-4', action='store_const', dest='proto',
                        const=4, help='Extract only IPv4 addresses (default)')
addr_group.add_argument('-6', action='store_const', dest='proto',
                        const=6, help='Extract only IPv6 addresses')
addr_group.add_argument('-a', '--all', action='store_const', dest='proto',
                        const=None, help='Extract IPv4 and IPv6 addresses')
parser.set_defaults(proto=default_proto)
ipv4_sre = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
ipv6_re = re.compile(r"[0-9a-f]{0,4}:[0-9a-f]{0,4}:[0-9a-f:]{0,38}")

# This mess stolen from
# http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
ipv6_sre = r"""
        (?!.*::.*::)                # Only a single whildcard allowed
        (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
        (?:                         # Repeat 6 times:
            [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
        ){6}                        #
        (?:                         # Either
            [0-9a-f]{0,4}           #   Another group
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
            [0-9a-f]{0,4}           #   Last group
            (?: (?<=::)             #   Colon iff preceeded by exacly one colon
             |  (?<!:)              #
             |  (?<=:) (?<!::) :    #
             )                      # OR
         |                          #   A v4 address with NO leading zeros
            (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            (?: \.
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            ){3}
        )
    """
#re.VERBOSE | re.IGNORECASE )

def get_ip_regex(proto=None):
    if   4 == proto:
        ip_sre = ipv4_sre
    elif 6 == proto:
        ip_sre = ipv6_sre
    #else:
        #ip_sre = r"(?:%s)|(?:%s)" % (ipv6_sre, ipv4_sre)
    return re.compile(ip_sre, re.VERBOSE|re.IGNORECASE)


def ipx_line(ip_re, line, proto=None):
    ips = []
    for i in ip_re.findall(line):
        try:
            # We could specify the protocol version here, but the regexes
            # are strict enough that there's no need
            ips.append(netaddr.IPAddress(i))
        except netaddr.AddrFormatError:
            pass

    return ips

if __name__ == '__main__':
    args = parser.parse_args()

    ip_re = get_ip_regex(args.proto)

    # If we're reading from stdin, don't use fileinput.
    # The fileinput module buffers stdin until you hit Ctrl-D, meaning that
    # for the common use case of pasting input into a pipeline of the form
    # 'ipx | xargs', you need to hit Ctrl-D twice. This is maddening.
    if 0 == len(args.file):
        for line in sys.stdin.readlines():
            for i in ipx_line(ip_re, line):
                print(i)
        sys.exit(0)

    for line in fileinput.input(args.file):
        for i in ipx_line(ip_re, line):
            print(i)
