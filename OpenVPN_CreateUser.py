#!/usr/bin/env python3
import random
import subprocess
import argparse

"""
This script work us OpenVPN User Management CLI. Currently,Script only can add or delete user. 

"""



def get_opts():
    """Get arguments from the commandline"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--username',help='Username',type=str, required=True)
    parser.add_argument('-a','--add',help='Add User',action='store_true')
    parser.add_argument('-d','--delete',help='Delete User',action='store_true')
    return parser.parse_args()

def create_user(self):
    username=self.username
    gr_name = input("Please enter OpenVPN Group Name\n")
    subprocess.Popen(['/usr/local/openvpn_as/scripts/sacli', '--user', username, '--key', '"type"', '--value', '"user_connect"', 'UserPropPut'])
    subprocess.Popen(['/usr/local/openvpn_as/scripts/sacli', '--user', username, '--key', 'conn_group', '--value', gr_name, 'UserPropPut'])
    p=str(random.randrange(345,999,21))
    password=(username.split(".")[0] + '@' + p)
    subprocess.Popen(['/usr/local/openvpn_as/scripts/sacli', '--user', username, '--new_pass', password, 'SetLocalPassword'])
    subprocess.Popen(['/usr/local/openvpn_as/scripts/sacli', 'start'])
    print("Your username is {} and Password: {}.Pleaes open https://my-vpn.fack.net/ in the browser and download OpenVPN client as per your Laptop's OS.\n".format(username,password))
   

def delete_user(self):
    username=self.username
    subprocess.Popen(['/usr/local/openvpn_as/scripts/sacli', '--user', username, 'UserPropDelAll'])
    subprocess.Popen(['/usr/local/openvpn_as/scripts/sacli', 'start'])
    print("{} deleted from OpenVPN\n".format(username))



def main():
    opt=get_opts()
    if opt.add:
        create_user(opt)
    elif opt.delete:
        delete_user(opt)
    else:
        print("Arguments Missing")


if __name__ == '__main__':
    main()
