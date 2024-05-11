from langchain_community.embeddings.gigachat import GigaChatEmbeddings

from params import params

model = GigaChatEmbeddings(
    credentials=params['creds'],
    scope=params['scope'],
    verify_ssl_certs=params['verify_ssl_certs'],
    model=params['model']
)
