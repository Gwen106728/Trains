# -*- coding: utf-8 -*-

import sys
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class RuleInfomation():
    def __init__(self):
        self.ruleDict = {}
        pass

    def analysisRule(self):
        path = sys.path[0]
        if os.path.isdir(path):
            xmlPath = os.path.join(path, '..', 'config', 'config.xml')
            tree = ET.parse(xmlPath)
            root = tree.getroot()
            for question in root.findall('question'):
                classname = self.getChildText(question, 'classname')[0]
                parameter = self.getChildText(question, 'parameter')[0]
                value, type = self.getChildText(question, 'value')
                no = question.get('no')  # 子节点下属性name的值
                self.ruleDict.setdefault(classname, {}).setdefault(no, []).extend([parameter, value, type])

    @staticmethod
    def getChildText(root, name):
        try:
            text = root.find(name).text
            tag = root.find(name).get('type')
        except:
            text = None
            tag = None
        return text, tag


if __name__ == '__main__':
    RuleInfomation().analysisRule()
