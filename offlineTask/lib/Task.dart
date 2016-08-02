import 'dart:async';
import 'dart:io';
import 'package:redis/redis.dart';

abstract class Task {
  String taskName;
  final String redisTaskOngoing = "task-meta/ongoing";
  final String redisTaskSuccess = "task-meta/success";
  final String redisTaskPopKey;
  final String redisTaskPushKey;
  final String redisTaskFailKey;
  RedisConnection rcon = new RedisConnection();
  Command rcommand;
  bool inited = false;
  bool retryFail = false;

  Task(String taskName, [bool retryFail = false])
      :
        this.taskName=taskName,
        this.redisTaskPopKey="task-pending/" + taskName,
        this.redisTaskPushKey="task-finish/" + taskName,
        this.redisTaskFailKey="task-fail/" + taskName,
        this.retryFail=retryFail;


  Demon(int min) async {
    Duration duration=new Duration(minutes: min);
    while(true){
      await go();
      sleep(duration);
    }
  }

  Future<List<String>> getInitQueue();

  Future<bool> taskOperation(String result);

  void init(){}

  _single_go(String hash) async {
    String people = await rcommand.send_object(["GET", "people/" + hash]);
    bool b = await taskOperation(people);
    if (b) {
      await rcommand.send_object(
          ["SMOVE", this.redisTaskPopKey, this.redisTaskPushKey, hash]);
    } else {
      await rcommand.send_object(
          ["SMOVE", this.redisTaskPopKey, this.redisTaskFailKey, hash]);
      print("not successs on:" + people);
    }
  }

  go() async {
    init();
    await _initTaskQueue();
    List<String> target_hashs = await rcommand.send_object(
        ["SMEMBERS", this.redisTaskPopKey]);
    List<Future> result = new List();
    int concurrency_control = 1;
    int count = 0;
    for (String hash in target_hashs) {
      count++;
      result.add(_single_go(hash));
      if (count == concurrency_control) {
        count = 0;
        await Future.wait(result);
        result.clear();
      }
    }
    await Future.wait(result);
    await _summary();
  }

  _summary() async {
    int fail = await rcommand.send_object(["SCARD", this.redisTaskFailKey]);
    int succ = await rcommand.send_object(["SCARD", this.redisTaskPushKey]);
    int total = fail + succ;
    print("task-finished:total:$total, fail:$fail");
    rcon.close();
  }

  _initTaskQueue() async {
    rcommand = await rcon.connect('localhost', 6379);
    if (rcommand != null) {
      int response =await rcommand.send_object(
          ["SADD", this.redisTaskOngoing, taskName]);
      if (response == 1) {
        List<String> people = await getInitQueue();
        print("init queue");
        for (String person in people) {
          await rcommand.send_object(["SADD", this.redisTaskPopKey, person]);
          print("add person to pending:$person");
        }
        print("task added");
      } else {
        print("task already exists, try to resume");
        if (this.retryFail) {
          List<String> failed = await rcommand.send_object(
              ["SMEMBERS", this.redisTaskFailKey]);
          for (String person in failed) {
            await rcommand.send_object(
                ["SMOVE", this.redisTaskFailKey, this.redisTaskPopKey, person]);
            print("add person to pending:$person");
          }
          print("task added");
        }
      }
    }
    return;
  }


}