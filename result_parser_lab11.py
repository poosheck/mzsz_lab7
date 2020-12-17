import csv
import matplotlib.pyplot as plt


def main():
    data_sets = [
        {
            'set': '1',
            'spread': None,
            'remove': None,
            'available': None,
            'loops': [{
                'loop': '1',
                'data': {
                    'removed': [],
                    'infected': [],
                    'healthy': [],
                    'step': []
                }
            }]
        }
    ]
    with open('results11.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['data_set'] != data_sets[-1]['set']:
                data_sets.append({
                    'set': row['data_set'],
                    'spread': row['spread_chance'],
                    'remove': row['remove_chance'],
                    'available': row['available_chance'],
                    'loops': [{
                        'loop': '1',
                        'data': {
                            'removed': [],
                            'infected': [],
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
                        'healthy': [],
                        'step': []
                    }
                })
            if data_sets[-1]['spread'] == None:
                data_sets[-1]['spread'] = row['spread_chance']
            if data_sets[-1]['remove'] == None:
                data_sets[-1]['remove'] = row['remove_chance']
            data_sets[-1]['loops'][-1]['data']['removed'].append(int(row['total_removed'])/int(row['nodes'])*100)
            data_sets[-1]['loops'][-1]['data']['infected'].append(int(row['total_infected'])/int(row['nodes'])*100)
            data_sets[-1]['loops'][-1]['data']['healthy'].append(int(row['healthy'])/int(row['nodes'])*100)
            data_sets[-1]['loops'][-1]['data']['step'].append(int(row['step']))

    for set in data_sets:
        plt.figure()
        i = 0
        for loop in set['loops']:
            if i == 0:
                plt.plot(loop['data']['step'], loop['data']['removed'], 'r', alpha=0.2, label="Removed nodes")
                plt.plot(loop['data']['step'], loop['data']['infected'], 'b', alpha=0.2, label="Infected nodes")
                plt.plot(loop['data']['step'], loop['data']['healthy'], 'g', alpha=0.2, label="Healthy nodes")
                i = 10
            else:
                plt.plot(loop['data']['step'], loop['data']['removed'], 'r', alpha=0.2)
                plt.plot(loop['data']['step'], loop['data']['infected'], 'b', alpha=0.2)
                plt.plot(loop['data']['step'], loop['data']['healthy'], 'g', alpha=0.2)
        plt.title('Spread chance: {}, Removing chance: {}, Available chance: {}'.format(set['spread'], set['remove'], set['available']))
        plt.xlabel('Simulation step')
        plt.ylabel('Percent of population')
        plt.legend(loc="center right")
    plt.show()

if __name__ == '__main__':
    main()
