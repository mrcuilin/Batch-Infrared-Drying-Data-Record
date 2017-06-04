# Batch-Infrared-Drying-Data-Record
The data record system based on the RaspberryPi 3 B and Mettler Toledo HB43-S Moisture Analyzer.  For the Tunnel Drying Chemical Engineering Unit Operation Experiment.

The folder contains the whole project files.
<p>
The folder Django is the Django Project folder contains a project named as 'exps', which has an App named as 'sensor'<br>
The app should be start by a selfstartup script, in the RP3. It should be the file /etc/rc.local<br>
       cd /home/pi/DryingExp/Django/exps<br>
       python manage.py runserver 0.0.0.0:8000<br>
The 2 lines above should be added into the rc.local file, as the file is shown.
</p>
<p>
The folder PyService contains a Service scripts ReadService.py. It will run in background, read the data via serial interface repeatly, when the status written in the MySQL DB is RUNNING and ENABLED ( In the DB serialdata --> status TABLE )<br>
The Svc.sh is a watchdog script. Should be trigger repeatly by the OS every few miniutes, ( Ex. By the crontab, also added in this project ).
</p>

这个项目是一个用于通过串行口采集天平称量值的系统。系统基于RaspberryPi 3 B(树莓派3 B)实现，采集两台梅特勒HB43-S水分测定仪的数据。串行通信使用两个了USB->RS232的接口芯片CP2102的接口电路板，对应端口是 /dev/ttyUSB0和 /dev/ttyUSB1。<br>
系统在化工原理单元操作实验--干燥实验中使用。<br>
库中包含了所有必要的文件：<br>
Django文件夹中包含了使用Python 2.7 Django 1.9.6创建的WEB项目的全部文件，项目名exps，app名sensor1和sensor2分别对应两台测定仪<br>
Django项目可以通过在/etc/rc.local加入自启动脚本：<br>
       cd /home/pi/DryingExp/Django/exps <br>
       python manage.py runserver 0.0.0.0:8000<br>
来进行自启。相应的rc.local文件也已经包含<br>
PyService文件运行了2个后台服务ReadService1.py和ReadService2.py，用于自动在后台采集数据。其受到MySQL-->serialdata --> status库中的状态ENABLE和RUNNING的控制。<br>
这个后台服务由一个看门狗脚本Svc.sh监控，如果发现服务失效退出，则会重新将其启动。Svc.sh可以被操作系统重复触发，例如/etc/crontab文件。涉及的文件也已经放在库里。<br>
DB文件夹放了一个MySQL的数据库备份文件，其中包含了一些真实的实验数据。<br>

在不具备有线、无线网络环境中使用时，Raspberry也可以被配置成一个独立WiFi热点以备连接，相关的配置可以参看我的另一个项目Batch-Fluided-Bed-Drying/Configurations


