import os
import weaviate

client = weaviate.connect_to_wcs(
    cluster_url=os.getenv('WCS_URL'),
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv('WCS_API_KEY')),
    headers={
        'creds': os.environ['CREDS'],
        'scope': os.environ['SCOPE'],
        'verify_ssl_certs': os.environ['VERIFY_SSL_CERTS'],
        'model': os.environ['MODEL']
    }
)
