from model import model
from data import Data

import weaviate.classes as wvc
from weaviate.classes.config import Configure, Property, DataType, VectorDistances
from weaviate_client import client


def connect_to_weaviate():
    news_collection = None
    try:
        if client.collections.exists('News'):
            news_collection = client.collections.get('News')
            print('Weaviate collection exists')
        else:
            print('Weaviate collection does not exist, creating...')
            news_collection = client.collections.create(
                name='News',
                vector_index_config=Configure.VectorIndex.hnsw(distance_metric=VectorDistances.COSINE),
                vectorizer_config=None,
                properties=[
                    Property(
                        name='doc_id',
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                        vectorize_property_name=False
                    ),
                    Property(
                        name='source',
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                        vectorize_property_name=False
                    ),
                    Property(
                        name='url',
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                        vectorize_property_name=False
                    ),
                    Property(
                        name='title',
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                        vectorize_property_name=False
                    ),
                    Property(
                        name='content',
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                        vectorize_property_name=False
                    ),
                    Property(
                        name='created_at',
                        data_type=DataType.TEXT,
                        skip_vectorization=True,
                        vectorize_property_name=False
                    )
                ],
                generative_config=None
            )
    except Exception as e:
        print('Failed to connect to Weaviate\n', e)
    finally:
        return news_collection


def load_obj_to_weaviate(collection, properties):
    vector = __get_embeddings_for_doc(properties)
    with collection.batch.dynamic() as batch:
        batch.add_object(properties=properties, vector=vector)


def __get_embeddings_for_doc(properties):
    len_limits = [None, 2048, 1792, 1536, 1280, 1024, 768]
    success = False
    tries = 0
    embeddings = None
    while not success:
        try:
            embeddings = model.embed_documents([
                (properties['title'] + '. ' + properties['content'])[:len_limits[tries]]
            ])[0]
            success = True
        except Exception as e:
            tries += 1
            if tries == 7:
                print('Failed getting embeddings\n', e)
                break
    return embeddings


def __get_embeddings_for_query(query_input):
    return model.embed_documents([query_input])[0]


def vector_query(collection, query_input):
    query_response = collection.query.near_vector(
        near_vector=__get_embeddings_for_query(query_input),
        distance=0.2,
        return_metadata=wvc.query.MetadataQuery(distance=True)
    )
    return query_response.objects


def main():
    if client.is_ready():
        print('Weaviate client is ready')
    else:
        print('Weaviate client is not ready')
        return
    weaviate_collection = connect_to_weaviate()
    try:
        items = []
        for item in weaviate_collection.iterator():
            items.append(item)
        if not items:
            data = Data()
            print('The collection is empty, adding objects...')
            news_dicts = data.get_dict_list(data.load_dataframe('news/db_1000.csv'))
            for i, news_dict in enumerate(news_dicts):
                print(i + 1, '\tAdding object')
                load_obj_to_weaviate(weaviate_collection, news_dict)
        while True:
            query = input('\nEnter query: ')
            if query == 'exit':
                client.close()
                return
            similar_objects = vector_query(weaviate_collection, query)
            print(f'There are {len(similar_objects)} similar objects found:\n')
            for i, obj in enumerate(similar_objects):
                print(f'--- {i + 1} ---', obj, '\n')
    except Exception as e:
        print('Something went wrong\n', e)
        client.close()


if __name__ == '__main__':
    main()
