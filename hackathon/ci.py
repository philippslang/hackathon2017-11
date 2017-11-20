import sqlite3 as sql


class TestResult:
    STATUS = ['passed', 'failed', 'na']

    def __init__(self):
        self.name = ''
        self.cost = 0
        self.istatus = self.STATUS.index('na')

    def status(self):
        return self.STATUS[self.istatus]


class Result:

    def __init__(self):
        self.tests = []
        self.score = 0

    def __repr__(self):
        return 'res'


class CI:

    def __init__(self, tests, dbfname):
        self.tests = tests
        self.build()
        self.db = sql.connect(dbfname)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.db.close()

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
