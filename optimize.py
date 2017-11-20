import hackathon

DBFNAME = 'data_train.csv'


def optimize():
    tests = hackathon.tests.Tests(order=[])

    with hackathon.ci.CI(tests, DBFNAME) as ci:
        for result in ci:
            print(result)

            '''
            for test in result.test_results:
                print(test.name, test.cost, test.status())
            break
            '''

            tests.order = result.test_names()
            tests.order = sorted(result.test_names())
        print(ci)


if __name__ == '__main__':
    optimize()
