from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

EMBEDDINGS_MODEL='all-MiniLM-L6-v2'

embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_MODEL,
        model_kwargs={'device': 'cuda'},  # Use 'cuda' if GPU available
        encode_kwargs={'normalize_embeddings': True}
    )

document = [
    'im am Muzafar',
    'He likes cricket',
    'who are you? tell me '

]
query = 'what is my name ?'

doc_emb = embeddings.embed_documents(document)
query_emb = embeddings.embed_documents(query)

scores = cosine_similarity(query_emb,doc_emb)[0]

print(scores)
index= np.argmax(np.array(scores))
print(document[index])
print('Similarity scores is: ', scores[index])


