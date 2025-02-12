from os import listdir
from json import dump
from csv import DictReader


# store 10th, 25th and 50th percentiles largest block fees,
# when 50th percentile is larger than one_lot_max_fee, store the block
percentiles = [10, 25, 50]

# set to minimum fee and see troublesome times
lot_size = 1e6
redemption_fee = 0.005

# bytes in our one lot redemption transaction (the critical one)
one_lot_tx_bytes = 240

# max fee the agent can py for one lot redemption
one_lot_max_fee = lot_size * redemption_fee


def to_one_lot_tx_fee(fee, vsize):
    return int(one_lot_tx_bytes * fee / vsize)

def file_name_iterator():
    for dir_name in listdir('data'):
        for file_name in listdir('data/' + dir_name):
            yield f'data/{dir_name}/{file_name}'

data = []
file_names = file_name_iterator()
for file_name in file_names:

    fees = []
    with open(file_name) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            if row['fee'] == '0':
                continue
            fee = int(row['fee'])
            vsize = int(row['vsize'])
            fee_per_byte = to_one_lot_tx_fee(fee, vsize)
            fees.append(fee_per_byte)
    if len(fees) == 0: continue
    fees.sort()

    obj = {f'fee_{fee_p}': fees[len(fees) * fee_p // 100] for fee_p in percentiles}
    if (max(obj.values()) > one_lot_max_fee):
        data.append({
            **obj,
            'file': file_name,
            'block': int(row['block_num']),
            'timestamp': int(row['median_time'])
        })

dump(data, open(f'data_{one_lot_max_fee}.json', 'w'), indent=2)
