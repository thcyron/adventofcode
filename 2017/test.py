from subprocess import check_output
import sys


def test_day(day, result):
    global all_passed

    f = f'day{day}'
    check_output(f'clang++ -o {f} -Wall -std=c++1z {f}.cpp', shell=True)
    out = check_output(f'./{f} < {f}.txt', shell=True)
    lines = out.decode().strip().split('\n')

    if lines != result:
        print(f'day {day}: {lines} does not match expected result {result}')
        all_passed = False


all_passed = True

test_day('01', ['1251', '1244'])
test_day('02', ['53460', '282'])
test_day('03', ['475', '279138'])
test_day('04', ['325', '119'])
test_day('05', ['372139', '29629538'])
test_day('06', ['14029', '2765'])

if not all_passed:
    sys.exit(1)
