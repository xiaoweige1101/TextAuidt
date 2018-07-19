#!/usr/bin/env python
# encoding:utf-8


"""
敏感词处理
从文件中读取敏感词,添加不同类别的敏感词,保存到txt或者DB中

>>>s = SensitiveWords()
>>>s.get_sensitive_word('./data/SensitiveWords/ad.txt') # 读取文件中的敏感词
>>>s.add_sensitive_word(u'default')                     # 添加敏感词 unicode
>>>s.add_sensitive_word('minitrill', word_type='ad')    # 添加敏感词并指定敏感词类型
>>>s.save_data()                                        # 保存敏感词数据
>>>s.sensitive_word_dict                                # 核心数据被保存在字典中

author    :   @h-j-13
time      :   2018-7-19
"""


class SensitiveWords(object):
    # Singleton
    _instance = None

    def __new__(cls, *args, **kw):
        """单例模式"""
        if not cls._instance:
            cls._instance = super(SensitiveWords, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.file_path_list = ['./data/SensitiveWords/ad.txt',
                               './data/SensitiveWords/dirty.txt',
                               './data/SensitiveWords/gun.txt',
                               './data/SensitiveWords/politics.txt',
                               './data/SensitiveWords/pron.txt',
                               './data/SensitiveWords/default.txt']
        self.sensitive_word_dict = {}
        for file in self.file_path_list:
            self.get_sensitive_word(file)

    def get_sensitive_word(self, path):
        """从文件中读取敏感词"""
        with open(path, 'rb') as f:
            sensitive_word_type = str(path).split('/')[-1].replace('.txt', '')
            self.sensitive_word_dict[sensitive_word_type] = set()
            for line in f:
                if line.strip():
                    self.sensitive_word_dict[sensitive_word_type].add(line.strip().decode('utf-8'))

    def add_sensitive_word(self, word, word_type='default'):
        """添加敏感词"""
        if type(word) == str:
            word = word.decode('utf-8')
        if word_type in self.sensitive_word_dict.keys() or word_type == 'default':
            self.sensitive_word_dict[word_type].add(word)

    def save_data(self):
        """存储数据到文件中"""
        for word_type in self.sensitive_word_dict.keys():
            file_path = filter(lambda x: word_type in x, self.file_path_list)[0]
            with open(file_path, 'wb') as f:
                for word in self.sensitive_word_dict[word_type]:
                    f.write(word.encode("utf-8"))
                    f.write("\n")