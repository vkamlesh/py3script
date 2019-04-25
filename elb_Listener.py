#!/usr/bin/env python3
import boto3.session
import sys
from beautifultable import BeautifulTable

region = sys.argv[1]
profile = sys.argv[2]

session = boto3.session.Session(profile_name = region)
elb_new = session.client('elb',region_name = profile)
table = BeautifulTable()
table.column_headers = ["ELB Name", "Protocol", "LoadBalancerPort", "InstanceProtocol", "InstancePort"]

elb_name = elb_new.describe_load_balancers()


for name in elb_name['LoadBalancerDescriptions']:
    for listner in name['ListenerDescriptions']:
        if 'Listener' in listner.keys():
            for i, j in zip([listner.get('Listener')], range(len([listner.get('Listener')]))):
                    table.insert_row(j,[ name.get('LoadBalancerName'), i.get('Protocol'),  i.get('LoadBalancerPort'),  i.get('InstanceProtocol'),  i.get('InstancePort') ])
print(table)
