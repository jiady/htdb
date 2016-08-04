import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

import 'Task.dart';
import 'config_private.dart' as config;


class FaceTask extends Task {
  http.Client client;

  FaceTask(String taskName, [bool retryFail = false]) :
        super(taskName, retryFail) {
    this.client = new http.Client();
  }

  String api = "/v2/detection/detect";
  String apiUrl = "apicn.faceplusplus.com";
  String todayRecommand = "";


  @override
  Future<bool> taskOperation(String result) async {
    try {
      Map json = JSON.decode(result);
      String url = json["image_href"];
      String hash = json["hash_id"];
      Map requestJson = new Map<String, String>();
      requestJson["api_key"] = config.apiKey;
      requestJson["api_secret"] = config.apiSecret;
      requestJson["mode"] = "oneface";
      requestJson["attribute"] = "gender,age";
      requestJson["url"] = url;
      Uri requestUri = new Uri.http(apiUrl, api, requestJson);
      http.Response response = await this.client.get(requestUri);
      Map responseJson = JSON.decode(response.body);
      print(responseJson);
      List faces = responseJson["face"];
      int iftarget = await super.rcommand.send_object(
          ["sismember", "target_people", hash]);
      for (Map face in faces) {
        Map faceResult = new Map<String, dynamic>();
        faceResult["age"] = face["attribute"]["age"]["value"];
        faceResult["age_range"] = face["attribute"]["age"]["range"];
        faceResult["gender"] = face["attribute"]["gender"]["value"];
        faceResult["confidence"] = face["attribute"]["gender"]["confidence"];
        await super.rcommand.send_object(
            ["set", "face/" + hash, JSON.encode(faceResult)]);
        if (iftarget == 1) {
          await super.rcommand.send_object(
              ["sadd", "target-has-face", hash]);
          var r=await super.rcommand.send_object([
            "lpush", todayRecommand, hash
          ]);
          print(r);
        } else {
          await super.rcommand.send_object(
              ["sadd", "non-target-has-face", hash]);
        }
        print("has face in $hash");
        return true;
      }
      if(iftarget==1){
        await super.rcommand.send_object([
          "rpush",todayRecommand,hash]);
      }
      print("no face in $hash");
      return true;
    } catch (e, s) {
      print(e);
      print(s);
      return false;
    }
  }

  @override
  void init(){
    DateTime dateTime = new DateTime.now();
    todayRecommand = "today_recommand/" + dateTime.year.toString() + "-" +
        dateTime.month.toString() + "-" + dateTime.day.toString();
  }

  @override
  Future<List<String>> getInitQueue() async {
    List<String> keys = await super.rcommand.send_object(["keys", "people/*"]);
    List<String> hashs = new List<String>();
    for (String key in keys) {
      hashs.add(key.substring(7));
    }
    return hashs;
  }

}