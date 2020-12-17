from igraph import *
import random
import os
import csv
from random import randrange

# import matplotlib.pyplot as plt

def save_results(results):
    with open('results9.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, results[0].keys())
        writer.writeheader()
        writer.writerows(results)

## Wstępne zarażanie
def zasiewanko(seed_size, all_nodes, g):
    axes = []
    w1 = 0

    while w1 < seed_size:
        ax = randrange(all_nodes)
        if ax not in axes:
            g.vs[ax]["infected"] = 1
            g.vs[ax]["immunity"] = 1
            g.vs[ax]["inf_by"] = 'seed'
            axes.append(ax)
            w1 += 1

## Zarażanie / kontakt
def zarazanko(attacked, spreader, step, g, spread_chance):
    if g.vs[attacked]['available'] == 0:
        return
    x_1 = round((random.uniform(0, 1)), 2)
    g.vs[spreader]["attacks"] += 1

    if x_1 <= spread_chance:
        g.vs[attacked]["stepinfected"] = step
        g.vs[attacked]["infected"] = 1
        g.vs[attacked]["immunity"] = 1
        g.vs[spreader]["inf_nei"] += 1
        g.vs[attacked]["inf_by"] = g.vs[spreader]["name"]
        # print("! ZARAZONO !", attacked)

    elif x_1 > spread_chance:
        g.vs[attacked]["step_att"] += 1
        g.vs[attacked]["attempts"] += 1
        g.vs[attacked]["last_con_s"] = step
        # print("kontakt :", g.vs[attacked]["name"])

## Inicjacja sieci
def init_network(g, reset = False):
    deg = []

    for i in range(0, Graph.vcount(g)):
        if reset == False:
            neighborstab = g.neighbors(i, mode="out")
            node = {'name': i, 'degree': len(neighborstab)}
            deg.append(node)
            g.vs[i]["name"] = i
            g.vs[i]["degree"] = len(neighborstab)

        g.vs[i]["stepinfected"] = 0
        g.vs[i]["infected"] = 0
        g.vs[i]["immunity"] = 0
        g.vs[i]["step_att"] = 0
        g.vs[i]["attempts"] = 0
        g.vs[i]["inf_nei"] = 0
        g.vs[i]["inf_by"] = 0
        g.vs[i]["inf_dur"] = 0
        g.vs[i]["last_con_s"] = 0
        g.vs[i]["attacks"] = 0
        g.vs[i]['removed'] = 0
        g.vs[i]['available'] = 1

def simulation_loop(g, options, loop, results, set, debug = False, print_flag = False):
                    zasiewanko(options['seed_pool'], Graph.vcount(g), g)

                    ## Zarażanie trwa póki istnieją zarażający
                    isInfecting = True

                    step = 0
                    recovered = 0
                    attacked = 0
                    attacked_nodes = []
                    infected = 0
                    removed = 0

                    while isInfecting:
                        spreaders = []
                        step += 1
                        infected_step = 0
                        ## Ustalenie zarażających
                        for j in range(0, Graph.vcount(g)):
                            g.vs[j]["available"] = 1
                            if g.vs[j]["infected"] == 1:
                                spreaders.append(j)
                            if round((random.uniform(0, 1)), 2) <= options['available_chance']:
                                g.vs[j]["available"] = 0

                        # print(spreaders)
                        random.shuffle(spreaders)

                        ## Iterowanie zarażających
                        for spreader in spreaders:
                            if g.vs[spreader]['available'] == 0:
                                continue

                            ## Sprawdzanie sąsiedztwa zarażającego
                            neighborstab = g.neighbors(spreader, mode="out")
                            if len(neighborstab) > 0:
                                notinfected = []

                                for i in neighborstab:
                                    ## Sprawdzanie czy sąsiedzi są odporni
                                    if g.vs[i]["immunity"] == 0:
                                        notinfected.append(i)

                                ## Kontakt i próba zarażenia
                                if notinfected:
                                    for contacted in notinfected:
                                        zarazanko(contacted, spreader, step, g, options['spread_chance'])

                        active_spreaders = 0
                        recovered_this_step = 0
                        attacks_this_step = 0
                        attacked_nodes_this_step = 0
                        removed_this_step = 0

                        for i in range(0, Graph.vcount(g)):
                            if g.vs[i]['removed'] == 0:
                                attacked += g.vs[i]["step_att"]
                                attacks_this_step += g.vs[i]["step_att"]
                                g.vs[i]["step_att"] = 0

                                if g.vs[i]["last_con_s"] == step:

                                    attacked_nodes_this_step += 1

                                    if g.vs[i]["name"] not in attacked_nodes:
                                        attacked_nodes.append(g.vs[i]["name"])

                                if g.vs[i]["stepinfected"] == step:
                                    infected_step += 1
                                    infected += 1

                                if g.vs[i]["stepinfected"] != step and g.vs[i]["infected"] == 1:
                                    active_spreaders += 1

                                if g.vs[i]["infected"] == 1:
                                    g.vs[i]["inf_dur"] = step - g.vs[i]["stepinfected"]

                                if g.vs[i]["infected"] == 1:
                                    if round((random.uniform(0, 1)), 2) <= options['remove_chance']:
                                        g.vs[i]["removed"] = 1
                                        active_spreaders -= 1
                                        removed_this_step += 1
                                        removed += 1
                        if print_flag:
                            print("All nodes:", Graph.vcount(g), "Active nodes:", Graph.vcount(g) - removed, "Edges:", Graph.ecount(g), "Step:", step,
                                  "\nSpreading rate:", options['spread_chance'], "Recovering rate:", options['recovery_chance'],
                                  "Seed ratio:", options['seed_ratio'], "Seed count:", options['seed_pool'],
                                  "\nActive spreaders:", active_spreaders, "Total infected:", infected,
                                  "Infected this step:", infected_step,
                                  "\nTotal recovered:", recovered, "Recovered this step:", recovered_this_step,
                                  '\nTotal attacks:', attacked, 'Attacks this step :', attacks_this_step,
                                  'Total attacked nodes:', len(attacked_nodes), 'Nodes attacked this step:',
                                  attacked_nodes_this_step,
                                  '\nTotal removed:', removed, 'Removed this step:', removed_this_step,
                                   'Healthy:', Graph.vcount(g) - removed - active_spreaders)

                        results.append({
                            'data_set': set,
                            'sample': loop,
                            'nodes': Graph.vcount(g),
                            'edges': Graph.ecount(g),
                            'step': step,
                            'spread_chance': options['spread_chance'],
                            'recovery_rate': options['recovery_chance'],
                            'remove_chance': options['remove_chance'],
                            'seed_ratio': options['seed_ratio'],
                            'seed_count': options['seed_pool'],
                            'active_spreader': active_spreaders,
                            'total_infected': infected,
                            'infected_step': infected_step,
                            'total_recovered': recovered,
                            'recovered_step': recovered_this_step,
                            'total_attacks': attacked,
                            'attacks_step': attacks_this_step,
                            'total_attacked_nodes': len(attacked_nodes),
                            'attacked_notes_step': attacked_nodes_this_step,
                            'total_removed': removed,
                            'removed_step': removed_this_step,
                            'healthy': Graph.vcount(g) - removed - active_spreaders,
                            'available_chance': options['available_chance']
                        })

                        if debug == True:
                            ask = input('continue?(Y/N)')
                            if ask == "Y" or ask == "y":
                                continue
                            elif ask == "N" or ask == "n":
                                break

                        #if Graph.vcount(g) - removed == 0 or step >= 200:
                        if step >= 200:
                            isInfecting = False

def main():

    if os.path.exists('results9.csv'):
        os.remove('results9.csv')


    g = Graph.Read_Ncol('facebook_combined.txt', directed=False)
    init_network(g)

    ## Próg aktywacji / szansa zarażenia
    pp_list = [0.05]  # b prog aktywacji

    ## Próg wyzdrowienia
    rec_list = [0.1]  # m rec

    ## Początkowy procent zarażonej populacji
    seed_list = [1]  # n wezlow
    # pok = [0.1, 0.2, 0.3, 0.4]

    remove_list = [0.05]
    available_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.9]

    results = []
    set = 1
    for spread_chance in pp_list:
        for recovery_chance in rec_list:
            for seed_ratio in seed_list:
                for remove_chance in remove_list:
                    for available_chance in available_list:
                        seed_pool = round((seed_ratio / 100) * Graph.vcount(g))
                        loop = 1

                        while loop <= 10:
                            print('Set: ', set, 'Loop: ', loop)
                            options = {
                                'spread_chance': spread_chance,
                                'recovery_chance': recovery_chance,
                                'seed_ratio': seed_ratio,
                                'seed_pool': seed_pool,
                                'remove_chance': remove_chance,
                                'available_chance': available_chance
                            }
                            simulation_loop(g = g,
                                            options = options,
                                            loop = loop,
                                            results = results,
                                            set = set,
                                            debug=False)
                            init_network(g, True)
                            loop += 1
                        set += 1

    save_results(results)


if __name__ == '__main__':
    main()