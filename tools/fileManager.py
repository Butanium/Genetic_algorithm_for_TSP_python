from os import walk


def save(liste, title ="save", subtitle =""):
    _, _, filenames = next(walk("/saves"))
    m = -1
    for i in filenames:
        if title+"_" in i:
            m = max(int(i.split('_')[-1].split('.')[0]), m)
    f = open("C:/Users/Clement/Documents/prépa/algogen/saves/" + title + "_" + subtitle+"_"+ str(m + 1) + ".txt", "w")
    for i in liste[:-1]:
        f.write(str(i) + "\n")
    f.write(str(liste[-1]))


def str_to_list(s):
    return s[1:-1].split(',')


def load(index, l=False, prefix = "save",fun=int):
    _, _, filenames = next(walk("/saves"))
    for i in filenames:
        if prefix+"_" in i:
            if int(i.split('_')[-1].split('.')[0]) == index:
                file = open("C:/Users/Clement/Documents/prépa/algogen/saves/"+i, "r")
                break
    else:
        raise NameError('file :'+ prefix + "_" +str(index)+ ' not found')
    datas = file.read().split("\n")
    if l:
        return list(map(lambda x: list(map(fun, x)), list(map(str_to_list, datas))))

    return list(map(fun, datas))

