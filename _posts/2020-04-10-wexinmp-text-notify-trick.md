---
layout: post
title: 微信公众号文字群发推送排版小技巧
date: 2020-4-10 09:44:12 +0800
categories: 运营
show_excerpt_image: true
---

> ⚠️ 2020 年 4 月更新，在最新的微信公众号运营公告《关于文字群发外链能力回收的通知》中，微信公众号不再支持通过 a 标签来群发文字格式的外站链接。建议通过关键字自动回复方式发送链接给读者。  

微信纯文字推送直接编辑或者粘贴后会存在换行错乱的问题，以往的方式为逐个换行，然后多次发送预览来确认排版无误。

![](/assets/img/posts/wexinmp-text-notify-trick/68FB5248-C8F6-4480-BB72-6A76454F27D3.png)

这里介绍一种保持格式的方式，不用二次排版。在编辑器中随便输入几个字母，选中后右键菜单检查元素。

![](/assets/img/posts/wexinmp-text-notify-trick/5B5F9738-CE04-42A3-8611-696A62F81D6D.png)

定位到对应的 DOM 节点后，双击编辑直接替换节点中的文字。尽管编辑器显示还是错误的，实际推送结果已经排版正常。（下图：编辑器排版与替换 DOM 内容推送对比）

![](/assets/img/posts/wexinmp-text-notify-trick/6B94B452-6C81-4E4F-91ED-2F96A4219915.png)
