# -*- coding: utf-8 -*-
from GraphInfoAly import GraphFactory
from engine import TrainsEngine
import sys
sys.path.append("..")

class TrainsStarts():
    @staticmethod
    def bootStart(graph, reportPath=None):
        """
        :param graph: 地图，字符串形式，可为txt文件或直接的地图，地图可一次输入多张
        :param reportPath:
        :return: output [[Output #1: 9,Output #2: 5,...],...], 结果为列表套列表
        """
        graphInfo = GraphFactory(graph)
        trains = TrainsEngine(graphInfo, reportPath)
        trains.execution()

        return trains.output

if __name__ == '__main__':
    graph = "AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7;" \

    # graph = "/usr/test.txt"
    output = TrainsStarts.bootStart(graph)
    print output