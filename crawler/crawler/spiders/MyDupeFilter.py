from scrapy.dupefilters import RFPDupeFilter
import redis
from crawler import redis_const


class MyDupeFilter(RFPDupeFilter):
    def __init__(self, path=None, debug=False):
        RFPDupeFilter.__init__(self, path=None, debug=False)
        self.rclient = redis.StrictRedis(host="localhost", port=6379, db=0)

    def request_seen(self, request):
        if request.method == 'GET' and "com/people" in request.url:
            people = request.url.split("/")[-1]
            if self.rclient.sismember(redis_const.SET_SEEN, people) or self.rclient.sismember(
                    redis_const.SET_SUCCESS, people):
                return True
            else:
                self.rclient.sadd(redis_const.SET_SEEN, people)
        else:
            return RFPDupeFilter.request_seen(self, request)
