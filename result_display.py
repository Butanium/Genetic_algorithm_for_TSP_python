import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def show_cities(cities, ax):
    is_3D = len(cities[0]) == 3
    my_x = []
    my_y = []
    if is_3D:
        my_z = []
    else:
        my_z = 0

    for city in cities:
        my_x.append(city[0])
        my_y.append(city[1])
        if is_3D:
            my_z.append(city[2])
    if is_3D:
        ax.scatter(my_x, my_y, my_z)
    else:
        ax.scatter(my_x, my_y)


def show_path(path, cities, method_name=''):
    is_3D = len(cities[0]) == 3
    fig = plt.figure()
    if is_3D:
        ax = fig.add_subplot(111, projection='3d')
    else:
        ax = fig.add_subplot(111)
    show_cities(cities, ax)
    my_x = []
    my_y = []
    if is_3D:
        my_z = []
    else:
        my_z = 0

    for city_index in path:
        my_x.append(cities[city_index][0])
        my_y.append(cities[city_index][1])
        if is_3D:
            my_z.append(cities[city_index][2])

    my_x.append(cities[path[0]][0])
    my_y.append(cities[path[0]][1])
    if is_3D:
        my_z.append(cities[path[0]][2])
    plt.title(method_name + ' path')
    if is_3D:
        ax.plot(my_x, my_y, my_z)
    else:
        ax.plot(my_x, my_y)
    plt.show()
