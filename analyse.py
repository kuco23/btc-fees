from json import load
from datetime import datetime

blocks = load(open('data_5000.0.json'))
blocks.sort(key = lambda x: int(x['block']))

def get_data(lot_size, redemption_fee, perc=90):
    max_fee = lot_size * redemption_fee

    data = []

    interval = []
    last_block = None
    for block in blocks:
        if block[f'fee_{perc}'] <= max_fee: continue
        if last_block is None or block['block'] > last_block['block'] + 1:
            if last_block is not None:
                start = interval[0]['timestamp']
                end = interval[-1]['timestamp']
                minutes = int((end - start) / 60)
                if minutes > 0:
                    start_date = datetime.fromtimestamp(start)
                    data.append({
                        'start_time': start_date,
                        'duration_minutes': minutes,
                        'start_block': interval[0]['block'],
                        'n_blocks': len(interval),
                    })
            interval.clear()
        interval.append(block)
        last_block = block

    return data