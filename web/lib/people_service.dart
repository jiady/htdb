import 'dart:async';
import 'package:angular2/core.dart';
import 'package:http/browser_client.dart';
import 'package:http/http.dart';
import 'person.dart';
import 'dart:html';

import 'dart:convert';

@Injectable()
class PeopleService {
  final BrowserClient _http;
  final String slash = "%2f";
  static const _url = "http://127.0.0.1:7379/";


  Future<String> send(String cmd, String value) async {
    try {
      String url = _url + cmd + "/" + value.replaceAll("/", slash);
      final response = await _http.get(url);
      return response.body;
    } catch (e) {
      print(e);
    }
  }


  PeopleService(this._http);

  Future<List<String>> getTargetIds() async {
    String response = await this.send("SMEMBERS", "target_people");
    return JSON.decode(response)["SMEMBERS"];
  }

  Future<Person> getIdInfo(String id) async {
    try {
      String response = await this.send("GET", "people/" + id);
      String data = JSON.decode(response)["GET"];

      data = data.replaceAll("\\x", "");
      print(data);
      Map<String, dynamic> json = JSON.decode(data);
      Person ret = new Person.FromJson(json);
      return ret;
    }catch(e){
      print(e);
    }
  }

  Future<List<Person>> getPeople() async {
    List<String> hash_ids = await getTargetIds();
    List<Future<Person>> people =new List<Person>();
    Future<List<Person>> ret;
    for (String id in hash_ids) {
      Person p= getIdInfo(id);
      people.add(p);

    }

    return Future.wait(people).then((rt)=>rt);
    //return people;
  }


}