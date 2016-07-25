#!/bin/python
# -*- coding: UTF-8 -*-
# ignored, this file store password info
import config_private
import requests
import json


class Mail:
    @classmethod
    def send_mail(cls, subject, text):
        params = {
            "from": "HTDB<beauty@discover.go>",
            "to": config_private.mail_to_address,
            "subject": subject,
            "text": text,
        }
        auth = ("api", config_private.mail_api_key)
        r = requests.post(config_private.mail_http_url, auth=auth, data=params)
        di = json.loads(r.text)
        print "mail response:" + str(r.status_code) + "  " + r.text
        return r.status_code == 200


if __name__ == '__main__':
    r = Mail.send_mail("hi", "hello world")
