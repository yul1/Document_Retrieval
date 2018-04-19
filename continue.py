        self.rStore = {}
        termCountRE = re.compile('(\w+):(\d+)')#w指的是提取所有道德字母，d是提取所有的数字
        f = open(retrieveFile,'r')
        for line in f:
            qid = int(line.split(' ',1)[0])#以空格来进行分割，分割一次
            self.rStore[qid] = {}#qid是第几行
            for (term,count) in termCountRE.findall(line):
                self.rStore[qid][term] = int(count)