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
  Map<String,Person> _cachePerson= new Map<String,Person>();
  Map<String,String> _cacheReview = new Map<String,String>();

  get review=>_cacheReview;

  Future<Map> _getRedisJson(key)async{
    String data =await _send_list("GET",[key]);
    if(data!=null) {
      data = data.replaceAll("\\x", "");
      Map<String, dynamic> json = JSON.decode(data);
      return json;
    }
    return null;
  }

  Future _send_list(String cmd,List values)async{
    String response= await this.send_list(cmd,values);
    return  JSON.decode(response)[cmd];
  }

  PeopleService(BrowserClient _http):
      super(_http);

  Future<List<String>> getTargetIds(String indexKey,{bool cache:true}) async {
    if(cache && _cache_index.containsKey(indexKey)){
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
        if(_cachePerson.containsKey(id)) return _cachePerson[id];
        Person ret=null;
        Map json=await _getRedisJson("people/" + id);
        if (json!=null){
           ret= new Person.FromJson(json);
        }
        Map face=await _getRedisJson("face/"+id);
        if(face!=null){
          ret.setFace(face);
        }
        _cachePerson[id]=ret;
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

  Future<String> getReviewInfo(String id) async {
    try {
      if(_cacheReview.containsKey(id)) return _cacheReview[id];
      String ret=null;
      ret =await _send_list("GET",["review/" + id]);
      if (ret!=null){
        _cacheReview[id]=ret;
        return ret;
      }else{
        print(ret);
      }
    }catch(e){
      String ret =await _send_list("GET",["review/" + id]);
      print(ret);
    }
  }

  String indexTag(String indexKey,int offset,int length){
    return indexKey+"/"+offset.toString()+"/"+length.toString();
  }
  List<Person> ifhasPeople(String indexKey,{int offset:0, int length:50}){
    String indextag=indexTag(indexKey,offset,length);
    if(_cache.containsKey(indextag)){
      return _cache[indextag];
    }
    return null;
  }
  Stream<Person> getPeople(String indexKey,{int offset:0, int length:50, bool cache:true}) async* {
    String indextag=indexTag(indexKey,offset,length);
    List<String> hash_ids = await getTargetIds(indexKey,cache: cache);
    List<Person> people =new List<Person>();
    Future<List<Person>> ret;
    for (int i=offset;i<offset+length && i<hash_ids.length;i++) {
      Person p= await getIdInfo(hash_ids[i]);
      if(p!=null)
        yield p;
        people.add(p);
    }
    _cache[indextag]=people;
  }

  Stream<List<String>> getReview(String indexKey,{int offset:0, int length:50, bool cache:true}) async* {
    List<String> hash_ids = await getTargetIds(indexKey,cache: cache);
    for (int i=offset;i<offset+length && i<hash_ids.length;i++) {
      String p= await getReviewInfo(hash_ids[i]);
      if(p!=null)
        yield [hash_ids[i],p];
    }
  }

  Future<bool> MovePerson(String p, String from, String to) async {
    String f="status/"+from;
    String t="status/"+to;
    var res= await _send_list("SMOVE",[f,t,p]);
    if(res!=null && res==1) return true;
    return false;
  }

  Future<bool> like(String p) async{
    String name="status";
    var res= await _send_list("SADD",[name,p]);
    if(res!=null && res==1) {
      name = "status/Not-Started";
      res = await _send_list("SADD", [name, p]);
      if(res!=null && res==1) {
        return true;
      }
    }
    return false;
  }

  Future<bool> setReview(String p,String c) async {
    if(_cacheReview.containsKey(p)){
      if (_cacheReview[p]==c) return true;
    }
    _cacheReview.remove(p);
    var res= await _send_list("SET",["review/"+p,c]);
    if(res!=null && res[1]=="OK"){
      return true;
    }
    return false;
  }

}