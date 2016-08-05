import 'redis_service.dart';
import 'package:http/browser_client.dart';
import 'package:angular2/core.dart';
import 'dart:convert';
import 'dart:async';

@Injectable()
class CrawlerMataService extends RedisService {
  CrawlerMataService(BrowserClient _http) :
        super(_http);
  Map sets_name =
  {
    "传播节点":"propogation_people",
    "目标节点":"target_people",
    "无账号爬虫成功":"crawler/requests-success/noAccount",
    "无账号爬虫失败":"crawler/requests-fail/noAccount",
    "无账号爬虫已入队":"crawler/requests-seen/noAccount",
    "无账号爬虫待调度":"crawler/pending/set/noAccount",
    "有账号爬虫成功":"crawler/requests-success/withAccount",
    "有账号爬虫已入队":"crawler/requests-seen/withAccount",
    "有账号爬虫待调度":"crawler/pending/set/withAccount",
  };

  Future<Map> getCrawlerInfo() async {
    Map ret = new Map();
    for (String key in sets_name.keys) {
      String response = await this.send("SCARD", sets_name[key]);
      ret[key] = JSON.decode(response)["SCARD"];
    }
    String response = await this.send("INFO", "memory");
    ret["内存"] = JSON.decode(response)["INFO"];

    response = await this.send("INFO", "cpu");
    ret["CPU"] = JSON.decode(response)["INFO"];

    response = await this.send("INFO", "persistence");
    ret["备份"] = JSON.decode(response)["INFO"];

    return ret;
  }

  Future<Map> getTaskInfo() async {
    Map ret = new Map();
    String response = await this.send("SMEMBERS", "task-meta/ongoing");
    List<String> tasks = JSON.decode(response)["SMEMBERS"];
    ret["进行中任务"] = tasks;
    for (String task in tasks) {
      String response = await this.send("SCARD", "task-finish/" + task);
      ret["任务" + task + "完成数"] = JSON.decode(response)["SCARD"];
      response = await this.send("SCARD", "task-pending/" + task);
      ret["任务" + task + "待进行"] = JSON.decode(response)["SCARD"];
      response = await this.send("SCARD", "task-fail/" + task);
      ret["任务" + task + "失败数"] = JSON.decode(response)["SCARD"];
    }
    return ret;
  }

  Future<String> getKey(String key) async {
    String response = await this.send("GET", key);
    return JSON.decode(response)["GET"];
  }

  Future<String> setKey(String key, String value) async {
    String response = await this.send_list("SET", [key, value]);
    return getKey(key);
  }

}