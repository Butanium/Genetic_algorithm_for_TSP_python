import random
from random import randint
from math import ceil, floor
from sys import exit
import time
from itertools import permutations as permute_list_base

on = True
off = False
import matplotlib.pyplot as plt


def createCity(nbCity, limits):
    return [[(randint(limits[i][0], limits[i][1])) for i in [0, 1, 2]] for j in range(nbCity)]


def get_trip_len(city1, city2):  # calcule la distance à parcourir entre 2 villes
    # calculate the distance to reach city2 from city1
    if city1 == city2:
        return 0
    trip_len = sum([(city1[i] - city2[i]) ** 2 for i in range(3)]) ** .5
    # delta_h = city2[2] - city1[2]
    # slope = delta_h / trip_len
    # trip_len += slope
    return trip_len


def create_city_weight(cities):  # create the weight matrix in which all distance between cities are stored
    cMatrix = []
    for i in range(len(cities)):
        l = []
        for j in range(len(cities)):
            l.append(get_trip_len(cities[i], cities[j]))
        cMatrix.append(l)
    return cMatrix


class Indiv:  # an indiv is a potential solution to the problem, here it's just a list of cities which shape a route
    def __init__(self, genes=()):
        self.score = 'not defined'
        self.adn = list(genes)

    def random_creation(self, city_count, city_indexs, ):  # randomly generate the indiv route
        c = [i for i in city_indexs]
        for i in range(city_count):
            rd = randint(0, len(c) - 1)
            self.adn.append(c[rd])
            c.pop(rd)
        if len(self.adn) < city_count:
            print('not enough cities')

    def get_score(self, weightMatrix):  # return the route length
        self.score = 0
        for i in range(-1, len(self.adn) - 2):
            self.score += weightMatrix[self.adn[i]][self.adn[i + 1]]
        return self.score

    def print(self, weight_matrix=()):
        if self.score == 'not defined' and weight_matrix:
            self.get_score(weight_matrix)
        print('score : ', self.score, 'adn : ', self.adn)


def insert_indiv(indiv_list, indiv_score):  # dichotomy algorithm to sort indivs by score
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


def sort_indivs(indiv_list, weight_matrix):  # sort indivs in score ascending order
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


def reproduce(dad, mum, city_count, repro_mode=1):  # mix 2 indivs to make a new one
    son_adn = []
    if repro_mode == 1:  # first half of dad completed by the mum order : dad = [1,3,4,2] + mum [2,3,1,4] -> [1,3,2,4]
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


def mutate(dude: Indiv, mut_rate, city_count):  # random change in the indiv adn
    nb_mutation = round(city_count * mut_rate)
    for i in range(nb_mutation):
        a = randint(0, city_count - 1)
        while True:
            b = randint(0, city_count - 1)
            if b != a:
                break
        dude.adn[a], dude.adn[b] = dude.adn[b], dude.adn[a]


def manage_reproduction(nbIndiv, nb_elite, indiv_list, city_count, selection_rate=.3, mutation_rate=.1):  # manage
    #  reproduction between the selected indivs
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


def genesis(indiv_count, g_city_count):  # first generation, entirely random
    indiv_list = []
    gen_city_indexs = [i for i in range(g_city_count)]
    for i in range(indiv_count):
        indiv = Indiv()
        indiv.random_creation(g_city_count, gen_city_indexs)
        indiv_list.append(indiv)
    return indiv_list


def run_generation(g_list_indivs, g_weights_matrix, g_city_count, g_indiv_count=500, g_mutation_rate=.1,
                   g_selection_rate=.3, g_elite_size=3, ):  # a normal generation
    global generation_scores
    g_list_indivs = sort_indivs(g_list_indivs, g_weights_matrix)
    generation_scores.append(g_list_indivs[0].score)
    new_gen = manage_reproduction(g_indiv_count, g_elite_size, g_list_indivs, g_city_count, g_selection_rate,
                                  g_mutation_rate)
    for i in range(g_elite_size + 1):
        new_gen.append(g_list_indivs[i])

    return new_gen


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


def brute_force(nb_city, weight_matrix):  # brute force algorithm to compare it with the genetic algorithm
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


# global_parameters
# genetic algorithm
global_city_count = 11
global_mutation_rate = .1
global_selection_rate = .3
global_indiv_count = 300
global_nb_elite = 3
cityMatrix = []
cities = createCity(10, [[0, 100] for i in range(3)])
weights = create_city_weight(cities)

# miscs
brute_force_comparaison = off

population = genesis(global_indiv_count, global_city_count)
t = time.process_time()
generations = []
generation_scores = []

for i in range(100):
    generations.append(time.process_time() - t)
    population = run_generation(population, weights, global_city_count, global_indiv_count, global_mutation_rate,
                                global_selection_rate, global_nb_elite)



plt.subplot(211)
markers_on = [i for i in range(len(generations)) if i % 4 == 0 or i < 10]
plt.plot(generations, generation_scores, marker='.', markevery=markers_on)
plt.title('Genetic algorithm performance on time')
plt.ylabel('best indiv score per generation')
plt.xlabel('time (s)')
algo_gen_time = time.process_time() - t
best_indiv = sort_indivs(population, weights)[0]
best_indiv.print(weights)
algo_gen_score = best_indiv.score
if brute_force_comparaison:
    plt.subplot(212)
    brute_time = time.process_time()
    brute_force_x = []
    brute_force_y = []
    bestPath, bestScore = brute_force(global_city_count, weights)
    brute_time = time.process_time() - brute_time
    brute_force_x.append(brute_time)
    brute_force_y.append(bestScore)
    plt.plot(brute_force_x, brute_force_y, )

    plt.title('Brute force performance on time')
    plt.ylabel('brute force score')
    plt.xlabel('time (sà')

    print("the genetic algorithm took " + str(algo_gen_time)
          + "s to run\n while the brute force one took : " + str(brute_time) + "\n" +
          "the genetic algorithm reached " + str((100 - (algo_gen_score - bestScore) / bestScore)) +
          "% of the best score " + str(algo_gen_score) + " (algo score and) " + str(bestScore) + " (best score)")
plt.show()
