# -*- coding: utf-8 -*-
from scrapy.exceptions import IgnoreRequest


class ImhumanMiddleware(object):
    def process_request(self, request, spider):
        if spider.stop:
            spider.flog.error("ignored requests:@%s@", request.url)
            raise IgnoreRequest()

        if "www.zhihu.com/imhuman" in request.url:
            spider.stop = True

    def process_response(self, request, response, spider):
        if "www.zhihu.com/imhuman" in request.url:
            spider.myMail.send_timed(1200, "imhuman报警", response.body)
