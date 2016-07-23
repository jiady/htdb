// @ignoreProblemForFile UNUSED_IMPORT
// @ignoreProblemForFile UNUSED_SHOWN_NAME
library angular2.src.compiler.view_compiler.view_binder.template.dart;

import 'view_binder.dart';
import 'package:angular2/src/core/reflection/reflection.dart' as _ngRef;
import 'package:angular2/src/facade/collection.dart' show ListWrapper;
import '../template_ast.dart' show TemplateAst, TemplateAstVisitor, NgContentAst, EmbeddedTemplateAst, ElementAst, ReferenceAst, VariableAst, BoundEventAst, BoundElementPropertyAst, AttrAst, BoundTextAst, TextAst, DirectiveAst, BoundDirectivePropertyAst, templateVisitAll;
import 'compile_element.dart' show CompileElement;
import 'compile_view.dart' show CompileView;
import 'event_binder.dart' show bindRenderOutputs, collectEventListeners, bindDirectiveOutputs;
import 'lifecycle_binder.dart' show bindDirectiveAfterContentLifecycleCallbacks, bindDirectiveAfterViewLifecycleCallbacks, bindDirectiveDestroyLifecycleCallbacks, bindPipeDestroyLifecycleCallbacks, bindDirectiveDetectChangesLifecycleCallbacks;
import 'property_binder.dart' show bindRenderText, bindRenderInputs, bindDirectiveInputs, bindDirectiveHostProps;
import 'package:angular2/src/facade/collection.template.dart' as i0;
import '../template_ast.template.dart' as i1;
import 'compile_element.template.dart' as i2;
import 'compile_view.template.dart' as i3;
import 'event_binder.template.dart' as i4;
import 'lifecycle_binder.template.dart' as i5;
import 'property_binder.template.dart' as i6;
export 'view_binder.dart';

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
}
