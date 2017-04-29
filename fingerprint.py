# coding:utf-8
import md5


class FingerPrint(object):
    def __init__(self):
        object.__setattr__(self, '__tmp', {})

    def get(self, key):
        key = key.lower()
        __tmp = self.__getattribute__('__tmp')
        if not __tmp.get(key):
            __tmp[key] = md5.md5(key).hexdigest()
        return __tmp.get(key)

    def __getattr__(self, key):
        key = key.lower()
        return self.get(key)

    def __setattr__(self, key, v):
        raise AttributeError('Read Only Attribute')

if __name__ == '__main__':
    fingerprint = FingerPrint()
    print fingerprint.aaa
    print fingerprint.bbb
    print fingerprint.aaa == fingerprint.AAA
