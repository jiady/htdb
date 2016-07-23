// @ignoreProblemForFile UNUSED_IMPORT
// @ignoreProblemForFile UNUSED_SHOWN_NAME
library angular2.src.router.directives.router_link_transform.template.dart;

import 'router_link_transform.dart';
import 'package:angular2/src/core/reflection/reflection.dart' as _ngRef;
import 'package:angular2/compiler.dart' show TemplateAstVisitor, ElementAst, BoundDirectivePropertyAst, BoundElementPropertyAst, DirectiveAst, TemplateAst;
import 'package:angular2/core.dart' show Injectable;
import 'package:angular2/src/compiler/expression_parser/ast.dart' show AstTransformer, Quote, AST, LiteralArray, LiteralPrimitive;
import 'package:angular2/src/compiler/expression_parser/parser.dart' show Parser;
import 'package:angular2/src/facade/exceptions.dart' show BaseException;
import 'package:angular2/compiler.template.dart' as i0;
import 'package:angular2/core.template.dart' as i1;
import 'package:angular2/src/compiler/expression_parser/ast.template.dart' as i2;
import 'package:angular2/src/compiler/expression_parser/parser.template.dart' as i3;
import 'package:angular2/src/facade/exceptions.template.dart' as i4;
export 'router_link_transform.dart';

var _visited = false;
void initReflector() {
if (_visited) return; _visited = true;
_ngRef.reflector
..registerType(RouterLinkTransform, new _ngRef.ReflectionInfo(
const [const Injectable()],
const [const [Parser]],
(Parser parser) => new RouterLinkTransform(parser),
const [TemplateAstVisitor])
)
;
i0.initReflector();
i1.initReflector();
i2.initReflector();
i3.initReflector();
i4.initReflector();
}
