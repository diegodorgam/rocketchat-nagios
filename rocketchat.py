#!/usr/bin/python

# Copyright (c) 2015 Andre Freitas <p.andrefreitas@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import urllib2
import json

VERSION = "0.0.1"

CONFIG = {
    "avatar": "https://slack.global.ssl.fastly.net/7bf4/img/services/nagios_128.png", #noqa
    "alias": "Nagios",
    "colors": {
        "OK": "#36a64f",
        "CRITICAL": "#d00000",
        "WARNING": "#daa038",
        "UNKNOWN": "#e3e4e6"
    }
}

TEMPLATE_SERVICE = "{hostalias}/{servicedesc} is {servicestate}:<br/>{serviceoutput}" #noqa
TEMPLATE_HOST = "Host {hostalias} is {hoststate}:<br/>{hostoutput}"  #noqa

def parse():
    parser = argparse.ArgumentParser(description='Sends Rocket.Chat webhooks')
    parser.add_argument('--url', help='Webhook URL', required=True)
    parser.add_argument('--hostalias', help='Host Alias', required=True)
    parser.add_argument('--notificationtype', help='Notification type',
                        required=True)
    parser.add_argument('--hoststate', help='Host State')
    parser.add_argument('--hostoutput', help='Host Output')
    parser.add_argument('--servicedesc', help='Service Description')
    parser.add_argument('--servicestate', help='Service State')
    parser.add_argument('--serviceoutput', help='Service Output')
    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=VERSION))
    args = parser.parse_args()
    return args


def encode_special_characters(text):
    text = text.replace("%", "%25")
    return text

def render_template(template, args):
    text = template.format(**vars(args))
    return encode_special_characters(text)


def create_data(args, config):
    text = render_template(
        TEMPLATE_SERVICE if args.servicestate else TEMPLATE_HOST,
        args
    )
    state = args.servicestate if args.servicestate else args.hoststate
    color = config["colors"][state]
    payload = {
        "alias": config["alias"],
        "avatar": config["avatar"],
        "attachments": [
            {
                "text": text,
                "color": color
            }
        ]
    }

    data = "payload=" + json.dumps(payload)
    return data


def request(url, data):
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response.read()

if __name__ == "__main__":
    args = parse()
    data = create_data(args, CONFIG)
    response = request(args.url, data)
    print response
