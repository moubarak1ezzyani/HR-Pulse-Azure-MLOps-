# Nettoyage NLP (Step 1)
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from tqdm import tqdm
from IPython.display import display 

# -> Initialize NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

def clean_text_pipeline(text): 
    
    if pd.isna(text) or not isinstance(text, str):
        return ""

    # --- Normalization & Noise Removal (Regex)

    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    
    # --- Tokenization
    tokens = word_tokenize(text)
    
    # --- Stop Words Removal
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words]
    
    # --- Lemmatization (Root finding)
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    
    return " ".join(tokens)

# -> Load Data
file_path="../data/raw/df_hr.csv"
df_init=pd.read_csv(file_path)
df_init.head(5)

# -> the Pipeline 
print("Running NLP Pipeline on Job Descriptions...")
tqdm.pandas() # to use .progress_apply() => progress bar
df_init['cleaned_description'] = df_init['Job Description'].progress_apply(clean_text_pipeline)

# -> Results
print("\n--- Processing Complete ---")
display(df_init[['Job Description', 'cleaned_description']].head(3))