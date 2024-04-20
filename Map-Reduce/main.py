import asyncio
import time

from data import Data
from map_reduce import MapReduce

sources = ['Ru24', 'Interfax', 'Tass']


async def reduce():
    tasks = [asyncio.create_task(map_reduce.reduce(node)) for node in map_reduce.nodes]
    return await asyncio.gather(*tasks)

if __name__ == '__main__':
    start = time.perf_counter()
    data = Data()
    db = data.load_dataframe('data/db.csv')
    db = db[['source', 'title']]
    db = db[db['title'].apply(lambda x: isinstance(x, str))]
    map_reduce = MapReduce(db, sources)
    map_reduce.map()
    nodes_lengths = map_reduce.shuffle()
    start_reduce = time.perf_counter()
    lengths = asyncio.run(reduce())
    end_reduce = time.perf_counter()
    print(f'Reduce operation completed in: {end_reduce - start_reduce:.3f}\n')
    output_data = []
    for i in range(len(sources)):
        output_data.append({'source': sources[i], 'average_title_length': lengths[i], 'total_titles': nodes_lengths[i]})
    output = data.create_dataframe(output_data)
    data.save_dataframe(output, 'outputs/output.csv')
    print(output, '\n')
    end = time.perf_counter()
    print(f'Total time: {end - start:.3f}')
