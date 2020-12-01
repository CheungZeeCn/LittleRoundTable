#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
剧本
            todo:
                在合适的地方做hook, 做安全检查, 针对new 和 reply 两个调用
                在合适的地方加入的剧本文本的预处理
                关键节点的日志

"""
import sys
import random
from confs import conf

from .ScriptLoader import ScriptLoader
from libs import utils
from libs.TextSimilarity import SimiEngine
import logging


class DialogueContext(dict):
    """
        上下文对象，当前包含了session data
    """
    global_session_id_counter = 1
    MAX_COUNTER = 100000000

    @classmethod
    def gen_session_id(cls):
        session_id = cls.global_session_id_counter
        cls.global_session_id_counter += 1
        if cls.global_session_id_counter > cls.MAX_COUNTER:
            logging.info("global_session_id_counter increase to {}, reset".format(cls.MAX_COUNTER))
        return session_id

    def __init__(self, context=None):
        self['session_id'] = "{}_{:010d}".format(utils.now_date_str(), self.gen_session_id())
        self['script_id'] = 0
        self['difficulty'] = 0
        self['user_id'] = 0

        # 上下文信息
        self['user_id'] = 0
        self['now_turn_block_id'] = 0
        self['next_turn_block_id'] = 0
        self['now_segment_id'] = 0
        self['next_segment_id'] = 0
        self['last_turn_block_id'] = -1
        self['last_main_turn_block_id'] = -1
        # 对话详细记录 demo 状态比较需要
        self['history'] = []
        # 对话详细记录 id path
        self['history_turn_block_id_path'] = []
        if context is not None:
            self.update(context)


class DialogueManager(object):
    def __init__(self):
        self.scripts = {}
        self.simi_engine = SimiEngine()

    def load_scripts(self, script_ids=None, data_format='json', uri=''):
        """
            将指定id的剧本加载到内存中, 字典结构;
        :param script_ids: 列表行，如果None, 加载所有剧本;
        :param data_format: json, json文件;
        :param uri: 资源路径

        :return:
        """
        if data_format == 'json':
            all_scripts = ScriptLoader.load_data_from_json_file(uri)
            if script_ids is not None:
                for sid in script_ids:
                    self.scripts[sid] = all_scripts[sid]
            else:
                self.scripts = all_scripts

    @staticmethod
    def random_choose(values):
        """
            如果是单串，直接返回，如果是列表，随机选取一个字符串返回。
        :param values:
        :return:
        """
        if isinstance(values, str):
            return values
        elif len(values) == 1:
            return values[0]
        else:
            return random.choice(values)

    def weight_choose_path(self, this_turn_block_id, last_main_turn_block_id, turn_blocks, difficulty):
        """
            根据当前block 的信息，
            结合difficulty决定的异议概率,
            选择下一个block
                如果本身不在异议中，难度选择和是否有异议分支可以选，决定是否跳异议
                如果本身在异议中(这里依赖了假设: 从哪里进异议，就从哪里回去)
                    如果有异议分支，直接在异议分支中选择
                    如果没有异议分支，走主流程
            ** 注意 ** 当前不支持 weight 字段
        :param this_turn_block:
        :param last_main_turn_block: 用于判断异议是否该跳出了
        :param turn_blocks:
        :param difficulty:
        :return:
        """
        this_turn_block = turn_blocks[this_turn_block_id]
        this_type = this_turn_block['type']
        cids = this_turn_block['children_ids']
        # next_turn_block_id = None
        objection_cids = this_turn_block['objection_children_ids']
        main_cids = this_turn_block['main_children_ids']
        should_choose_objection = False

        if this_type != 'objection':  # 不在异议流程, 且有异议可选， 且随机数符合难度要求, 才会出异议 #
            if len(objection_cids) != 0 and difficulty > 0:  # 如果异议难度被打开，且有异议可以选 #
                if random.random() < difficulty:  # 选中要出异议
                    # 挑一个异议
                    should_choose_objection = True
            # 没有进入异议流程
            if should_choose_objection is True:
                next_turn_block_id = random.choice(objection_cids)
            else:
                next_turn_block_id = random.choice(main_cids)
        else: # 在异议流程中
            if last_main_turn_block_id in cids:
                #如果可以出去回到主流程了, 递归选择下一个主流程
                next_turn_block_id = self.weight_choose_path(last_main_turn_block_id, last_main_turn_block_id, turn_blocks, 0)
            else:
                next_turn_block_id = random.choice(cids)
        return next_turn_block_id

    def new(self, script_id, user_id, difficulty, session_id=None):
        """
            新建一个对话
                1. 创建会话上下文
                2. 创建对应的session
                3. 加载剧本内容,进行返回

            如果有错误，会设置 status 为 error， 然后写reply的 error_msg 字段
        :param script_id:
        :param user_id:
        :param session_id:
        :return:
        """
        if session_id is not None:
            param_context = {'script_id': script_id, 'user_id': user_id, 'session_id': session_id, 'difficulty': difficulty}
        else:
            param_context = {'script_id': script_id, 'user_id': user_id, 'difficulty': difficulty}

        if script_id not in self.scripts:
            return None, {'error_msg': 'script not exist'}, 'error'

        context = DialogueContext(param_context)

        now_turn_block_id = 0
        context['now_turn_block_id'] = now_turn_block_id
        context['now_segment_id'] = 0

        context, reply, next_status = self.do_reply(context)
        return context, reply, next_status

    @staticmethod
    def move_context_to(context, hit_turn_block_id, turn_blocks):
        old_turn_block_id = context['now_turn_block_id']
        context['now_turn_block_id'] = hit_turn_block_id
        context['now_segment_id'] = turn_blocks[hit_turn_block_id]['segment_id']
        context['last_turn_block_id'] = old_turn_block_id
        if turn_blocks[old_turn_block_id]['type'] == 'default':
            context['last_main_turn_block_id'] = old_turn_block_id

        context['history'].append(turn_blocks[old_turn_block_id])
        context['history_turn_block_id_path'].append(old_turn_block_id)
        return context

    def do_reply(self, context, user_answer=None, jump_flag=False):
        """
            根据用户的回答，生成后续内容, 兼容开始状态
        :param context:
        :param user_answer:
        :param jump_flag: 是否允许按相似度跳节点
        :return: reply:[session, context, answer, reply]
        """
        script_id = context['script_id']
        script = self.scripts[script_id]
        turn_blocks = script['data']['turn_blocks']
        if jump_flag is True:
            raise NotImplementedError
        else:  # 不允许跳转
            # 分析用户回答和潜在回答的相似度
            # 确定命中的程度
            #     1. 命中当前
            #     2. 命中邻居(非异议情况才允许)
            #     3. 不命中
            # 确认回复什么东西:
            #     1. 选路
            #     2. 根据优先级选择回复内容
            #     3. 回复tips

            reply = {
                "feedback": {},
                "tips": '',
                "reply": '',
                "next_turn_block_id": '',
                "now_turn_block_id": ''
            }

            # 验证回答
            hit_code = -1
            if user_answer is not None:
                candidate_turn_block_ids = self.collect_candidate_turn_block_ids(script, context)
                target_turn_block_id = context['next_turn_block_id']
                hit_code, hit_score, hit_turn_block_id, kw_details = \
                    self.score(user_answer, target_turn_block_id, candidate_turn_block_ids, script)

                if hit_code == 2: #命中
                    feedback = {'evaluation': '答的不错', 'score': hit_score, 'kw_details': kw_details}
                elif hit_code == 1: #命中
                    feedback = {'evaluation': '换了个方法嘛，也行', 'score': hit_score, 'kw_details': kw_details}
                elif hit_code == 0: #
                    feedback = {'evaluation': '回答错误, 请重新回答', 'score': hit_score, 'kw_details': kw_details}
                reply['feedback'] = feedback

                # move now_turn_block to hit_turn_block_id
                if hit_code != 0:
                    # 看情况 update context 中的
                    # now_turn_block_id, last_turn_block_id, last_main_turn_block_id,
                    # history, history_turn_block_id_path
                    context = self.move_context_to(context, hit_turn_block_id, turn_blocks)
                else:
                    context = self.move_context_to(context, context['now_turn_block_id'], turn_blocks)

            now_turn_block_id = context['now_turn_block_id']
            now_turn_block = turn_blocks[now_turn_block_id]
            last_main_turn_block_id = context['last_main_turn_block_id']
            difficulty = context['difficulty']

            if hit_code != 0: # 回答正确才会进行选路
                # 选路
                next_turn_block_id = self.weight_choose_path(now_turn_block_id,
                                                             last_main_turn_block_id, turn_blocks, difficulty)
                context['next_turn_block_id'] = next_turn_block_id
                context['next_segment_id'] = turn_blocks[next_turn_block_id]['segment_id']
            else:
                next_turn_block_id = context['next_turn_block_id']

            # 生成tips
            reply['tips'] = turn_blocks[next_turn_block_id]['tips']

            # 选择回复
            reply['reply'] = self.gen_reply_in_order(now_turn_block, turn_blocks[next_turn_block_id],
                                                     turn_blocks[last_main_turn_block_id])
            next_status = turn_blocks[next_turn_block_id]['type']

            return context, reply, next_status

    @staticmethod
    def collect_turn_block_answers(turn_block):
        ret = [turn_block['standard_answer']] + turn_block['similar_answer']
        return ret

    def score(self, user_answer, target_turn_block_id, candidate_turn_block_ids, script):
        """
            衡量用户回答的情况, 针对不能随便跳的情况
                1. 找到最相似的那个
                2. 确定是回答到了兄弟环节，hit_code=1 还是正确答案 hit_code=2
                3. 还是说根本就是答错了哦. hit_code=0

        :param user_answer:
        :param target_turn_block_id:
        :param candidate_turn_block_ids:
        :param script:
        :return: hit_code,命中情况  hit_score,命中分数, hit_turn_block_id, 命中的block_id
        """
        # pick values
        turn_blocks = script['data']['turn_blocks']
        candidate_answers = []
        candidate_answer_ids = []
        for tbid in candidate_turn_block_ids:
            answers = self.collect_turn_block_answers(turn_blocks[tbid])
            for answer in answers:
                candidate_answers.append(answer)
                candidate_answer_ids.append(tbid)
        # calc simi and argsmax it
        hit_score, hit_turn_block_id = self._score(user_answer, candidate_answers, candidate_answer_ids)

        if hit_score < 60: # 回答不中
            return 0, hit_score, hit_turn_block_id, {}

        # post score rules
        score_diff, score_details= self.post_kw_rules(user_answer, turn_blocks[hit_turn_block_id])
        score_details['ori_score'] = hit_score

        hit_score += score_diff
        hit_score = round(min(100, hit_score), 0)

        if hit_turn_block_id != target_turn_block_id: # 兄弟节点
            return 1, hit_score, hit_turn_block_id, score_details
        else: # 命中
            ""
            return 2, hit_score, hit_turn_block_id, score_details

    @staticmethod
    def post_kw_rules(user_answer, turn_block, unit=5, max_diff=20):
        score_diff = 0
        bonus_keywords = []
        minus_keywords = []

        for kw in turn_block['bonus_keywords']:
            if kw in user_answer:
                score_diff += unit
                bonus_keywords.append(kw)

        for kw in turn_block['minus_keywords']:
            if kw not in user_answer:
                score_diff -= unit
                minus_keywords.append(kw)

        if score_diff > max_diff:
            score_diff = max_diff
        elif score_diff < -1 * max_diff:
            score_diff = -1 * max_diff

        return score_diff, {'bonus_keywords': bonus_keywords, 'minus_keywords': minus_keywords}

    def _score(self, user_answer, candidate_answers, candidate_answer_ids):
        """
            去相似度最高的那个为答案, 然后计分
        :param user_answer:
        :param values:
        :param ids:
        :return:
        """
        #filter step
        ret_list = self.simi_engine.jaccard_above(user_answer, candidate_answers, conf.filter_jaccard_above)
        candidate_answers = [candidate_answers[ret[1]] for ret in ret_list]
        candidate_answer_ids = [candidate_answer_ids[ret[1]] for ret in ret_list]
        logging.info("filter after, ids:{}".format(candidate_answers))

        if len(candidate_answers) == 0:
            return 0, 0
        #simi step
        similar_score, similar_id = self._similar_score(user_answer, candidate_answers, candidate_answer_ids)

        #hardcode here todo: find a good way/strategy
        if similar_score < conf.SIMI_ABOVE:
            return 0, 0

        similar_score *= 100
        similar_score = max(60, similar_score)

        score = min(100, similar_score)

        return score, similar_id

    def _similar_score(self, user_answer, candidate_answers, candidate_answer_ids):
        top_one_index, similar_score = self.simi_engine.top1_similarity_bert(user_answer, candidate_answers)
        #top_one_index, similar_score = self.simi_engine.async_top1_similarity_bert(user_answer, candidate_answers)
        return similar_score, candidate_answer_ids[top_one_index]

    def collect_candidate_turn_block_ids(self, script, context, jump_flag=False):
        """
            生成当前block的候选可跳block， 目前默认不允许乱跳.
        :param script:
        :param context:
        :param jump_flag:
        :return:
        """
        target_turn_block_id = context['next_turn_block_id']
        target_turn_block = script['data']['turn_blocks'][target_turn_block_id]
        now_turn_block_id = context['now_turn_block_id']
        now_turn_block = script['data']['turn_blocks'][now_turn_block_id]
        candidate_turn_block_ids = set([target_turn_block_id])

        if jump_flag is not False:
            raise NotImplementedError
        else:
            # 如果在异议流程中，只能跳异议的兄弟节点
            if target_turn_block['type'] == 'objection':
                candidate_turn_block_ids = candidate_turn_block_ids.union(now_turn_block['objection_children_ids'])
            else:
                # 如果在正常流程中，只能跳正常流程的兄弟节点
                candidate_turn_block_ids = candidate_turn_block_ids.union(now_turn_block['main_children_ids'])
        return list(candidate_turn_block_ids)

    @classmethod
    def gen_reply_in_order(cls, this_turn_block, next_turn_block, last_main_turn_block):
        """
            不允许跳转， 返回回复
            1. 整理出当前的候选可行回答列表
            2. 寻找相似度, 看是否命中
            3. 如果可行回答列表内有命中，对话推进
                3.1. 回答命中的是 这一轮应该回答的内容, 反馈是 配置里面的高分配置, 对话推进到这个block中
                3.2. 回答命中的是这一轮的兄弟节点内容， 也还行, 反馈是 配置里面的 同节点提醒, 对话推进到对应的兄弟节点中
                3.3. 回复的内容需要按一定的优先级来选择
                    3.3.1 下一个的intro
                    3.3.2 当前block的默认回复
                    3.3.3 如果是异议跳主流程，选用最上一个主流程的默认回复
            4. 如果可行回答列表中没有命中，回复 "什么？|嗯？" 反馈是 配合里面的 请再说一遍 ;

        :return:
        """
        if next_turn_block['intro'] != '':
            return cls.random_choose(next_turn_block['intro'])
        elif len(this_turn_block['default_replies']) != 0:
            return cls.random_choose(this_turn_block['default_replies'])
        else:
            return cls.random_choose(last_main_turn_block['default_replies'])
