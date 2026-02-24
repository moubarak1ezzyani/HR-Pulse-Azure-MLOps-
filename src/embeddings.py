# HF & ChromaDB (Step 2)
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from tqdm import tqdm


def create_vector_db(csv_path, db_path="../models/chroma_db"):

    print(f"Loading cleaned data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Drop rows where the cleaned description might be empty
    df = df.dropna(subset=['cleaned_description'])
    
    print("Initializing ChromaDB Client...")
    # This creates a persistent local database in the folder "./chroma_db"
    chroma_client = chromadb.PersistentClient(path=db_path)
    
    # We use the default HuggingFace model for embeddings
    sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()
    
    # Create or load the collection
    collection_name = "hr_jobs_collection"
    collection = chroma_client.get_or_create_collection(
        name=collection_name, 
        embedding_function=sentence_transformer_ef
    )
    
    print("Generating embeddings and inserting into ChromaDB...")
    
    # Prepare data for ChromaDB (Requires lists of strings)
    # We use the DataFrame index as the ID for simplicity
    documents = df['cleaned_description'].tolist()
    metadatas = [{"job_title": str(title)} for title in df['Job Title'].tolist()]
    ids = [str(i) for i in df.index.tolist()]
    
    # ChromaDB can handle batches, but for huge datasets, it's better to chunk.
    # For this dataset, we can usually insert directly:
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ Successfully embedded {collection.count()} jobs into ChromaDB!")

if __name__ == "__main__":
    INPUT_FILE = "../data/raw/df_hr_cleaned.csv" 
    create_vector_db(INPUT_FILE)