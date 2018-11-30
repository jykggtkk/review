对gitlab的使用主要从两个角度去分析，一个是管理员，一个是开发提交者。

# 1. 管理员使用

## 1.1 初始配置

浏览器访问 http://服务器IP:11000 
第一次访问会默认以root管理员用户登陆，需要输入两遍密码。
登陆后，可以看到，gitlab中主要围绕着以下几个概念进行操作：
  
| project | 项目 |
|:--------|:----| 
| **user** | **用户** |
| **group** | **团队** |

![主界面](https://upload-images.jianshu.io/upload_images/13323529-aa8fcf844aebd467.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果是作为个人使用，那么使用root用户创建project就可以实现上传下载代码了。
如果是小团队项目，就需要创建group，并在group中创建projects，添加user到group中，并给用户相应的权限。

### 1.1.1 关闭系统注册功能

为了便于管理，可以选择关闭gitlab的注册功能.
在主界面左边条依次选择 **Settings -> General -> Sign-up restrictions** ,点击 Expand 按钮，在 **Sign-up restrictions**  选项处将勾点掉，下拉点击 **Save changes** 就可以了。

### 1.1.2 修改网站logo

为了让我们的gitlab看起来更符合项目，可以对网站的logo进行调整，在 **Appearance** 中对 导航条图标（Navigation bar）、网站图标（Favicon）、登陆页图标（Sign in/Sign up pages）进行设置。

## 1.2 代码管理

### 1.2.1  团队协作方式

gitlab团队协作主要有两种方式：

#### 使用fork

* 项目负责人在gitlab上新建一个项目，并分享URL给开发人员
* 开发人员在负责人的gitlab项目页面上点击“fork”按钮，将此项目fork到自己的gitlab上，这相当于是从负责人那拷贝了一份项目副本，无论开发人员如何修改代码都不会影响负责人那master分支上的代码
* 然后开发人员可以根据自己的项目分工，像对待普通项目一样做clone、add、commit、push等操作
* 如果开发人员人为一个小模块做好了，可以点击“**New Merge Request**”按钮，向负责人发送代码合并请求，要合并的代码文件也会以列表的形式同时发送给负责人，此时负责人会看到开发人员的请求，经审核如果代码没问题则会合并模块，并向开发人员发送确认合并的通知 

#### 不使用fork

1. 负责人为开发人员分别创建开发分支（namedev_branch）

* 项目负责人在gitlab上新建一个项目，并为每一个开发人员创建一个开发分支（namedev_branch）
* 开发人员clone项目之后，经git branch检查发现本地只有master分支，因此也需要把属于自己的开发分支也一起获取下来
> `git fetch origin namedev_branch:namedev_branch`
> `#拉取远程的一个叫namedev_branch的分支，并在本地创建一个叫namedev_branch的分支和远程的分支匹配`
* 切换到namedev_branch分支
> `git checkout namedev_branch`
* 之后的操作如同对待普通项目一样
> `git add hello.py`
> `git commit -m "add hello.py"`
> `git push -u origin namedev_branch #需要注意，是push到远程的namedev_branch分支`

~~这个方式感觉有风险，项目成员要注意自己的branch，很容易因为忽略branch直接向master提交变更，对代码管理会添加麻烦~~

2. 负责人不为开发人员分别创建开发分支 （开发者自己创建）

* 虽然项目负责人不分别为开发人员创建分支，但是需要把他们添加到一个group中，否则开发人员在向项目push自己的开发分支时遇到权限错误
* 开发人员在把项目clone之后需要为自己新建一个开发分支（namedev_branch），因为经由git branch查看发现本地只有master分支
> `git branch namedev_branch  #新建分支`
> `git checkout namedev_branch  #切换到开发分支`
> `git push origin namedev_branch  #将新建的开发分支push到远程项目上`
* 之后的操作如同对待普通项目一样
> `git add hello.py`
> `git commit -m "add hello.py"`
> `git push -u origin namedev_branch #需要注意，是push到远程的namedev_branch分支`　　    

之后，两种方式下项目负责人都可以在项目的gitlab主页上看到每个开发人员的工作进度，并考虑何时merge开发人员的分支到master分支上以完善项目。
所有成员包括项目负责人除克隆、修改、提交代码这些操作外，其它merge、建立分支等操作都在Gitlab网页端进行。
所有分支中，master分支为主干分支，此分支的代码不允许直接修改，只能由其它分支（一般只由develop分支）发出merge请求，经项目管理员代码审查通过后合并代码，普通开发者无权执行push、merge等操作，确保此分支任何时候、任何tag处导出的项目代码都是稳定可正常运行的代码；develop分支为开发分支，可以接受由其它分支发起的merge请求，同样只能经项目管理员代码审查通过后予以合并。

### 1.2.2 团队初始化 

假设我们项目组分为两个组team1、team2，每个组有不同的组员和对应的不同的子项目,对项目组用户开放项目的访问，使用fork方式来做代码的更新和提交。
因此我们的gitlab的架构大概是这样的：

![团队分组](https://upload-images.jianshu.io/upload_images/13323529-ded6fd053a3a8e17.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1. 创建Group，在主界面上方的加号选择**New Group**,创建Group只需要填写 Group path 、Group name、Description  几个选项就可以了。Visibility Level选项选择 Private-私有仓库
2. 创建user，对需要加进来的团员，由管理员负责给他们创建相应的用户，创建用户需要填写合法的Email地址，正常情况下会向这个Email发送登陆的初始连接，但是如果不方便的话，也可以在创建后由管理员修改这个user的初始登陆密码。
3. 选中Group添加相应的user，user的角色分以下几种：Guest、Reporter、Developer、Maintainer、owner，基本上我们只会用到guest和developer两种。
4. 在Group中创建project，选中Subgroup，点击 New project 来创建新的项目。
5. 项目完成创建后，相应的团队成员也可以使用fork来获取项目的内容,fork后属于成员自己的项目的git地址是不一样的，这个一定要注意，后面提交代码都是提交到这个fork项目的地址，只有在网页端发起merge request 以及从master更新fork项目时才会用到主项目

### 1.2.3 代码提交管理 

当有新的代码提交请求时，项目负责人可以通过查看merge requests获取到来自fork或者branch的合并请求：
![请求合并列表](https://upload-images.jianshu.io/upload_images/13323529-6bdb8f0b55eda65e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
接受合并时，可以选择 Open in Web IDE 来检查审核变更的内容，确认没问题后点击Merge按钮来合并。
![完成审核后合并](https://upload-images.jianshu.io/upload_images/13323529-6bb43eb4f0b12ce5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 1.2.4 活跃度查询

右边条选择 Project -> Activity 可以看到push、merge、issue、comment（讨论）等信息
选择 Cycle Analytics 可以看到图形化的分析内容，这部分需要有足够的数据支持，还需要好好研究下。
> Cycle Analytics measures the time it takes to go from an idea to production for each project you have.
> 周期分析功能是监测从每个项目一个想法到产品所需的时间。

## 项目开发方式  issue+milestone+label

如何结合gitlab提供的这些功能来完整的梳理、管理一个产品、或者一个模块的开发方式
定义一个开发任务从开始如何分配到最后如何标识完成的过程。
这一块是用好gitlab的重点，否则就是用gitlab来做一个简单的代替svn的版本管理工具

# 2. 开发人员操作

## 2.1 登陆gitlab fork项目

项目成员首先利用浏览器进入gitlab的系统后，查看自己的group和project，并fork自己需要参与开发的project。
> 在project的detail界面中点击fork按钮。

fork时会提示选择**Namespace**，这个选择是用来决定这个工程所属的，可以选Users,或者选择Groups，这个会影响到后面工程的url，项目成员都统一选择users本人的命名空间就可以了。 

## 2.2 登陆gitlabfork项目

项目内容获取主要使用git客户端工具来实现，项目开发人员首先要在本机安装git客户端软件，[下载地址](https://www.git-scm.com/)
安装时基本都采用默认设置就可以了。
安装完成后我们主要使用Git Bash命令行工具来工作。

## 2.3 设置账户信息

设置修改本地对应的gitlab用户和邮箱。

```

#修改用户名和邮箱的命令
git config --global user.name "duwj"
git config --global user.email "duwj@gitlab.com"

#可以选择不设置全局的，而是临时的，但必须在一个 本地repository目录下：
git config --local  user.name "duwj"
git config --local user.email "duwj@gitlab.com"

#查看用户名和邮箱
git config user.name
git config user.email

``` 

## 2.4 配置ssh连接信息  （windows下没调成功）

1. 创建 SSH密钥
通过下面的命令生成密钥，将命令中的YOUR_EMAIL@YOUREMAIL.COM替换为注册Gitlab时用的Email地址。

`ssh-keygen -t rsa -C "duwj@gitlab.com"`

注意：Enter passphrase (empty for no passphrase) :时，可以直接按两次回车键输入一个空的 passphrase；也可以选择输入一个 passphrase 口令，如果此时你输入了一个passphrase，请牢记，之后每次提交时都需要输入这个口令来确认。

2. 获取公钥内容

SSH密钥生成结束后，根据提示信息找到SSH目录（通常ssh密钥保存路径均为~/.ssh 目录），会看到私钥id_rsa和公钥id_rsa.pub这两个文件，不要把私钥文件id_rsa的信息透露给任何人。
用记事本打开id_rsa.pub，复制里面的所有内容以备下一步使用。
3. 将密钥中的公钥添加到Gitlab
登录Gitlab的web站点，进入个人资料设置 - SSH Keys页面，将第2步所获得的内容粘贴在文本框key内，并填写title以便记忆，而后保存。

## 2.5 克隆代码

在gitlab网页端进入project的detail中可以下拉看到提示的代码信息。
* Create a new repository  创建新的本地库

```
git clone git@ip:test/test/document.git #注意这个地址是fork后的项目地址
cd document
```

这样在本地就可以获取到fork的项目内容。

## 2.6 正常代码更新提交

```
touch README.md
git add README.md 
git commit -m "add README"
git push -u origin master
```

## 2.7 更新本地仓库内容命令

```
git pull 
```

## 2.8 请求合并到master

在网页端进入到project的detail界面后，如果fork的项目代码有变动，在界面右上角会提示**Create merge request** 来提交合并申请
![提交合并申请](https://upload-images.jianshu.io/upload_images/13323529-aabdeaf19f2a2948.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


点击创建后，输入本次提交的title和描述，描述要说明本次提交修改的脚本、修改的内容等信息，便于管理员审核。


## 2.9 【关键】同步最新master库内容

fork后的项目不会自动从master主分支获取更新，需要负责fork的开发人员自己更新版本

如何更新已经fork的代码：
* 首先要先确定一下是否建立了主repo的远程源：

在本地项目库下执行 `git remote -v`
 
* 如果里面只能看到你自己的两个源(fetch 和 push)，那就需要添加主repo的源：

```
git remote add upstream https://github.com/被fork的仓库.git  
#这个地址是master主库的地址
git remote -v #能看到upstream了，后面upstream就是用来更新内容的分支
```

* fetch源分支的新版本到本地

执行 `git fetch upstream`

执行后本地库的内容会更新为与master库一致的内容 

* 合并本地两个版本的代码：

执行 `git merge upstream/master`

* 将在本地合并后的代码push到自己的github上去，以更新github上fork的仓库

执行 `git push origin master `

执行后网页端的仓库内容更新为合并后的新版本


对于开发人员来说，会使用fork克隆项目，会使用本地git客户端对项目内容进行更新、编辑、提交，会在网页端提交代码合并申请并且规范编写申请描述就足够了。
对管理人员来说，使用gitlab能方便的知道每个员工负责的内容的提交进度情况，方便对他们提交的代码进行质量的检查走读，还有更多统计类、开发进度管理等等功能，但是需要熟练掌握gitlab上的一些功能使用方法，比如使用issue来管理开发任务分配，使用milestone来制定和管理里程碑等等。


# 3. gitlab使用开发规范
参考：[gitlab使用开发规范](https://blog.csdn.net/ruanhao1203/article/details/80440824)