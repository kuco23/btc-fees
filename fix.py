from json import load, dump

file = load(open('data_5000.0.json'))
for row in file:
    row['fee_10'] = int(row['fee_10'])
    row['fee_25'] = int(row['fee_25'])
    row['fee_50'] = int(row['fee_50'])
dump(file, open('data_5000.0.json', 'w'), indent=2)