Work In Process
==

导航请移步到: http://python-cn.github.io

**star的人们啊, 被star不是目的, 要来贡献代码哦(●'◡'●)ﾉ♥**

说明
--

这里只包含等待开发的Todo List. 会尽量更新到最新状态.

有兴趣参与者请使用: [trello](https://trello.com/b/JM2OEXPA/firefly)去获取最新的任务列表. 防止任务已被认领造成重复.

沟通请使用: [pythoncn-slack](https://pythoncn.slack.com)(需要邀请, 请发邮件到ciici123@gmail.com, 或者联系组内其他成员),
参与开发者才会被通过(slack没有灌水区)，请谨慎加入

## 学习准备

假如你觉得你还没有能力做下面的todo list, 可以先准备以下一些知识, 将来会用到

- react
- oauth2
- select2
- flask-wtf
- flask-restful
- flask ext

英语好的不妨看这个视频教程[http://discoverflask.com](https://github.com/realpython/discover-flask)

PS: 其他的firefly的依赖的列表在这里: http://python-cn.github.io/#/post/used.md

## 集思广益

社区不是我一个人的观点, 需要大家作为一个潜在受众一起思考: 你希望有什么功能. 然后来建新的card, 去完成你认为有价值的任务.

## Todo List

以下是一些定义:

1. 主题 = model里面的Post, 就是一篇文章
2. 评论 = model里面的Comment, 对一篇文章的评论
3. 首页 = 首页显示了文章的列表, 默认按活跃时间排序
4. 单个主题 = 类似/post/post_id/这样的链接. 包含文章正文, 对应评论等

- [x] 主题的分类model, 早期可以是先插入的一些固定数据,比如devops, web开发, 爬虫..(选项不重要, 要有后台的支持) - [halfcrazy]
- [ ] 主题的分类model的接口. 前端可以通过ajax调用这个url 获得全部的分类信息: 分类id, 分类名, 分类描述 - [halfcrazy]
- [ ] 创建主题时候可以通过select2选择分类, 效果类似meta.discourse.org创建主题的分类下拉框效果(可以只是功能, 没有css样式) - [mozillazg]
- [ ] 创建请求中会带上分类的参数, 后端save的时候会生成含有分类的主题(Post)
- [ ] 首页渲染时, 能获得某主题对应的分类.
- [ ] 用户创建新主题后会使用[Effeckt.css](https://github.com/h5bp/Effeckt.css), 闪到主题列表的最上面
- [ ] 设计阅读量的实现, 就是刷新一下页面, 阅读量就会+1 - [mozillazg]
- [ ] 让每个主题页面(http://web:port/post/post_id/)里面显示出评论的内容. - [dongweiming]
- [ ] 首页注册和登陆页面的浏览器兼容性(chrome下正常, FF下不正常)
- [x] 注册页面当用户名/密码/邮箱都有正确输入的时候让`注册`按钮变成enable - [dongweiming]
- [ ] 设计用户个人页面, 只需要包含对应的view, 个人基本信息: 注册源(微博/github/google), 昵称, 头像(使用Gravatar)等，加入时间, 用户id
- [ ] 设计用户设置密码页面, 对应的view, 简陋的模板
- [x] 设计用户密码找回方案 - [halfcrazy]
- [ ] 用户可以设置自己介绍, 坐标(比如北京), 以及个人的站点
- [ ] 用户可以设置github/stackoverflow的地址
- [x] 用户model, oauth2方案 - [dongweiming]
- [x] 使用sweetalert替代alert - [dongweiming]
- [ ] 对主题和评论可以like和取消like. 没有unlike
- [ ] 主题和平台太多的分页设计
- [ ] follow用户的功能
- [ ] 站内信模型
- [ ] 提醒模型(类似豆瓣的提醒)
- [ ] @ 能弹出被@用户
- [ ] @ 的消息能被该用户收到提醒
- [ ] 使用站内信和其他人私聊
- [ ] 首页每个类型都能排序, 比如按分类, 按最热
- [ ] 设计公告位
- [ ] 每当用户发表新的评论, 应该把该主题提到最前(最近活跃)
- [ ] 完成单个主题页面, 样式, 展示评论, 能在评论下发表新评论
- [ ] 能评论其他人的评论
- [ ] 站内信未读 给标志标示
- [ ] 主题内容在首页就可以预览, 可以选择`阅读更多`点到单个主题页
- [ ] 发布主题可以上传图片(也可粘贴一个图片url)
- [ ] 单个主题可以看到上传的图片
- [ ] 发布主题可以插入视频url
- [ ] 单个主题可以看到视频
- [ ] 个人发表的主题页
- [ ] 徽章系统, 但是不能种类多, 我想目前只包含开发者
- [ ] 设计一个好看的logo
- [ ] 微博oauth2登录
- [ ] QQoauth2登录
- [ ] 豆瓣oauth2登录 - [halfcrazy]
- [ ] 本站注册登录
- [ ] 设计管理员系统(可能是一个子url, 也可能是一个其他的项目),就是可以开发者的权限, 有对应权限的开发者可以删帖, 修改标题等. 但是一切操作都要被系统记录(flask-admin好丑)
- [ ] 设计站内检索，全文本检索方案
- [ ] 社区事件系统, 无论做什么操作, 都是一个事件, 能够容易的单个人获得操作记录, 单种类型的操作记录, 比如可以列出来创建主题的时间列表
- [ ] 用户个人页面能看到用户的操作记录(默认按时间排序), 比如回复什么主题, 创建了什么主题. follow了xx
- [ ] 把现有的代码都补上事件
- [ ] 和github一样. 有页面的键盘快捷键, 给这种类型的geek最好的体验 - [dongweiming]
- [ ] 全局的log系统, 用于debug. 产生应用的log等. 有点tornado的效果. 可配置的 类似fabric
- [ ] 给项目的log加上颜色. 但是不要直接使用第三方库
- [ ] 鼠标移到用户名字上, 会弹出用户的一个信息框. 获得用户的一些基本信息.
- [ ] 社区的缓存系统. 比如用户的会话缓存, 文章内容的缓存(在文章更新的时候有对应的更新操作)
- [ ] 社区的消息push, 我目前想的是一个websocket. 通过js获得数据后渲染(有相关工作经验的最好)
- [ ] 社区的issue系统. 主要和我们的slack关联, 可以给我提交bug, 意见和建议
- [ ] 有意见建议, 就需要一个和提交者的通道. 借用提醒,站内信等让用户得到最新的反馈
- [ ] 主题可微博分享
- [ ] 主题可豆瓣分享
- [ ] 个人页面可以拉取用户的对应网站的数据. 比如github的源列表, star数, following数.
- [ ] 拉取用户对应网站数据的设计, 可以使用celery, rq等.
- [ ] 用户可以选择隐藏那些属性不被人看到
- [ ] timeline设计. 用户可以选择timeline模式. 和twitter效果类似.
- [ ] 实验室开关. 我们应该设计一个lab模式. 激进的用户或者开发者可以选中, 尝鲜最新的特性功能.
- [ ] 用户可以删除自己发布的主题. 主题默认指向失效用户, 其中的内容和评论不变. 但和用户无关了(这个模式大家讨论)
- [ ] 用户可以删除自己发布的评论. 评论会被去掉. 这个评论被其他人评论得数据还在. 只是源评论会显示`已失效`(这个模式大家讨论)
- [ ] 数据库备份. 用户所有的删除后的数据都有副本. 方便用户导出和恢复.


贡献者列表可以看这里: [CONTRIBUTORS.txt](https://github.com/python-cn/firefly/blob/master/CONTRIBUTORS.txt)

[dongweiming]: https://github.com/dongweiming
[halfcrazy]: https://github.com/halfcrazy
[mozillazg]: https://github.com/mozillazg
