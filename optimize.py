import hackathon

DBFNAME = 'data_train.csv'


def optimize():
    tests = hackathon.tests.Tests(order=[])

    with hackathon.ci.CI(tests, DBFNAME) as ci:
        for result in ci:
            print(result)
            tests.order.append('test')


if __name__ == '__main__':
    optimize()
