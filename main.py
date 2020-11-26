import random
from random import randint
from math import ceil, floor
from sys import exit
import time
from itertools import permutations as permute_list_base
on = True
off = False

def createCity(nbCity, limits):
    return [[(randint(limits[i][0], limits[i][1])) for i in [0, 1, 2]] for j in range(nbCity)]


def get_trip_len(city1, city2):
    if city1 == city2:
        return 0
    trip_len = sum([(city1[i] - city2[i]) ** 2 for i in range(3)]) ** .5
    # delta_h = city2[2] - city1[2]
    # slope = delta_h / trip_len
    # trip_len += slope
    return trip_len


def create_city_weight(cities):
    cMatrix = []
    for i in range(len(cities)):
        l = []
        for j in range(len(cities)):
            l.append(get_trip_len(cities[i], cities[j]))
        cMatrix.append(l)
    return cMatrix


class Indiv:
    def __init__(self, genes=()):
        self.score = 'not defined'
        self.adn = list(genes)

    def random_creation(self, city_count, city_indexs, ):
        c = [i for i in city_indexs]
        for i in range(city_count):
            rd = randint(0, len(c) - 1)
            self.adn.append(c[rd])
            c.pop(rd)
        if len(self.adn) < city_count:
            print('not enough cities')

    def get_score(self, weightMatrix):
        self.score = 0
        for i in range(-1, len(self.adn) - 2):
            self.score += weightMatrix[self.adn[i]][self.adn[i + 1]]
        return self.score

    def print(self, weight_matrix=()):
        if self.score == 'not defined' and weight_matrix:
            self.get_score(weight_matrix)
        print('score : ', self.score, 'adn : ', self.adn)


def insert_indiv(indiv_list, indiv_score):
    debug = 0
    mini = 0
    sup = len(indiv_list) - 1
    while debug < 10 ** 5:
        if sup - mini <= 1:
            major = indiv_list[sup].score
            minor = indiv_list[mini].score
            if major < indiv_score:
                return sup + 1
            elif indiv_score <= minor:
                return mini
            else:
                return sup
        index = (sup + mini) // 2
        if indiv_score < indiv_list[index].score:
            sup = index
        elif indiv_score > indiv_list[index].score:
            mini = index
        else:
            return index

    return 'finish exception'


def sort_indivs(indiv_list, weight_matrix):
    debug_list = []
    sorted_indiv_list = []
    first = True
    for indiv in indiv_list:
        score = indiv.get_score(weight_matrix)
        if first:
            sorted_indiv_list.append(indiv)
            debug_list.append(indiv.score)
            first = False
            continue
        index = insert_indiv(sorted_indiv_list, score)
        sorted_indiv_list.insert(index, indiv)
        debug_list.insert(index, indiv.score)

    return sorted_indiv_list


def reproduce(mum, dad, city_count, repro_mode=1):
    son_adn = []
    if repro_mode == 1:
        for i in range(city_count // 2):
            son_adn.append(dad.adn[i])
        for j in range(city_count):
            if mum.adn[j] in son_adn:
                continue
            son_adn.append(mum.adn[j])
    elif repro_mode == 2:
        pass
    # noinspection PyTypeChecker
    if len(son_adn) < city_count:
        print('caca')
    return Indiv(son_adn)


def mutate(dude: Indiv, mut_rate, city_count):
    nb_mutation = round(city_count * mut_rate)
    for i in range(nb_mutation):
        a = randint(0, city_count - 1)
        while True:
            b = randint(0, city_count - 1)
            if b != a:
                break
        dude.adn[a], dude.adn[b] = dude.adn[b], dude.adn[a]


def manage_reproduction(nbIndiv, nb_elite, indiv_list, city_count, selection_rate=.3, mutation_rate=.1):
    litter = []
    nb_breeder = floor(selection_rate * nbIndiv)
    nb_repro_per_indiv = (nbIndiv - nb_elite) // nb_breeder
    nb_elite_repro = nb_repro_per_indiv // 2
    for i in range(nb_breeder):
        breeder = indiv_list[i]
        repro_list = list(range(nb_elite_repro))
        if i < nb_elite_repro:
            repro_list.remove(i)
        for j in repro_list:
            son = reproduce(breeder, indiv_list[j], city_count)
            mutate(son, mutation_rate, city_count)
            litter.append(son)

        for h in range(nb_repro_per_indiv - nb_elite_repro):
            while True:
                a = randint(0, nb_breeder)
                if a != i:
                    break
            son = reproduce(breeder, indiv_list[a], city_count)
            mutate(son, mutation_rate, city_count)
            litter.append(son)
    for i in range(nbIndiv - nb_elite - nb_repro_per_indiv * nb_breeder):
        b = randint(0, nb_breeder // 2)
        while True:
            a = randint(0, nb_breeder // 2)
            if a != i:
                break
        son = reproduce(indiv_list[a], indiv_list[b], city_count)
        mutate(son, mutation_rate, city_count)
        litter.append(son)
    return litter


def genesis(indiv_count, g_city_count):
    indiv_list = []
    gen_city_indexs = [i for i in range(g_city_count)]
    for i in range(indiv_count):
        indiv = Indiv()
        indiv.random_creation(g_city_count, gen_city_indexs)
        indiv_list.append(indiv)
    return indiv_list


debug_indiv = None


def run_generation(g_list_indivs, g_weights_matrix, g_city_count, g_indiv_count=500, g_mutation_rate=.1,
                   g_selection_rate=.3, g_elite_size=3, ):
    global debug_indiv
    g_list_indivs = sort_indivs(g_list_indivs, g_weights_matrix)
    print(g_list_indivs[0].score)

    print(debug_indiv in g_list_indivs)

    new_gen = manage_reproduction(g_indiv_count, g_elite_size, g_list_indivs, g_city_count, g_selection_rate,
                                  g_mutation_rate)
    for i in range(g_elite_size + 1):
        new_gen.append(g_list_indivs[i])
    debug_indiv = g_list_indivs[0]
    return new_gen


def swap(list, a, b):
    list[a], list[b] = list[b], list[a]


def get_permutations(list, to_print=(), perms_list=()):
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


def brute_force(nb_city, weight_matrix):
    permutations = permute_list_base([i for i in range(nb_city)])

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
    return best_path, maxi


# global_parameters
# genetic algorithm
global_city_count = 10
global_mutation_rate = .1
global_selection_rate = .3
global_indiv_count = 300
global_nb_elite = 3
cityMatrix = []
cities = createCity(10, [[0, 100] for i in range(3)])
weights = create_city_weight(cities)

# miscs
brute_force_comparaison = on


population = genesis(300, 10)
# a = Indiv()
# a.random_creation(global_city_count, [i for i in range(global_city_count)])
# b = Indiv()
# b.random_creation(global_city_count, [i for i in range(global_city_count)])
# a.get_score(weights)
# b.get_score(weights)
# print(id(a.score), a.score, id(b.score), b.score)
# print(id(a.adn), id(b.adn))
# print(weights)
# for i in population:
#    if len(i.adn)
t = time.process_time()
for i in range(100):
    population = run_generation(population, weights, 10)
algo_gen_time = time.process_time() - t
best_indiv = sort_indivs(population, weights)[0]
best_indiv.print(weights)
algo_gen_score = best_indiv.score
if brute_force_comparaison:
    brute_time = time.process_time()
    bestPath, bestScore = brute_force(global_city_count, weights)
    brute_time = time.process_time() - brute_time

    print("the genetic algorithm took " + str(algo_gen_time)
          + "s to run\n while the brute force one took : " + str(brute_time) + "\n" +
          "the genetic algorithm reached " + str((100-(algo_gen_score-bestScore)/bestScore))+
          "% of the best score " + str(algo_gen_score)+ " (algo score and) "+ str(bestScore) + " (best score)")
