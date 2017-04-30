# coding:utf-8
import urlparse


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


def get_root(url=""):
    if url == "":
        return ""
    temp = urlparse.urlparse(url)
    url = temp.hostname
    print url
    if url.count(":") > 0:
        url = url.split(":")[0]
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
        else:
            hostname = url

    return scheme, hostname, port, "/" + path, query

# a, b, c, d, e = get_url_info("file:////baidu.com:8080/aa/bb?http://www.baidu.com,aaa.csads")
# print a, b, c, d, e
# a = urlparse.urlsplit("https://www.baidu.com:8080/aa.jsp?a=123&b=456")
# print a
