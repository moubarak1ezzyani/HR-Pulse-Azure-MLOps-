import time
import os
import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from tqdm import tqdm
from config import ENDPOINT,KEY, DATA_PATH, EXTRACT_PATH_OUPUT



def authenticate_client():
    return TextAnalyticsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))


def run_ner_extraction(data_path, output_path, limit=100):
    client = authenticate_client()
    df = pd.read_csv(data_path)

    # Process only the requested limit
    df_subset = df.head(limit).copy()

    all_skills = []

    print(f"Extracting skills for {limit} jobs using Azure NER...")

    # Process 1 by 1 to avoid batch limits
    for i, row in tqdm(df_subset.iterrows(), total=len(df_subset)):
        description = str(row["Job Description"])[:1000]  # 1000 chars
        try:
            response = client.recognize_entities([description])
            doc = response[0]
            if not doc.is_error:
                # relevant skills are in 'Skill' or 'Product' categories
                skills = [
                    entity.text
                    for entity in doc.entities
                    if entity.category in ["Skill", "Product"]
                ]
                all_skills.append(", ".join(list(set(skills))))
            else:
                all_skills.append("")
        except Exception as e:
            print(f"\nError at row {i}: {e}")
            all_skills.append("")

        # Free tier pause
        time.sleep(1.0)

    df_subset["extracted_skills"] = all_skills
    df_subset.to_csv(output_path, index=False)
    print(f"\nExtraction complete. Saved {len(df_subset)} records to {output_path}")


if __name__ == "__main__":
    run_ner_extraction(DATA_PATH, EXTRACT_PATH_OUPUT, limit=100)