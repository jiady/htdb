// @ignoreProblemForFile UNUSED_IMPORT
// @ignoreProblemForFile UNUSED_SHOWN_NAME
library angular2.src.compiler.view_compiler.compile_query.template.dart;

import 'compile_query.dart';
import 'package:angular2/src/core/reflection/reflection.dart' as _ngRef;
import 'package:angular2/src/facade/collection.dart' show ListWrapper;
import 'package:angular2/src/facade/lang.dart' show isPresent, isBlank;
import '../compile_metadata.dart' show CompileQueryMetadata, CompileTokenMap;
import '../identifiers.dart' show Identifiers;
import '../output/output_ast.dart' as o;
import 'compile_element.dart' show CompileElement;
import 'compile_method.dart' show CompileMethod;
import 'compile_view.dart' show CompileView;
import 'util.dart' show getPropertyInView;
import 'package:angular2/src/facade/collection.template.dart' as i0;
import 'package:angular2/src/facade/lang.template.dart' as i1;
import '../compile_metadata.template.dart' as i2;
import '../identifiers.template.dart' as i3;
import '../output/output_ast.template.dart' as i4;
import 'compile_element.template.dart' as i5;
import 'compile_method.template.dart' as i6;
import 'compile_view.template.dart' as i7;
import 'util.template.dart' as i8;
export 'compile_query.dart';

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
}
