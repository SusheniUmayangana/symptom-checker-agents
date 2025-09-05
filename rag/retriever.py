from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def build_vector_db(chunks):
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("data/embeddings/")
    return db