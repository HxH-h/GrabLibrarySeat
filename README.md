### 起因
<font size="3">每次一到快考试的时候，图书馆人数暴增，预约不到自己想坐的位置
</font>
### 使用

* 依赖包: selenium包和requests包
* Edge官网下载Edge的无头浏览器，下载后解压，将exe文件放入到项目根目录下
* 在constant.py中的U和P变量填写自己的用户名和密码
* 运行request.py
### 原理
* 使用selenium通过Edge无头浏览器登录，获取cookie
* 使用requests包 向预约座位的对应接口发起请求，实现预约
* 注：本来是想只使用requests包，但是登录界面是由校园门户统一登录，登录后有多次重定向过程，在重定向时，通过响应头设置Cookie。使用requests每次都被导向错误页面，无法正确获取Cookie。无奈只能使用无头浏览器的方式
