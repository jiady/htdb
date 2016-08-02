import 'dart:async';
import 'package:angular2/core.dart';
import 'package:http/browser_client.dart';
import 'package:http/http.dart';
import 'person.dart';
import 'redis_service.dart';
import 'dart:convert';

@Injectable()
class PeopleService extends RedisService {
  Map<String,List<Person>> _cache=new Map<String,List<Person> >();
  Map<String,List<String>> _cache_index=new Map<String,List<String> >();

  Future<Map> _getRedisJson(key)async{
    String response=await this.send("GET",key);
    String data = JSON.decode(response)["GET"];
    if(data!=null) {
      data = data.replaceAll("\\x", "");
      Map<String, dynamic> json = JSON.decode(data);
      return json;
    }
    return null;
  }

  PeopleService(BrowserClient _http):
      super(_http);

  Future<List<String>> getTargetIds(String indexKey) async {
    if(_cache_index.containsKey(indexKey)){
      return _cache_index[indexKey];
    }
    if(indexKey.substring(0,5)=="today"){
      String response = await this.send_list("LRANGE", [indexKey,"0","-1"]);
      _cache_index[indexKey] = JSON.decode(response)["LRANGE"];
    }else {
      String response = await this.send("SMEMBERS", indexKey);
      _cache_index[indexKey] = JSON.decode(response)["SMEMBERS"];
    }
    return _cache_index[indexKey];
  }

  Future<Person> getIdInfo(String id) async {
    try {
        Person ret=null;
        Map json=await _getRedisJson("people/" + id);
        if (json!=null){
           ret= new Person.FromJson(json);
        }
        Map face=await _getRedisJson("face/"+id);
        if(face!=null){
          ret.setFace(face);
        }
        return ret;
    }catch(e){
      String response = await this.send("GET", "people/" + id);
      String data = JSON.decode(response)["GET"];
      print(e);
      print(data);
      Map<String, dynamic> json = JSON.decode(data);
      Person ret = new Person.FromJson(json);
    }
  }

  String indexTag(String indexKey,int offset,int length){
    return indexKey+"/"+offset.toString()+"/"+length.toString();
  }

  Future<List<Person>> getPeople(String indexKey,{int offset:0, int length:50}) async {
    String indextag=indexTag(indexKey,offset,length);
    if(_cache.containsKey(indextag)){
      return _cache[indextag];
    }
    List<String> hash_ids = await getTargetIds(indexKey);
    List<Person> people =new List<Person>();
    Future<List<Person>> ret;
    for (int i=offset;i<offset+length && i<hash_ids.length;i++) {
      Person p= await getIdInfo(hash_ids[i]);
      if(p!=null)
        people.add(p);
    }
    _cache[indextag]=people;
    return people;
  }


}