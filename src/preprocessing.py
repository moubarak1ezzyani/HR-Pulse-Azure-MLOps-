# Nettoyage NLP (Step 1)
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from tqdm import tqdm
from IPython.display import display 

# -> 1. Initialize NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# -> 2. Load Data
file_path = "../data/raw/df_hr.csv"
df = pd.read_csv(file_path)

print("🚀 Starting Global Data Cleaning Pipeline...\n")

# ==========================================
# PHASE 1 : TABULAR DATA CLEANING (Salary, Size, Revenue)
# ==========================================
print("Step 1: Cleaning tabular columns (Salary, Size, Revenue)...")

# --- A. Nettoyage du Salaire (Ton script intégré) ---
def calculate_avg_salary(sal_string):
    try:
        if '-' in str(sal_string):
            min_sal = float(sal_string.split('-')[0])
            max_sal = float(sal_string.split('-')[1])
            return (min_sal + max_sal) / 2
        else:
            return float(sal_string)
    except ValueError:
        return None

# Extraire la partie avant '(   ' et enlever '$' et 'K'
salary_cleaned = df['Salary Estimate'].apply(lambda x: str(x).split('(')[0].strip())
salary_cleaned = salary_cleaned.str.replace('$', '', regex=False).str.replace('K', '', regex=False)
# Optionnel : nettoyer "Employer Provided Salary:" si présent
salary_cleaned = salary_cleaned.str.replace('Employer Provided Salary:', '', regex=False).str.strip()

df['Avg_Sal_K'] = salary_cleaned.apply(calculate_avg_salary)

# --- B. Nettoyage de Size et Revenue ---
def clean_size(text):
    text = str(text)
    if pd.isna(text) or "Unknown" in text or text == "-1":
        return 0
    numbers = re.findall(r'\d+', text)
    if len(numbers) == 2:
        return (int(numbers[0]) + int(numbers[1])) / 2
    elif len(numbers) == 1:
        return int(numbers[0])
    return 0

def clean_revenue(text):
    text = str(text).lower()
    if "unknown" in text or "non-applicable" in text or text == "-1":
        return 0
    numbers = re.findall(r'\d+', text)
    if not numbers:
        return 0
    numbers = [float(n) for n in numbers]
    avg = sum(numbers) / len(numbers)
    if "billion" in text:
        avg = avg * 1000 # Convert billions to millions
    return avg

df['Size_Avg'] = df['Size'].apply(clean_size)
df['Revenue_Avg_Millions'] = df['Revenue'].apply(clean_revenue)

# Suppression des colonnes brutes
df = df.drop(columns=['Salary Estimate', 'Size', 'Revenue'])


# ==========================================
# PHASE 2 : NLP PIPELINE (Job Descriptions)
# ==========================================
print("\nStep 2: Starting NLP Pipeline on Job Descriptions...")

tqdm.pandas(desc="NLP Processing")
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

print("   -> A. Lowercasing and removing noise...")
df['cleaned_description'] = (df['Job Description']
                             .astype(str)
                             .str.lower()
                             .replace(r'[^a-z\s]', '', regex=True))

print("   -> B. Tokenizing text...")
df['cleaned_description'] = df['cleaned_description'].progress_apply(
    lambda text: word_tokenize(str(text))
)

print("   -> C. Removing stop words & lemmatizing...")
df['cleaned_description'] = df['cleaned_description'].progress_apply(
    lambda token_list: " ".join([lemmatizer.lemmatize(w) for w in token_list if w not in stop_words])
)

# ==========================================
# PHASE 3 : RESULTS & EXPORT
# ==========================================
print("\n--- Processing Complete ---")
# Affichage de contrôle
display(df[['Company Name', 'Avg_Sal_K', 'Size_Avg', 'Revenue_Avg_Millions', 'cleaned_description']].head(3))

# Sauvegarde finale
clean_file_path = "../data/raw/df_hr_cleaned.csv"
df.to_csv(clean_file_path, index=False)
print(f"\n✅ Cleaned data saved successfully to: {clean_file_path}")
# import pandas as pd
# import re
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from nltk.tokenize import word_tokenize
# from tqdm import tqdm
# from IPython.display import display 

# # -> Initialize NLTK resources
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)
# nltk.download('wordnet', quiet=True)
# nltk.download('omw-1.4', quiet=True)

# def clean_text_pipeline(text): 
    
#     if pd.isna(text) or not isinstance(text, str):
#         return ""

#     # --- Normalization & Noise Removal (Regex)

#     text = text.lower()
#     text = re.sub(r'[^a-z\s]', '', text)
    
#     # --- Tokenization
#     tokens = word_tokenize(text)
    
#     # --- Stop Words Removal
#     stop_words = set(stopwords.words('english'))
#     tokens = [w for w in tokens if w not in stop_words]
    
#     # --- Lemmatization (Root finding)
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(w) for w in tokens]
    
#     return " ".join(tokens)

# # -> Load Data
# file_path="../data/raw/df_hr.csv"
# df_init=pd.read_csv(file_path)
# df_init.head(5)

# # -> the Pipeline 
# print("Running NLP Pipeline on Job Descriptions...")
# tqdm.pandas() # to use .progress_apply() => progress bar
# df_init['cleaned_description'] = df_init['Job Description'].progress_apply(clean_text_pipeline)

# # -> Results
# print("\n--- Processing Complete ---")
# display(df_init[['Job Description', 'cleaned_description']].head(3))