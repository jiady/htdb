import 'dart:async';
import 'dart:math';

import 'package:angular2/core.dart';
import 'package:angular2/router.dart';

import 'people_service.dart';
import 'person.dart';
import 'dashboard_list_component.dart';


@Component(
    selector: 'dashboard_component',
    templateUrl: 'dashboard_component.html',
    directives: const[ROUTER_DIRECTIVES,DashBoardListComponent]
)
class DashboardComponent implements OnInit {

  DashboardComponent(this._routeParams):
    _Status="Not-Started";

  List<String> get availableStatus{
    return new List<String>.from(allStatus)..remove(_Status);
  }

  List<String> allStatus=[
    "Not-Started",
    "In-Progress",
    "No-Response",
    "Abandoned",
    "Failed"
  ];
  String  _Status;

  set status(s){
    _Status=s;
    dashBoardListComponent.init(s);
  }
  String get status=> _Status;

  @ViewChild(DashBoardListComponent)
  DashBoardListComponent dashBoardListComponent;

  final RouteParams _routeParams;

  @override
  ngOnInit() {

  }
}