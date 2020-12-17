import csv
import matplotlib.pyplot as plt


def main():
    data_sets = [
        {
            'set': '1',
            'spread_1': None,
            'spread_2': None,
            'seed_1': None,
            'seed_2': None,
            'remove': None,
            'loops': [{
                'loop': '1',
                'data': {
                    'removed': [],
                    'infected': [],
                    'infected_1': [],
                    'infected_2': [],
                    'healthy': [],
                    'step': []
                }
            }]
        }
    ]
    with open('results10.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['data_set'] != data_sets[-1]['set']:
                data_sets.append({
                    'set': row['data_set'],
                    'spread_1': row['spread_chance_1'],
                    'spread_2': row['spread_chance_2'],
                    'seed_1': row ['seed_ratio_1'],
                    'seed_2': row ['seed_ratio_2'],
                    'remove': row['remove_chance'],
                    'loops': [{
                        'loop': '1',
                        'data': {
                            'removed': [],
                            'infected': [],
                            'infected_1': [],
                            'infected_2': [],
                            'healthy': [],
                            'step': []
                        }
                    }]
                }
                )
            if row['sample'] != data_sets[-1]['loops'][-1]['loop']:
                data_sets[-1]['loops'].append({
                    'loop': row['sample'],
                    'data': {
                        'removed': [],
                        'infected': [],
                        'infected_1': [],
                        'infected_2': [],
                        'healthy': [],
                        'step': []
                    }
                })
            if data_sets[-1]['spread_1'] == None:
                data_sets[-1]['spread_1'] = row['spread_chance_1']
            if data_sets[-1]['spread_2'] == None:
                data_sets[-1]['spread_2'] = row['spread_chance_2']
            if data_sets[-1]['seed_1'] == None:
                data_sets[-1]['seed_1'] = row['seed_ratio_1']
            if data_sets[-1]['seed_2'] == None:
                data_sets[-1]['seed_2'] = row['seed_ratio_2']

            data_sets[-1]['loops'][-1]['data']['infected'].append(int(row['total_infected'])/int(row['nodes'])*100)
            data_sets[-1]['loops'][-1]['data']['infected_1'].append(int(row['active_spreader_1'])/int(row['nodes'])*100)
            data_sets[-1]['loops'][-1]['data']['infected_2'].append(int(row['active_spreader_2'])/int(row['nodes'])*100)
            data_sets[-1]['loops'][-1]['data']['removed'].append(int(row['total_removed'])/int(row['nodes'])*100)

            data_sets[-1]['loops'][-1]['data']['step'].append(int(row['step']))

    for set in data_sets:
        plt.figure()
        i = 0
        for loop in set['loops']:
            if i == 0:
                plt.plot(loop['data']['step'], loop['data']['infected_1'], 'b', alpha=0.2, label="Infected nodes v1")
                plt.plot(loop['data']['step'], loop['data']['infected_2'], 'g', alpha=0.2, label="Infected nodes v2")
                plt.plot(loop['data']['step'], loop['data']['removed'], 'r', alpha=0.2, label="Removed")
                i = 10
            else:
                plt.plot(loop['data']['step'], loop['data']['infected_1'], 'b', alpha=0.2)
                plt.plot(loop['data']['step'], loop['data']['infected_2'], 'g', alpha=0.2)
                plt.plot(loop['data']['step'], loop['data']['removed'], 'r', alpha=0.2)

        plt.title('Virus 1 spread: {}%, Virus 2 spread: {}%,Virus 1 Seed: {}%, Virus 2 Seed: {}%'.format(set['spread_1'], set['spread_2'], set['seed_1'], set['seed_2']))
        plt.xlabel('Simulation step')
        plt.ylabel('Percent of population')
        plt.legend(loc="center right")
    plt.show()

if __name__ == '__main__':
    main()
