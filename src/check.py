# -*- coding: utf-8 -*-
from importlib import  import_module
import sys

class Check(object):
    def __init__(self):
        pass

    def initialization(self):
        pass

    def checkRule(self, routeInfo, ruleInfo):
        resultList = []
        for key, value in ruleInfo.items():
            f = __import__('rule.common', fromlist=True)
            train = getattr(f, key)
            print sys.path
            result = train(routeInfo).result(value)
            resultList.extend(result)
        resultList.sort(key=lambda x: x[0])
        return resultList

