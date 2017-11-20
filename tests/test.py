import hackathon
import tempfile
import os

FNAME = 'test.csv'


def test():
    if 1:
        with open(FNAME, 'w') as f:
            f.write('cl,effort,status,test')
            f.write('\n')
            f.write('0,1%2%3,0%1%0,t1%t2%t3')
            f.write('\n')
            f.write('1,3%4%5,1%0%0,t4%t5%t6')
            f.write('\n')
            f.write('1,3%4%5,0%0%1,t4%t5%t6')
            f.write('\n')
            f.write('1,3%4%5,0%0%1,t4%t5%t6')
            f.write('\n')
            f.write('1,3%4%5,0%0%0,t4%t5%t6')
            f.write('\n')
            f.write('1,3%4%5%6,0%0%1%0,t4%t5%t6%t7')
            f.write('\n')

    tests = hackathon.tests.Tests(order=[])
    with hackathon.ci.CI(tests, FNAME) as ci:
        i = 0
        for result in ci:
            print(result)
            if i == 0:
                assert result.score == 3
                for test in result.test_results:
                    if test.name == 't1':
                        assert test.cost == 1
                        assert test.status() == 'passed'
                    if test.name == 't2':
                        assert test.cost == 2
                        assert test.status() == 'failed'
                    if test.name == 't3':
                        assert test.cost == 3
                        assert test.status() == 'passed'
            if i == 1:
                assert result.score == 3
            if i == 2:
                assert result.score == 12
                tests.order = ['t6']
            if i == 3:
                assert result.score == 5
            if i == 4:
                assert result.score == None
                tests.order = ['t4', 't6', 'xx', 't7', 't5' ]
            if i == 5:
                assert result.score == 8
                for test in result.test_results:
                    if test.name == 't4':
                        assert test.cost == 3
                        assert test.status() == 'passed'
                    if test.name == 't5':
                        assert test.cost == 4
                        assert test.status() == 'passed'
                    if test.name == 't6':
                        assert test.cost == 5
                        assert test.status() == 'failed'
                    if test.name == 't7':
                        assert test.cost == 6
                        assert test.status() == 'passed'
            i += 1
        assert i == 6
        assert ci.score() == 31
        print(ci)
    
    os.remove(FNAME)
