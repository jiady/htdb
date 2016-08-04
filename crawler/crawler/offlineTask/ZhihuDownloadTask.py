from myTask import Task
import requests
import json
import abc
import time


class ZhihuDownloadTask(Task):
    header = None
    http_people_base = "https://api.zhihu.com/people/"
    topic_tail = "/following_topic?offset=0"
    answers_tail = "/answers?order_by=created&offset=0&limit=20"

    def __init__(self, name, logger, mail, retryFail=False, pipeline_key=[]):
        Task.__init__(self, name, logger, mail, retryFail=retryFail, pipeline_key=pipeline_key)
        Task.task_sleep = 7

    def getInitQueue(self):
        return Task.getInitQueueBySetNames(self, "target-has-face")

    def filter_out(self, hash_id):
        r = Task.rclient.get("people/" + hash_id)
        return json.loads(r)["school"] == "not-found"

    def get(self, url):
        time.sleep(Task.task_sleep)
        self.logger.info("getting " + url)
        response = requests.get(url, cookies=self.cookie, headers=self.header)
        self.logger.info("response:" + str(response.status_code))
        return response

    def post(self, url, payload):
        return requests.post(url, cookies=self.cookie, headers=self.header, data=payload)

    def init(self):
        auth = Task.rclient.get("crawler/auth")
        auth_info = json.loads(auth)
        self.access_token = auth_info["access_token"]
        self.cookie = auth_info["cookie"]
        self.auth_type = auth_info["token_type"]
        self.header = {
            "Authorization": self.auth_type.capitalize() + " " + self.access_token,
            "x-api-version": "3.0.23",
            "x-app-version": "4.4.0",
            "x-app-za": "OS=Android&Release=6.0.1&Model=MI+NOTE+LTE&VersionName=4.4.0&VersionCode=413&Width=1080&Height=1920&Installer=%E5%BA%94%E7%94%A8%E5%86%85%E5%8D%87%E7%BA%A7",
            "x-app-build": "release",
            "Connection": "Keep-Alive",
            "Host": "api.zhihu.com",
            "User-Agent": "Futureve/4.4.0 Mozilla/5.0 (Linux; Android 6.0.1; MI NOTE LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36 Google-HTTP-Java-Client/1.20.0 (gzip)",
            "Accept-Encoding": "gzip",
        }

    @abc.abstractmethod
    def taskOperation(self, hash):
        pass
