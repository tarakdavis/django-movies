# CSV import
# this reads the .data file and the .user file
def read_the_whaky_file_bruh(uID):
    with open('ml-100k/u.data') as f: # automatically closes the file when done
        reader = csv.reader(f, delimiter = '\t')
        specific_user_total_ratings = []
        for row in reader:

    return



#------item file ------
with open('ml-100k/u.item', encoding='latin_1') as f: # automatically closes the file when done
    reader = csv.reader(f, delimiter = '\t')
