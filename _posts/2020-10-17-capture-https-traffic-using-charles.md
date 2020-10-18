---
layout: post
title: macOS 使用 Charles 抓取 HTTPS 请求
date: 2020-10-17 22:41:46 +0800
categories: 工具
show_excerpt_image: true
---

![](/assets/img/posts/capture-https-traffic-using-charles/Header.jpg)

在用爬虫抓取公众号文章阅读量时遇到了解析 HTTPS 请求的问题。原理上各种工具都利用中间人攻击（Man-in-the-Middle Attack）的方式获取解密后的请求内容，实现这一步的基础就是中间人的证书被系统认可。

抓包工具有许多，推荐使用 Charles，同时有非常多的同类如 Surge、Wireshark、Fiddler 等等可以选择。

## TL;DR
* 安装 Charles 根证书
* **信任 Charles 根证书**
* 将指定站点加入 Charles SSL 代理清单

## 安装根证书
打开 Charles，点击顶栏的 Help 可以看到 SSL Proxying 选项，点击安装 Charles 根证书。

![](/assets/img/posts/capture-https-traffic-using-charles/1.png)

## 信任根证书
由于 macOS 的安全机制，添加了证书默认为不可信任的状态，这会导致无法正常访问内容。 

![](/assets/img/posts/capture-https-traffic-using-charles/877802E9-58D2-40C2-AA21-A500314967D1.png)

我们需要在钥匙串访问（Keychain）里找到 Charles 的证书，将信任部分改为“始终信任”，这个改动需要管理员权限。

![](/assets/img/posts/capture-https-traffic-using-charles/2.jpg)

## 将要抓取的域名加入 SSL 代理清单
尽管已经信任证书，Charles 默认不会使用 SSL 代理，需要用户指定域名。可以在代理中找到 SSL 的设置选项，列表里增加`域名:端口`，也可以直接在请求列表指定域名右键，然后 Enable SSL Proxying。

![](/assets/img/posts/capture-https-traffic-using-charles/3.jpg)

## 总结
整个环节并不复杂，不同工具的配置方式也大同小异，关键在于 **macOS 不会直接信任用户添加的证书，需要手动信任根证书**。附上 Charles 官方对不同平台的配置根证书的操作步骤，软件对 Windows、macOS、Android、iOS 等主流的平台都有支持。

[SSL Certificates](https://www.charlesproxy.com/documentation/using-charles/ssl-certificates/)：https://www.charlesproxy.com/documentation/using-charles/ssl-certificates/

![](/assets/img/posts/capture-https-traffic-using-charles/4.jpg)



