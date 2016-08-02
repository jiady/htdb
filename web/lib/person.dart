import 'package:json_object/json_object.dart';

class Person {
  String hash_id, href;
  String name, bio, introduction, school, major, city,image_href,url_name;
  String follower_num, followee_num, agree_num;
  JsonObject face;

  static Map<String,String> transform={
   "https://pic4.zhimg.com":"http://7xjdxk.com1.z0.glb.clouddn.com",
   "https://pic1.zhimg.com":"http://oatiypdqk.bkt.clouddn.com",
   "https://pic2.zhimg.com":"http://oatjlzlu9.bkt.clouddn.com",
   "https://pic3.zhimg.com":"http://oatjdupm8.bkt.clouddn.com",
  };
  setFace(Map json){
    if(json!=null){
        face=new JsonObject.fromMap(json);
    }
  }

  Person.FromJson(Map<String, String> json) {
    hash_id = json["hash_id"];
    name = json["name"];
    url_name = json["url_name"];
    bio = json["bio"];
    introduction = json["introduction"];
    school = json["school"];
    major = json["major"];
    city = json["city"];
    image_href = json["image_href"];
    for(String b in transform.keys){
      if(image_href.startsWith(b)){
        image_href=image_href.replaceFirst(b,transform[b]);
        break;
      }
    }
    href="http://www.zhihu.com/people/"+url_name;
    followee_num = json["followee_num"].toString();
    follower_num = json["follower_num"].toString();
    agree_num = json["agree_num"].toString();
  }
}