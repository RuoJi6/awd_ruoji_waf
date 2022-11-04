# wad_ruoji_waf

旨在awd比赛中，可以快速的部署waf，和文件监控



### phpwaf文件夹



#### waf3_ruoji_1.php

这个文件可以检测get post herade中的攻击payload，sql，代码执行



只能在Linux使用，会在tmp目录下生成一个1log目录，会生成五个txt文件，其中：
Attack_Big_information.txt 为详细的数组日志
sy.txt 为所有的访问日志
hacker_re.txt 为攻击者访问日志
xxfw.txt 为所有请求日志（包括post 数据包）
hacker_data.txt 为攻击者请求日志（包括post 数据包
此waf脚本如果检测到攻击者请求中带有flag，就会输出假的flag
此waf脚本还存在误报（注意，如果部署后，页面访问为空白，请更换浏览器访问）



#### ip_heimd.php

为Ip黑名单，填入ip地址，可以禁止访问页面

请在Index.php文件使用include包含文件，ip_heimd.php文件需要在waf3_ruoji_1.php文件前面

 include 'ip_heimd.php';

 include 'waf3_ruoji_1.php';

这样，因为ip_heimd.php为黑名单，禁止访问的



### 监控文件夹



jiank_py2_z

文件为不需要环境，可以部署的脚本，这个需要输入两参数，一个是需要备份监控的文件，一个是备份文件目录



python2wj_z.py

需要python2环境，这个需要输入两参数，一个是需要备份监控的文件，一个是备份文件目录



python2wjian.py

需要python2环境，这个不需要输入参数，这个文件会直接备份监控和这个脚本同一个目录的文件，备份文件也在同目录



python3wj.py

需要python3环境，需要输入需要备份监控的文件夹



python2的脚本有bug，当文件夹被删除时，恢复失败

python3脚本当有带有空格的文件被删除，恢复失败

