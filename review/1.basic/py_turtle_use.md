# python之绘制图形库turtle

turtle库是python的基础绘图库，[官方手册](https://docs.python.org/2/library/turtle.html)

这个库被介绍为一个最常用的用来给孩子们介绍编程知识的方法库，其主要是用于程序设计入门，是标准库之一，利用turtle可以制作很多复杂的绘图。

### turtle原理理解

turtle名称含义为“海龟”，我们想象一只海龟，位于显示器上窗体的正中心，在画布上游走，它游走的轨迹就形成了绘制的图形。
海龟的运动是由程序控制的，它可以变换颜色，改变大小（宽度）等。

### 绘图窗体

`turtle.setup(width,height,startx,starty)`

使用turtle的setup函数，可以在屏幕中生成一个窗口（窗体），设置窗体的大小和位置，这个窗口就是画布的范围。
画布的最小单位是像素，屏幕的坐标系以左上角为原点（0，0）分布。

图：![屏幕坐标系及窗体](https://upload-images.jianshu.io/upload_images/13323529-f952a2dbd0585210.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

setup的四个参数分别指的是 
* width：窗体的宽度
* height：窗体的高度
* startx:窗体距离屏幕边缘的左边像素距离
* starty:窗体距离屏幕上面边缘的像素距离
其中，后两个参数是可选项，如果不填写该参数，窗口会默认显示在屏幕的正中间。

setup()也是可选的，只是需要定义窗口的大小及位置是才使用。

###  turtle空间坐标体系

#### 绝对坐标

以屏幕中间为原点（0，0），形成四象限的坐标体系。

![绝对坐标体系](https://upload-images.jianshu.io/upload_images/13323529-afffece4027ac011.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以使用`turtle.goto(x,y)`方法来让海龟沿着绝对坐标进行运动：
```
import turtle

turtle.goto(100,100)
turtle.goto(100,-100)
turtle.goto(-100,-100)
turtle.goto(-100,100)
turtle.goto(0,0)
```
#### 海龟坐标

是以海龟的视角的坐标体系，分为四个方向：
 ![海龟坐标体系](https://upload-images.jianshu.io/upload_images/13323529-e38c18a79e0cd04d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用以下方法可以使海龟在指向的方向上移动、转向等。

```
turtle.fd(distance)   #前进
turtle.bk(distance)   #后退
turtle.rt(angle)      #右转
turtle.lt(angle)      #左转

```

####  空间坐标体系下绘图


```
import turtle 

turtle.left(45)
turtle.fd(150)
turtle.right(135)
turtle.fd(300)
turtle.left(135)
turtle.fd(150)
```
通过这几句可以在画布上实现一个斜着的Z字。


###  turtle角度坐标体系

#### 绝对角度坐标

绝对坐标体系下 有一个绝对角度体系

使用`turtle.seth()`方法改变海龟的朝向，但不运动

#### 海龟角度坐标

海龟的角度坐标体系下，只分左转和右转两种情况。
使用以下方法来改变它的角度：

```
turtle.left(angle) #向海龟左边改变运行方向
turtle.right(angle) #向海龟右边改变运行方向
```

### RGB色彩体系

三种基础颜色：`red green blue `构成万物色。
能够覆盖视力能感知的所有颜色。
在计算机RGB色彩体系中，每个基础颜色的取值范围是0-255的整数，或0-1的小数

常用颜色：

| 英文名称  | RGB整数值 |RGB小数值|中文名称|
|:----------:|:-----:|:----------:|:-----:|
|white|255,255,255|1,1,1|白色|
|yellow|255,255,0|1,1,0|黄色|
|magenta|255,0,255|1,0,1|洋红|
|cyan|0,255,255|0，1，1|青色|
|blue|0,0,255|0，0，1|蓝色|
|black|0,0,0|0，0，0|黑色|
|purple|160,32,240|0.63,0.13,0.94|紫色|

使用`turtle.colormode(mode)`来调整海龟的颜色，默认采用RGB小数值，可以切换为整数值
mode 小数值模式： 1.0
mode 整数值模式： 255


### turtle 函数介绍

#### 画笔控制函数

##### 画笔操作后一直有效，一般成对使用

```
turtle.penup()  # turtle.pu()  抬起画笔，不再画线

turtle.pendown() # turtle.pd() 落下画笔，继续画线

```
##### 画笔设置后一直有效，直到下次重新设置

```
turtle.pensize(width)  # turtle.width(width)  设置画笔的宽度
turtle.pencolor(color) # color 为 色彩RGB值 设置画笔的颜色

# color参数 有三种形式
# 颜色字符串
turtle.pencolor('purple')  # 小写
# RGB小数值
turtle.pencolor(0.63,0.13,0.94) #三个小数值
# RGB数值元组  
turtle.pencolor((0.63,0.13,0.94))  # 一个三元素元组

```

#### 运动控制函数

控制画笔的行进： 走直线&走曲线
```
# 直线
turtle.forward(d)  # turtle.fd(d)   d为参数行进距离   控制画笔向前走d长度的直线  d可以为负数，表示向后运动

# 曲线
turtle.circle(r,extent=None) # 根据半径r绘制extent角度的弧形    r 默认圆心在画笔左端点距离r长度的地方  extent是绘制的角度，默认绘制完整的圆形
turtle.circle(100) # 在画笔的左侧（也就是上方）100距离的位置上然后以弧形来运动，没有设置extent参数，因此会绘制整个圆形
turtle.circle(-100,90) #圆心在画笔的右侧100距离（也就是下方）上，然后extent为90，因此绘制一个90度的弧形。
```

#### 方向控制函数

控制h画笔面对的方向：绝对角度 & 画笔角度

```
# 绝对角度转向函数
turtle.setheading(angle)  # turtle.seth(angle)  改变画笔的面向的角度（ 初始方向是画布的正右方）  参数angle是绝对坐标系的角度    

#画笔角度转向函数
turtle.left(angle)  # 向左转angle度
turtle.right(angle) # 向右转angle度

```
方向控制函数只改方向，但是不会动，运动由运动控制函数实现。

熟悉以上这些，就能完成基本的绘图了 

样例：

```
#PythonDraw.py
import turtle
turtle.setup(650, 350, 200, 200)
turtle.penup()
turtle.fd(-250)
turtle.pendown()
turtle.pensize(25)
turtle.pencolor("purple")
turtle.seth(-40)
for i in range(4):
    turtle.circle(40, 80)
    turtle.circle(-40, 80)
turtle.circle(40, 80/2)
turtle.fd(40)
turtle.circle(16, 180)
turtle.fd(40 * 2/3)
turtle.done()
```
```
import turtle

for i in range(9):
    turtle.fd(100)
    turtle.left(80)
    i=i+1
turtle.done()
```


本文参考 [ Python语言程序设计课程](https://www.icourse163.org/course/BIT-268001) 
更多函数方法使用 参考文章 [python之绘制图形库turtle](https://www.cnblogs.com/bravestarrhu/p/8287261.html)