# coding:utf-8
import MicroCore
import urllib2

# Encode
encode = MicroCore.Encode()
print encode.gbk2gbk('测试')
print encode.gbk2utf8('测试')
print encode.utf82gbk(encode.gbk2utf8('测试'))
print encode.utf82utf8('测试')

# Encrypted
encrypted = MicroCore.Encrypted()
print encrypted.md5("测试")
print encrypted.sha1("测试")
print encrypted.sha224("测试")
print encrypted.sha256("测试")
print encrypted.sha384("测试")
print encrypted.sha512("测试")
print encrypted

# util
print MicroCore.is_ip_addr("127.0.0.1")
print MicroCore.is_ip_addr("127.0.0.256")
print MicroCore.get_root("http://www.baidu.com")
print MicroCore.get_root("http://www.a.a.com")
scheme, host, port, path, query = MicroCore.get_url_info("http://aaa.bbb.com/a?url=http://www.baidu.com")
print 'scheme:', scheme, 'host:', host, 'port:', port, 'path:', path, 'query:', query
html = urllib2.urlopen("http://baike.baidu.com/link?url=gOaIoVZuRW0DpBbnwyIStiBM4f4zNE_bLTAYypWwqt8w4cPU2BQiDXOh6aewyCStHGojqVwLtZ8sJU405Ic9rmEHw-VtqMM7-7ldqyFzAYhsit_3brt2ICdPldWJNGok9Fp7-y1Z3cBXvlI5Mm7-y__5ygMGHlyHEsobv6TQ1cuW765O5Zez7Y8SmIiLGdf0lFN9yzQP9cs0jla0WGTK1EdYnq135uJ3A-7lU2TdbfW").read()
for link in MicroCore.parseLink(html):
    print link
