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

    tests = hackathon.tests.Tests(order=[])
    with hackathon.ci.CI(tests, FNAME) as ci:
        i = 0
        for result in ci:
            print(result)
            if i == 0:
                assert result.score == 3
            if i == 1:
                assert result.score == 3
            if i == 2:
                assert result.score == 12
                tests.order = ['t6']
            if i == 3:
                assert result.score == 5
            i += 1
        assert i == 4
        assert ci.score() == 23
        print(ci)
    
    os.remove(FNAME)
