# -*- coding: utf-8 -*-
import threading
from report import ReportFactory
from routeInfoAly import RouteInfo
from ruleConfig import RuleInfomation
from check import Check
import Queue


class TrainsEngine(object):
    def __init__(self, graphInfo, reportPath):
        self.graphAly = graphInfo.analysisGraphPath()
        self.outputObj = ReportFactory().reportObj(reportPath)
        self.ruleInfo = self.ruleAly()

        self.myqueue = Queue.Queue(maxsize=10)

        self.last = 0
        self.start = 0
        # 解析类型
        self.result = []
        self.output = []

    def ruleAly(self):
        ruleInfo = RuleInfomation()
        ruleInfo.analysisRule()
        return ruleInfo

    def execution(self):
        t1 = threading.Thread(target=self.graph)
        t2 = threading.Thread(target=self.trainsRoute)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # TODO 输出处理
        self.output = self.outputObj.output(self.result)

    def graph(self):
        # 处理graph 入参
        graphList = self.graphAly.alyGraphInput()

        while 1:
            if graphList == []:
                self.last = 1
                self.start = 1
                break
            if self.myqueue.full() is False:
                routeInfo = self.getGrah(graphList.pop())
                self.myqueue.put(routeInfo)
                self.start = 1

    def trainsRoute(self):
        # 处理一个地图具体业务
        while 1:
            if self.start == 0:
                continue
            if self.myqueue.empty() is False:
                routeInfo = self.myqueue.get()
                # resultList 一组答案
                resultList = self.check(routeInfo)
                self.result.append(resultList)
            if self.myqueue.empty() and self.last:
                break


    def getGrah(self, routeList):
        # 解析线路
        routeInfo = RouteInfo()
        routeInfo.getRouteDict(routeList)

        return routeInfo

    def check(self, routeInfo):
        task = Check()
        # task.initi()
        resultList = task.checkRule(routeInfo, self.ruleInfo.ruleDict)
        return resultList