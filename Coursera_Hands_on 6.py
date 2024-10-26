# global scope
my_global = 10


def fn1():
    enclosed_v = 8

    def fn2():
        local_v = 5
        print("Access To Global:", my_global)
        print("Access To Enclosed:", enclosed_v)
        print("Access To Local:", local_v)

    fn2()


fn1()

