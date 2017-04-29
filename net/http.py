#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib
import url as urlutil
import socket
import StringIO
import zlib
import gzip


class RAWException(Exception):
    pass


class Microhttp:
    def __init__(self):
        pass

    def __str__(self):
        return "我们不是原创，我们只做高仿\n" \
               "在此，感谢看轮子的胖次，感谢Medici Yan表哥\n" \
               "感谢看热闹的同学们\n" \
               "有发现bug请联系QQ1197795981\n" \
               "\t\t守护者 2017.04.25"

    def _make_connection(self, scheme, host, port):
        if scheme == "https":
            return httplib.HTTPSConnection(host, int(port))
        else:
            return httplib.HTTPConnection(host, int(port))

    def http(self, url, post=None, **kwargs):
        raw = kwargs.get("raw", None)
        headers = kwargs.get('headers', {})
        rheaders = {}
        cookies = kwargs.get('cookies', set())
        method = 'POST' if post != None else 'GET'
        scheme, host, port, path, query = urlutil.get_url_info(url)
        if not host:
            raise RAWException("主机解析出错")
        if raw:
            pass
        else:
            pass
        conn = self._make_connection(scheme, host, port)
        conn.request(method, path + "?" + query)
        response = conn.getresponse()
        tmp = response.getheaders()
        for key, value in tmp:
            rheaders[key] = value
        return response.status, rheaders, response.read(), rheaders.get('Location')

    def httpraw(self, url, raw, timeout=3):
        # 该方法不解析任何数据
        scheme, host, port, path, query = urlutil.get_url_info(url)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, int(port)))
        sock.sendall(raw)
        responseMapper = {}
        ver, code, status = 'HTTP/1.1', 200, ""
        body = ""
        buffered = ""
        upkey = ""
        jumpurl = ""
        while True:
            # 取响应行
            buff = sock.recv(1)
            buffered += buff
            if buffered.endswith("\r\n"):
                # print buffered
                ver, code, status = buffered.split(" ", 2)
                code = int(code)
                buffered = ""
                break
        # print "Code:", code
        while True:
            # 取响应头
            buff = sock.recv(1)
            buffered += buff
            if buffered.endswith("\r\n"):
                # print buffered
                buffered = buffered.strip()
                if not buffered:
                    break
                # 如果为一行
                key = ""
                value = ""
                if buffered.count(": "):
                    # 如果包含键值对
                    key, value = buffered.split(": ", 10)
                else:
                    key = upkey
                    value = buffered
                if responseMapper.has_key(key):
                    responseMapper[key] = responseMapper.get(key) + value
                else:
                    responseMapper[key] = value
                # 清空缓冲区
                buffered = ""
        # print "Response:", responseMapper
        length = responseMapper.get("Content-Length", -1)
        length = int(length)
        encode = responseMapper.get("Content-Encoding", '')
        if length < 0:
            if encode == "gzip":
                blength = 0
                buff = ""
                while True:
                    buffered = sock.recv(1)
                    if buffered and len(buffered) == 1:
                        buff += buffered
                        if buff.endswith("\r\n"):
                            buff = buff.strip()
                            blength = int(buff, 16)
                            b = sock.recv(blength).split("\r\n")[0]
                            print blength, len(b), repr(b)
                            body = gzip.GzipFile(fileobj=StringIO.StringIO(b)).read()
                            break
            else:
                while True:
                    # 取请求实体
                    buffered = sock.recv(1024)
                    if buffered and len(buffered) == 1024:
                        # print buffered
                        body += buffered
                    else:
                        body += buffered
                        break
        else:
            body = sock.recv(length)
        if encode == 'deflate':
            try:
                body = zlib.decompress(body, - zlib.MAX_WBITS)
            except:
                body = zlib.decompress(body)

        # print "Body:", body
        sock.close()
        if 300 <= code <= 305:
            jumpurl = responseMapper.get('Location', "")
        allbody = ver + " " + str(code) + " " + status
        for key in responseMapper:
            allbody += key + ": " + responseMapper.get(key) + "\r\n"
        allbody += "\r\n" + body
        return code, responseMapper, body, jumpurl, allbody


if __name__ == '__main__':
    print Microhttp()
