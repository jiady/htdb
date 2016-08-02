import 'package:angular2/core.dart';
import 'package:angular2/router.dart';

@Component(
    selector: "my-nav",
    templateUrl: "nav.html",
    directives: const[ROUTER_DIRECTIVES])
class NavComponent implements OnInit {
  DateTime dateTime = new DateTime.now();
  List routerOfToady=new List();

  @override
  ngOnInit() {
    String key = "today_recommand/" + dateTime.year.toString() + "-" +
        dateTime.month.toString() + "-" + dateTime.day.toString();
    routerOfToady=['UserList',{'index':key,'offset':'0'}];
  }

}