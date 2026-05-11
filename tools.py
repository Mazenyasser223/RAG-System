from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")

vector_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

retriever = vector_db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 5, 
        "score_threshold": 0.5
    }
)

def retrieve_documents(query: str):
    docs = retriever.invoke(query)
    return docs