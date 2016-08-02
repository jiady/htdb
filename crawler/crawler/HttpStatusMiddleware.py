from scrapy.exceptions import IgnoreRequest
import redis_const


class HttpStatusMiddleware(object):
    def process_response(self, request, response, spider):
        if response.status == 200:
            pass
        elif response.status == 404 or response.status == 410 or response.status == 400:
            if "com/people" in response.url:
                url_name = response.url.split("/")[-1]
                spider.flog.warning("get invalid status:@"+response.url+" give up")
                spider.rclient.smove(spider.seen_S, spider.fail_S, url_name)
                raise IgnoreRequest()
        elif response.status == 403:
            spider.myMail.send_timed("http status 403", "see if cookie invalide:" + response.body)
            raise IgnoreRequest()
        return response
