# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class ComparaFactory(object):
    def __init__(self, value, type):
        self.value = int(value)
        self.type = type


    def choice(self):
        if self.type == 'maximum':
            return Maximum(self.value)
        elif self.type == 'exactly':
            return Exactly(self.value)
        elif self.type == 'lessThan':
            return LessThan(self.value)


class Functions(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def compara(self, value, count):
        pass


class Maximum(Functions):
    def __init__(self, maximum):
        super(Maximum, self).__init__()
        self.maximum = maximum
        pass

    def compara(self, value, count):
        if value <= self.maximum:
            count += 1
        return count


class Exactly(Functions):
    def __init__(self, exactly):
        super(Exactly, self).__init__()
        self.exactly = exactly
        pass

    def compara(self, value, count):
        if value == self.exactly:
            count += 1
        return count


class LessThan(Functions):
    def __init__(self, lessThan):
        super(LessThan, self).__init__()
        self.lessThan = lessThan
        pass

    def compara(self, value, count):
        if value < self.lessThan:
            count += 1
        return count
