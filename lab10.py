from igraph import *
import random
import os
import csv
from random import randrange


# import matplotlib.pyplot as plt

def save_results(results):
    with open('results10.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, results[0].keys())
        writer.writeheader()
        writer.writerows(results)


## Wstępne zarażanie
def zasiewanko(seed_size_1, seed_size_2, all_nodes, g):
    axes = []
    w1 = 0

    while w1 < seed_size_1:
        ax = randrange(all_nodes)
        if ax not in axes:
            g.vs[ax]["infected_virus_1"] = 1
            g.vs[ax]["inf_by"] = 'seed'
            axes.append(ax)
            w1 += 1

    w1 = 0
    while w1 < seed_size_2:
        ax = randrange(all_nodes)
        if ax not in axes:
            g.vs[ax]["infected_virus_2"] = 1
            g.vs[ax]["inf_by"] = 'seed'
            axes.append(ax)
            w1 += 1


## Zarażanie
def zarazanko(attacked, spreader, step, g, spread_chance, virus):
    x_1 = round((random.uniform(0, 1)), 2)
    g.vs[spreader]["attacks"] += 1

    if g.vs[attacked]["infected_virus_2"] == 1:
        x_1 /= 1.5
    if x_1 <= spread_chance:
        if virus == "infected_virus_1":
            g.vs[attacked]["stepinfected_1"] = step
        else:
            g.vs[attacked]["stepinfected_2"] = step
        g.vs[attacked][virus] = 1
        g.vs[spreader]["inf_nei"] += 1
        g.vs[attacked]["inf_by"] = g.vs[spreader]["name"]
        # print("! ZARAZONO !", attacked)


## Inicjacja sieci
def init_network(g, reset=False):
    deg = []

    for i in range(0, Graph.vcount(g)):
        if reset == False:
            neighborstab = g.neighbors(i, mode="out")
            node = {'name': i, 'degree': len(neighborstab)}
            deg.append(node)
            g.vs[i]["name"] = i
            g.vs[i]["degree"] = len(neighborstab)

        g.vs[i]["stepinfected_1"] = 0
        g.vs[i]["stepinfected_2"] = 0
        g.vs[i]["infected_virus_1"] = 0
        g.vs[i]["infected_virus_2"] = 0

        g.vs[i]["step_att"] = 0
        g.vs[i]["attempts"] = 0
        g.vs[i]["inf_nei"] = 0
        g.vs[i]["inf_by"] = 0
        g.vs[i]["inf_dur"] = 0
        g.vs[i]["last_con_s"] = 0
        g.vs[i]["attacks"] = 0
        g.vs[i]['removed'] = 0


def simulation_loop(g, options, loop, results, set, debug=False, print_flag=False):
    zasiewanko(options['seed_pool_1'], options['seed_pool_2'], Graph.vcount(g), g)

    ## Zarażanie trwa póki istnieją zarażający
    isInfecting = True

    step = 0
    recovered = 0
    attacked = 0
    attacked_nodes = []
    removed = 0

    while isInfecting:
        infected = 0
        spreaders = []
        step += 1
        infected_1_step = 0
        infected_2_step = 0

        ## Ustalenie zarażających wirus 1
        for j in range(0, Graph.vcount(g)):
            if g.vs[j]["infected_virus_2"] == 1 and g.vs[j]["removed"] == 0:
                spreaders.append(j)
        # print(spreaders)
        random.shuffle(spreaders)
        ## Iterowanie zarażających
        for spreader in spreaders:
            ## Sprawdzanie sąsiedztwa zarażającego
            neighborstab = g.neighbors(spreader, mode="out")
            if len(neighborstab) > 0:
                notinfected = []

                for i in neighborstab:
                    if g.vs[i]['infected_virus_2'] != 1:
                        notinfected.append(i)

                ## Kontakt i próba zarażenia
                if notinfected:
                    for contacted in notinfected:
                        zarazanko(attacked=contacted,
                                  spreader=spreader,
                                  step=step,
                                  g=g,
                                  spread_chance=options['spread_chance_2'],
                                  virus="infected_virus_2")

        ## Ustalenie zarażających wirus 2
        spreaders = []
        for j in range(0, Graph.vcount(g)):
            if g.vs[j]["infected_virus_1"] == 1 and g.vs[j]["removed"] == 0:
                spreaders.append(j)
        # print(spreaders)
        random.shuffle(spreaders)
        ## Iterowanie zarażających
        for spreader in spreaders:
            ## Sprawdzanie sąsiedztwa zarażającego
            neighborstab = g.neighbors(spreader, mode="out")
            if len(neighborstab) > 0:
                notinfected = []

                for i in neighborstab:
                    if g.vs[i]['infected_virus_1'] != 1:
                        notinfected.append(i)

                ## Kontakt i próba zarażenia
                if notinfected:
                    for contacted in notinfected:
                        zarazanko(attacked=contacted,
                                  spreader=spreader,
                                  step=step,
                                  g=g,
                                  spread_chance=options['spread_chance_1'],
                                  virus="infected_virus_1")

        active_spreaders_1 = 0
        active_spreaders_2 = 0
        recovered_this_step = 0
        removed_this_step = 0

        for i in range(0, Graph.vcount(g)):
            if g.vs[i]['removed'] == 0:
                if g.vs[i]["infected_virus_1"] == 1 or g.vs[i]["infected_virus_2"] == 1:
                    infected += 1
                if g.vs[i]["stepinfected_1"] == step:
                    infected_1_step += 1
                if g.vs[i]["stepinfected_2"] == step:
                    infected_2_step += 1

                if g.vs[i]["stepinfected_1"] != step and g.vs[i]["infected_virus_1"] == 1:
                    active_spreaders_1 += 1

                if g.vs[i]["stepinfected_2"] != step and g.vs[i]["infected_virus_2"] == 1:
                    active_spreaders_2 += 1

                if g.vs[i]["infected_virus_1"] == 1:
                    if round((random.uniform(0, 1)), 2) <= options['remove_chance']:
                        g.vs[i]["removed"] = 1
                        active_spreaders_1 -= 1
                        if g.vs[i]["infected_virus_2"] == 1:
                            active_spreaders_2 -= 1
                        removed_this_step += 1
                        removed += 1

                if g.vs[i]["infected_virus_2"] == 1:
                    if round((random.uniform(0, 1)), 2)*4 <= options['remove_chance']:
                        g.vs[i]["removed"] = 1
                        active_spreaders_2 -= 1
                        if g.vs[i]["infected_virus_1"] == 1:
                            active_spreaders_1 -= 1
                        removed_this_step += 1
                        removed += 1

        if print_flag == True:
            print("All nodes:", Graph.vcount(g), "Active nodes:", Graph.vcount(g) - removed, "Edges:", Graph.ecount(g), "Step:", step,
                  "\nSpreading rate v1:", options['spread_chance_1'], "Spreading rate v2:", options['spread_chance_2'],
                  "Recovering rate:", options['recovery_chance'],
                  "\nSeed ratio v1:", options['seed_ratio_1'], "Seed ratio v2:", options['seed_ratio_2'],
                  "\nSeed count v1:", options['seed_pool_1'],"Seed count v2:", options['seed_pool_2'],
                  "\nActive spreaders v1:", active_spreaders_1, "Active spreaders v2:", active_spreaders_2,
                  "\nInfected this step v1:", infected_1_step,"Infected this step v2:", infected_2_step,
                  "\nTotal infected:", infected,
                  "\nTotal recovered:", recovered, "Recovered this step:", recovered_this_step,
                  '\nTotal removed:', removed, 'Removed this step:', removed_this_step)

        results.append({
            'data_set': set,
            'sample': loop,
            'nodes': Graph.vcount(g),
            'edges': Graph.ecount(g),
            'step': step,
            'spread_chance_1': options['spread_chance_1']*100,
            'spread_chance_2': options['spread_chance_2']*100,
            'recovery_rate': options['recovery_chance'],
            'remove_chance': options['remove_chance'],
            'seed_ratio_1': options['seed_ratio_1'],
            'seed_ratio_2': options['seed_ratio_2'],
            'seed_count_1': options['seed_pool_1'],
            'seed_count_2': options['seed_pool_2'],
            'active_spreader_1': active_spreaders_1,
            'active_spreader_2': active_spreaders_2,
            'total_infected': infected,
            'infected_1_step': infected_1_step,
            'infected_2_step': infected_2_step,
            'total_recovered': recovered,
            'recovered_step': recovered_this_step,
            'total_attacked_nodes': len(attacked_nodes),
            'total_removed': removed,
            'removed_step': removed_this_step
        })

        if debug == True:
            ask = input('continue?(Y/N)')
            if ask == "Y" or ask == "y":
                continue
            elif ask == "N" or ask == "n":
                break

        if step >= 50:
            # if Graph.vcount(g) - removed == 0 or step >= 500:
            isInfecting = False


def main():
    if os.path.exists('results10.csv'):
        os.remove('results10.csv')

    g = Graph.Read_Ncol('facebook_combined.txt', directed=False)
    init_network(g)

    ## Próg aktywacji / szansa zarażenia
    pp1_list = [0.01, 0.02]  # b prog aktywacjizarażenia
    pp2_list = [0.01, 0.02]  # b prog aktywacji

    ## Próg wyzdrowienia
    rec_list = [0.1]  # m rec

    ## Początkowy procent zarażonej populacji
    seed1_list = [1]  # n wezlow
    seed2_list = [1]  # n wezlow
    # pok = [0.1, 0.2, 0.3, 0.4]

    remove_list = [0.05]

    results = []
    set = 1
    for spread_chance_1 in pp1_list:
        for spread_chance_2 in pp2_list:
            for recovery_chance in rec_list:
                for seed_ratio_1 in seed1_list:
                    for seed_ratio_2 in seed2_list:
                        for remove_chance in remove_list:
                            seed_pool_1 = round((seed_ratio_1 / 100) * Graph.vcount(g))
                            seed_pool_2 = round((seed_ratio_2 / 100) * Graph.vcount(g))
                            loop = 1

                            while loop <= 10:
                                print('Set: ', set, 'Loop: ', loop)
                                options = {
                                    'spread_chance_1': spread_chance_1,
                                    'spread_chance_2': spread_chance_2,
                                    'recovery_chance': recovery_chance,
                                    'seed_ratio_1': seed_ratio_1,
                                    'seed_ratio_2': seed_ratio_2,
                                    'seed_pool_1': seed_pool_1,
                                    'seed_pool_2': seed_pool_2,
                                    'remove_chance': remove_chance
                                }
                                simulation_loop(g=g,
                                                options=options,
                                                loop=loop,
                                                results=results,
                                                set=set,
                                                debug=False,
                                                print_flag=False)
                                init_network(g, True)
                                loop += 1
                            set += 1

    save_results(results)


if __name__ == '__main__':
    main()
