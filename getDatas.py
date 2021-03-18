from simulations import simulationsRunner as simR
import numpy as np
from tools import fileManager
import matplotlib.pyplot as plt
from playsound import playsound

ON, OFF = True, False

"""data parameters :"""
selection_rate_data = OFF
mutation_rate_data = OFF
hybrid_comparison_data = ON

simR.genetic_algorithm = True
simR.global_generation_count = 500
simR.global_nb_city = 25
simR.show_graph = False
simR.show_path = False
ra = []
rq1 = []
rq2 = []
rmax = []
rmin = []
sim_per_val = 40
start = 0.015
end = 0.07
precision = 20
save_sub = str(start) + '-' + str(end) + ', ' + str(precision) + " pts"

if selection_rate_data:
    mutation_rate_data = OFF
    save_title = "selection rate"
elif mutation_rate_data:
    save_title = "mutation rate"
elif hybrid_comparison_data:
    save_title = "hybrid comparison"

v = list(map(lambda x: round(x, 4), np.linspace(start, end, precision)))
if selection_rate_data:
    for i in v:
        simR.global_selection_rate = i
        a = simR.run(", selection rate : " + str(round(i * 100, 1)) + "%")
        r = [a]
        inf = a
        sup = a
        for _ in range(sim_per_val - 1):
            a = simR.run(", selection rate : " + str(round(i * 100, 1)) + "%")
            r.append(a)
            inf = min(inf, a)
            sup = max(sup, a)
        ra.append(sum(r) / sim_per_val)
        rmin.append(inf)
        rmax.append(sup)
        r.sort()
        rq1.append(sum(r[:sim_per_val // 4]) / (sim_per_val // 4))
        rq2.append(sum(r[-1:-(sim_per_val // 4) - 1:-1]) / (sim_per_val // 4))
    plt_title = "selection rate result, " + str(sim_per_val) + " sim per value"
elif mutation_rate_data:
    for i in v:
        simR.global_mutation_rate = i
        a = simR.run(", mutation rate : " + str(round(i * 100, 1)) + "%")
        r = [a]
        inf = a
        sup = a
        for _ in range(sim_per_val - 1):
            a = simR.run(", mutation rate : " + str(round(i * 100, 1)) + "%")
            r.append(a)
            inf = min(inf, a)
            sup = max(sup, a)
        ra.append(sum(r) / sim_per_val)
        rmin.append(inf)
        rmax.append(sup)
        r.sort()
        rq1.append(sum(r[:sim_per_val // 4]) / (sim_per_val // 4))
        rq2.append(sum(r[-1:-(sim_per_val // 4) - 1:-1]) / (sim_per_val // 4))
    plt_title = "mutation rate result, " + str(sim_per_val) + " sim per value"
elif hybrid_comparison_data:
    v = [0, [[50, 1], [500, .2]], [[100, 1], [500, .2]],[[150, 1], [500, 0.2]], [[200, 1], [500, 0.2]]]
    for i in v:
        a = simR.run("curriculum : "+str(i), i)
        r = [a]
        inf = a
        sup = a
        for _ in range(sim_per_val - 1):
            a = simR.run("curriculum : "+str(i), i)
            r.append(a)
            inf = min(inf, a)
            sup = max(sup, a)
        ra.append(sum(r) / sim_per_val)
        rmin.append(inf)
        rmax.append(sup)
        r.sort()
        rq1.append(sum(r[:sim_per_val // 4]) / (sim_per_val // 4))
        rq2.append(sum(r[-1:-(sim_per_val // 4) - 1:-1]) / (sim_per_val // 4))
    plt_title="hybrid comparison result, " + str(sim_per_val) + " sim per value"
    v = [0]+[i[0][0] for i in v[1:]]

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
fig.set_title(plt_title)
ax.legend()
plt.show()
playsound("miscs/Terminated.mp3")
