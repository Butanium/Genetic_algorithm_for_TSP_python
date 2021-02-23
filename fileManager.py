from os import walk


def save(liste):
    _, _, filenames = next(walk("C:/Users/Clement/Documents/prépa/algogen/saves"))
    m = -1
    for i in filenames:
        if "_" in i:
            m = max(int(i.split('_')[-1].split('.')[0]), m)
    f = open("C:/Users/Clement/Documents/prépa/algogen/saves/save_" + str(m + 1) + ".txt", "w")
    for i in liste[:-1]:
        f.write(str(i) + "\n")
    f.write(str(liste[-1]))


def str_to_list(s):
    return s[1:-1].split(',')


def load(i, l=False, fun=int):
    file = open("C:/Users/Clement/Documents/prépa/algogen/saves/save_" + str(i) + ".txt", "r").read().split("\n")
    if l:
        return list(map(lambda x: list(map(fun, x)), list(map(str_to_list, file))))

    return list(map(fun, file))

