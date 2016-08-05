#!bin/bash

rm -f *.log
rm -f *.txt
rm -f *.out

cp crawler/with_account_settings.py crawler/settings.py
nohup scrapy crawl zhihu -a master=True -a user="13148444851" -a pwd="jia123456" -a sub_name="with1" -a sub_type="withAccount" > with1.txt 2>&1 &
echo "withaccount started"
sleep 5 # wait above to started

cp crawler/no_account_settings.py crawler/settings.py
nohup scrapy crawl zhihu -a sub_name="no1" -a master=True -a sub_type="noAccount" > no1.txt 2>&1 &
echo "no  account started"
echo "shutdown cmd:killall scrapy"