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


def simulated_annealing(city_count, weight_matrix, x_list, y_list, precision =.9993):
    start_time = process_time()

    indexs = [i for i in range(city_count)]
    chosen_route = []
    temperature = city_count / 4
    for i in range(city_count):  # generate first route
        a = randint(0, len(indexs) - 1)
        chosen_route.append(indexs[a])
        indexs.pop(a)
    energy = get_route_len(weight_matrix, chosen_route)
    x_list.append(process_time()-start_time)
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
        x_list.append(process_time()-start_time)
        y_list.append(energy)
        temperature *= precision
        #print(temperature)

    return chosen_route, energy
