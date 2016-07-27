from scrapy.dupefilters import RFPDupeFilter
import redis
from crawler import redis_const


class MyDupeFilter(RFPDupeFilter):
    def __init__(self, path=None, debug=False):
        RFPDupeFilter.__init__(self, path=None, debug=False)
        self.rclient = redis.StrictRedis(host="localhost", port=6379, db=0)

    def request_seen(self, request):
       return False
