import os
import weaviate

client = weaviate.connect_to_wcs(
        cluster_url=os.getenv('WCS_URL'),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv('WCS_API_KEY')),
        headers={
            'creds': os.getenv('CREDS'),
            'scope': os.getenv('SCOPE'),
            'verify_ssl_certs': os.getenv('VERIFY_SSL_CERTS'),
            'model': os.getenv('MODEL')
        }
    )
