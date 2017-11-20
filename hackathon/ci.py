import pandas as pd
DELIM = '%'


class TestResult:
    STATUS = ['passed', 'failed']

    def __init__(self, name, cost, status):
        self.name = name
        self.cost = cost
        self.istatus = self.STATUS.index(status)

    def status(self):
        return self.STATUS[self.istatus]


class Result:

    def __init__(self, cl, tests, score):
        self.cl = cl
        self.tests = tests
        self.score = score

    def __repr__(self):
        ntests = len(self.tests)
        nfailures = sum(1 for test in self.tests if test.status() == 'failed')
        return '{:d} tests, {:d} failures, score = {:d}.'.format(ntests, nfailures, self.score)


class CI:

    def __init__(self, tests, dbfname):
        self.tests = tests
        self.db = pd.read_csv(dbfname)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return

    def result(self, row):
        tests = row[4].split(DELIM)
        status = row[3].replace('0', 'passed').replace('1', 'failed').split(DELIM)
        cost = [int(i) for i in row[2].split(DELIM)]
        test_results = [TestResult(tests[i], cost[i], status[i]) for i in range(len(tests))]
        cl = int(row[1])
        return Result(cl, test_results, 0)

    def __iter__(self):
        for row in self.db.itertuples():
            yield self.result(row)
        return
