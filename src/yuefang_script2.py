import copy
import pprint
import json
import kp_setup
import os
import logging


script_info_template = {
    # 剧本id
    "script_id": -1,
    # 剧本标题
    "title": "未命名",
    # 剧本副标题
    "sub_title": "",
    # 图片
    "image": "",
    # 描述
    "description": "待补充",
    # 目标人群, 初中高 通用
    "agent_group": "通用",
    # 目标人群类型, 保留
    "agent_type": "通用",
    # 目标客户群
    "customer_group": "通用",
    # 目标产品
    "product": "通用",
    # 场景
    "script_scene": "通用",
    # 策略, 默认html文本
    "strategy": "待补充",
    # 标签列表, 可以用来支持检索
    "tags": [],
    # 保留字段 json 格式长串
    "reserved": ""
}

segment_info_template = {
    # 环节标题
    "title": "未命名",
    "segment_id": -1,
    "description": ""
}

turn_block_template = {
    # 对话 block id / 意图
    "turn_block_id": -1,
    #  意图名称
    "title": "未命名意图",
    #  所属环节
    "segment_id": -1,
    #  权重, 同一个parent下的block之间按权重跳转
    "weight": 10,
    # 对话类型 default / objection / ?
    "type": "default",
    # 这一轮回答的建议，要求必填
    "tips": "",
    # intro; 引子 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
    # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
    # 异议的情况也是这样
    "intro": "",
    # 标准回答
    "standard_answer" : "",
    # 相似回答
    "similar_answer" : [],
    # 这一轮回答的不错的话，就会有这个机器回复
    "default_replies": [],
    # 加分关键字列表
    "bonus_keywords": [],
    # 减分关键字列表
    "minus_keywords": [],
    # 上层父亲节点
    "parent_ids": [],
    # 下层子节点
    "children_ids": []
}



"""
data here
"""


#约访
script_info_demo = {
    # id
    "script_id": 1,
    # 剧本标题
    "title": "约访客户是成功销售的第一步",
    # 剧本副标题
    "sub_title": "电话约访实训",
    # 图片
    "image": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1565946986864&di=aade53a5feb06ccfa7e2f17d43ced03b&imgtype=0&src=http%3A%2F%2Fimg.mp.sohu.com%2Fupload%2F20170526%2Fe94981e4486f4b78a5f4e745652f8a98_th.png",
    # 描述
    "description": ("""电话约访对于代理人，特别是初级代理人来说是非常重要的一步。本剧本从开场环节的方法论开始演练，过程中还模拟了常见的 "客户说"""
            """没有时间"、 "客户说不需要面谈"、 "客户信息难收集"等情况，希望能够帮助到广大代理人进行充分预演，祝大家旗开得胜！"""),
    # 目标人群, 初中高 通用
    "agent_group": "初级代理人",
    # 目标客户群
    "customer_group": "通用",
    # 目标产品
    "product": "通用",
    # 场景
    "script_scene": "电话约访",
    # 策略, 默认html文本
    "strategy": """
<div>    
<b>情景描述</b>
<p>
保险销售员在电话约访客户时，不知怎样说开场白，才能给客户留下良好的第一印象。
</p>
<b>错误应对</b>
<p>
1.“杜先生，您好，我是xx保险公司的刘××，不知您是否听说过我们公司？
(这种开场白既没有向客户说明打电话的目的，也没有解释自己的工作对客户有什么利益和好处，很难引起客户的兴趣)
</p>
<p>
2.“您好，杜先生，我是x×保险公司的刘××，请问您以前买过保险吗？”
(这种开场白一上来就对客户进行提问，很容易引起客户的戒备心理)
</p>
<p>
3.“您好，杜先生，我是××保险公司的刘××，前几天我给您发过一份财富保障方面的资料，不知道您看了没有？”
(这种开场白没有设身处地考虑客户的处境，客户如果很忙，即使收到资料也不见得有时间看，所以这种开场白很容易得到客户的否定回答)
</p>
<p>
4.“您好，杜先生，我是×保险公司的刘××，不知道您明天否有空？我想去拜访您一下。”
(这种开场白很容易遭到客户的拒绝，保险销售员要想成功约见客户最好别问客户是否有空，而应该直接向客户预约时间)
</p>

<b>情景解析</b>
<p>
开场白是保险销售员成功约访客户的关键，开场白就像一本书的书名，说得正确、得当，能迅速赢得客户的好感，并勾起客户的好奇心；反之，则会引起客户的反感，或者让客户觉得索然无味，失去继续听下去的欲望，甚至随时终止通话。因此在打电话之前，保险销售员一定要设计好自己的开场白。
那么，保险销售员该如何设计自己的开场白呢？
<p>
<b>请求帮忙法</b>
<p>
即通过向客户发出某种请求的方式开场，比如：“您好，我是××保险公司的x×，有件事想麻烦您一下！”一般情况下，这种向客户请求帮忙的方式，客户往往不好意思马上拒绝，保险销售员也就有机会与客户继续交谈了。
第三者介绍法
即以双方都认识的第三者的介绍作为开场，比如：“您好，我是×保险公司的××，是××的朋友，是他介绍我给您打电话的。我和x既是朋友关系，也是客户关系，一年前他在我这里购买了一款保险产品，年下来，他感觉我们公司的产品和服务都很不错，所以……”通过第三者的介绍，不仅能在很大程度上解除客户的戒备心理，而且更容易打开话题，与客户建立起信任关系。
</p>
<b>牛群效应法</b>
<p>
在草原上，牛群总是很有规律地往一个方向跑。将这种现象移植到人类的市场行为中，就是所谓的“牛群效应法”，即向客户提出其同行、朋友等已经采取了某种行动，从而引导客户也采取同样的行动。比如：“您好，我是××保险公司的xx,上个月，您的朋友x×在我们公司购买了xx保险，请问您有没有这方面的需求呢？”保险销售员在电话开场白中，向客户提起其朋友正在使用自己的保险产品，能在很大程度上刺激客户对保险的兴趣。
</p>
<b>巧借东风法</b>
<p>
诸葛亮在赤壁之战中，巧借东风一把火烧掉了曹操的几十万大军。在电话开场白中，保险销售员也可以巧妙地借用身边的“东风”，比如曾经留给客户的保险资料。这种借力往往有四两拨千斤的效果。
</p>
<b>话术示范</b>
<p>
范例1
保险销售员：“您好，温先生，我是××保险公司的保险顾问刘x,实在抱歉，打扰您了，我们公司正在做一个市场调研，能否请您帮个忙呢？”
(利用请求帮忙法开场)
客户：“我现在很忙，没时间啊。”
保险销售员：“没关系，那我1小时后再打给您吧，谢谢您的支持。”(1小时后再次打电话给客户)
保险销售员：“温先生，您好！我是小刘啊，刚才给您打过电话了，您叫我1小时后再打来
(营造一种与客户很熟悉的气氛，以拉近与客户的距离感)
</p>
<p>
范例2
保险销售员：“温先生，您好，我是××保险公司的保险顾问刘×，是您的朋友王ⅹX先生介绍我打电话给您的，王先生是我们公司的老客户，他认为我们的产品很符合您的需求，所以让我打电话跟您聊聊
(利用第三者介绍法开场)
客户：“哦？我怎么没听他说过呢？”
保险销售员：“是吗？那真不好意思，估计是王先生最近忙，还没来得及给您说吧。您看我真是心急，冒冒失失地就给您打电话了。
客户：“没关系。”
保险销售员：“温先生，我给您简单介绍一下我们的保险产品吧…
</p>(引入保险产品介绍)
<p>
范例3
保险销售员：“温先生，您好，我是××保险公司的保险顾问刘×。是这样的，上个月，您的同事赵X×和黄××在我们公司购买了一款保险产品，据我了解，这款保险产品挺适合您这个职业的，请问您有没有这方面的需求呢？”
(利用牛群效应法开场)
客户：“呵呵，是什么保险产品啊？”
(客户明显对保险产品产生了兴趣)
保险销售员：“是一款叫×x的产品，它……”
(引入保险产品介绍)
范例4
保险销售员：“温先生，您好，我是××保险公司的保险顾问刘×，是这样的，您上个月给我们公司打过咨询电话，我当时给您提供了一份资料。这次打电话给您，是想了解一下您对资料有哪些不明白的地方，我可以给您做个解释说明。
(利用巧借东风法开场)
客户：“有，里面有一条……是什么意思啊？
保险销售员：“哦，这条的意思是…”
</p>
</div>    
    """,
    # 标签列表, 可以用来支持检索
    "tags": ['电话', '电话约访', '开场']
}

def gen_new_script(data):
    global script_info_template
    script_info = copy.deepcopy(script_info_template)
    script_info.update(data)
    return script_info

def gen_new_segment(data):
    global segment_info_template
    segment_info = copy.deepcopy(segment_info_template)
    segment_info.update(data)
    return segment_info

def gen_new_block(data):
    global turn_block_template
    turn_block_info = copy.deepcopy(turn_block_template)
    turn_block_info.update(data)
    return turn_block_info

def manual_combine_segments():
    segments = []
    segment_info_demo0 = {
        "title": "开场",
        "segment_id": 0,
        "description": "电话约访客户，不知道怎样说开场白，才能给客户留下第一印象"
    }
    segments.append(gen_new_segment(segment_info_demo0))

    segment_info_demo1 = {
        "title": "约访",
        "segment_id": 1,
        "description": "如何跟客户明确见面时间地点"
    }
    segments.append(gen_new_segment(segment_info_demo1))
    return segments


def manual_combine_blocks():
    global turn_block_template
    blocks = []
    turn_block_demo_start = {
        # 对话 block id / 意图
        "turn_block_id": 0,
        #  意图名称
        "title": "开场",
        #  所属环节
        "segment_id": 0,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "start",
        # 这一轮回答的建议，要求必填
        "tips": "",
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "",
        # 标准回答
        "standard_answer" : "",
        # 相似回答
        "similar_answer" : [],
        # 这一轮回答的不错的话，就会有这个机器回复
        "default_replies": ["(假设您的客户叫马里奥，您叫孙悟空)喂，谁呀?", "(假设您的客户叫马里奥，您叫孙悟空)您好，请问是?", "(假设您的客户叫马里奥，您叫孙悟空)喂？"],
        # 加分关键字列表
        "bonus_keywords": [],
        # 减分关键字列表
        "minus_keywords": [],
        # 上层父亲节点
        "parent_ids": [],
        # 下层子节点
        "children_ids": [1, 2, 3]
    }

    blocks.append(gen_new_block(turn_block_demo_start))

    # 1 2 3  对应3种方法和分支, 节点关系要清晰
    turn_block_demo_1 = {
        # 对话 block id / 意图
        "turn_block_id": 1,
        #  意图名称
        "title": "\"请求帮忙法\"开场",
        #  所属环节
        "segment_id": 0,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "default",
        # 这一轮回答的建议，要求必填
        "tips": "利用\"请求帮忙法\"开场",
        #  所属环节
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "",
        # 标准回答
        "standard_answer" : "您好，马先生，我是平安寿险的保险顾问孙悟空, 实在抱歉，打扰您了，我们公司正在做一个市场调研，能否请您帮个忙呢？",
        # 相似回答
        "similar_answer" : ["您好，马先生，我是平安寿险的保险顾问孙悟空, 实在抱歉，打扰您了，我们公司正在做一个星级用户调研，能否请您帮帮忙？", ],
        # 这一轮回答的不错的话，就会有这个机器回复
        "default_replies": ["哦，好呀", "可以", "请说"],
        # 加分关键字列表
        "bonus_keywords": ["帮忙", "帮", "帮帮忙"],
        # 减分关键字列表
        "minus_keywords": ["平安"],
        # 上层父亲节点
        "parent_ids": [0],
        # 下层子节点
        "children_ids": [4, 5]
    }
    blocks.append(gen_new_block(turn_block_demo_1))

    turn_block_demo_2 = {
        # 对话 block id / 意图
        "turn_block_id": 2,
        #  意图名称
        "title": "\"第三者介绍法\"开场",
        #  所属环节
        "segment_id": 0,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "default",
        # 这一轮回答的建议，要求必填
        "tips": "利用\"第三者介绍法\"开场 (第三者叫王先生)",
        #  所属环节
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "",
        # 标准回答
        "standard_answer" : "马先生，您好，我是平安寿险的保险顾问孙悟空，是您的朋友王ⅹx先生介绍我打电话给您的，王先生是我们公司的老客户，他认为我们的产品很符合您的需求，所以让我打电话跟您聊聊",
        # 相似回答
        "similar_answer" : ["马先生，您好，我是平安寿险的保险顾问孙悟空，是您的朋友王ⅹx先生介绍我打电话给您的，王先生是我们公司的老客户，他觉得我们有一款产品非常适合您，所以让我来跟您聊聊"],
        # 这一轮回答的不错的话，就会有这个机器回复
        "default_replies": ["哦，好呀", "请说"],
        # 加分关键字列表
        "bonus_keywords": ["介绍", "客户", "朋友", "适合", "需求"],
        # 减分关键字列表
        "minus_keywords": ["平安"],
        # 上层父亲节点
        "parent_ids": [0],
        # 下层子节点
        "children_ids": [7, 8]
    }
    blocks.append(gen_new_block(turn_block_demo_2))

    turn_block_demo_3 = {
        # 对话 block id / 意图
        "turn_block_id": 3,
        #  意图名称
        "title": "\"牛群效应法\"开场",
        #  所属环节
        "segment_id": 0,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "default",
        # 这一轮回答的建议，要求必填
        "tips": "利用\"牛群效应法\"开场",
        #  所属环节
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "",
        # 标准回答
        "standard_answer" : "马先生，您好，我是平安寿险的保险顾问孙悟空。是这样的，上个月，您的同事赵xx和黄xx在我们公司购买了一款保险产品，据我了解，这款保险产品挺适合您这个职业的，请问您有没有这方面的需求呢？",
        # 相似回答
        "similar_answer" : ["马先生，您好，我是平安寿险的保险顾问孙悟空。是这样的，上个月，您的朋友赵xx和黄xx在我们公司购买了一款保险产品，据我了解，这款产品在您的这个职业圈内很受欢迎，想来了解下您有没有这方面的需求。"],
        # 这一轮回答的不错的话，就会有这个机器回复
        "default_replies": ["哦，好呀", "可以", "请说"],
        # 加分关键字列表
        "bonus_keywords": ["客户", "朋友", "适合", "需求", "受欢迎", "职业", "圈"],
        # 减分关键字列表
        "minus_keywords": ["平安"],
        # 上层父亲节点
        "parent_ids": [0],
        # 下层子节点
        "children_ids": [8]
    }
    blocks.append(gen_new_block(turn_block_demo_3))

    # 请求帮忙法的后续, 产品调研 省略版
    turn_block_demo_4 = {
        # 对话 block id / 意图
        "turn_block_id": 4,
        #  意图名称
        "title": "产品调研(省略)",
        #  所属环节
        "segment_id": 0,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "default",
        # 这一轮回答的建议，要求必填
        "tips": '请回复 "此处省略调研过程" 模拟此环节',
        #  所属环节
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "好吧，那你说吧",
        # 标准回答
        "standard_answer" : "此处省略调研过程",
        # 相似回答
        "similar_answer" : [],
        # 这一轮回答的不错的话，就会有这个机器回复
        "default_replies": ["你们有什么产品可以介绍给我吗？", "您看哪些产品适合我?"],
        # 加分关键字列表
        "bonus_keywords": [],
        # 减分关键字列表
        "minus_keywords": [],
        # 上层父亲节点
        "parent_ids": [1],
        # 下层子节点
        "children_ids": [9]
    }
    blocks.append(gen_new_block(turn_block_demo_4))

    # 请求帮忙法的异议
    turn_block_demo_5 = {
        # 对话 block id / 意图
        "turn_block_id": 5,
        #  意图名称
        "title": "客户异议\"我没有时间\"",
        #  所属环节
        "segment_id": 0,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "objection",
        # 这一轮回答的建议，要求必填
        "tips": "约今天稍后时间(1小时候后)",
        #  所属环节
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "我没有时间哦",
        # 标准回答
        "standard_answer" : "不好意思，打扰到您，我今天稍后时间给你打电话可以吗？请问1小时后可以吗？大概就占用您5分钟左右。",
        # 相似回答
        "similar_answer" : ["不好意思，打扰到您, 请问1小时后方便打电话给您吗？大概就占用您5分钟时间。"],
        # 这一轮回答的不错的话，就会有这个机器回复
        "default_replies": ["可以，1小时以后再给我打电话吧。", "好的，1小时后给我打电话。", "哎呀，好吧，1小时候再打给我吧。"],
        # 加分关键字列表
        "bonus_keywords": ["打扰", "方便", "稍后", "1", "小时", "5分钟"],
        # 减分关键字列表
        "minus_keywords": ["1小时"],
        # 上层父亲节点
        "parent_ids": [1],
        # 下层子节点
        "children_ids": [6]
    }
    blocks.append(gen_new_block(turn_block_demo_5))

    # 请求帮忙法的异议后续
    turn_block_demo_6 = {
        # 对话 block id / 意图
        "turn_block_id": 6,
        #  意图名称
        "title": "客户异议\"我没有时间\"后续1",
        #  所属环节
        "segment_id": 0,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "objection",
        # 这一轮回答的建议，要求必填
        "tips": "1小时过去了，您拨通了客户电话。记得营造熟悉气氛，拉近距离",
        #  所属环节
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "",
        # 标准回答
        "standard_answer" : "马先生，您好！我是平安的小孙啊，刚才给您打过电话了，您叫我1小时后再打来。",
        # 相似回答
        "similar_answer" : ["马先生，您好！我是平安的小孙啊，刚才您叫我1小时后再打来，请问现在方便吗?"],
        # 这一轮回答的不错的话，就会有这个机器回复
        "default_replies": ["哦， 说吧", "哦，刚刚那位啊，好的，说吧"],
        # 加分关键字列表
        "bonus_keywords": ["刚刚", "刚才"],
        # 减分关键字列表
        "minus_keywords": [],
        # 上层父亲节点
        "parent_ids": [5],
        # 下层子节点
        "children_ids": [1]
    }
    blocks.append(gen_new_block(turn_block_demo_6))


    # 第三者介绍法的异议
    turn_block_demo_7 = {
        # 对话 block id / 意图
        "turn_block_id": 7,
        #  意图名称
        "title": "客户异议\"第三者没有提及\"",
        #  所属环节
        "segment_id": 0,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "objection",
        # 这一轮回答的建议，要求必填
        "tips": "赶紧道歉，说自己心急、冒失。",
        #  所属环节
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "咿？老王没有和我提过啊？",
        # 标准回答
        "standard_answer" : "是吗？那真不好意思，估计是王先生最近忙，还没来得及给您说吧。您看我真是心急，冒冒失失地就给您打电话了",
        # 相似回答
        "similar_answer" : [],
        # 这一轮回答的不错的话，就会有这个机器回复, 这块有优先级, intro 优先级最高、然后到异议的结尾、然后异议处理前的block的默认?
        "default_replies": [],
        # 加分关键字列表
        "bonus_keywords": ["不好意思", "抱歉", "心急", "冒失"],
        # 减分关键字列表
        "minus_keywords": [],
        # 上层父亲节点
        "parent_ids": [2],
        # 下层子节点
        "children_ids": [2]
    }
    blocks.append(gen_new_block(turn_block_demo_7))

    # 请求帮忙法的后续, 产品调研 省略版
    turn_block_demo_8 = {
        # 对话 block id / 意图
        "turn_block_id": 8,
        #  意图名称
        "title": "产品介绍环节(省略)",
        #  所属环节
        "segment_id": 0,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "default",
        # 这一轮回答的建议，要求必填
        "tips": '请回复 "此处省略产品介绍环节" 模拟此环节',
        #  所属环节
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "",
        # 标准回答
        "standard_answer" : "此处省略产品介绍环节",
        # 相似回答
        "similar_answer" : [],
        # 这一轮回答的不错的话，就会有这个机器回复
        "default_replies": ["不错，我有点兴趣。", "嗯，这产品不错。"],
        # 加分关键字列表
        "bonus_keywords": [],
        # 减分关键字列表
        "minus_keywords": [],
        # 上层父亲节点
        "parent_ids": [2, 3],
        # 下层子节点
        "children_ids": [9]
    }
    blocks.append(gen_new_block(turn_block_demo_8))

    # 带上资料为由，约上时间
    turn_block_demo_9 = {
        # 对话 block id / 意图
        "turn_block_id": 9,
        #  意图名称
        "title": "资料为由，限定时间，二选一法约见面",
        #  所属环节
        "segment_id": 1,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "default",
        # 这一轮回答的建议，要求必填
        "tips": '以带资料为由约见面，限定时间(15分钟)，二选一法约见面(明后天)',
        #  所属环节
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "",
        # 标准回答
        "standard_answer" : "更详细的内容我这边要带上资料才能给您更好的讲解哦，您看这样合适不，我们约明天或者后天见个面，整个过程不会超过15分钟。",
        # 相似回答
        "similar_answer" : [],
        # 这一轮回答的不错的话，就会有这个机器回复
        "default_replies": ["明天下午5点我家这边的星巴克吧, 购物公园这边这个, 如何？"],
        # 加分关键字列表
        "bonus_keywords": ["资料", "材料", "讲解", "明天", "后天", "明后天", "15分钟"],
        # 减分关键字列表
        "minus_keywords": [],
        # 上层父亲节点
        "parent_ids": [4, 8],
        # 下层子节点
        "children_ids": [10]
    }
    blocks.append(gen_new_block(turn_block_demo_9))

    # 带上资料为由，约上时间
    turn_block_demo_end = {
        # 对话 block id / 意图
        "turn_block_id": 10,
        #  意图名称
        "title": "结束",
        #  所属环节
        "segment_id": 1,
        #  权重, 同一个parent下的block之间按权重跳转
        "weight": 10,
        # 对话类型 default / objection / start / end
        "type": "end",
        # 这一轮回答的建议，要求必填
        "tips": '恭喜您！约访成功！',
        #  所属环节
        # intro, 引子; 如果上一轮block有多个分支,  且这个block被随机选中, 如果intro有内容，
        # 上一轮block的回答default_replies就不会被使用，优先使用这个intro的内容
        # 异议的情况也是这样
        "intro": "",
        # 标准回答
        "standard_answer" : "",
        # 相似回答
        "similar_answer" : [],
        # 这一轮回答的不错的话，就会有这个机器回复
        "default_replies": [],
        # 加分关键字列表
        "bonus_keywords": [],
        # 减分关键字列表
        "minus_keywords": [],
        # 上层父亲节点
        "parent_ids": [9],
        # 下层子节点
        "children_ids": []
    }
    blocks.append(gen_new_block(turn_block_demo_end))
    return blocks


def build_script_from_raw_code():
    script_info = gen_new_script(script_info_demo)
    segments = manual_combine_segments()
    blocks = manual_combine_blocks()
    script = {
        "info": script_info,
        "data": {
            "segments": segments,
            "turn_blocks": blocks
        }
    }
    return script

def print_script_tree(script):
    """
        1. 先深遍历这棵树, 打出树的结构
        2. 打出对话套路
            那么有那么几个点要注意:
                分支嵌套深度
                因为有环存在，所以要记录之前访问过的路
                实现回复的优先级?
                    1. 如果有intro 优先用下一个intro的回复来做输出.
                    2. 其次如果在异议环节，使用异议上描述的回答.
                    3. 最后，使用当前block的默认回复.
    :param script:
    :return:
    """
    visited_paths = []
    visited_ids = []
    visited_depths = []

    stack = []
    depth = 1

    stack.append((script['data']['turn_blocks'][0], depth))

    while len(stack) != 0:
        block, depth = stack.pop()
        visited_paths.append(block)
        visited_ids.append(block['turn_block_id'])
        visited_depths.append(depth)

        depth += 1

        for c_id in reversed(block['children_ids']):
            if c_id in visited_ids:
                continue
            else:
                stack.append((script['data']['turn_blocks'][c_id], depth))

    print("先深遍历: ")
    for block in visited_paths:
        print_block(script['data']['segments'], block)
    print("遍历剧本，模拟对话内容:")



def print_block(segments, block):
    segment = segments[block['segment_id']]
    print("===== {}:{}:{}:{} =====".format(segment['segment_id'], segment['title'], block['turn_block_id'], block['title']))
    print("tips: {}".format(block['tips']))
    print("intro: {}".format(block['intro']))
    print("type: {}".format(block['type']))
    print("standard_answer: {}".format(block['standard_answer']))
    print("default_replies: {}".format(block['default_replies']))
    print("bonus_keywords: {}".format(block['bonus_keywords']))
    print("minus_keywords: {}".format(block['minus_keywords']))
    print("parent_ids: {}".format(block['parent_ids']))
    print("children_ids: {}".format(block['children_ids']))
    print("=============================")




if __name__ == '__main__':
    pass
    #script_info.update(script_info_demo)
    #pprint.pprint(script_info['strategy'])
    #print(script_info['strategy'])
    #segment_info = copy.deepcopy(segment_info_template)
    #segment_info.update(segment_info_demo)
    #print(segment_info)
    script = build_script_from_raw_code()
    #pprint.pprint(script)
    print(json.dumps({script['info']['script_id']: script}))
    #print_script_tree(script)
    output_file_path = os.path.join(kp_setup.data_dir, "scripts.repo.new.json")
    with open(output_file_path, 'w') as f:
        f.write(json.dumps({script['info']['script_id']: script}))
        logging.info("dump scripts to json file [{}]".format(output_file_path))





