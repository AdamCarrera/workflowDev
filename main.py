def function1():
    print('goodbye')


def function2(x1, x2):
    x3 = x1 * x2
    return x1 * x2 + x3


def main():
    function1()
    y = function2(1, 3)


if __name__ == '__main__':
    main()
