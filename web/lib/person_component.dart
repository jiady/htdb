import 'dart:async';
import 'dart:math';

import 'package:angular2/core.dart';
import 'package:angular2/router.dart';

import 'people_service.dart';
import 'person.dart';


@Component(
    selector: 'person_component',
    templateUrl: 'person_component.html'
)
class PersonComponent {

  @Input('person')
  Person person;

}