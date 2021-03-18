import simulations.simulationsRunner as sim
sim.global_nb_city = 50
sim.show_path = True
sim.global_indiv_count = 1000
sim.global_generation_count = 10000
"""go to to the sim script to change parameters or change the from here"""
sim.run(curriculum=[[200, 1], [1000, .2]])
