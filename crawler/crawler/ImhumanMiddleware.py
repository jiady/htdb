import mail.py

class ImhumanMiddleware(object):

    def process_request(self, request, spider):
        if "www.zhihu.com/imhuman" in request.url:
            spider.stop = True;

    def process_response(self, request, response, spider):

