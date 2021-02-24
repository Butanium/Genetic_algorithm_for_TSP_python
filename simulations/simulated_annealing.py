from random import randint
from math import ceil
from random import random
from numpy import exp
from time import process_time


def swap(list_, a, b):
    list_[a], list_[b] = list_[b], list_[a]


def get_route_len(weight_matrix, route):
    score = 0
    for i in range(-1, len(route) - 2):
        score += weight_matrix[route[i]][route[i + 1]]
    return score


def simulated_annealing(city_count, weight_matrix, x_list, y_list, precision=1000):
    start_time = process_time()
    decrement = 1 - 1 / precision
    indexs = [i for i in range(city_count)]
    chosen_route = []
    temperature = city_count / 4
    for i in range(city_count):  # generate first route
        a = randint(0, len(indexs) - 1)
        chosen_route.append(indexs[a])
        indexs.pop(a)
    energy = get_route_len(weight_matrix, chosen_route)
    x_list.append(process_time() - start_time)
    y_list.append(energy)

    while temperature >= 1:
        route = [i for i in chosen_route]
        for i in range(ceil(temperature)):
            a = randint(0, city_count - 1)
            while True:
                b = randint(0, city_count - 1)
                if b != a:
                    break
            swap(route, a, b)
        new_energy = get_route_len(weight_matrix, route)
        r = random()
        if exp(-(new_energy - energy) / temperature) > r:
            chosen_route = route
            energy = new_energy
            x_list.append(process_time() - start_time)
            y_list.append(energy)
        temperature *= decrement
        # print(temperature)
    x_list.append(process_time() - start_time)
    y_list.append(energy)
    return chosen_route, energy


def random_change(route):
    """randomly change the route :
    ex :
    i = 1
    j = 4
    [5,3,4,2,1,6] -> [6,1,4,2,3,5]
    """
    last_index = len(route) - 1
    i = randint(0, last_index - 1)
    j = randint(i + 1, last_index)
    new_route = []
    for k in range(last_index - j + 1):
        new_route.append(route[last_index - k])
    for k in range(j - i - 1):
        new_route.append(route[i + k + 1])
    for k in range(i + 1):
        new_route.append(route[i - k])
    return new_route


def simulated_annealing_v2(city_count, weight_matrix, x_list, y_list, start_temp=.5, precision=10000, iterations=30000):
    temperature = start_temp
    start_time = process_time()
    decrement = 1 - 1 / precision
    indexs = [i for i in range(city_count)]
    chosen_route = []

    for i in range(city_count):  # generate first route
        a = randint(0, len(indexs) - 1)
        chosen_route.append(indexs[a])
        indexs.pop(a)

    energy = get_route_len(weight_matrix, chosen_route)
    x_list.append(process_time() - start_time)
    y_list.append(energy)
    for j in range(iterations):
        new_route = random_change(chosen_route)
        new_energy = get_route_len(weight_matrix, new_route)
        r = random()
        if exp(-(new_energy - energy) / temperature) > r:
            chosen_route = new_route
            energy = new_energy
            x_list.append(process_time() - start_time)
            y_list.append(energy)
        temperature *= decrement
        # print(temperature)
    x_list.append(process_time() - start_time)
    y_list.append(energy)
    return chosen_route, energy
