import pandas as pd
import time
from chromadb import Client, Settings
from chromadb.utils import embedding_functions

def build_vectorstore_from_filtered(df):
    print(f"Building vectorstore from {len(df)} filtered meals.")

   
    client = Client(Settings(persist_directory="./chroma_db", anonymized_telemetry=False))

    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="mixedbread-ai/mxbai-embed-large-v1"
    )

    

    # Create or get collection
    collection = client.get_or_create_collection(
        name="meal_embeddings",
        embedding_function=embedding_func
    )

    # Clear old documents if re-running
    if collection.count() > 0:
        collection.delete(ids=collection.get()['ids'])

    # Add documents
    collection.add(
        documents=df['title'].tolist(),
        metadatas=df[['calories', 'protein']].to_dict('records'),
        ids=[str(i) for i in df.index]
    )

    return collection


# ------------------- Step 2: Compute precision and recall@k ------------------- #
def compute_precision_recall_at_k(collection, queries, ground_truth, k=10):
    results = collection.query(query_texts=queries, n_results=k)
    retrieved_ids_list = results['ids']

    precision_scores = []
    recall_scores = []

    for i, expected_ids in enumerate(ground_truth):
        returned_ids = set(retrieved_ids_list[i])
        expected_ids = set(expected_ids)
        true_positives = len(returned_ids & expected_ids)

        precision = true_positives / k
        recall = true_positives / len(expected_ids) if expected_ids else 0

        precision_scores.append(precision)
        recall_scores.append(recall)

    avg_precision = sum(precision_scores) / len(precision_scores)
    avg_recall = sum(recall_scores) / len(recall_scores)

    return avg_precision, avg_recall


def measure_latency(collection, query_text, n_results=10):
    start = time.perf_counter()
    _ = collection.query(query_texts=[query_text], n_results=n_results)
    end = time.perf_counter()
    latency_ms = (end - start) * 1000
    return latency_ms

if __name__ == "__main__":
    # Sample dataset
    df = pd.DataFrame({
        'title': ['Lentil, Apple, and Turkey Wrap ', 'Spinach Noodle Casserole ', 'Beef Tenderloin with Garlic and Brandy ', 'Aztec Chicken'],
        'calories': [426, 547, 174, 625],
        'protein': [30, 20,11, 39]
    })

    # Query-to-ground-truth ID mapping
    queries = ['chicken recipe', 'vegan protein dish']
    expected_relevant_ids = [['0'], ['1', '3']]  # Based on 'title' indexing

    # Step 1: Build vectorstore
    collection = build_vectorstore_from_filtered(df)

    # Step 2: Evaluate metrics
    precision, recall = compute_precision_recall_at_k(collection, queries, expected_relevant_ids, k=10)
    print(f"\n Precision@10: {precision:.2f}")
    print(f"🔁 Recall@10: {recall:.2f}")

    # Step 3: Latency
    print("\n Query Latency:")
    for q in queries:
        latency = measure_latency(collection, q)
        print(f" - '{q}': {latency:.2f} ms")
