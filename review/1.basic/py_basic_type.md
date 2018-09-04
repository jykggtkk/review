# python变量概念
python中的变量不需要声明，但使用时必须赋值。
变量在创建时会在内存中开辟一个空间。
基于变量的数据类型，解释器会分配指定内存，并决定什么数据可以被存储在这段指定的内存中。
因此，变量可以指定不同的数据类型，这些变量可以存储整数，小数或字符。
## 变量赋值即创建
```
counter = 100 # 赋值整型变量
miles = 1000.0 # 浮点型
name = "John" # 字符串

print(counter)
print(miles)
print(name)
```
## 多个变量赋值
同时为多个变量赋值相同的值:`a = b = c = 1`创建一个整型对象，值为1，三个变量被分配到相同的内存空间上。
同时为多个变量指定不同类型的值:`a, b, c = 1, 2, "john"`两个整型对象 1 和 2 分别分配给变量 a 和 b，字符串对象 "john" 分配给变量 c。
_在 Python 中，变量就是变量，它没有类型，我们所说的"类型"是变量所指的内存中对象的类型。_
# 标准数据类型
在内存中存储的数据可以有多种类型。
Python定义了一些标准类型，用于存储各种类型的数据。
Python中有六个标准的数据类型：
* Number（数字）
* String（字符串）
* List（列表）
* Tuple（元组）
* Set（集合）
* Dictionary（字典）

Python3 的六个标准数据类型中：
* 不可变数据（3 个）：Number（数字）、String（字符串）、Tuple（元组）
  >_不可改变的数据类型，这意味着改变数字数据类型会分配一个新的对象_
* 可变数据（3 个）：List（列表）、Dictionary（字典）、Set（集合）
  >_可变数据类型，意味着对以上数据类型进行复制创建时，只是创建了相应内存内容的一个新的连接_
## 类型查看及判断
内置的`type()`函数可以用来查询变量所指的对象类型
`type(counter)`
_使用`print(type(counter)`方法输出`type()`结果时，python3显示`<class 'int'>`，而python2显示`<type 'int'>`_
此外还可以用`isinstance()`来判断：
`isinstance(counter, int)`,函数返回一个布尔值
在使用时，两种方法都可以用来判断类型匹配，似乎`isinstance()`更方便些，实际上这两种方法最重要的区别需要注意一下：
* `type()`不会认为子类是一种父类类型。
* `isinstance()`会认为子类是一种父类类型。
```
class Foo(object):
    pass

class Bar(Foo):
    pass

print(type(Foo()) == Foo)   #return True
print(type(Bar()) == Foo)   #return False
print(isinstance(Bar(),Foo)) #return True
```
## Number（数字）
数字数据类型用于存储数值。
当指定一个值时，Number对象就会被创建：`var_int = 10`
注意：
* Python3支持 int(整型)、float(浮点型)、bool(布尔型)、complex(复数)
   > _Python3只有一种整数类型 int，表示为长整型，没有 python2 中的 Long。python3的int没有长度限制(实际上由于机器内存的有限，我们使用的整数是不可能无限大的)_
* Python2支持int(有符号整型)、long(长整型)、float(浮点型)、bool(布尔型)、complex(复数)
   >_long也可以代表八进制和十六进制，以L结尾以显式声明其类型，建议不再使用这种类型_
* 布尔型的值域为关键字True和False，注意首字母大写，实际值分别对应为1和0，可以和其他数值做计算
* 浮点型也可以使用科学计数法表示(`2.5e2 = 2.5 x 102 = 250.0`)
```
var_int = 10      #int型
var_bool = True   #bool型
var_float = -21.9  #float型
var_complex = 4.53e-7j   #complex型

var_science = 32.3e+5    #float型科学记数法

var_bool_add = var_int + var_bool #布尔值与int型做加减运算

del var_int   #通过使用del语句删除单个对象的引用
del var_float, var_science,var_bool,var_complex,var_bool_add   #通过使用del语句删除多个对象的引用
``` 
## String（字符串）
字符串或串(String)是由数字、字母、下划线组成的一串字符,一般用单引号 ' 或双引号 " 括起来，同时使用反斜杠 \ 转义特殊字符。
Python 没有单独的字符类型，一个字符就是长度为1的字符串。
String类型可以作为一种字串列表对文本内容进行截取处理，有2种取值顺序：
* 从左到右索引默认0开始的，最大范围是字符串长度少1
* 从右到左索引默认-1开始的，最大范围是字符串开头

|  R|  U|  N|  O|  O|  B|
|:--|:--|:--|:--|:--|:--|
|  0|  1|  2|  3|  4|  5|
| -6| -5| -4| -3| -2| -1|

实现从字符串中获取一段子字符串可以使用 __[头下标:尾下标]__ 来截取相应的字符串，其中下标是从 0 开始算起，可以是正数或负数，下标可以为空表示取到头或尾
__[头下标:尾下标]__ 获取的子字符串包含头下标的字符，但不包含尾下标的字符。
```
str = 'Hello World!'

print(str[0])     #'H'      字符串中的第一个字符
print(str[1:5])   #'ello'   第二位到第六位字符
print(str[2:])    #'llo World!'  从三个字符开始的字符串
print(str[:4])    #'Hell'   从开头的4位字符 
print(str[-7:-3]) #' Wor' 从倒数第7位到倒数第四位
print(str[:-3])   #'Hello Wor' 从倒数最后一位到倒数第四位
print(str[-3:])   #'ld!' 从倒数第三位到倒数第一位

print(str * 2)    #'Hello World!Hello World!' 输出字符串两次
print(str + "TEST")  #'Hello World!TEST' 输出连接的字符串

print('H' in str)      #如果字符串中包含给定的字符返回 True
print("M" not in str) #如果字符串中不包含给定的字符返回 True
```
### 字符串转义
符串中的转义字符为\，在其中包含的转义字符如下：
|转义符|解释|
|:----|:--|
|`\\`|反斜杠\|
|`\”`|双引号 “|
|`\’`|单引号 ‘|
|`\n`|换行|
|`\r`|回车|
|`\t`|制表|

如果不想让反斜杠发生转义，可以在字符串前面添加一个 r，表示原始字符串：
```
print('Ru\noob')    # Ru  oob
print(r'Ru\noob')   # Ru\noob
```
另外，反斜杠(\)可以作为续行符，表示下一行是上一行的延续

### 格式字符串  % 
python格式化字符串有%和format_spec两种字符串格式控制符。
字符串输入数据格式类型(%格式操作符号)比较多，常用的就是 %s 和 %d 
|类型 |含义|
|:----|:--|
|%%|百分号标记 |
|%c|字符及其ASCII码|
|%s|字符串| 
|%d|有符号整数(十进制)| 
|%e|浮点数字(科学计数法)|
|%f|浮点数字(用小数点符号)|
|%g|浮点数字(根据值的大小采用%e或%f)| 

使用格式规范（拓展）：
`%[(name)][flag][width][.][precision]type`
name:可为空，数字(占位),命名(传递参数名,不能以数字开头)以字典格式映射格式化，其为键名
`flag =  "+" | "-" | "#" | "0"　` 标记格式限定符号,包含+-#和0,+表示右对齐(会显示正负号),-左对齐,前面默认为填充空格(即默认右对齐)，0表示填充0，#表示八进制时前面补充0,16进制数填充0x,二进制填充0b
width:宽度(最短长度,包含小数点,小于width时会填充)
precision:小数点后的位数 
type:输入格式类型
样例：
```
#简单的：
print('本篇文章作者是%s ,发表于%s,年龄是%d岁'%('linghuanyun','CSDN',18))
#复杂的：
print("%.5f" %5) #输出5.000000
print("%-7s3" %("python"))#输出python 3
print("%.3e" %2016)#输出2.016e+03,也可以写大E
print("%d %s" %(123456,"myblog"))#输出123456 myblog
print("%(what)s is %(year)d" % {"what":"this year","year":2016})#输出this year is 2016
```
### format_spec格式（拓展）
对字符串有更深的格式化需求时，可以参考这种格式的样例酌情使用
{[name][:][[fill]align][sign][#][0][width][,][.precision][type]}
用{}包裹name命名传递给format以命名=值 写法,非字典映射
fill：指待格式化的字符串
`align =  "<" | ">" | "=" | "^"　`　#align是对齐方式，<是左对齐， >是右对齐，^是居中对齐。
`sign  =  "+" | "-" | " "　`　#sign是符号， +表示正号， -表示负号
width:宽度(最短长度,包含小数点,小于width时会填充)
precision:小数点后的位数
type:输入格式类型 
样例：
```
print("{:,}".format(123456)) #输出123,456
print("{a:w^8}".format(a="8")) #输出www8wwww,填充w
print("{0} with {1}".format("hello","fun"))   #输出hello with fun,这与CSharp的格式化字符(占位符)相似
print("{}{}{}".format("spkk",".","cn"))   #输出spkk.cn
print("{a[0]}{a[1]}{a[2]}".format(a=["spkk",".","cn"]))    #输出spkk.cn
print("{dict[host]}{dict[dot]}{dict[domain]}".format(dict={"host":"www","domain":"spkk.cn","dot":"."}))    #输出www.spkk.cn
print("{a}{b}".format(a="python",b="3"))    #输出python3
print("{who} {doing} {0}".format("python",doing="like",who="I"))    #输出I like python
```
