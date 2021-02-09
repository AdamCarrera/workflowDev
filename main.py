def function1():
    print('goodbye')


def function2(x1, x2, x4):
    x3 = x1 * x2
    # TEST COMMENTS!! CAN YOU READ THIS!!?
    return x1 * x2 + x3 + x4


def main():
    function1()
    y = function2(1, 3, 2)
    print(y)


if __name__ == '__main__':
    main()
