import 'dart:async';
import 'dart:math';

import 'package:angular2/core.dart';
import 'package:angular2/router.dart';

import 'people_service.dart';
import 'person.dart';


@Component(
    selector: 'list_show',
    templateUrl: 'list_show.html',
    directives: const[ROUTER_DIRECTIVES]
)
class ListComponent implements OnInit {
  final PeopleService _peopleService;
  final RouteParams _routeParams;

  ListComponent(this._peopleService, this._routeParams) :page_content_num=50;
  List<Person> people = new List<Person>();
  int current_page_num = 0;
  int total_page_num = 1;
  final int page_show = 10;
  final int page_content_num;
  List<Map> pageTobeshowed=new List<Map>();

  updatePageNum() async {
    pageTobeshowed.clear();
    int start = max(current_page_num - page_show, 1);
    int end=min(current_page_num+page_show,total_page_num);
    String index = _routeParams.get("index");
    for(int i=start;i<=end;i++){
      Map d=new Map();
      d["page_id"]=i;
      d["router"]=['UserList',{'index':index,'offset':(page_content_num*(i-1)).toString()}];
      pageTobeshowed.add(d);
    }

  }


  Future<Null> getPeople(String index,int offset) async {
    people = _peopleService.ifhasPeople(index,offset: offset);
    if(people==null) {
      people=new List<Person>();
      await for(Person p in _peopleService.getPeople(index, offset: offset)){
        people.add(p);
      }
    }
    print("total people:");
    print(people.length);
  }

  void like(Person p){
    p.liked=true;
    _peopleService.like(p.hash_id).then((bool b){
      if(b==false)  p.liked=false;
    });
  }

  @override
  ngOnInit() {
    current_page_num = 0;
    String index = _routeParams.get("index");
    int offset = int.parse(_routeParams.get("offset"));
    current_page_num=offset~/page_content_num+1;
    _peopleService.getTargetIds(index).then((List a) {
      total_page_num = (a.length ~/ page_content_num) + 1;
      updatePageNum();
    });
    getPeople(index,offset);
  }
}