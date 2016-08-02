import 'dart:async';

import 'package:angular2/core.dart';
import 'package:angular2/router.dart';
import 'crawler_meta_service.dart';

@Component(
    selector: 'manage',
    templateUrl: 'show.html'
)
class ManageComponent implements OnInit,OnDestroy{
  Map info=new Map();
  CrawlerMataService _metaService;
  RouteParams _routeParams;
  ManageComponent(this._metaService,this._routeParams);
  Timer timer;
  String title="";

  @override
  ngOnDestroy() {
    timer?.cancel();
  }

  void updateCrawlerInfo(Timer t){
    _metaService.getCrawlerInfo().then((Map v){
      info=v;
      print("crawler info updated");
    });
  }
  void updateTaskInfo(Timer t){
    _metaService.getTaskInfo().then((Map v){
      info=v;
      print("task info updated");
    });
  }


  @override
  ngOnInit() async {
    Duration duration=new Duration(seconds: 4);
    title=_routeParams.get("type");
    if(title=="crawler") {
      info=await _metaService.getCrawlerInfo();
      timer = new Timer.periodic(duration, updateCrawlerInfo);
    }else if(title=="task"){
      info=await _metaService.getTaskInfo();
      timer = new Timer.periodic(duration, updateTaskInfo);
    }
  }
}