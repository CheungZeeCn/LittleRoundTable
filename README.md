# 这是啥 What is this

小圆桌对练机器人的起名灵感来源于百万圆桌会议(MDRT)，是全球寿险精英的最高盛会，通过人机对练的方式辅助处理代理人熟悉销售话术。如果有合适的剧本配合，小圆桌可以从客户约访、面访、需求激发、产品推介、异议处理...等等场景去模拟客户，训练代理人的话术能力.

# 有啥特点 Highlights
 * DEMO级别，但结构清晰
 * 粗糙，且有潜力
 * 适当的搭配后，可以支持一定并发
 
# DM 设计和图示
 
# 接下来怎弄 Todo list
 可以做的东西还比较多
  * 提升用户交互体验:一个友好的UI
  * 提升对话语义模型:有现成的语料，请考虑sbert做句子嵌入，然后再调用分类模型来打分；如果没有监督语料，可以参考最近的bert-flow做句子嵌入；

# 咋样安装 Install
环境要求:
 * Linux/Mac
 * python3.7

clone 或者我们的源码，安装如下依赖:
 * sklearn
 * tornado
 * jieba
 * numpy


安装第三方服务依赖 [bert as service](https://github.com/hanxiao/bert-as-service/blob/master/README.md]):
```bash

pip install bert-serving-server  # server
pip install bert-serving-client  # client, independent of `bert-serving-server`

```

Done.


# 走起！Getting Started

先起 bert-as-service
``` bash
bert-serving-start -model_dir (你的中文bert地址)models/chinese_L-12_H-768_A-12/ -num_worker=1 # num_worker 看需要增加
```

再起咱们的服务
```bash
$python Server.py
2019-09-27 16:22:12,072 [INFO][kp_setup.py:52]: KP Setup Done, root_dir:[/Users/xxxx/opdir/PycharmProjects/LittleRoundTable]
2019-09-27 16:22:12,985 [INFO][Server.py:116]: exec: /Users/xxxx/anaconda3/bin/python /Users/xxxx/opdir/PycharmProjects/LittleRoundTable/src/WorkerServer.py --port=10811 --worker_name=woker_10811
2019-09-27 16:22:12,990 [INFO][Server.py:116]: exec: /Users/xxxx/anaconda3/bin/python /Users/xxxx/opdir/PycharmProjects/LittleRoundTable/src/WorkerServer.py --port=10812 --worker_name=woker_10812
2019-09-27 16:22:13,009 [INFO][Server.py:137]: master server: Listening port: 10810, worker num: 2
2019-09-27 16:22:13,394 [INFO][kp_setup.py:52]: KP Setup Done, root_dir:[/Users/xxxx/opdir/PycharmProjects/LittleRoundTable]
2019-09-27 16:22:13,398 [INFO][kp_setup.py:52]: KP Setup Done, root_dir:[/Users/xxxx/opdir/PycharmProjects/LittleRoundTable]
2019-09-27 16:22:14,652 [INFO][WorkerServer.py:231]: worker_name: woker_10811 Listening port: 10811
2019-09-27 16:22:14,662 [INFO][WorkerServer.py:231]: worker_name: woker_10812 Listening port: 10812
```

访问一下看看, 用postman发new请求:
```
method 选择 post
body 选择 raw 和 JSON(application/json)
body 内容：
{"openId": "zhangzhi", "difficultyLevel": 1, "scriptId": 1}
```
访问一下看看, 用postman发reply请求:
```
method 选择 post
body 选择 raw 和 JSON(application/json)
body 内容：
{"sessionId":"YOUR_SESSION_ID FROM the RESPONSE of new() REQUEST", "agentAnswer":"马先生，您好，我是平安寿险的保险顾问孙悟空。是这样的，上个月，您的同事赵xx和黄xx在我们公司购买了一款保险产品，据我了解，这款保险产品挺适合您这个职业的，请问您有没有这方面的需求呢？"}
```

# 请我吃饭 Contact Me
如果拿去商用，我也不能把你怎么样，不过请邮件告诉我，咱们多多交流。

email: paaizhangz@gmail.com

