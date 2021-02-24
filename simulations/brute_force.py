import time
from itertools import permutations as permute_list_base


def swap(list, a, b):
    list[a], list[b] = list[b], list[a]


def get_permutations(list, to_print=(), perms_list=()):  # hand made permutation code (useless)
    if not to_print:
        perms_list = [list]
    for i in range(len(list)):
        swap(list, 0, i)
        if i != 0:
            tp = [i for i in to_print]
            tp.extend([i for i in list])
            perms_list.append(tp)
        end_list = [i for i in to_print]
        end_list.append(list[0])
        if len(list) > 2:
            get_permutations([list[i] for i in range(1, len(list))], end_list, perms_list)
    return perms_list

get_permutations(['a','b','c','d'])

def brute_force_algorithm(nb_city, weight_matrix):  # brute force algorithm to compare it with the genetic algorithm
    permutations = permute_list_base([i for i in range(nb_city)])
    global brute_force_x
    global brute_force_y
    global brute_time
    # hand made code : get_permutations([i for i in range(nb_city)])
    maxi = False
    best_path = []
    for path in permutations:
        score = 0
        for i in range(-1, len(path) - 2):
            score += weight_matrix[path[i]][path[i + 1]]
        if not maxi or score < maxi:
            maxi = score
            best_path = path
            brute_force_x.append(time.process_time() - brute_time)
            brute_force_y.append(maxi)

    return best_path, maxi
