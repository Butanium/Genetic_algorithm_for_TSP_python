from simulations import simulationsRunner
import numpy as np
from tools import fileManager
import matplotlib.pyplot as plt
from playsound import playsound

ON, OFF = True, False

"""data parameters :"""
selection_rate_data = OFF
mutation_rate_data = ON

simulationsRunner.genetic_algorithm = True
simulationsRunner.global_generation_count = 300
simulationsRunner.global_nb_city = 25
simulationsRunner.show_graph = False
simulationsRunner.show_path = False
ra = []
rq1 = []
rq2 = []
rmax = []
rmin = []
n = 40
start = 0.015
end = 0.07
precision = 20
save_sub = str(start) + '-' + str(end) + ', ' + str(precision) + " pts"
if selection_rate_data:
    mutation_rate_data = OFF
    save_title = "selection rate"
elif mutation_rate_data:
    save_title = "mutation rate"
else:
    exit()

v = list(map(lambda x: round(x, 4), np.linspace(start, end, precision)))
if selection_rate_data:
    for i in v:
        simulationsRunner.global_selection_rate = i
        a = simulationsRunner.run(", selection rate : " + str(round(i * 100, 1)) + "%")
        r = [a]
        inf = a
        sup = a
        for _ in range(n - 1):
            a = simulationsRunner.run(", selection rate : " + str(round(i * 100, 1)) + "%")
            r.append(a)
            inf = min(inf, a)
            sup = max(sup, a)
        ra.append(sum(r) / n)
        rmin.append(inf)
        rmax.append(sup)
        r.sort()
        rq1.append(sum(r[:n // 4]) / (n // 4))
        rq2.append(sum(r[-1:-(n // 4) - 1:-1]) / (n // 4))
    plt.title("selection rate result, " + str(n) + " sim per value")
elif mutation_rate_data:
    for i in v:
        simulationsRunner.global_mutation_rate = i
        a = simulationsRunner.run(", mutation rate : " + str(round(i * 100, 1)) + "%")
        r = [a]
        inf = a
        sup = a
        for _ in range(n - 1):
            a = simulationsRunner.run(", mutation rate : " + str(round(i * 100, 1)) + "%")
            r.append(a)
            inf = min(inf, a)
            sup = max(sup, a)
        ra.append(sum(r) / n)
        rmin.append(inf)
        rmax.append(sup)
        r.sort()
        rq1.append(sum(r[:n // 4]) / (n // 4))
        rq2.append(sum(r[-1:-(n // 4) - 1:-1]) / (n // 4))
    plt.title("mutation rate result, " + str(n) + " sim per value")

fileManager.save(list(zip(v, ra)), save_title + "_average", save_sub)
fileManager.save(list(zip(v, rq1)), save_title + "_firstQuartile", save_sub)
fileManager.save(list(zip(v, rq2)), save_title + "_thirdQuartile", save_sub)
fileManager.save(list(zip(v, rmax)), save_title + "_worstCase", save_sub)
fileManager.save(list(zip(v, rmin)), save_title + "_bestCase", save_sub)

ax, fig = plt.subplots()
plt.plot(v, ra, color="blue", label="average")
plt.plot(v, rmax, color="red", label="worst case")
plt.plot(v, rmin, color="green", label="best case")
plt.plot(v, rq1, color="cyan", label="First quartile")
plt.plot(v, rq2, color="orange", label="Third quartile")
ax.legend()
plt.show()
playsound("Terminated.mp3")
