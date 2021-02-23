import main
import numpy as np
import matplotlib.pyplot as plt
from playsound import playsound
ON,OFF = True, False
param_list = ["selection_rate", "mutation_rate"]

"""data parameters :"""
selection_rate_data = OFF
mutation_rate_data = ON


main.genetic_algorithm = True
main.global_generation_count = 300
main.global_nb_city = 25
main.show_graph = False
main.show_path = False
ra = []
rq1 = []
rq2 = []
rmax = []
rmin = []
n = 40
v = np.linspace(0, 1, 40)
if selection_rate_data:
    for i in v:
        main.global_selection_rate = i
        a = main.run(", selection rate : " + str(round(i * 100, 1)) + "%")
        r = [a]
        inf = a
        sup = a
        for _ in range(n - 1):
            a = main.run(", selection rate : " + str(round(i * 100, 1)) + "%")
            r.append(a)
            inf = min(inf, a)
            sup = max(sup, a)
        ra.append(sum(r) / n)
        rmin.append(inf)
        rmax.append(sup)
        r.sort()
        rq1.append(sum(r[:n // 4]) / (n // 4))
        rq2.append(sum(r[-1:-(n // 4) - 1:-1]) / (n // 4))
    plt.title("selection rate result, "+str(n)+" sim per value")
elif mutation_rate_data:
    for i in v:
        main.global_mutation_rate = i
        a = main.run(", mutation rate : " + str(round(i * 100, 1)) + "%")
        r = [a]
        inf = a
        sup = a
        for _ in range(n - 1):
            a = main.run(", mutation rate : " + str(round(i * 100, 1)) + "%")
            r.append(a)
            inf = min(inf, a)
            sup = max(sup, a)
        ra.append(sum(r) / n)
        rmin.append(inf)
        rmax.append(sup)
        r.sort()
        rq1.append(sum(r[:n // 4]) / (n // 4))
        rq2.append(sum(r[-1:-(n // 4) - 1:-1]) / (n // 4))
    plt.title("mutation rate result, "+str(n)+" sim per value")

print(ra)
print(rmax)
print(rmin)
ax, fig = plt.subplots()
plt.plot(v, ra, color="blue", label="average")
plt.plot(v, rmax, color="red", label="worst case")
plt.plot(v, rmin, color="green", label="best case")
plt.plot(v, rq1, color="cyan", label="First quantile")
plt.plot(v, rq2, color="orange", label="Third quantile")
ax.legend()
plt.show()
playsound("Terminated.mp3")
