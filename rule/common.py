# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from compara import ComparaFactory
import copy

class Rule(object):
    __metaclass__ = ABCMeta
    commonDistance = {}

    def __init__(self, routeInfo):
        self.output = None
        self.routeInfo = routeInfo
        self.stopCount = 1
        self.value = None
        self.type = None
        self.maxlenght = None
        self.stopagain = []

    @abstractmethod
    def result(self, ruleDict):
        pass

    @staticmethod
    def stopsItem(ruleParameter):
        parameter, value, type = ruleParameter
        path = [x.upper() for x in parameter.split('-')]
        return path, value, type

    def getDistance(self, path):
        """
        :param path:["A", "E",...]
        :return:distance
        """
        graphDict = self.routeInfo.graphDict
        distance = 0
        for stop in path:
            graphDict = graphDict.get(stop, None)
            if isinstance(graphDict, dict):
                continue
            elif isinstance(graphDict, str):
                distance += int(graphDict)
                graphDict = self.routeInfo.graphDict
                graphDict = graphDict.get(stop)
            else:
                distance = 0
                break
        return distance

    def cycleCheck(self, allDistanceList):
        distanceList = allDistanceList[0]
        newdistanceList = distanceList[:]
        for path in distanceList:
            if self.value and int(self.value) > len(path) - 2:
                end, star = path[-2], path[-2]
                distanceList = self.getAllDistance([star, end])
                pathList = self.combinePath(path, distanceList)
                newdistanceList.extend(pathList)
            if self.maxlenght and int(self.maxlenght) > path[-1]:
                end, star = path[-2], path[-2]
                distanceList = self.getAllDistance([star, end])
                pathList = self.combinePath(path, distanceList)
                newdistanceList.extend(pathList)
        allDistanceList[0] = newdistanceList


    def combinePath(self, path, distanceList):
        if self.value:
            sub = int(self.value) - len(path) + 2
        elif self.maxlenght:
            sub = int(self.maxlenght) - path[-1]
        pathList = []
        for newPath in distanceList:
            while self.value and sub >= len(newPath) - 2:
                newPath = self.findnew(newPath, path)
                pathList.append(newPath)
            while self.maxlenght and sub >= newPath[-1]:
                newPath = self.findnew(newPath, path)
                pathList.append(newPath)
        return pathList

    def findnew(self, newPath, path):
        item = newPath[1:-1]
        olditem = path[:-1]
        oldlen = path[-1]
        olditem.extend(item)
        newlen = oldlen + newPath[-1]
        olditem.append(newlen)

        return olditem

    def getCommonDistance(self, path):
        if len(path) == 2:
            pathList = [path]
        elif len(path) > 2:
            pathList = [[path[i], path[i + 1]] for i in range(len(path))]
        else:
            pathList = []

        alldistanceList = []
        for pathItem in pathList:
            # if Rule.commonDistance.get(tuple(pathItem), None):
            #     distanceList = Rule.commonDistance.get(tuple(pathItem), None)
            # else:
            distanceList = self.getAllDistance(pathItem)

            # Rule.commonDistance.setdefault(tuple(pathItem), []).extend(distanceList)
            alldistanceList.append(distanceList)
        return alldistanceList

    def getAllDistance(self, path):
        """
        :param path:["A","B"]
        :return: distanceList
        """
        star, end = path
        graphDict = self.routeInfo.graphDict

        starValue = graphDict.get(star, None)

        distanceList = []
        if starValue:
            endValue = starValue.get(end, None)
            if endValue is None and ((self.value and self.stopCount <= self.value) or self.maxlenght):
                distanceList = self.childStar(starValue, end, star)
            elif endValue is None and self.value is None and self.maxlenght is None:

                distanceList = self.childStar(starValue, end, star)
            elif isinstance(endValue, str):
                distanceList = [[star, end, int(endValue)]]
                if self.value or self.maxlenght:
                    newstarValue = copy.deepcopy(starValue)
                    newstarValue.pop(end)
                    distanceList.extend(self.childStar(newstarValue, end, star))
            elif self.value and self.stopCount > self.value:
                distanceList = []

        return distanceList

    def childStar(self, starValue, end, star):
        distanceList = []
        self.stopCount += 1
        for stop in starValue:
            if self.value is None and self.maxlenght is None and stop in self.stopagain:
                continue
            elif self.value is None and self.maxlenght is None:
                self.stopagain.append(stop)
            dst = self.getAllDistance([stop, end])
            for item in dst:
                item[-1] += int(starValue[stop])
                if self.maxlenght and item[-1] <= int(self.maxlenght):
                    distanceList.append(item)

                elif self.maxlenght is None:
                    distanceList.append(item)
        for item in distanceList:
            item.insert(0, star)
        return distanceList

    def getShortestStops(self, allDistanceList):
        count = 0
        if len(allDistanceList) > 1:
            pass
        else:
            distanceList = allDistanceList[0]
            comparas = ComparaFactory(self.value, self.type).choice()
            for path in distanceList:
                value = len(path) - 2
                count = comparas.compara(value, count)
        return count

    def getShortest(self, allDistanceList):
        shortest = 0
        if len(allDistanceList) > 1:
            pass
        else:
            distanceList = allDistanceList[0]
            try:
                shortest = sorted(distanceList, key=lambda x: x[-1])[0][-1]
            except:
                pass
        return shortest

    def getLength(self, allDistanceList):
        count = 0
        if len(allDistanceList) > 1:
            pass
        else:
            distanceList = allDistanceList[0]
            comparas = ComparaFactory(self.maxlenght, self.type).choice()
            for path in distanceList:
                value = path[-1]
                count = comparas.compara(value, count)
        return count


class Distance(Rule):
    def __init__(self, routeInfo):
        super(Distance, self).__init__(routeInfo)

    def result(self, ruleDict):
        """
        :param ruleDict:{no:[parameter, maximum, exactly]}
        :return:
        """
        result = []
        for no, ruleParameter in ruleDict.items():
            path = self.stopsItem(ruleParameter)[0]
            distance = self.getDistance(path)
            result.append((int(no), distance))
        return result


class Stops(Rule):
    def __init__(self, routeInfo):
        super(Stops, self).__init__(routeInfo)
        self.stopCount = 1

    def result(self, ruleDict):
        result = []
        for no, ruleParameter in ruleDict.items():
            path, self.value, self.type = self.stopsItem(ruleParameter)
            allDistanceList = self.getCommonDistance(path)
            self.cycleCheck(allDistanceList)
            number = self.getShortestStops(allDistanceList)
            result.append((int(no), number))
        return result


class Shortest(Rule):
    def __init__(self, routeInfo):
        super(Shortest, self).__init__(routeInfo)

    def result(self, ruleDict):
        result = []
        for no, ruleParameter in ruleDict.items():
            path = self.stopsItem(ruleParameter)[0]
            allDistanceList = self.getCommonDistance(path)
            number = self.getShortest(allDistanceList)
            result.append((int(no), number))
        return result


class Length(Rule):
    def __init__(self, routeInfo):
        super(Length, self).__init__(routeInfo)

    def result(self, ruleDict):
        result = []
        for no, ruleParameter in ruleDict.items():
            path, self.maxlenght, self.type = self.stopsItem(ruleParameter)
            allDistanceList = self.getCommonDistance(path)
            self.cycleCheck(allDistanceList)
            count = self.getLength(allDistanceList)
            result.append((int(no), count))
        return result
