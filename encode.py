# coding:utf-8
import hashlib


class Encode:
    def __init__(self, encode=""):
        self.encode = encode

    def __getattr__(self, name):
        return Encode(name)

    def __call__(self, *args):
        code1, code2 = self.encode.split("2")
        return ''.join(args).decode(code1).encode(code2)


class Encrypted:
    def __init__(self, methodname=""):
        self.__method = methodname

    def __getattr__(self, name):
        return Encrypted(name)

    def __str__(self):
        return "支持的加密操作：" + ','.join(['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'])

    def __call__(self, *args):
        obj = hashlib.new(self.__method)
        obj.update(''.join(args))
        return obj.hexdigest()


if __name__ == '__main__':
    encode = Encode()
    print encode.gbk2gbk('测试')
    print encode.gbk2utf8('测试')
    print encode.utf82gbk('测试')
    print encode.utf82utf8('测试')

    a = Encrypted()
    print a.sha512('123456')
    print a.md5('123456')
    print a