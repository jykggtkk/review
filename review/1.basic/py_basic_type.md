python基本数据类型及常用方法
# python变量概念
Python 中的变量不需要声明。

变量在创建变量时会在内存中开辟一个空间。

基于变量的数据类型，解释器会分配指定内存，并决定什么数据可以被存储在这段指定的内存中。

因此，变量可以指定不同的数据类型，这些变量可以存储整数，小数或字符。
## 变量赋值即创建
每个变量在使用前都必须赋值，变量赋值以后该变量才会被创建。
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
  >不可改变的数据类型，这意味着改变数字数据类型会分配一个新的对象
* 可变数据（3 个）：List（列表）、Dictionary（字典）、Set（集合）
  >可变数据类型，意味着对以上数据类型进行复制创建时，只是创建了相应内存内容的一个新的连接

## 类型查看及判断
内置的 type() 函数可以用来查询变量所指的对象类型
`type(counter)`

_使用`print(type(counter)`方法输出`type()`结果时，python3显示`<class 'int'>`，而python2显示`<type 'int'>`_

此外还可以用`isinstance()`来判断：

`isinstance(counter, int)`,函数返回一个布尔值

在使用时，两种方法都可以用来判断类型匹配，似乎`isinstance()`更方便些，实际上这两种方法最重要的区别需要注意一下：
* type()不会认为子类是一种父类类型。
* isinstance()会认为子类是一种父类类型。
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
   > Python3只有一种整数类型 int，表示为长整型，没有 python2 中的 Long。python3的int没有长度限制(实际上由于机器内存的有限，我们使用的整数是不可能无限大的)
* Python2支持int(有符号整型)、long(长整型)、float(浮点型)、bool(布尔型)、complex(复数)
   >long也可以代表八进制和十六进制，以L结尾以显式声明其类型，建议不再使用这种类型
* 布尔型的值域为关键字True和False，注意首字母大写，实际值分别对应为1和0，可以和其他数值做计算
* 浮点型也可以使用科学计数法表示(`2.5e2 = 2.5 x 102 = 250.0`)
演示：
```
var_int = 10      #int型
var_float = -21.9  #float型
var_science = 32.3e+5    #float型科学记数法

#通过使用del语句删除单个或多个对象的引用
del var_int 
del var_float, var_bool,var_complex
``` 