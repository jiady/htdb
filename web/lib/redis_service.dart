import 'dart:async';
import 'package:angular2/core.dart';
import 'package:http/browser_client.dart';

import 'dart:convert';

@Injectable()
class RedisService {
  final BrowserClient _http;
  final String slash = "%2f";
  static const _url = "http://127.0.0.1:7379/";
  bool login=false;

  Future<String> send(String cmd, String value) async {
    return send_list(cmd,[value]);
  }

  Future<String> send_list(String cmd, List<String> values) async {
    try {
      String url = _url + cmd  ;
      for(String value in values) {
        url+="/"+value.replaceAll("/", slash);
      }
      Map<String,String> headers=new Map<String,String>();
      final auth=BASE64.encode(UTF8.encode("jiady:atleastthisisonlyinterface"));
      headers["Authorization"]="Basic $auth";
      final response = await _http.get(url,headers:headers);
      return response.body;
    } catch (e) {
      print(e);
    }
  }

  RedisService(this._http);

}