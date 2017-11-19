import hackathon


def optimize():
    tests = hackathon.tests.Tests()
    tests.order = ['some', 'more']
    ci = hackathon.ci.CI(tests)
    for cl in ci:
        print(cl)
        tests.order.append('test')


if __name__ == '__main__':
    optimize()
