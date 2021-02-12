def function1():
    print('goodbye')


def function2(x1, x2):
    x3 = x1 * x2
    # TEST COMMENTS!! CAN YOU READ THIS!!?
    for x in x1:
        print(x)


# Add documentation
def function3(x1):
    for x in x1:
        print(x + 2)


def function4(x1, x2, x3):
    y = x1 + x2 + x3
    return y


def main():
    function1()
    function2([1, 2, 3], 3)


if __name__ == '__main__':
    main()
