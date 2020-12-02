 ![image](https://github.com/CheungZeeCn/LittleRoundTable/blob/main/images/UI.png?raw=true)

# 小圆桌是什么？ What is this
针对保险话术培训场景设计的陪练机器人的demo

小圆桌对练机器人的起名灵感来源于百万圆桌会议(MDRT)，是全球寿险精英的最高盛会，通过人机对练的方式辅助处理代理人熟悉销售话术。如果有合适的剧本配合，小圆桌可以从客户约访、面访、需求激发、产品推介、异议处理...等等场景去模拟客户，训练代理人的话术能力.

# 当前代码有什么特点 Highlights
 * DEMO级别，但结构清晰
 * 粗糙，且有潜力
 * 适当的搭配后，可以支持一定并发
 
# 创新点在哪里 What's new
相对对常见的一问一答背诵式的机器人设计，在拟人上做了如下思考：
 * 单句打分：培训是有目的的，从微观上看，最终用户是要流利的说出某些话术（文本）的，所以这里需要有单句级别的评分，也是对对话的内容的一种约束要求； 
 * 多分支寻路： *好的销售核心能力不是回答，而是提问*，所以要时刻锻炼用户的主动说能力。更具像来说，在真实的销售环节，用户为了达到一个目标，是可以有多种对话路径。如果用图结构来表达对话，每个节点是一个意图点，那么就是一个父节点有多个子节点，只要最终对话可以推进到某个结果节点，就是完成了最终目标。这就要求DM有比较强的灵活性。另外，每一种意图的表达有多种说法（标准说法与相似说法），这对于对话内容，是一种对自由的要求；
 * 异议弹出: 真实销售环节中，对话往往不会顺风顺水。譬如你刚要推销某样产品的时候，客户可能会说“停，你不用说了，那xxx我知道，太贵了，坑人。” 这其实就是异议弹出环节，我们针对这种情况也需要进行仿真，从而培养我们用户在真实场景下的随机应变能力。
 * 灵活的对话管理模式支持(放出来的版本在全局计分部分应该还么有支持，需要用户开发)：
    * 针对学习场景，用户是有可能出现记不住下一个话术应该说的是什么的情况，这时候可以允许答案的候选节点是当前环节中的任意一个意图，这样最终计分只需要考虑命中节点的路径、顺序和每个节点的得分即可；
    * 针对进阶一点的学习场景，可以限制答案的候选节点的子节点中，这就不允许用户忘记节点话术或者打乱顺序了，可以针对话术稍微熟练一点的时候，也可以满足相对宽松的通关要求；
    * 针对通关场景，可以严格要求用户按照提示回答随机到的指定子节点，这是最严格的一种限制，相当于在图中随机生成了一个路径，用户要严格按照路径去推进。
  
# 核心设计  Core abstractions
 * 剧本数据模型：
   * 结构层次: 剧本->环节->意图->答案
   * 剧本由环节串联组合而成，环节单入口，单出口(可给予后续基于环节为颗粒来进行剧本辅助生成的基础能力);
   * 环节内意图多分支，分主流程和异议流程
   * 一个意图有标准答案和相似说法
    ![image](https://github.com/CheungZeeCn/LittleRoundTable/blob/main/images/juben.png?raw=true)
  
 * DM核心策略:

   ![image](https://github.com/CheungZeeCn/LittleRoundTable/blob/main/images/dm1.png?raw=true)
  
   ![image](https://github.com/CheungZeeCn/LittleRoundTable/blob/main/images/dm2.png?raw=true)

 
# 距离真实可用差哪些东西 Todo list
 可以做的东西还比较多
  * 提升用户交互体验:一个友好的UI；
  * 提升对话语义模型:有现成的语料，请考虑sbert做句子嵌入，然后再调用分类模型来打分；如果没有监督语料，可以参考最近的bert-flow做句子嵌入；
  * 适当的训练语料语料增强，以及剧本意图节点的语料增强；
  * 自定义的贴合你的业务场景的打分方式，单句打分可以考虑如语言流畅度、关键字、语速等因素；对练打分可以参考命中节点顺序，各个节点打分等；

# 咋样安装 Install
环境要求 base os/env:
 * Linux/Mac
 * python3.7/3.6

clone 我们的源码，安装如下依赖  requirements:
 * sklearn
 * tornado
 * jieba
 * numpy
 * bert as service 
 * ... 


安装第三方服务依赖 [bert as service](https://github.com/hanxiao/bert-as-service/blob/master/README.md]):
```bash

pip install bert-serving-server  # server
pip install bert-serving-client  # client, independent of `bert-serving-server`

```

Done.


# 走起！Getting Started

launch bert-as-service
``` bash
bert-serving-start -model_dir (你的中文bert地址 model dir)models/chinese_L-12_H-768_A-12/ -num_worker=1 # num_worker 
```

launch server
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
{"sessionId":"YOUR_SESSION_ID FROM the RESPONSE of new() REQUEST", "agentAnswer":"马先生，您好，我是xxx保险的保险顾问孙悟空。是这样的，上个月，您的同事赵xx和黄xx在我们公司购买了一款保险产品，据我了解，这款保险产品挺适合您这个职业的，请问您有没有这方面的需求呢？"}
```

# 请我吃饭 Contact Me
可以免费拿去商用，不过请邮件告诉我一下，希望有机会可多多交流
 ![image](https://github.com/CheungZeeCn/LittleRoundTable/blob/main/images/shoukuan.png?raw=true)
email: cheungzeecn@gmail.com

