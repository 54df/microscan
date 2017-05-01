# coding:utf-8
import urlparse
import hashlib


def is_ip_addr(ip=""):
    if ip == "":
        return False
    try:
        ip = [int(x) for x in ip.split(".")]
    except:
        return False
    if len(ip) != 4:
        return False
    for x in ip:
        if x > 255 or x < 0:
            return False
    return True


def parseLink(html=""):
    from HTMLParser import HTMLParser

    class Html(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.result = set()

        def getResult(self):
            return self.result

        def handle_startendtag(self, tag, attrs):
            self.handle_starttag(tag, attrs)
            self.handle_endtag(tag)

        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                for key, value in attrs:
                    if key == "href":
                        self.result.add(value)

    h = Html()
    h.feed(html)
    return h.result


def get_root(url=""):
    if url == "":
        return ""
    url = get_url_info(url)[1]
    if url.count(".") > 1:
        url = '.'.join(url.split(".")[-2:])
    return url


def get_url_host(url):
    host = urlparse.urlparse(url)[1]
    if ':' in host:
        host = host[:host.find(':')]
    return host


def get_url_info(url):
    # return scheme host port path query
    if not url:
        return '', '', '', '', ''
    scheme = ""

    def getport(scheme):
        if scheme == "http":
            return '80'
        elif scheme == "https":
            return "443"
        else:
            return ""

    if url.startswith("file:///"):
        return 'file', url[8:], '', '', ''
    if url.count("://") > 0:
        tmp = url.split("://")[0]
        if tmp.isalpha():
            scheme = tmp
    hostname = ""
    port = ""
    path = ""
    query = ""
    if scheme:
        tmp = url.split("://", 1)[1]
        if tmp.count("/") > 0:
            host, querystring = tmp.split('/', 1)
            if host.count(":") > 0:
                hostname, port = host.split(":", 1)
            else:
                hostname = host
                port = getport(scheme)
            if querystring.count("?") > 0:
                path, query = querystring.split("?", 1)
            else:
                path = querystring
                query = ""
        else:
            if tmp.count(":") > 0:
                hostname, port = tmp.split(":", 1)
            else:
                hostname = tmp
                port = getport(scheme)
    else:
        port = "80"
        if url.count("/") > 0:
            host, querystring = url.split('/', 1)
            if host.count(":") > 0:
                hostname, port = host.split(":", 1)
            else:
                hostname = host
            if querystring.count("?") > 0:
                path, query = querystring.split("?", 1)
            else:
                path = querystring
                query = ""
        elif url.count(":") > 0:
            hostname, port = url.split(":", 1)
        else:
            hostname = url

    return scheme, hostname, int(port), "/" + path, query


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

# a, b, c, d, e = get_url_info("file:////baidu.com:8080/aa/bb?http://www.baidu.com,aaa.csads")
# print a, b, c, d, e
# a = urlparse.urlsplit("https://www.baidu.com:8080/aa.jsp?a=123&b=456")
# print a
