# HF & ChromaDB (Step 2)
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from tqdm import tqdm


def create_vector_db(csv_path, db_path="../models/chroma_db"):

    print(f"Loading cleaned data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # cleaned description : Drop empty rows 
    df = df.dropna(subset=['cleaned_description'])
    
    print("Initializing ChromaDB Client...")
    
    # local chroma db 
    chroma_client = chromadb.PersistentClient(path=db_path)
    
    # embeddings : default HuggingFace model  
    sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()
    
    # Create / load the collection
    collection_name = "hr_jobs_collection"
    collection = chroma_client.get_or_create_collection(
        name=collection_name, 
        embedding_function=sentence_transformer_ef
    )
    
    print("Generating embeddings and inserting into ChromaDB...")
    
    # ChromaDB : Prepare data (Requires lists of strings)
    # for simplicity : index -> ID  
    documents = df['cleaned_description'].tolist()
    metadatas = [{"job_title": str(title)} for title in df['Job Title'].tolist()]
    ids = [str(i) for i in df.index.tolist()]
    
    # batches/chunks : huge datasets -> chunk (possible with chroma db)
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ Successfully embedded {collection.count()} jobs into ChromaDB!")

if __name__ == "__main__":
    INPUT_FILE = "../data/raw/df_hr_cleaned.csv" 
    create_vector_db(INPUT_FILE)