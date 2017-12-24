# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta


class ReportFactory(object):
    def __init__(self):
        pass

    def reportObj(self, path):
        if path is None:
            report = ReportList()
        else:
            report = ReportTxt(path)
        return report


class Report(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def output(self, result):
        pass


class ReportList(Report):
    def __init__(self, path=None):
        self.reportPath = path

    def output(self, result):
        # 打印+返回列表
        newresult = []
        output = []
        for resultList in result:
            for question in resultList:
                if question[1] != 0:
                    resultStr = "Output #%s: %s" %(question[0], question[1])
                    newresult.append(resultStr)
                    print resultStr
                else:
                    resultStr = "Output #%s: NO SUCH ROUTE" % question[0]
                    newresult.append(resultStr)
                    print resultStr
            output.append(newresult)
        return output

class ReportTxt(Report):
    def __init__(self, path):
        self.outputPath = path

    def output(self, result):
        # TODO 判断路径出报告
        pass
