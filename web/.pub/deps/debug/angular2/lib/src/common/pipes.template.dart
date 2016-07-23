// @ignoreProblemForFile UNUSED_IMPORT
// @ignoreProblemForFile UNUSED_SHOWN_NAME
library angular2.src.common.pipes.template.dart;

import 'pipes.dart';
import 'package:angular2/src/core/reflection/reflection.dart' as _ngRef;
import 'pipes/async_pipe.template.dart' as i0;
import 'pipes/common_pipes.template.dart' as i1;
import 'pipes/date_pipe.template.dart' as i2;
import 'pipes/i18n_plural_pipe.template.dart' as i3;
import 'pipes/i18n_select_pipe.template.dart' as i4;
import 'pipes/json_pipe.template.dart' as i5;
import 'pipes/lowercase_pipe.template.dart' as i6;
import 'pipes/number_pipe.template.dart' as i7;
import 'pipes/replace_pipe.template.dart' as i8;
import 'pipes/slice_pipe.template.dart' as i9;
import 'pipes/uppercase_pipe.template.dart' as i10;
export 'pipes.dart';
export 'pipes/async_pipe.dart' show AsyncPipe;
export 'pipes/common_pipes.dart' show COMMON_PIPES;
export 'pipes/date_pipe.dart' show DatePipe;
export 'pipes/i18n_plural_pipe.dart' show I18nPluralPipe;
export 'pipes/i18n_select_pipe.dart' show I18nSelectPipe;
export 'pipes/json_pipe.dart' show JsonPipe;
export 'pipes/lowercase_pipe.dart' show LowerCasePipe;
export 'pipes/number_pipe.dart' show NumberPipe, DecimalPipe, PercentPipe, CurrencyPipe;
export 'pipes/replace_pipe.dart' show ReplacePipe;
export 'pipes/slice_pipe.dart' show SlicePipe;
export 'pipes/uppercase_pipe.dart' show UpperCasePipe;

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
i10.initReflector();
}
