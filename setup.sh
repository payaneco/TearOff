#!/bin/bash

apt-get install -y fonts-ipaexfont

#cp /home/pi/TearOff/startup_calendar.sh /usr/local/bin/
sed -i -e "s/exit 0\$/\/home\/pi\/TearOff\/startup_calendar.sh\n\nexit 0/g" /etc/rc.local

python3 /home/pi/TearOff/auto_calendar.py
