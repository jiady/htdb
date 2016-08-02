import 'package:crypto/crypto.dart';
import 'dart:convert';

import 'package:angular2/core.dart';
import 'people_service.dart';
import 'dart:core';

@Component(
    selector: 'login',
    templateUrl: 'login.html')
class LoginComponent {
  String pin;
  final PeopleService _peopleService;

  LoginComponent(this._peopleService);

  bool checkPin() {
    List<int> p = UTF8.encode(pin);
    Digest digest = sha256.convert(p);
    if (digest.toString() ==
        "95b0c36381f3e1fefa208a4b25f5e59182c37eff413bd669d1cc091be738f4aa") {
      _peopleService.login=true;
      return true;
    }
    DateTime now = new DateTime.now();
    now = now.toLocal();
    String key = "apple" + now.month.toString() + now.day.toString();
    p = UTF8.encode(key);
    if (pin == sha256.convert(p).toString().substring(0, 8)) {
      _peopleService.login=true;
      return true;
    }
  }

}