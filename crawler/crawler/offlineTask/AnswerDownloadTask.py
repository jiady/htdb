from ZhihuDownloadTask import ZhihuDownloadTask
import requests
from pymongo import MongoClient, HASHED


class AnswerDownloadTask(ZhihuDownloadTask):
    def __init__(self, name, logger, mail, retryFail=False, pipeline_key=[]):
        ZhihuDownloadTask.__init__(self, name, logger, mail, retryFail=retryFail, pipeline_key=pipeline_key)
        self.mclient = MongoClient('localhost', 27017)
        self.colletions = self.mclient.zhihu_db.answers
        self.colletions.create_index([('hash_id', HASHED)])

    def taskOperation(self, hash_id):
        answers_to_store = list()
        request_url = self.http_people_base + hash_id + self.answers_tail
        data = set()
        while True:
            r = self.get(request_url)
            response = r.json()
            for t in response["data"]:
                url = t["url"]
                answer = self.get(url).json()
                answers_to_store.append(
                    {
                        "question_url": answer["question"]["url"],
                        "answer_url": answer["url"],
                        "content": answer["content"],
                        "question_title": answer["question"]["title"]
                    }
                )
            if response["paging"]["is_end"]:
                break
            else:
                request_url = response["paging"]["next"]
        data_to_store = dict()
        data_to_store["hash_id"] = hash_id
        data_to_store["data"] = answers_to_store
        self.colletions.insert_one(data_to_store)
        return True
