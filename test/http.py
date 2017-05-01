# coding:utf-8
import MicroCore

mm = MicroCore.Microhttp()

# 直接访问网页栗子
code, headers, body, jumpurl, allbody = mm.http('https://www.baidu.com')
print code, headers, body, jumpurl, allbody

# 带post访问栗子
code, headers, body, jumpurl, allbody = mm.http('https://www.baidu.com', post='''aaaaaaaaaaaaaaaaaaaaaaa''')
print code, headers, body, jumpurl, allbody

# 代理栗子
code, headers, body, jumpurl, allbody = mm.http('https://www.baidu.com', proxy="127.0.0.1:8080")
print code, headers, body, jumpurl, allbody

# raw请求栗子(解析头)
code, headers, body, jumpurl, allbody = mm.http('https://www.baidu.com', proxy="http://127.0.0.1:8080", raw='''
GET / HTTP/1.1
User-Agent: python/request

''')
print code, headers, body, jumpurl, allbody

# cookie栗子
code, headers, body, jumpurl, allbody = mm.http("http://www.baidu.com", headers={'User-Agent': '6666666666'},
                                                cookies={'a': 'b'}, raw='''GET /index.html HTTP/1.1
action: 123456''')
print code, headers, body, jumpurl, allbody

# raw请求栗子
code, headers, body, jumpurl, allbody = mm.httpraw('http://www.baidu.com', 'GET / HTTP/1.1\r\n\r\n')
print code, headers, body, jumpurl, allbody
