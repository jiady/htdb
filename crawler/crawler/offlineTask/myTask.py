import abc
import redis
import time

class Task:
    redisTaskOngoing = "task-meta/ongoing"
    rclient = redis.StrictRedis(host="localhost", port=6379, db=0)
    task_sleep = 0

    def __init__(self, name, logger, mail, retryFail=False, pipeline_key=[]):
        self.taskName = name
        self.mail = mail
        self.pipeline_key = pipeline_key
        self.retryFail = retryFail
        self.rclient = redis.StrictRedis(host="localhost", port=6379, db=0)
        self.redisTaskPopKey = "task-pending/" + name
        self.redisTaskPushKey = "task-finish/" + name
        self.redisTaskFailKey = "task-fail/" + name
        self.logger = logger
        self.task_sleep = 0

    def demon(self, time_sleep=10):
        while True:
            try:
                self.go()
            except Exception, e:
                self.mail.send_timed(600, self.taskName + " exception", str(e))
            finally:
                time.sleep(time_sleep)

    def getInitQueueBySetNames(self, set_names):
        ret = []
        for name in set_names:
            ret.extend(self.rclient.smembers(set_names))
        return ret

    @abc.abstractmethod
    def getInitQueue(self):
        pass

    @abc.abstractmethod
    def taskOperation(self, hash):
        pass

    def init(self):
        pass

    def _singleTask(self, hash_id):
        try:
            r = self.taskOperation(hash_id)
            if r is not None:
                self.rclient.smove(self.redisTaskPopKey, self.redisTaskPushKey, hash_id)
                if r:
                    for key in self.pipeline_key:
                        self.rclient.sadd(key, hash_id)
        except Exception, e:
            self.rclient.smove(self.redisTaskPopKey, self.redisTaskFailKey, hash_id)
            self.logger.warning("not success on:" + hash_id + ":" + str(e))


    def _initTaskQueue(self):
        if not self.rclient.sismember(self.redisTaskOngoing, self.taskName):
            list_hash = self.getInitQueue()
            for hash_id in list_hash:
                self.rclient.sadd(self.redisTaskPopKey, hash_id)
                self.logger.info("add person to pending:" + hash_id)
            self.logger.info("task added")
            self.rclient.sadd(self.redisTaskOngoing, self.taskName)
        else:
            self.logger.info("task already exists, try to resume")
            if self.retryFail:
                list_hash = self.rclient.smembers(self.redisTaskFailKey)
                for hash_id in list_hash:
                    self.rclient.smove(self.redisTaskFailKey, self.redisTaskPopKey, hash_id)
                    self.logger.info("add person to pending:" + hash_id)
            self.logger.info("task added")

    def _summary(self):
        fail = self.rclient.scard(self.redisTaskFailKey)
        succ = self.rclient.scard(self.redisTaskPushKey)
        total = fail + succ
        self.logger.info("task finished:%d, fail:%d", total, fail)

    def _valid(self, hash_id):
        try:
            if self.filter_out(hash_id):
                self.rclient.smove(self.redisTaskPopKey, self.redisTaskFailKey, hash_id)
                self.logger.warning("filtered:" + hash_id + ":")
                return False
            return True
        except Exception, e:
            self.rclient.smove(self.redisTaskPopKey, self.redisTaskFailKey, hash_id)
            self.logger.warning("not success on filter:" + hash_id + ":" + str(e))
            return False

    def filter_out(self, hash_id):
        return False

    def go(self):
        self.init()
        self._initTaskQueue()
        while True:
            hash_id = self.rclient.srandmember(self.redisTaskPopKey)
            if hash_id is not None:
                if self._valid(hash_id):
                    self._singleTask(hash_id)
            else:
                break
        self._summary()
