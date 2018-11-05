#coding: utf8
'''
实现对指定字符串内容基于某个密钥的加解密内容输出
密钥使用base64多加一层处理

version: v0.0.1
author:  Duwj
date: 2018-10-24
'''

import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64

class optcrypt():
    def __init__(self, key):
        self.key = str(base64.b64decode(key))
        self.mode = AES.MODE_CBC
        #self.iv = Random.new().read(AES.block_size)
    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def aesencrypt(self, text):

        #密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        cipher = AES.new(self.key, self.mode, self.key)
        #cipher=AES.new(bytes(self.key), self.mode,Random.new().read(AES.block_size))

        #加密文本text必须为16的倍数
        add = 16 - (len(text) % 16)
        text = text + ('\0' * (16 - (len(text) % 16)))
        self.ciphertext = cipher.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)
     
    #解密   
    def aesdecrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        #16进制转回后解密
        plain_text = cryptor.decrypt(a2b_hex(text))

        #rstrip()去掉补的空格
        return plain_text.rstrip('\0')


if __name__ == '__main__':
    #设置环境编码
    reload(sys)
    sys.setdefaultencoding('utf8')
    #测试
    pc = optcrypt('c3VubGluZW1kcDIwMTgxMQ==') 
    e = pc.aesencrypt("duwj") 
    d = pc.aesdecrypt("d518cdd30b854b84f5aa7c5511e03e38") 
    print "info:sunline,encrypt:"+e+",decrypt:"+d      
 