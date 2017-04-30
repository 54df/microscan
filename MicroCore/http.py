#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib
import url as urlutil
import socket
import StringIO
import zlib
import gzip
import ssl


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
        method = kwargs.get('method')
        res_headers = {}
        req_headers = {}
        cookies = kwargs.get('cookies', {})
        method = method if method != None else 'POST' if post != None else 'GET'
        scheme, host, port, path, query = urlutil.get_url_info(url)
        req_url = path
        if query:
            req_url += "?" + query
        if not host:
            raise RAWException("主机解析出错")
        if type(post) == unicode:
            post = post.encode('utf-8', 'ignore')
        if type(raw) == unicode:
            raw = raw.encode('utf-8', 'ignore')
        # 编译一个连接
        conn = self._make_connection(scheme, host, port)
        # 遍历请求头到请求头数组
        for key in headers:
            req_headers[key] = headers.get(key)
        c_tmp = []
        if cookies:
            for key in cookies:
                c_tmp.append(str(key) + "=" + str(cookies.get(key)))
            req_headers['Cookie'] = ';'.join(c_tmp)
        # 处理raw数据，兼容传参数(不知道是不是在给自己挖坑)
        if raw:
            post = ""
            raw = StringIO.StringIO(raw)
            first_line = raw.readline()
            first_line = first_line.strip()
            # 处理第一行请求数据，该行一半为请求行，也可能发生异常变成请求头，或者此行不包括空格冒号就是请求实体
            if first_line.count(' ') < 1 and first_line:
                if first_line.count(':') < 1:
                    post = first_line
                else:
                    req_headers[first_line.split(' ', 1)[0]] = first_line.split(' ', 1)[1]
            elif first_line.count(' ') < 2 and first_line:
                method, req_url = first_line.split(' ', 1)
            elif first_line:
                method, req_url, _ = first_line.split(' ', 2)
            # 读取剩下的请求行
            # 处理不包含冒号行，加入上一行请求中
            up_key = ""
            for line in raw:
                line = line.strip()
                if not line:
                    break
                if line.count(':') < 1:
                    req_headers[up_key] = req_headers.get(up_key, '') + line
                else:
                    line = line.split(':', 1)
                    up_key = line[0]
                    req_headers[line[0]] = line[1]
            # 处理请求实体
            for line in raw:
                line = line.strip()
                if post:
                    post += line
                else:
                    post = line
            post = post.strip()
            if not post:
                post = None
        # 设置缺失的请求头,位置比较特殊，优先用户设置
        if post:
            req_headers['Content-Length'] = str(len(post))
            req_headers['Content-Type'] = req_headers.get('Content-Type', 'application/x-www-form-urlencoded')
            if method == 'GET':
                req_headers.pop('Content-Length')
        req_headers['Accept-Encoding'] = req_headers.get('Accept-Encoding', 'gzip, deflate')
        req_headers['Connection'] = req_headers.get('Connection', 'Keep-Alive')
        req_headers['User-Agent'] = req_headers.get('User-Agent',
                                                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36")
        # 开始请求
        # print method, req_url, post, req_headers
        conn.request(method, req_url, post, req_headers)
        response = conn.getresponse()
        # 处理返回头
        tmp = response.getheaders()
        body = response.read()
        code = response.status
        all_body = "HTTP/1.1 " + str(code) + "\r\n"
        for key, value in tmp:
            res_headers[str(key)] = str(value)
            all_body += (str(key) + ":" + str(value) + "\r\n")
        jump_url = ''
        if 300 <= code <= 305:
            jump_url = res_headers.get('Location', '')
            jump_url = req_headers.get('location', '') if not jump_url else jump_url
        all_body += '\r\n' + body
        return code, res_headers, body, jump_url, all_body

    def httpraw(self, url, raw, timeout=3):
        # 该方法不解析任何数据
        scheme, host, port, path, query = urlutil.get_url_info(url)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        if scheme == "https":
            sock = ssl.wrap_socket(sock)
        sock.connect((host, int(port)))
        sock.sendall(raw)
        response_mapper = {}
        ver, code, status = 'HTTP/1.1', 200, ""
        body = ""
        buffered = ""
        up_key = ""
        jump_url = ""
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
                if buffered.count(":"):
                    # 如果包含键值对
                    key, value = buffered.split(":", 1)
                else:
                    key = up_key
                    value = buffered
                if response_mapper.has_key(key):
                    response_mapper[key] = response_mapper.get(key) + value
                else:
                    response_mapper[key] = value
                # 清空缓冲区
                buffered = ""
        # print "Response:", response_mapper
        length = response_mapper.get("Content-Length", -1)
        length = int(length)
        encode = response_mapper.get("Content-Encoding", '')
        if length < 0:
            if encode == "gzip":
                buff = ""
                while True:
                    buffered = sock.recv(1)
                    if buffered and len(buffered) == 1:
                        buff += buffered
                        if buff.endswith("\r\n"):
                            buff = buff.strip()
                            b_length = int(buff, 16)
                            b = sock.recv(b_length).split("\r\n")[0]
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
            except Exception, e:
                body = zlib.decompress(body)
        sock.close()
        if 300 <= code <= 305:
            jump_url = response_mapper.get('Location', "")
        all_body = ver + " " + str(code) + " " + status
        for key in response_mapper:
            all_body += key + ":" + response_mapper.get(key) + "\r\n"
        all_body += "\r\n" + body
        return code, response_mapper, body, jump_url, all_body


if __name__ == '__main__':
    print Microhttp()
