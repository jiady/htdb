import 'package:angular2/core.dart';
import 'package:angular2/platform/browser.dart';
import 'package:htdb/app_component.dart';
import 'package:http/browser_client.dart';


void main() {
  bootstrap(AppComponent, [
    provide(BrowserClient, useFactory: () => new BrowserClient(), deps: [])
  ]);
}
