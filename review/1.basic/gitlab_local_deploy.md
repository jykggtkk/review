最近要新起一个较大型的项目，鉴于之前用SVN的不良体验，准备在这个项目中使用gitlab来做代码管理，顺便利用gitlab的统计功能来辅助项目管理。
# 1. gitlab安装
## 1.1 gitlab ce or ee
Community Edition or Enterprise Edition，ce和ee分别指的是社区版和企业版，毫无疑问社区版已经能满足我们的需求了。
## 1.2 系统准备
使用centos7作为gitlab服务器操作系统，在安装前需要做基础环境的准备：
```
yum install curl policycoreutils openssh-server openssh-clients 
#相关软件要么系统已经有了 要么在系统安装盘ISO文件中可以获取到，需要做的就是把ISO文件挂载，然后在yum源配置中进行添加，这里就步介绍了
```
这里没有选择安装postfix，鉴于项目实施环境，有可能使用局域网邮箱，如果需要用postfix，可以安装并启动：
```
yum install postfix
systemctl start postfix
```
## 1.3 安装gitlab-ce
如果能连到互联网环境，且网络条件比较好，我尝试直接yum安装也很顺利。
`yum install gitlab-ce`
```
[root@localhost gitlab]# yum list |grep gitlab

gitlab-ce.x86_64                            11.4.5-ce.0.el7            @gitlab-ce

```
如果这种方式不行，则可以使用清华大学的镜像源:

新建`/etc/yum.repos.d/gitlab-ce.repo`，内容为:
```
[gitlab-ce]
name=Gitlab CE Repository
baseurl=https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el$releasever/
gpgcheck=0
enabled=1 
```
然后执行安装：
```
sudo yum makecache
sudo yum install gitlab-ce
```
方法参考：[Gitlab Community Edition 镜像使用帮助](https://mirror.tuna.tsinghua.edu.cn/help/gitlab-ce/)

如果不能链接外网，则从[清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/)下载rpm包进行安装。
`rpm -ivh gitlab-ce-11.4.5-ce.0.el7.x86_64.rpm`

# 2. gitlab基础配置
gitlab安装很简单，并且安装后既可以直接执行运行命令，但是其默认的一些设置参数并不合理，需要修改一下。

## 2.1 修改系统端口
GitLab默认会占用80、8080和9090端口，如果服务器上还有tomcat、Jenkins等其他服务，可能会遇到端口冲突。
所以，这一步操作将会修改GitLab的默认端口为11000、11001和11002。
用vim打开gitlab的配置文件：
`vim /etc/gitlab/gitlab.rb`

找到关键字：`external_url 'http://127.0.0.1'`
将其内容改为：`external_url 'http://<服务器地址或域名>:11000'`

找到关键字：`unicorn['port'] = 8080`
将其内容改为：`unicorn['port'] = 8080`

找到关键字：`prometheus['listen_address'] = 'localhost:9090'`
将其内容改为：`prometheus['listen_address'] = 'localhost:11002'`

修改服务端口后，还需要将系统的这些端口进行开放：
```
# 开放端口11000 11001和11002 
/sbin/iptables -I INPUT -p tcp --dport 11000 -j ACCEPT  
/sbin/iptables -I INPUT -p tcp --dport 11001 -j ACCEPT  
/sbin/iptables -I INPUT -p tcp --dport 11002 -j ACCEPT  
```

## 2.2 修改邮件设置
应用默认使用postfix，在安装postfix后，再去设置其他的邮箱是没有效果的

#### 2.2.1 使用postfix
执行`vim /etc/gitlab/gitlab.rb`进入到配置文件，找到关键字`Email Settings`修改下面的参数:
```
### Email Settings 
gitlab_rails['gitlab_email_enabled'] = true 
gitlab_rails['gitlab_email_from'] = 'gitlab@http://<服务器地址或域名>' 
gitlab_rails['gitlab_email_display_name'] = 'GitLab' 
# gitlab_rails['gitlab_email_reply_to'] = 'noreply@example.com'
```
设置完成后，重配postfix，执行`dpkg-reconfigure postfix` 或者`vi /etc/postfix/main.cf`
[postfix设置参考](http://wiki.ubuntu.org.cn/UbuntuHelp:PostfixBasicSetupHowto/zh)

#### 2.2.2 使用其他SMTP邮箱

```
### Email Settings 
gitlab_rails['gitlab_email_enabled'] = true 
### GitLab email server settings 
###! Docs: https://docs.gitlab.com/omnibus/settings/smtp.html 
###! **Use smtp instead of sendmail/postfix.** 
gitlab_rails['smtp_enable'] = true 
gitlab_rails['smtp_address'] = "smtp.example.com" 
gitlab_rails['smtp_port'] = 25 
gitlab_rails['smtp_user_name'] = "xxxx@example.com" 
gitlab_rails['smtp_password'] = "这里填授权密码" 
gitlab_rails['smtp_domain'] = "example.com" 
gitlab_rails['smtp_authentication'] = "login" 
gitlab_rails['smtp_enable_starttls_auto'] = true 
gitlab_rails['smtp_tls'] = true 
###! **Can be: 'none', 'peer', 'client_once', 'fail_if_no_peer_cert'** 
###! Docs: http://api.rubyonrails.org/classes/ActionMailer/Base.html 
gitlab_rails['smtp_openssl_verify_mode'] = 'peer' 
user['git_user_email'] = "xxxx@example.com" 
gitlab_rails['gitlab_email_from'] = "xxxx@example.com"

```
完成配置后可以测试下邮箱：
```
#进入控制台
gitlab-rails console
#发送测试邮件
Notify.test_email('收件人邮箱', '邮件标题', '邮件正文').deliver_now
```

## 2.3 其他设置
#### 2.3.1 解决GitLab头像无法正常显示
原因：gravatar被墙
解决办法：
```
vim /etc/gitlab/gitlab.rb
#gitlab_rails['gravatar_plain_url'] = 'http://gravatar.duoshuo.com/avatar/%{hash}?s=%{size}&d=identicon' 
#修改为： 
gitlab_rails['gravatar_plain_url'] = 'http://gravatar.duoshuo.com/avatar/%{hash}?s=%{size}&d=identicon' 
#然后在命令行执行： 
gitlab-ctl reconfigure 
gitlab-rake cache:clear RAILS_ENV=production
```

#### 2.3.2 解决EOFError: end of file reached

```
vim /etc/gitlab/gitlab.rb
gitlab_rails['smtp_tls']  = false
#修改为：
gitlab_rails['smtp_tls'] = true
```

以上gitlab配置内容参考文章：https://www.jianshu.com/p/dbb4543bdd8e

gitlab完成配置后，需要执行 `gitlab-ctl reconfigure` 命令使得配置生效

# 3. gitlab服务命令
## 3.1 Service Management Commands
这类命令来管理服务
| command   | function |
|:----------|:-----| 
| start | 启动所有服务 | 
| stop | 关闭所有服务 | 
| restart |  重启所有服务 |  
| status | 查看所有服务状态 | 
| tail | 查看日志信息 | 
| service-list |  列举所有启动服务 |  
| graceful-kill |  平稳停止一个服务 | 

举例：
```
#启动所有服务
[root@localhost gitlab]# gitlab-ctl start
#启动单独一个服务
[root@localhost gitlab]# gitlab-ctl start nginx
#查看日志，查看所有日志
[root@localhost gitlab]# gitlab-ctl tail
#查看具体一个服务的日志,类似tail -f
[root@localhost gitlab]# gitlab-ctl tail nginx
```

## 3.2 General Commands
全局命令
| command   | function |
|:----------|:-----| 
| help | 帮助 | 
| reconfigure | 修改配置文件之后，重新加载 | 
| show-config |  查看所有服务配置文件信息 |  
| uninstall | 卸载这个软件 | 
| cleanse | 清空gitlab数据 | 
| service-list |  列举所有启动服务 |  
| graceful-kill |  平稳停止一个服务 | 

举例：
```
#显示所有服务配置文件
[root@localhost gitlab]#gitlab-ctl show-config
#卸载gitlab
[root@localhost gitlab]#gitlab-ctl uninstall
```

## 3.3 DatabaseCommands
数据库命令
| command   | function |
|:----------|:-----| 
| pg-upgrade | 更新postgresql版本 | 
| revert-pg-upgrade | 还远先前的(离现在正在使用靠近的版本)一个数据库版本 | 
| show-config |  查看所有服务配置文件信息 |  
| uninstall | 卸载这个软件 | 
| cleanse | 清空gitlab数据 | 
| service-list |  列举所有启动服务 |  
| graceful-kill |  平稳停止一个服务 | 

举例：
```
#升级数据库
[root@localhost gitlab]# gitlab-ctl pg-upgrade
Checking for an omnibus managed postgresql: OK
Checking if we already upgraded: OK
The latest version 9.6.1 is already running,nothing to do
#降级数据库版本
[root@localhost gitlab]# gitlab-ctl revert-pg-upgrade
```

安装完成后，使用浏览器打开 `http://服务器IP/域名:11000`进入登陆界面


参考文章列表: 
https://blog.csdn.net/wh211212/article/details/72627803