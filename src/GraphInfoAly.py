# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import os
import re


class GraphFactory(object):
    def __init__(self, graphInfo):
        self.graphInfo = graphInfo

    def analysisGraphPath(self):
        # if isinstance(list, self.graphInfo):
        #     graphAly = GraphListAly()
        # elif
        if os.path.isfile(self.graphInfo):
            graphAly = GraphPathAly(self.graphInfo)
        elif isinstance(self.graphInfo, str):
            graphAly = GraphStrAly(self.graphInfo)
        else:
            graphAly = None
        return graphAly


class GraphAnalysis(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.graphInfo = None
        pass

    @abstractmethod
    def alyGraphInput(self):
        pass

    @staticmethod
    def getRouteList(line):
        # return [(graphName, routes)]
        # 解析输入的地图语句
        graphs = []
        for graph in line.split(';'):
            if graph.strip() == '':
                continue
            try:
                name, routes = graph.split(':')
            except:
                routes = graph
                name = None
            graphs.append((name, routes))
        return graphs


class GraphStrAly(GraphAnalysis):
    def __init__(self, graphInfo):
        self.graphInfo = graphInfo
        self.graphList = []

    def alyGraphInput(self):
        # 解析地图
        # for graph in self.graphInfo.split(';'):
        #     name, routes = graph.split(':')
        #     self.graphList.append((name, routes))
        # return self.graphList
        return self.getRouteList(self.graphInfo)

class GraphListAly(GraphAnalysis):
    def __init__(self, graphInfo):
        self.graphInfo = graphInfo
        self.graphList = []

    def alyGraphInput(self):
        return self.graphList


class GraphPathAly(GraphAnalysis):
    def __init__(self, graphInfo):
        self.graphInfo = graphInfo
        self.graphList = []

    def alyGraphInput(self):
        with open(self.graphInfo) as f:
            for line in f:
                # 解析地图
                self.graphList.extend(self.getRouteList(line))

        return self.graphList
