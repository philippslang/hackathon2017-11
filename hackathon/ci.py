class TestResult:
    STATUS = ['passed', 'failed']

    def __init__(self):
        self.name = ''
        self.cost = 0
        self.istatus = self.STATUS.index('passed')
    
    def status(self):
        return self.STATUS[self.istatus]


class Result:

    def __init__(self):
        self.tests = []
        self.score = []

    def __repr__(self):
        return 'res'


class CI:

    def __init__(self, tests):
        self.tests = tests
        self.build()

    def build(self):
        self.i = 0
        self.N = 2

    def result(self):
        return Result()

    def __iter__(self):
        while self.i < self.N:
            yield self.result()
            self.i += 1
        return

    