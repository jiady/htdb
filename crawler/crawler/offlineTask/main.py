import redis
from AnswerDownloadTask import *
from crawler.mylogger import MyLogger
from crawler.mail import Mail

if __name__ == "__main__":
    # rclient = redis.StrictRedis(host="localhost", port=6379, db=0)
    # rclient.set("crawler/auth",
    #             '''{"user_id":741968131819331584,"uid":"b8a53718c64f8fc87d34ce4f8ba421e8","access_token":"2.0AGDAsxUATAoMAAAAQwPIVwBgwLMVAEwKAHDA-Lpo6wkMAAAAYAJVTUMDyFcA8CaT5Zbc1ZRueZ4Y_lbDBgFlSLVbPH2LzISIjzXwURx8xE8jgdIxqw==","expires_in":2592000,"token_type":"bearer","cookie":{"q_c0":"2|1:0|10:1470133827|4:q_c0|92:Mi4wQUdEQXN4VUFUQW9BY01ENHVtanJDUXdBQUFCZ0FsVk5Rd1BJVndEd0pwUGxsdHpWbEc1NW5oai1Wc01HQVdWSXRR|45f17abc740ee3b57d4e75af649aac3e5b869db02758d0b2081bf6628793eb18","z_c0":"2|1:0|10:1470133827|4:z_c0|92:Mi4wQUdEQXN4VUFUQW9BY01ENHVtanJDUXdBQUFCZ0FsVk5Rd1BJVndEd0pwUGxsdHpWbEc1NW5oai1Wc01HQVdWSXRR|6e72d7af44afb82e5284fb29ae19f6f16b49ba1cb514e5e23d3dbcbaf25d5cd9"},"refresh_token":"2.00000001029c7520a4b21afa6"}''')
    name = "answers-download"
    logger = MyLogger.from_name(name)
    mail = Mail(logger)
    answerDownloadTask = AnswerDownloadTask(name, logger, mail, pipeline_key=["task-pending/nlp"], retryFail=True)
    answerDownloadTask.go()
