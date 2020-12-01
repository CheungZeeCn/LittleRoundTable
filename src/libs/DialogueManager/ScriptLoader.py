#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
剧本
"""
import json
import logging


class ScriptLoader(dict):
    @staticmethod
    def load_data_from_json_file(file_loc):
        ret_scripts = {}
        try:
            data = open(file_loc).read().strip()
            scripts = json.loads(data)
            for k, v in scripts.items():
                k = int(k)
                turn_blocks = v['data']['turn_blocks']
                for this_turn_block in turn_blocks:
                    cids = this_turn_block['children_ids']
                    objection_cids = [cid for cid in cids if turn_blocks[cid]['type'] == 'objection']
                    main_cids = [cid for cid in cids if turn_blocks[cid]['type'] != 'objection']
                    this_turn_block['objection_children_ids'] = objection_cids
                    this_turn_block['main_children_ids'] = main_cids
                ret_scripts[int(k)] = v
        except Exception as e:
            logging.error("load data error: {}".format(e))
        return ret_scripts
