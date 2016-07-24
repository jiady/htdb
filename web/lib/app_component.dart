import 'person.dart';
import 'people_service.dart';
import 'dart:async';

import 'package:angular2/core.dart';


@Component(
    selector: 'my-app',
    templateUrl: 'list_show.html',
    providers: const [PeopleService])
class AppComponent implements OnInit{
  final PeopleService _peopleService;
  AppComponent(this._peopleService);
  List<Person> people;

  Future<Null> getPeople() async{
    people=await _peopleService.getPeople();
    print("total people:");
    print(people.length);
  }
  @override
  ngOnInit() {
    getPeople();
  }
}