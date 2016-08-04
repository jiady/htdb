from ZhihuDownloadTask import ZhihuDownloadTask
import requests


class TopicDownloadTask(ZhihuDownloadTask):
    def __init__(self, name, logger, mail, retryFail=False, pipeline_key=[]):
        ZhihuDownloadTask.__init__(self, name, logger, mail, retryFail=False, pipeline_key=pipeline_key)

    def taskOperation(self, hash_id):
        request_url = self.httpbase + hash_id + self.topic_tail
        data = set()
        while True:
            r = requests.get(request_url,
                             cookies=self.cookie,
                             headers=self.header)
            response = r.json()
            for t in response["data"]:
                data.add(t["name"])
            if response["paging"]["is_end"]:
                break
            else:
                request_url = response["paging"]["next"]
        self.rclient.sadd("topic/" + hash_id, data)
        return True
