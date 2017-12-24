# -*- coding: utf-8 -*-
import re


class RouteInfo(object):
    def __init__(self):
        self.name = None
        self.routes = None
        self.graphDict = {}
        pass

    def getRouteDict(self, graphList):
        # 解析地图信息
        self.name, self.routes = graphList
        for route in self.routes.split(','):
            try:
                star, end, distance = re.findall(r'\w', route)
            except:
                continue
            self.graphDict.setdefault(star, {}).setdefault(end, None)
            self.graphDict[star][end] = distance
