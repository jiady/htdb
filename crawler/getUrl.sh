# !bin/bash

cat $1 | grep "zhihu.com/people" | sed "s@.*zhihu.com/people/@@g;s@>@@g" > $1.in
