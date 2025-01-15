import openai
import numpy as np
from sentence_transformers import SentenceTransformer


# Configure Azure OpenAI
def get_embedding(sentence):
    # Load a pre-trained Sentence Transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate embeddings (this is a 2D array)
    embeddings = model.encode(sentence)

    # Flatten the embeddings to 1D
    embeddings = embeddings.flatten()  # or embeddings = embeddings[0] if it's a (1, 384) array
    return embeddings


def compute_similarity_score(input_text, compare_texts, metric="cosine"):
    """
    Computes similarity scores between the input text and each of the comparison texts.
    Returns a dictionary with scores for each text.
    """
    input_embedding = get_embedding(input_text)

    scores = {}
    for i, text in enumerate(compare_texts):
        compare_embedding = get_embedding(text)

        if metric == "euclidean":
            score = np.linalg.norm(input_embedding - compare_embedding)  # L2 Distance
        elif metric == "manhattan":
            score = np.sum(np.abs(input_embedding - compare_embedding))  # L1 Distance
        elif metric == "cosine":
            # Compute cosine similarity
            score = np.dot(input_embedding, compare_embedding) / (
                        np.linalg.norm(input_embedding) * np.linalg.norm(compare_embedding))  # Cosine Similarity
            score = round(score, 4)  # Normalize score to 4 decimal places

        scores[f"Match with String {i + 1}"] = score

    return scores




# # Example usage
# input_text = ["Artificial intelligence is revolutionizing industries."]
# compare_texts = [
#     "AI is transforming the business world.",
#     "Machine learning and AI are shaping the future.",
#     "Deep learning improves AI capabilities significantly."#
#]
# input_text = ["Bhibhas Singh, luknow, F:Akhilesh Kumar Singh"]
# compare_texts = [["Vibhas Kumar Singh, Lucknow F: Akhilesh Singh"],
#  ["Bibhas  Singh, Lucknow, F: Akhilesh Singh Yadav"],
# ["Vibhas Singh F: Akhilesh Kumar Lucknow"]]
# Compute similarity scores
# scores = compute_similarity_score(input_text, compare_texts, metric="cosine")
#
# # Print results
# for match, score in scores.items():
#     print(f"{match}: {score}")

# input_text = ["Bhashini Singh, RaiBareilly, F:Akhilesh Singh Yadav"]
# compare_texts = [["Vibhas Kumar Singh, Lucknow F: Akhilesh Singh"],
#  ["Bibhas  Singh, Lucknow, F: Akhilesh Kumar Singh"],
# ["Vibhas Singh F: Akhilesh Kumar Lucknow"]]
# Compute similarity scores
