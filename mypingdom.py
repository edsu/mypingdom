#!/usr/bin/env python3

import os
import sys
import json
import time
import smtplib

from urllib.request import urlopen

# TODO: maybe this configuration should be in a yaml file?

sites = [
    {
        'name': 'mith',
        'url': 'https://mith.umd.edu',
        'cache_bust': True
    },
    {
        'name': 'docnow',
        'url': 'https://demo.docnow.io/api/v1/world',
        'check': lambda resp: len(json.load(resp)) > 0
    }
]


from_email = 'ehs@pobox.com'
to_email = 'ehs@pobox.com'
smtp_host = 'smtp.pobox.com'
smtp_port = 587
username = 'ehs@pobox.com'
password = os.environ.get('SMTP_PASSWORD') 

if password is None:
    sys.exit('You must set the SMTP_PASSWORD environment variable!')

template = '''From: {from_email:s}
To: {to_email:s}
Subject: {subject:s}

{body:s}
'''

def send_email(alert_name, body):
    try:
        smtp = smtplib.SMTP(smtp_host, smtp_port)
        smtp.starttls()
        smtp.login(username, password)
        msg = template.format(
            from_email=from_email,
            to_email=to_email,
            subject="MyPingdom Alert: {}".format(alert_name),
            body=body
        )
        smtp.sendmail(from_email, [to_email], msg)
    except Exception as e: 
        print('Failed sending message: {}'.format(e))

def check(f, resp):
    try:
        return f(resp)
    except:
        return False

# look at sites and report on any failures by email

for site in sites:
    fail = None

    url = site['url'] 
    if site.get('cache_bust'):
        url += "?t={}".format(time.time())

    try:
        resp = urlopen(url)
        if site.get('check') and not check(site['check'], resp):
            fail = 'Check failed.'
        elif resp.code != 200:
            fail = "Response code not 200 OK."
    except Exception as e:
        fail = str(e)

    if fail is not None:
        send_email(site['name'], 'Failed to get {0}\n\n{1}'.format(site['url'], fail))
