// @ignoreProblemForFile UNUSED_IMPORT
// @ignoreProblemForFile UNUSED_SHOWN_NAME
library angular2.src.router.route_registry.template.dart;

import 'route_registry.dart';
import 'package:angular2/src/core/reflection/reflection.dart' as _ngRef;
import 'dart:async';
import 'package:angular2/core.dart' show Injectable, Inject, OpaqueToken, ComponentFactory;
import 'package:angular2/src/facade/async.dart' show PromiseWrapper;
import 'package:angular2/src/facade/collection.dart' show ListWrapper, Map, StringMapWrapper;
import 'package:angular2/src/facade/exceptions.dart' show BaseException;
import 'package:angular2/src/facade/lang.dart' show isPresent, isArray, isBlank, isType, isString, isStringMap, StringWrapper, Math, getTypeNameForDebugging;
import 'instruction.dart' show Instruction, ResolvedInstruction, RedirectInstruction, UnresolvedInstruction, DefaultInstruction;
import 'route_config/route_config_impl.dart' show RouteConfig, Route, AuxRoute, RouteDefinition;
import 'route_config/route_config_normalizer.dart' show normalizeRouteConfig, assertComponentExists;
import 'rules/route_paths/route_path.dart' show GeneratedUrl;
import 'rules/rule_set.dart' show RuleSet;
import 'rules/rules.dart' show PathMatch, RedirectMatch, RouteMatch;
import 'url_parser.dart' show parser, Url, convertUrlParamsToArray;
import 'utils.dart' show getComponentAnnotations, getComponentType;
import 'package:angular2/core.template.dart' as i0;
import 'package:angular2/src/facade/async.template.dart' as i1;
import 'package:angular2/src/facade/collection.template.dart' as i2;
import 'package:angular2/src/facade/exceptions.template.dart' as i3;
import 'package:angular2/src/facade/lang.template.dart' as i4;
import 'instruction.template.dart' as i5;
import 'route_config/route_config_impl.template.dart' as i6;
import 'route_config/route_config_normalizer.template.dart' as i7;
import 'rules/route_paths/route_path.template.dart' as i8;
import 'rules/rule_set.template.dart' as i9;
import 'rules/rules.template.dart' as i10;
import 'url_parser.template.dart' as i11;
import 'utils.template.dart' as i12;
export 'route_registry.dart';

var _visited = false;
void initReflector() {
if (_visited) return; _visited = true;
_ngRef.reflector
..registerType(RouteRegistry, new _ngRef.ReflectionInfo(
const [const Injectable()],
const [const [dynamic, const Inject(ROUTER_PRIMARY_COMPONENT)]],
(dynamic _rootComponent) => new RouteRegistry(_rootComponent))
)
;
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
i10.initReflector();
i11.initReflector();
i12.initReflector();
}
