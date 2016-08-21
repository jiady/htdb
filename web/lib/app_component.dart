import 'package:angular2/core.dart';

import 'people_service.dart';
import 'package:angular2/router.dart';
import 'nav_component.dart';
import 'login_component.dart';
import 'list_component.dart';
import 'crawler_meta_service.dart';
import 'manage_component.dart';
import 'setting_component.dart';
import 'dashboard_component.dart';


@Component(
    selector: 'my-app',
    templateUrl: 'app.html',
    directives: const [ROUTER_DIRECTIVES, NavComponent],
    providers: const [PeopleService, ROUTER_PROVIDERS,CrawlerMataService])
@RouteConfig(const[
  const Route(path: '/login',
      name: 'Login',
      component: LoginComponent,
      useAsDefault: true),
  const Route(path: '/dashboard',
      name: 'DashBoard',
      component: DashboardComponent),
  const Route(path:'/userlist/:index/:offset',
      name:"UserList",
      component: ListComponent),
  const Route(path:'/meta/:type',
      name:"Meta",
      component: ManageComponent),
  const Route(path:'/settings',
      name:"Setting",
      component: SettingComponent)
])
class AppComponent {}
