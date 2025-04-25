from sentence_transformers import SentenceTransformer, util

# Load the model once at startup
model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(resume_text: str, job_description: str) -> float:
    # Convert texts into embeddings
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    # Compute cosine similarity
    similarity_score = util.cos_sim(resume_embedding, job_embedding)

    return float(similarity_score.item())  # Return as plain float