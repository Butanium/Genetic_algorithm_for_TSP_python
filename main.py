import random
from random import randint
from sys import exit
import time
import matplotlib.pyplot as plt

on = True
off = False


def create_city(nbCity, limits):
    global dimension
    return [[(randint(limits[i][0], limits[i][1])) for i in range(dimension)] for j in range(nbCity)]


def get_trip_len(city1, city2):  # calcule la distance à parcourir entre 2 villes
    # calculate the distance to reach city2 from city1
    if city1 == city2:
        return 0
    trip_len = sum([(city1[i] - city2[i]) ** 2 for i in range(len(city1))]) ** .5
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


def run_generation(g_list_indivs, g_weights_matrix, g_city_count, g_indiv_count=500, g_mutation_rate=.015,
                   g_selection_rate=.15, g_elite_size=3, g_nb_new_indiv=5):  # a normal generation
    global generation_scores
    g_list_indivs = sort_indivs(g_list_indivs, g_weights_matrix)
    generation_scores.append(g_list_indivs[0].score)
    new_gen = manage_reproduction(g_indiv_count, g_elite_size, g_list_indivs, g_city_count, g_selection_rate,
                                  g_mutation_rate, g_nb_new_indiv)
    for i in range(g_elite_size + 1):
        new_gen.append(g_list_indivs[i])

    return new_gen


dimension = 2
# global_parameters
# genetic algorithm
global_city_count = 50
global_mutation_rate = .015
global_selection_rate = .15
global_indiv_count = 500
global_nb_elite = 3
global_nb_new_indiv = 3
# Simulated_annealing
annealing_precision = 10**5


cityMatrix = []
cities = create_city(global_city_count, [[0, 100] for i in range(dimension)])

weights = create_city_weight(cities)

# algo switch
brute_force_comparaison = off  # if you want or not the script to run the brute force algorithm to compare
annealing_comparaison = on
genetic_algorithm = on

plt.suptitle(str(global_city_count) + " cities")

if genetic_algorithm:
    from genetic_algorithm import genesis, sort_indivs, manage_reproduction

    population = genesis(global_indiv_count, global_city_count)
    t = time.process_time()
    generations = []
    generation_scores = []
    for i in range(100):
        generations.append(time.process_time() - t)
        population = run_generation(population, weights, global_city_count, global_indiv_count, global_mutation_rate,
                                    global_selection_rate, global_nb_elite, global_nb_new_indiv)

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
    algo_gen_path = best_indiv.adn

if brute_force_comparaison:

    if genetic_algorithm:
        plt.subplot(212)
    from brute_force import brute_force_algorithm

    brute_time = time.process_time()
    brute_force_x = []
    brute_force_y = []
    brut_force_path, brute_force_score = brute_force_algorithm(global_city_count, weights)
    brute_time = time.process_time() - brute_time
    brute_force_x.append(brute_time)
    brute_force_y.append(brute_force_score)
    plt.plot(brute_force_x, brute_force_y, )

    plt.title('Brute force performance on time')
    plt.ylabel('brute force score')
    plt.xlabel('time (s)')
    if genetic_algorithm:
        print("the genetic algorithm took " + str(algo_gen_time)
              + "s to run\n while the brute force one took : " + str(brute_time) + "\n" +
              "the genetic algorithm reached " + str(
            (100 - (algo_gen_score - brute_force_score) * 100 / brute_force_score)) +
              "% of the best score " + str(algo_gen_score) + " (algo score and) " + str(
            brute_force_score) + " (best score)")

if annealing_comparaison:
    from simulated_annealing import simulated_annealing

    if genetic_algorithm:
        plt.subplot(212)
    annealing_time = time.process_time()
    annealing_x = []
    annealing_y = []
    annealing_path, annealing_score = simulated_annealing(global_city_count, weights, annealing_x, annealing_y,
                                                          annealing_precision)
    annealing_time = time.process_time() - annealing_time
    annealing_x.append(annealing_time)
    annealing_y.append(annealing_score)
    plt.plot(annealing_x, annealing_y, )
    plt.title('simulated annealing performance on time')
    plt.ylabel('simulated annealing score')
    plt.xlabel('time (s)')
    if genetic_algorithm:
        print("the genetic algorithm took " + str(algo_gen_time)
              + "s to run\n while the simulated annealing one took : " + str(annealing_time) + "\n" +
              "the genetic algorithm reached " + str(
            (100 - ((algo_gen_score - annealing_score) * 100 / annealing_score))) +
              "% of the best score " + str(algo_gen_score) + " (algo score and) " + str(
            annealing_score) + " (best score)")
plt.show()
import result_display

if annealing_comparaison:
    result_display.show_path(annealing_path, cities, 'simulated annealing')
if genetic_algorithm:
    result_display.show_path(algo_gen_path, cities, 'genetic algorithm')
if brute_force_comparaison:
    result_display.show_path(brut_force_path, cities, 'brute force')
