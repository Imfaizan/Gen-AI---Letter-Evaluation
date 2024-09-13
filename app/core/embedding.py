from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.settings import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def ingest_policy_documents(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Create embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    final_documents = text_splitter.split_documents(docs)
    
    # Save to ChromaDB
    db = Chroma.from_documents(final_documents, embeddings, persist_directory=settings.CHROMA_DB_DIR)
    db.persist()
