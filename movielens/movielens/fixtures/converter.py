import csv

def read_main_csv(csv_file):
    with open('csv_file', 'r') as f:
        with open ('csv_file', 'w') as w:
            for row in reader:
                row.replace('::', '+')
    return


def read_csv(csv_file, json_file):
    read_main_csv(csv_file)
    with open('csv_file', 'r') as f:
        reader = csv.reader(f, delimiter='+')




def main():
    csv_file = ['movies.dat', 'ratings.dat', 'users.dat']
    json_file = ['movies.json', 'ratings.json', 'users.json']
    read_main_csv(movie.dat)
