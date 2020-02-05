a = int(input("Size of A? "))
b = int(input("Size of B? "))


def al(a, b):
    if a == 0 or b == 0:
        return 1
    else:
        return al(a - 1, b - 1) + al(a - 1, b) + al(a, b - 1)


print(al(a, b))
