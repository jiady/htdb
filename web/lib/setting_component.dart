import 'dart:async';

import 'package:angular2/core.dart';
import 'package:angular2/router.dart';
import 'package:htdb/crawler_meta_service.dart';

@Component(
    selector: 'manage',
    templateUrl: 'setting.html'
)
class SettingComponent implements OnInit {
  Map info = new Map();
  Map setting = new Map();
  RouteParams _routeParams;
  CrawlerMataService _metaService;

  SettingComponent(this._routeParams, this._metaService);

  String title = "设置";



  setRedis(String k, v) async {
    info[k] = await _metaService.setKey(k, v);
    setting[k]="";
  }


  @override
  ngOnInit() async {
    info["crawler/auth"] = "loading...";
    info["crawler/web-cookie"] = "loading...";
    setting=new Map.from(info);
    for (String k in info.keys) {
      _metaService.getKey(k).then((String v) {
        info[k] = v;
        setting[k]=v;
      });
    }
  }
}