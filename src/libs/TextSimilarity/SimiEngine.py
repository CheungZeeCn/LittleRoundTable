#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   SimiEngine.py    
@Contact :   zhangz

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
22/8/19 下午4:07   zhangz     1.0         None
'''

import ngram
import jieba
from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SimiEngine(object):

    def __init__(self, bert_on=True):
        self.bc = BertClient()

    def top_k_similarity(self, input_text, candidates, k=1):
        #print(list(zip(range(len(candidates)), candidates)))
        ngram_index = ngram.NGram(zip(range(len(candidates)), candidates), n=2, key=lambda x:x[1])
        ret = ngram_index.search(input_text)
        ret_list = [(v[0], score) for v, score in ret[:k]]
        if len(ret_list) == 0:
            ret_list = [(0, 0)]
        return ret_list

    # todo 使用线程库变异步
    def top1_similarity_bert(self, input_text, candidates):
        vectors = self.bc.encode([input_text] + candidates)
        simis = cosine_similarity([vectors[0, :]], vectors[1:, :])
        return np.argmax(simis), np.max(simis)

    @staticmethod
    def jaccard_above(input_text, candidates, above=0.5):
        def jaccard(a, b):
            a_set = set(list(jieba.cut(a)))
            b_set = set(list(jieba.cut(b)))
            return len(a_set.intersection(b_set))/max(len(a_set.union(b_set)), 1)
        jaccards = [jaccard(input_text, c) for c in candidates]
        ret_list = []
        for i in range(len(jaccards)):
            if jaccards[i] >= above:
                ret_list.append((jaccards[i], i))
        return ret_list


if __name__ == '__main__':
    simi = SimiEngine()
    print(simi.top_k_similarity("您好啊", ["您好", "好呀", "您好呀"]))
