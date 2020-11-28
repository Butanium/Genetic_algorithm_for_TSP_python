import random
from random import randint
from sys import exit
import time
import matplotlib.pyplot as plt

on = True
off = False


def create_city(nbCity, limits):
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


# global_parameters
# genetic algorithm
global_city_count = 500
global_mutation_rate = .015
global_selection_rate = .15
global_indiv_count = 700
global_nb_elite = 3
global_nb_new_indiv = 10
cityMatrix = []
cities = create_city(global_city_count, [[0, 100] for i in range(3)])
weights = create_city_weight(cities)

# miscs
brute_force_comparaison = off  # if you want or not the script to run the brute force algorithm to compare
annealing_comparaison = on
genetic_algorithm = off

plt.suptitle(str(global_city_count) + " cities")

if genetic_algorithm:
    from genetic_algorithm import genesis, run_generation, sort_indivs

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

if brute_force_comparaison:

    if genetic_algorithm:
        plt.subplot(212)
    from brute_force import brute_force_algorithm

    brute_time = time.process_time()
    brute_force_x = []
    brute_force_y = []
    bestPath, bestScore = brute_force_algorithm(global_city_count, weights)
    brute_time = time.process_time() - brute_time
    brute_force_x.append(brute_time)
    brute_force_y.append(bestScore)
    plt.plot(brute_force_x, brute_force_y, )

    plt.title('Brute force performance on time')
    plt.ylabel('brute force score')
    plt.xlabel('time (s)')
    if genetic_algorithm:
        print("the genetic algorithm took " + str(algo_gen_time)
              + "s to run\n while the brute force one took : " + str(brute_time) + "\n" +
              "the genetic algorithm reached " + str((100 - (algo_gen_score - bestScore) * 100 / bestScore)) +
              "% of the best score " + str(algo_gen_score) + " (algo score and) " + str(bestScore) + " (best score)")

if annealing_comparaison:
    from simulated_annealing import simulated_annealing

    if genetic_algorithm:
        plt.subplot(212)
    annealing_time = time.process_time()
    annealing_x = []
    annealing_y = []
    annealing_path, annealing_score = simulated_annealing(global_city_count, weights, annealing_x, annealing_y)
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
