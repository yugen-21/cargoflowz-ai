import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def get_contacts_by_location(query, csv_path="data.csv", threshold=0.7):
    df = pd.read_csv(csv_path)
    df['LOCATION'] = df['LOCATION'].astype(str).str.lower().str.strip()

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Encode all locations
    location_embeddings = model.encode(df['LOCATION'].tolist())

    # Encode query
    query_embedding = model.encode([query.lower().strip()])

    # Compute cosine similarity
    similarities = cosine_similarity(query_embedding, location_embeddings)[0]

    # Filter matches
    matches = []
    for i, sim in enumerate(similarities):
        if sim >= threshold:
            name = df.iloc[i].get("NAME") or df.iloc[i].get("Name")
            email = df.iloc[i].get("EMAIL") or df.iloc[i].get("Email")
            if email:
                matches.append({"name": name, "email": email})

    return matches
