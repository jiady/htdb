// @ignoreProblemForFile UNUSED_IMPORT
// @ignoreProblemForFile UNUSED_SHOWN_NAME
library angular2.src.testing.internal.template.dart;

import 'internal.dart';
import 'package:angular2/src/core/reflection/reflection.dart' as _ngRef;
import 'dart:async';
import 'package:angular2/core.dart' show PLATFORM_INITIALIZER;
import 'package:angular2/platform/testing/browser.dart';
import 'package:angular2/src/core/di/provider.dart' show provide, Provider;
import 'package:angular2/src/core/reflection/reflection.dart';
import 'package:angular2/src/core/zone/ng_zone.dart' show NgZone;
import 'package:angular2/src/platform/dom/dom_adapter.dart' show DOM;
import 'package:test/test.dart';
import 'internal_injector.dart';
import 'package:angular2/core.template.dart' as i0;
import 'package:angular2/platform/testing/browser.template.dart' as i1;
import 'package:angular2/src/core/di/provider.template.dart' as i2;
import 'package:angular2/src/core/reflection/reflection.template.dart' as i3;
import 'package:angular2/src/core/zone/ng_zone.template.dart' as i4;
import 'package:angular2/src/platform/dom/dom_adapter.template.dart' as i5;
import 'internal_injector.template.dart' as i6;
import 'fake_async.template.dart' as i7;
import 'test_component_builder.template.dart' as i8;
import 'utils.template.dart' as i9;
export 'internal.dart';
export 'fake_async.dart';
export 'internal_injector.dart';
export 'test_component_builder.dart';
export 'utils.dart';

var _visited = false;
void initReflector() {
if (_visited) return; _visited = true;
i0.initReflector();
i1.initReflector();
i2.initReflector();
i3.initReflector();
i4.initReflector();
i5.initReflector();
i6.initReflector();
i7.initReflector();
i8.initReflector();
i9.initReflector();
}
