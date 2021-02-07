def function1():
    print('goodbye')


def function2(foo):
    for f in foo:
        print(f)


def main():
    function1()
    function2([1, 2, 3, 4, 5])


if __name__ == '__main__':
    main()