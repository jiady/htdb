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

  Exception _handleError(dynamic e) {
    // In a real world app, we might use a remote logging infrastructure
    // We'd also dig deeper into the error to get a better message
    print(e); // log to console instead
    return new Exception('Server error; cause: $e');
  }

  Future<String> send(String cmd, String value) async {
    try {
      String url = _url + cmd + "/" + value.replaceAll("/", slash);
      final response = await _http.get(url);
      return response.body;
    } catch (e) {
      throw _handleError(e);
    }
  }


  PeopleService(this._http);

  Future<List<String>> getTargetIds() async {
    String response = await this.send("SMEMBERS", "target_people");
    return JSON.decode(response)["SMEMBERS"];
  }

  Future<Person> getIdInfo(String id) async {
    String response = await this.send("GET", "people/" + id);
    Map<String,String> t=new Map<String,String>();

    print(JSON.encode(t));
    String data = JSON.decode(response)["GET"];
    data=data.replaceAll("\n","").replaceAll("': u'","':'").replaceAll("'","\"").replaceAll("True","\"true\"");

    Map<String,String> json=JSON.decode(data);
    Person ret = new Person.FromJson(json);
    return ret;
  }

  Future<List<Person>> getPeople() async {
    List<String> hash_ids = await getTargetIds();
    List<Person> people =new List<Person>();
    for (String id in hash_ids) {
      people.add(await getIdInfo(id));
      if (people.length>10)
        break;
    }
    return people;
  }


}