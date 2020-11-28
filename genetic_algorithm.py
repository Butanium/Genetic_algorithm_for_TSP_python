from random import randint
from math import floor


class Indiv:
    """an indiv is a potential solution to the problem, here it's just a list of cities which shape a route"""

    def __init__(self, genes=()):
        self.score = 'not defined'
        self.adn = list(genes)

    def random_creation(self, city_count, city_indexs, ):
        """randomly generate the indiv route"""
        c = [i for i in city_indexs]
        for i in range(city_count):
            rd = randint(0, len(c) - 1)
            self.adn.append(c[rd])
            c.pop(rd)
        if len(self.adn) < city_count:
            print('not enough cities')

    def get_score(self, weightMatrix):
        """return the route length"""
        self.score = 0
        for i in range(-1, len(self.adn) - 2):
            self.score += weightMatrix[self.adn[i]][self.adn[i + 1]]
        return self.score

    def print(self, weight_matrix=()):
        if self.score == 'not defined' and weight_matrix:
            self.get_score(weight_matrix)
        print('score : ', self.score, 'adn : ', self.adn)


def insert_indiv(indiv_list, indiv_score):
    """ dichotomy algorithm to sort indivs by score"""
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
    """sort indivs in score ascending order"""
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


def reproduce(dad, mum, city_count, repro_mode=1):
    """mix 2 indivs to make a new one"""
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


def mutate(dude: Indiv, mut_rate, city_count):
    """random change in the indiv adn"""
    nb_mutation = round(city_count * mut_rate)
    for i in range(nb_mutation):
        a = randint(0, city_count - 1)
        while True:
            b = randint(0, city_count - 1)
            if b != a:
                break
        dude.adn[a], dude.adn[b] = dude.adn[b], dude.adn[a]


def manage_reproduction(nbIndiv, nb_elite, indiv_list, city_count, selection_rate=.3, mutation_rate=.1,
                        nb_new_indiv=0):
    """manage the reproductions between the selected indivs"""

    litter = []
    nb_breeder = floor(selection_rate * nbIndiv)
    for i in range(nb_new_indiv):
        ind = Indiv()
        ind.random_creation(city_count, [i for i in range(city_count)])
        indiv_list.insert(nb_breeder, ind)
    # nb_breeder += nb_new_indiv
    nb_repro_per_indiv = (nbIndiv - nb_elite - nb_new_indiv) // nb_breeder
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
                a = randint(0, nb_breeder + nb_new_indiv)
                if a != i:
                    break
            son = reproduce(breeder, indiv_list[a], city_count)
            mutate(son, mutation_rate, city_count)
            litter.append(son)
    for i in range(nbIndiv - nb_elite - nb_new_indiv - nb_repro_per_indiv * nb_breeder):
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
    """randomly generate the first generation"""
    indiv_list = []
    gen_city_indexs = [i for i in range(g_city_count)]
    for i in range(indiv_count):
        indiv = Indiv()
        indiv.random_creation(g_city_count, gen_city_indexs)
        indiv_list.append(indiv)
    return indiv_list


def run_generation(score_list, g_list_indivs, g_weights_matrix, g_city_count, g_indiv_count=500, g_mutation_rate=.015,
                   g_selection_rate=.15, g_elite_size=3, g_nb_new_indiv=5):
    """run a generation"""
    g_list_indivs = sort_indivs(g_list_indivs, g_weights_matrix)
    score_list.append(g_list_indivs[0].score)
    new_gen = manage_reproduction(g_indiv_count, g_elite_size, g_list_indivs, g_city_count, g_selection_rate,
                                  g_mutation_rate, g_nb_new_indiv)
    for i in range(g_elite_size + 1):
        new_gen.append(g_list_indivs[i])

    return new_gen
