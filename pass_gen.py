#!/usr/bin/env python3

import sys
import string
import secrets
import re
import hashlib
import argparse
import getpass

def get_opts():

    """Get arguments from the commandline"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--length', help='Password Length', type=int, required=True)
    parser.add_argument('-md5sum', help="md5sum of password", type=str, )
    parser.add_argument('-p', '--password', help="User define password", type=str)

    return parser.parse_args()



def pass_gen(self):
    #sys.exit("The Opts value is {}".format(self))

    if self.length < 8 or self.length > 12:
        sys.exit("The password must be between 6 and 12 characters.\n")
    else:
        special_ch="($%&*+-/?@\!#^~)"
        alphabet = string.ascii_letters + string.digits + special_ch

        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(self.length))
            if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any([c for c in password if c in special_ch])
            and sum(c.isdigit() for c in password) >= 3):
                break
    return(password)


def pass_checker(self):
    if ' ' in self.password:
        sys.exit("The password contain Whitespce")

    password_rate = {0:'Bad', 2:'Weak', 3:'Medium', 4:'Strong'}
    password_strength = dict.fromkeys(['has_upper', 'has_lower', 'has_num', 'has_special'], False)

    if re.search(r'[A-Z]', self.password):
        password_strength['has_upper'] = True
    if re.search(r'[a-z]', self.password):
        password_strength['has_lower'] = True
    if re.search(r'[0-9]', self.password):
        password_strength['has_num'] = True
    if re.search(r"\W", self.password):
        password_strength['has_special'] = True

    score = len([b for b in password_strength.values() if b])

    return(password_rate[score])

def encode(self):

    encode_pwd = hashlib.md5(self.password.encode('utf-8')).hexdigest()
    print("You password md5sum is {}".format(encode_pwd))
    return encode_pwd

def main():
    opts=get_opts()

    if opts.length:
        pas=pass_gen(opts)
        print("New Password {}".format(pas))
    elif opts.password:
        check=pass_checker(opts)
        print("Password Stregnth {}".format(check))
    elif opts.md5sum:
        md5=encode(opts)
        print("MD5SUM: {}".format(md5))
    else:
        print("Arguments Missing")





if __name__ == '__main__':
    main()
