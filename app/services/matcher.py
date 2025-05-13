import os
import pandas as pd
from mistralai import Mistral
from sklearn.metrics.pairwise import cosine_similarity

def get_contacts_by_location(query, csv_path="data.csv", threshold=0.9):
    df = pd.read_csv(csv_path)
    df['LOCATION'] = df['LOCATION'].astype(str).str.lower().str.strip()
    locations = df['LOCATION'].tolist()
    all_texts = [query.lower().strip()] + locations

    api_key = os.environ.get("MISTRAL_API_KEY")

    # Mistral Embedding
    client = Mistral(api_key=api_key)
    response = client.embeddings.create(model="mistral-embed", inputs=all_texts)
    embeddings = [item.embedding for item in response.data]

    query_embedding = embeddings[0]
    location_embeddings = embeddings[1:]
    similarities = cosine_similarity([query_embedding], location_embeddings)[0]

    matches = []
    for i, sim in enumerate(similarities):
        location_text = df.iloc[i]["LOCATION"]
        name = df.iloc[i].get("NAME") or df.iloc[i].get("Name")
        email = df.iloc[i].get("EMAIL") or df.iloc[i].get("Email")

        # Match by similarity OR keyword match in location
        if (sim >= threshold or query.lower() in location_text) and email:
            matches.append({
                "name": name,
                "email": email,
                "similarity": round(float(sim), 4),
                "location": location_text
            })

    return matches
