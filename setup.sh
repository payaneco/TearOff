#!/bin/bash

apt-get install -y fonts-ipaexfont
chmod 755 -R /home/pi/TearDown/

# see https://language-and-engineering.hatenablog.jp/entry/20101210/p1#cron%E3%81%AB%E3%82%B8%E3%83%A7%E3%83%96%E7%99%BB%E9%8C%B2%E8%87%AA%E5%8B%95
# 登録したいジョブ
cron_job_line="@reboot /home/pi/TearOff/startup_calendar.sh > /home/pi/TearOff/auto_calendar.log"
# crontabファイル
cron_file="/var/spool/cron/root"
## crontabファイル準備
# 無ければ作る
[ -f ${cron_file} ] && touch ${cron_file}
## タスク登録
# 既に登録されているかどうかを判定
cron_job_line_for_grep="${cron_job_line//\\/\\\\}"
if [ `grep "${cron_job_line_for_grep}" "${cron_file}" | wc -l` -eq 0 ] ; then
  echo "not registered yet. begin registering..."
  
  # 追記
  echo "${cron_job_line}" >> "${cron_file}"
else
  echo "already registered."
fi
# cron再起動
/etc/init.d/crond restart
echo "registering finished."

python3 /home/pi/TearOff/auto_calendar.py > /home/pi/TearOff/auto_calendar.log
