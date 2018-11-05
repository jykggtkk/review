
# 背景
在实际项目实施中，会编写很多在服务器执行的作业脚本。程序中凡是涉及到数据库链接、操作系统用户链接、IP地址、主机名称的内容都是敏感信息。在纯内网系统中往因为开发时间紧迫，往往都直接将这些敏感信息明文方式写在脚本中了。
稍微规范一点的，创建一个通用的config文件，将所有这类敏感信息记录在这个文件中，脚本以读取文件方式获取这些信息。这种方式的好处是脚本不用在应用迁移、灾备部署的时候再起不同的版本，尤其是大数据平台作业运行的脚本，如果是需要做灾备集群，这种方式可以减少生产变更时的人工干预操作。但是这种方式仍不能解决安全性的问题，只要config文件泄露，那么平台会非常危险。
因此在这个config文件的基础上，对其进行改造，实现对内容的加密，而脚本使用时再对其进行解密。因此要求有一个程序能对文本内容进行加密，也能进行反向解密。
不可逆的加密方法使用最多的就是md5加密算法，我们一般用来检验文件的完整和安全性，不适用这个场景。
使用python语言对文本内容进行加解密有多种方式，从网上搜索结果看主要有以下几种：
# 1.方法一 使用base64转编码
Base64是一种用64个字符来表示任意二进制数据的方法。
用记事本打开exe、jpg、pdf这些文件时，我们都会看到一大堆乱码，因为二进制文件包含很多无法显示和打印的字符，所以，如果要让记事本这样的文本处理软件能处理二进制数据，就需要一个二进制到字符串的转换方法。Base64是一种最常见的二进制编码方法。
Base64的原理很简单，首先，准备一个包含64个字符的数组：
`['A', 'B', 'C', ... 'a', 'b', 'c', ... '0', '1', ... '+', '/']`
然后，对二进制数据进行处理，每3个字节一组，一共是3x8=24bit，划为4组，每组正好6个bit,得到4个数字作为索引，然后查表，获得相应的4个字符，就是编码后的字符串。
所以，Base64编码会把3字节的二进制数据编码为4字节的文本数据，长度增加33%，好处是编码后的文本数据可以在邮件正文、网页等直接显示。
如果要编码的二进制数据不是3的倍数，最后会剩下1个或2个字节怎么办？
Base64用\x00字节在末尾补足后，再在编码的末尾加上1个或2个=号，表示补了多少字节，解码的时候，会自动去掉。

## Python内置的base64可以直接进行base64的编解码：
```
import base64
userPassword="sunlinemdp201810"
unkownPassword=base64.b64encode(bytes(userPassword,'utf-8'))
print("加密后："+str(unkownPassword,'utf-8'))
kownPassword=str(base64.b64decode(unkownPassword),'utf-8')
print('解密后：'+kownPassword)
```
>补充说明：python3中对字符串加解密的方法 base64.encodestring('test') 不能用 因此只能采用bytes方法然后中间进行格式转换

>由于标准的Base64编码后可能出现字符+和/，在URL中就不能直接作为参数，所以又有一种"url urlsafe_b64encode"的base64编码方法，实现对+和/的转码，在现在使用的版本中这个功能已经整合在b64encode方法中了 
```
userPassword="sunlinemdp201810"
unkownPassword=base64.b64encode(bytes(userPassword,'utf-8'))
print("加密后："+str(unkownPassword,'utf-8'))
unkownPassword=base64.urlsafe_b64encode(bytes(userPassword,'utf-8'))
print("解密后："+str(unkownPassword,'utf-8'))
base64.urlsafe_b64decode(unkownPassword)
```

# 2.方法二 win32com.client
样例代码如下：
```
import win32com.client
def encrypt(key,content): # key:密钥,content:明文
    EncryptedData = win32com.client.Dispatch('CAPICOM.EncryptedData')
    EncryptedData.Algorithm.KeyLength = 5
    EncryptedData.Algorithm.Name = 2
    EncryptedData.SetSecret(key)
    EncryptedData.Content = content
    return EncryptedData.Encrypt()
def decrypt(key,content): # key:密钥,content:密文
    EncryptedData = win32com.client.Dispatch('CAPICOM.EncryptedData')
    EncryptedData.Algorithm.KeyLength = 5
    EncryptedData.Algorithm.Name = 2
    EncryptedData.SetSecret(key)
    EncryptedData.Decrypt(content)
    str = EncryptedData.Content
    return str

s1 = encrypt('sunline', 'hello world')
s2 = decrypt('sunline', s1)
print s1,s2
 
```
win32com是python操作windows程序的第三方包，放在服务器上使用不太合适。

# 3.方法三 PyCrypto
一个极好的用于信息安全的python库，包括所有主流算法。
#### crypto库的模块结构
* Crypto.Cipher: Symmetric- and asymmetric-key encryption algorithms. 
   >Crypto.Cipher.AES: AES symmetric cipher
   >Crypto.Cipher.ARC2: RC2 symmetric cipher
   >Crypto.Cipher.ARC4: ARC4 symmetric cipher
   >Crypto.Cipher.Blowfish: Blowfish symmetric cipher
   >Crypto.Cipher.CAST: CAST-128 symmetric cipher
   >Crypto.Cipher.DES: DES symmetric cipher
   >Crypto.Cipher.DES3: Triple DES symmetric cipher
   >Crypto.Cipher.PKCS1_OAEP: RSA encryption protocol according to PKCS#1 OAEP
   >Crypto.Cipher.PKCS1_v1_5: RSA encryption protocol according to PKCS#1 v1.5
   >Crypto.Cipher.XOR: XOR toy cipher
   >Crypto.Cipher.blockalgo: Module with definitions common to all block ciphers.
* Crypto.Hash: Hashing algorithms
   >Crypto.Hash.HMAC: HMAC (Hash-based Message Authentication Code) algorithm
   >Crypto.Hash.MD2: MD2 cryptographic hash algorithm.
   >Crypto.Hash.MD4: MD4 cryptographic hash algorithm.
   >Crypto.Hash.MD5: MD5 cryptographic hash algorithm.
   >Crypto.Hash.RIPEMD: RIPEMD-160 cryptographic hash algorithm.
   >Crypto.Hash.SHA: SHA-1 cryptographic hash algorithm.
   >Crypto.Hash.SHA224: SHA-224 cryptographic hash algorithm.
   >Crypto.Hash.SHA256: SHA-256 cryptographic hash algorithm.
   >Crypto.Hash.SHA384: SHA-384 cryptographic hash algorithm.
   >Crypto.Hash.SHA512: SHA-512 cryptographic hash algorithm.
   >Crypto.Hash.hashalgo
* Crypto.Protocol: Cryptographic protocols
   >Crypto.Protocol.AllOrNothing: This file implements all-or-nothing package transformations.
   >Crypto.Protocol.Chaffing: This file implements the chaffing algorithm.
   >Crypto.Protocol.KDF: This file contains a collection of standard key derivation functions.
* Crypto.PublicKey: Public-key encryption and signature algorithms.
   >Crypto.PublicKey.DSA: DSA public-key signature algorithm.
   >Crypto.PublicKey.ElGamal: ElGamal public-key algorithm (randomized encryption and signature).
   >Crypto.PublicKey.RSA: RSA public-key cryptography algorithm (signature and encryption).
* Crypto.Random
   >Crypto.Random.Fortuna
   >Crypto.Random.Fortuna.FortunaAccumulator
   >Crypto.Random.Fortuna.FortunaGenerator
   >Crypto.Random.Fortuna.SHAd256: SHA_d-256 hash function implementation.
   >Crypto.Random.OSRNG: Provides a platform-independent interface to the random number generators supplied by various operating systems.
   >Crypto.Random.OSRNG.fallback
   >Crypto.Random.OSRNG.nt
   >Crypto.Random.OSRNG.posix
   >Crypto.Random.OSRNG.rng_base
   >Crypto.Random._UserFriendlyRNG
   >Crypto.Random.random: A cryptographically strong version of Python's standard "random" module.
* Crypto.Signature: Digital signature protocols
   >Crypto.Signature.PKCS1_PSS: RSA digital signature protocol with appendix according to PKCS#1 PSS.
   >Crypto.Signature.PKCS1_v1_5: RSA digital signature protocol according to PKCS#1 v1.5
* Crypto.Util: Miscellaneous modules
   >Crypto.Util.Counter: Fast counter functions for CTR cipher modes.
   >Crypto.Util.RFC1751
   >Crypto.Util._counter
   >Crypto.Util._number_new
   >Crypto.Util.asn1
   >Crypto.Util.number
   >Crypto.Util.py21compat: Compatibility code for Python 2.1
   >Crypto.Util.py3compat: Compatibility code for handling string/bytes changes from Python 2.x to Py3k
   >Crypto.Util.randpool
   >Crypto.Util.strxor
   >Crypto.Util.winrandom
* Crypto.pct_warnings

对于服务器配置文件加密，不需要复杂的公钥方式，使用对称密钥算法AES足够满足我们的需求。

## 服务器文件加密实现
现在假定要对一个存储各类ip、账户、密码的global.properties文件进行加密，同时，支持在读取时进行解密。
global.properties的内容假定如下图所示：
```
bgp.inceptor.in1.ip=10.22.179.13
bgp.inceptor.in1.default=cmr
bgp.inceptor.in2.ip=10.22.179.14
bgp.inceptor.in2.default=default
bdp.ldap.mdp.username=mdp
bdp.ldap.mdp.password=mdp
```
每一行使用等号将信息分为两段，等号左边是信息项名称，等号右边是信息项具体的内容，我们要对信息项的具体的内容进行加密。
首先做需求分析，我们的需求可以拆分为以下几个：
1. 实现对指定字符串内容基于某个密钥的加解密内容输出
2. 读取指定加密配置文件，根据信息项名称读取指定内容后加解密输出
3. 读取指定配置文件，对文件内每一行信息项的具体内容进行加解密后生成新的加解密后的配置文件

第二步做程序设计，我是从功能上进行拆分设计：
基本功能包括：    
2. 加密解密      
3. 获取文件
4. 文件指定内容读取  #https://blog.csdn.net/tengxing007/article/details/72466187    读取properties文件
5. 运行日志 --后续--
6. 异常处理 --后续-- 

交互操作包括：
1. 参数读取解析
2. 具体功能实现，输出结果或生成文件

输入输出设计：
1. 输入：  功能类型 -d  对应 四种功能需求
2. 输入：  密钥 -k    密钥内容
3. 输入：  加密内容或解密内容 -c 对应功能2 
4. 输入：  配置文件路径名称  -f 对应功能 234
5. 输入：  信息项内容  -i    对应功能4
6. 输出：  加解密文   对应功能 1 4 
7. 输出：  文件路径及名称  对应功能 2 3 

 
附[加密算法介绍](https://blog.csdn.net/kamaliang/article/details/6690979)
附[pycrypto调用方法](https://www.dlitz.net/software/pycrypto/api/current/)

