import random
from random import randint
from sys import exit
import time
import matplotlib.pyplot as plt
import result_display
import fileManager

ON = True
OFF = False


def create_city(nbCity, limits):
    """create the cities"""
    global dimension
    return [[(randint(limits[i][0], limits[i][1])) for i in range(dimension)] for _ in range(nbCity)]


def get_trip_len(city1, city2):  # calcule la distance à parcourir entre 2 villes
    """calculate the distance to reach city2 from city1"""
    if city1 == city2:
        return 0
    trip_len = sum([(city1[i] - city2[i]) ** 2 for i in range(len(city1))]) ** .5
    # delta_h = city2[2] - city1[2]
    # slope = delta_h / trip_len
    # trip_len += slope
    return trip_len


def create_city_weight(cities):
    """create the weight matrix in which all distance between cities are stored"""
    cMatrix = []
    for i in range(len(cities)):
        l = []
        for j in range(len(cities)):
            l.append(get_trip_len(cities[i], cities[j]))
        cMatrix.append(l)
    return cMatrix


# global_parameters
dimension = 2
city_seed = 2  # -1 for random seed


# genetic algorithm
global_nb_city = 25
global_mutation_rate = .05
global_selection_rate = .2
global_indiv_count = 500
global_nb_elite = 3
global_nb_new_indiv = 3
global_generation_count = 1000
# Simulated_annealing
annealing_precision = 10 ** 5

cityMatrix = []
if city_seed == -1:
    cities = create_city(global_nb_city, [[0, 100] for i in range(dimension)])
else:
    cities = fileManager.load(city_seed, True)[:global_nb_city]
weights = create_city_weight(cities)

# algo switch
brute_force_comparaison = OFF  # if you want or not the script to run the brute force algorithm to compare
annealing_comparaison = OFF
annealing_comparaison_v2 = OFF
genetic_algorithm = OFF
genetic_graph_time = OFF
active = brute_force_comparaison + annealing_comparaison + annealing_comparaison_v2 + genetic_algorithm
show_path = OFF
show_graph = ON


plt.suptitle(str(global_nb_city) + " cities")



def run(title = ""):
    if genetic_algorithm:
        from genetic_algorithm import genesis, sort_indivs, run_generation

        population = genesis(global_indiv_count, global_nb_city)
        t = time.process_time()
        generations = []
        generation_scores = []
        for i in range(global_generation_count):
            generations.append(time.process_time() - t)
            population = run_generation(generation_scores, population, weights, global_nb_city, global_indiv_count,
                                        global_mutation_rate,
                                        global_selection_rate, global_nb_elite, global_nb_new_indiv)

        if show_graph:
            if active > 1:
                plt.subplot(211)
            markers_on = [i for i in range(len(generations)) if i % 4 == 0 or i < 10]
            if genetic_graph_time:
                plt.plot(generations, generation_scores, marker='.', markevery=markers_on)
                plt.xlabel('time (s)')
            else:
                plt.plot(generation_scores)
                plt.xlabel('generations')
            plt.title('Genetic algorithm performance on time'+title)
            plt.ylabel('best indiv score per generation')

        algo_gen_time = time.process_time() - t
        best_indiv = sort_indivs(population, weights)[0]
        print(title)
        best_indiv.print(weights)
        print('\n')
        algo_gen_score = best_indiv.score
        algo_gen_path = best_indiv.adn

    if brute_force_comparaison:

        if genetic_algorithm:
            plt.subplot(212)
        from brute_force import brute_force_algorithm

        brute_time = time.process_time()
        brute_force_x = []
        brute_force_y = []
        brut_force_path, brute_force_score = brute_force_algorithm(global_nb_city, weights)
        brute_time = time.process_time() - brute_time
        brute_force_x.append(brute_time)
        brute_force_y.append(brute_force_score)
        plt.plot(brute_force_x, brute_force_y, )

        plt.title('Brute force performance on time'+title)
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

        if genetic_algorithm or annealing_comparaison_v2:
            plt.subplot(212)
        annealing_time = time.process_time()
        annealing_x = []
        annealing_y = []
        annealing_path, annealing_score = simulated_annealing(global_nb_city, weights, annealing_x, annealing_y,
                                                              annealing_precision)
        annealing_time = time.process_time() - annealing_time
        annealing_x.append(annealing_time)
        annealing_y.append(annealing_score)
        plt.plot(annealing_x, annealing_y, )
        plt.title('simulated annealing performance on time'+title)
        plt.ylabel('simulated annealing score')
        plt.xlabel('time (s)')
        if genetic_algorithm:
            print("the genetic algorithm took " + str(algo_gen_time)
                  + "s to run\n while the simulated annealing one took : " + str(annealing_time) + "\n" +
                  "the genetic algorithm reached " + str(
                (100 - ((algo_gen_score - annealing_score) * 100 / annealing_score))) +
                  "% of the best score " + str(algo_gen_score) + " (algo score and) " + str(
                annealing_score) + " (best score)")

    if annealing_comparaison_v2:
        from simulated_annealing import simulated_annealing_v2

        if genetic_algorithm:
            plt.subplot(212)
        if not genetic_algorithm and annealing_comparaison:
            plt.subplot(211)
        annealing_time = time.process_time()
        annealing_x = []
        annealing_y = []
        annealing_v2_path, annealing_v2_score = simulated_annealing_v2(global_nb_city, weights, annealing_x, annealing_y,
                                                                       )
        annealing_time = time.process_time() - annealing_time
        annealing_x.append(annealing_time)
        annealing_y.append(annealing_v2_score)
        plt.plot(annealing_x, annealing_y, )
        plt.title('simulated annealing performance v2 on time'+title)
        plt.ylabel('simulated annealing v2 score')
        plt.xlabel('time (s)')
        if genetic_algorithm:
            print("the genetic algorithm took " + str(algo_gen_time)
                  + "s to run\n while the simulated annealing v2 one took : " + str(annealing_time) + "\n" +
                  "the genetic algorithm reached " + str(
                (100 - ((algo_gen_score - annealing_v2_score) * 100 / annealing_v2_score))) +
                  "% of the best score " + str(algo_gen_score) + " (algo score and) " + str(
                annealing_v2_score) + " (best score)")

    plt.show()
    if show_path:
        if annealing_comparaison:
            result_display.show_path(annealing_path, cities, 'simulated annealing'+title)
        if genetic_algorithm:
            result_display.show_path(algo_gen_path, cities, 'genetic algorithm'+title)
        if brute_force_comparaison:
            result_display.show_path(brut_force_path, cities, 'brute force'+title)
        if annealing_comparaison_v2:
            result_display.show_path(annealing_v2_path, cities, 'simulated annealing_v2'+title)
    return best_indiv.score if genetic_algorithm else None
