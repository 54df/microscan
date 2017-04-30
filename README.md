# MicroScan

现在的我很菜，在写一个仿Bugscan的项目，这里是我起步的第一步，另外，写的whatweb这个东西估计是不成了，都融合在这里了，分离出去就脱裤子放屁了，没什么意义

另外，发现bug请反馈给我，QQ:1197795981	  邮箱:minisafe@foxmail.com	    非常感谢

		守护者2017.4.29


该项目想尽量于2017年末前上线，域名microscan.top，主机还木有，web还木有写。



不知道该怎么写文档，就写在这吧。

打开方式分两种

import MicroCore

mm = MicroCore.Microhttp()
print mm.http('http://www.baidu.com')
print mm.httpraw('http://www.baidu.com','GET / HTTP/1.1\r\n\r\n')

就这两种,http和httpraw

返回值和hackhttp很相似，也是5个，分为
	
	code(int)	返回代码，成功是200这种
	headers(dic)	headers是以字典形式返回的，例{'Cookie':'JSESSIONID=1111111111111111111'}
	body(str)	body为返回正文,例<html>......</html>
	jumpurl(str)	如果返回代码300<=code<=305是会跳转的，该返回值为判断code，然后读headers里面的location
	allbody(str)	allbody是我自己拼接的，尽量像直接返回的socket




下面说说http和httpraw的区别

	httpraw有三个参数(url, raw, timeout=3),和hackhttp一样，raw里面可以直接复制burpsuite抓到的包，和hackhttp不同的地方就是，MicroCore直接用的socket发送数据，比httplib还要底层，这样对用户发送的包也有比较严格的限制，比如content-length，用户要自己手动计算字节数

	http有六个参数(url, post=None, raw=None, headers={}, method=None, cookies={},method=None(通过post或raw判断，默认为GET))，raw参数同样可以发送包，和hackhttp的区别在于，这个raw不是通过调用httpraw的方法实现的，而是自己处理的，会解析请求行，请求头，等等的字段，然后通过httplib来请求





上面说到底层库，其实不用urllib和urllib2是有原因的，因为这些库在返回错误代码的时候直接就抛异常了，不能看到返回的数据

MicroCore没有使用线程池，因为我比较菜，没有深刻理解线程池，等我搞明白了一定会加上





下面给几个栗子，方便大家理解我的辣鸡框架，也欢迎大家提出宝贵的意见或建议


	mm = MicroCore.Microhttp()
	code,headers,body,jumpurl,allbody=mm.http('http://www.baidu.com')
	请求数据:
	GET / HTTP/1.1
	Connection: Keep-Alive
	Accept-Encoding: gzip, deflate
	User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36
	
	数据结束




	code,headers,body,jumpurl,allbody=mm.http("http://www.baidu.com",headers={'User-Agent': '6666666666'},cookies={'a':'b'},raw='''GET /index.html HTTP/1.1
	action: 123456''')
	请求数据:
	GET /index.html HTTP/1.1
	action: 123456
	Connection: Keep-Alive
	Cookie: a=b
	Accept-Encoding: gzip, deflate
	User-Agent: 6666666666
	
	数据结束
	注：该方法优先使用raw的数据，比如headers里面写了User-Agent，raw里面也写了该请求头，优先使用raw里面的，我也不知道哪个是对的，只是跟着感觉走，大概是这样比较合理，如果post里面写了数据，会被raw里面的数据覆盖
	另外请注意此方法请求的报文，被raw改了！！！




	code,headers,body,jumpurl,allbody=mm.httpraw('http://www.baidu.com','GET / HTTP/1.1\r\n\r\n')
	请求数据
	GET / HTTP/1.1
	
	
	请求结束
	是的，这个方法就这么干脆




=======

