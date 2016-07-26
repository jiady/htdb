#!/bin/python
# -*- coding: UTF-8 -*-
# ignored, this file store password info
import config_private
import requests
import json
import time


class Mail:
    def __init__(self, flog):
        self.time_lock = {}
        self.flog = flog

    def send_timed(self, second_lock, subject, text):
        if (subject in self.time_lock) and self.time_lock[subject] + second_lock < time.time():
            self.flog.info("not send mail due to time_lock:sub:%s,text:%s", subject, text)
            return
        else:
            self.time_lock[subject] = time.time()
            self.send_retry(subject, text)

    def send_retry(self, subject, text):
        t = 1
        while not self.send_mail(subject, text):
            time.sleep(t)
            t *= 2
            if t > 512:
                self.flog.error("send mail failed");
                break

    def send_mail(self, subject, text):
        params = {
            "from": "HTDB<beauty@discover.go>",
            "to": config_private.mail_to_address,
            "subject": subject,
            "text": text,
        }
        auth = ("api", config_private.mail_api_key)
        r = requests.post(config_private.mail_http_url, auth=auth, data=params)
        self.flog.info("send mail:sub:%s,text:%s", subject, text)
        self.flog.info("send mail result:%d, %s", r.status_code, r.text)
        return r.status_code == 200


if __name__ == '__main__':
    r = Mail.send_mail(u"汉语", "hello world")
