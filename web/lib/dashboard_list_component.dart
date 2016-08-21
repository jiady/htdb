import 'dart:async';
import 'dart:math';

import 'package:angular2/core.dart';

import 'people_service.dart';
import 'person.dart';
import 'person_component.dart';


@Component(
    selector: 'dashboard_list_component',
    templateUrl: 'dashboard_list_component.html',
    directives: const[PersonComponent]
)
class DashBoardListComponent implements OnInit {
  final PeopleService _peopleService;

  List<Person> people;

  String editMode="read";

  @Input('status')
  String Status;

  @Input("allStatus")
  List<String> AllStatus;

  bool btn_success(String st)=>
    st=="In-Progress";

  bool btn_danger(String st)=>
      st=="Failed" ;

  bool btn_warning(String st)=>
      st=="Abandoned";

  bool btn_default(String st)=>
      st=="Not-Started";

  bool btn_primary(String st)=>
      st=="No-Response";


  List<int> pageNumsToBeShowed = new List<int>();
  Map<String,String> review=new Map<String,String>();

  List<Person> get showedPeople {
    int offset=(current_page_num-1)*page_content_num;
    int start=min(offset,people.length);
    int end=min(offset,people.length);
    return people.sublist(start,end);
  }

  DashBoardListComponent(this._peopleService):
        people=new List<Person>();

  Future<Null> getPeople(offset) async{
    return _getPeople("status/"+Status,offset);
  }

  Future<Null> _getPeople(String index,int offset) async {
    people=new List<Person>();
    await for(Person p in _peopleService.getPeople(index, offset: offset,cache:false)) {
      people.add(p..Status=Status);
      review[p.hash_id]="";
    }
    await for(List<String> s in _peopleService.getReview(index,offset: offset,cache: false)){
      review[s[0]]=s[1];
    };
    print("total people:");
    print(people.length);
  }

  Future updateReview(Person p){
    _peopleService.setReview(p.hash_id,review[p.hash_id]).then((bool b){
      if (b) editMode="Save Success on "+p.name;
      else editMode="Save Fail on "+p.name;
    });
  }

  final int page_content_num=50;
  int current_page_num = 1;
  int total_page_num=1;
  int current_offset=0;
  final int page_margin = 10;

  set current_page(page_num) {
    current_page_num=page_num;
    current_offset=(current_page_num-1)*page_content_num;
    int start=max(current_page_num-page_margin,1);
    int end=min(current_page_num+page_margin,total_page_num);

    pageNumsToBeShowed.clear();
    for(int i=start;i<=end;i++){
      pageNumsToBeShowed.add(i);
    }
    getPeople(current_offset);
  }

  void movePerson(String target,Person p){
    p.Status=target;
    _peopleService.MovePerson(p.hash_id,Status,target).then((bool b){
      if(b==false) p.Status=Status;
    });
  }

  init(String status){
    people.clear();
    Status = status;
    _peopleService.getTargetIds("status/"+Status,cache: false).then((List a) {
      total_page_num = (a.length ~/ page_content_num) + 1;
      current_page = 1;
    });
  }

  @override
  ngOnInit() async {
      init(Status);
  }
}