import csv


def read_csv(csv_file, json_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter='+')
        for row in reader:
            with open(json_file, 'a') as json:
                json.write('[\n')
            with open(json_file, 'a') as json:
                read_json(row, json_file)
            with open(json_file, 'a') as json:
                json.write(',\n]')


def read_json(row, json_file):
        if 'json_file' == 'movies.json':
            d = {
                'model': 'movieratings.movies',
                'pk': int(row[0]),
                'fields': {
                    'title': row[1],
                    'genre': row[2]
                }

            }
        elif 'json_file' == 'ratings.json':
            d = {
                'model': 'movieratings.ratings',
                'pk': None,
                'fields': {
                    'rater': int(row[0]),
                    'movie': int(row[1]),
                    'rating': int(row[2])
                }
            }
        elif 'json_file' == 'users.json':
            d = {
                'models': 'movieratings.users',
                'pk': int(row[0]),
                'fields': {
                    'gender': row[1],
                    'age': int(row[2]),
                    'occupation': int(row[3])
                }
            }

def main():
    csv_file = ['ml-1m/movies.dat', 'ml-1m/ratings.dat', 'ml-1m/users.dat']
    json_file = ['movies.json', 'ratings.json', 'users.json']
    for x in range(0, len(csv_file)+1):
        read_csv(csv_file[x], json_file[x])

if __name__ == '__main__':
    main()
