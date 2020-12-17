import csv
import matplotlib.pyplot as plt


def main():
    data_sets = [
        {
            'set': '1',
            'influence': None,
            'seed': None,
            'loops': [{
                'loop': '1',
                'data': {
                    'infected': [],
                    'step': []
                }
            }]
        }
    ]
    with open('results7.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['data_set'] != data_sets[-1]['set']:
                data_sets.append({
                    'set': row['data_set'],
                    'influence': row['influence'],
                    'seed': row['seed_ratio'],
                    'loops': [{
                        'loop': '1',
                        'data': {
                            'infected': [],
                            'step': []
                        }
                    }]
                }
                )
            if row['sample'] != data_sets[-1]['loops'][-1]['loop']:
                data_sets[-1]['loops'].append({
                    'loop': row['sample'],
                    'data': {
                        'infected': [],
                        'step': []
                    }
                })
            if data_sets[-1]['seed'] == None:
                data_sets[-1]['seed'] = row['seed_ratio']
            if data_sets[-1]['influence'] == None:
                data_sets[-1]['influence'] = row['influence']
            data_sets[-1]['loops'][-1]['data']['infected'].append(int(row['total_infected'])/int(row['nodes'])*100)
            data_sets[-1]['loops'][-1]['data']['step'].append(int(row['step']))

    for set in data_sets:
        plt.figure()
        i = 0
        for loop in set['loops']:
            if i == 0:
                plt.plot(loop['data']['step'], loop['data']['infected'], 'b', alpha=0.2, label="Infected nodes")
                i = 10
            else:
                plt.plot(loop['data']['step'], loop['data']['infected'], 'b', alpha=0.2)
        plt.title('Seed size: {}%, Social Influence: {}%'.format(set['seed'], (float(set['influence'])*100)))
        plt.xlabel('Simulation step')
        plt.ylabel('Percent of population')
        plt.legend(loc="center right")
    plt.show()

if __name__ == '__main__':
    main()
