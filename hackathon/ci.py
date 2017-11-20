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


class TestResults:

    def __init__(self, results=[]):
        self.results = results

    def nfailures(self):
        return sum(1 for test in self.results if test.status() == 'failed')

    def ntests(self):
        return len(self.results)

    def test_names(self):
        return [test.name for test in self.results]

    def failed_test_names(self):
        return [test.name for test in self.results if test.status() == 'failed']

    def cost(self, test_names):
        test_results = [test for test in self.results if test.name in test_names]
        return sum(test.cost for test in test_results)

    def test_index(self, test_name):
        test_names = [test.name for test in self.results]
        return test_names.index(test_name)

    def cost_upto_incl(self, idx):
        return sum(self.results[i].cost for i in range(idx + 1))


class Result:

    def __init__(self, cl, test_results, score):
        self.cl = cl
        self.test_results = test_results
        self.score = score

    def test_names(self):
        return self.test_results.test_names()

    def __repr__(self):
        ntests = self.test_results.ntests()
        nfailures = self.test_results.nfailures()
        return '{:d}: {:4d} tests, {:3d} failures, score = {}.'.format(self.cl, ntests, nfailures, self.score)


def effort_score(test_results, test_order):
    #print(test_order[:3])
    failed_tests = test_results.failed_test_names()
    matched_failed_tests = [test for test in failed_tests if test in test_order]
    matched_failed_tests_indices = [test_order.index(test) for test in matched_failed_tests]
    # failures in provided tests
    if matched_failed_tests_indices:
        imin = min(matched_failed_tests_indices)
        return test_results.cost(test_order[:imin])
    # tests failed but not in provided test order
    if failed_tests:
        failed_tests_indices = [test_results.test_index(test) for test in failed_tests]
        return test_results.cost_upto_incl(min(failed_tests_indices))
    # no failures
    return None


class CI:

    def __init__(self, tests, dbfname, score_function=effort_score):
        self.tests = tests
        self.db = pd.read_csv(dbfname)
        self.score_function = score_function
        self.score = 0

    def __repr__(self):
        return 'Final score = {:d}'.format(self.score)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return

    def result(self, row):
        """
        Schema here.
        """
        cl = int(row[1])
        tests = row[4].split(DELIM)
        status = row[3].replace('0', 'passed').replace('1', 'failed').split(DELIM)
        cost = [int(i) for i in row[2].split(DELIM)]
        test_results = TestResults([TestResult(tests[i], cost[i], status[i]) for i in range(len(tests))])
        score = self.score_function(test_results, self.tests.order)
        if score:
            self.score += score
        return Result(cl, test_results, score)

    def __iter__(self):
        for row in self.db.itertuples():
            yield self.result(row)
        return
