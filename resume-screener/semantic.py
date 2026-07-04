from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"
RELATED_THRESHOLD = 0.30

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def find_related_matches(missing_skills: set, resume_skills: set) -> dict:
    """For each JD skill the resume doesn't explicitly list, find the closest resume
    skill by meaning -- e.g. resume has 'TensorFlow', JD wants 'Machine Learning'."""
    if not missing_skills or not resume_skills:
        return {}

    model = get_model()
    missing_list = list(missing_skills)
    resume_list = list(resume_skills)

    missing_embeddings = model.encode(missing_list, convert_to_tensor=True)
    resume_embeddings = model.encode(resume_list, convert_to_tensor=True)
    similarity = util.cos_sim(missing_embeddings, resume_embeddings)

    related = {}
    for i, jd_skill in enumerate(missing_list):
        best_idx = int(similarity[i].argmax())
        best_score = float(similarity[i][best_idx])
        if best_score >= RELATED_THRESHOLD:
            related[jd_skill] = {
                "closest_skill": resume_list[best_idx],
                "similarity": round(best_score, 2),
            }
    return related


def semantic_similarity(text_a: str, text_b: str) -> float:
    """Overall semantic closeness between two blocks of text (e.g. whole resume vs whole JD)."""
    model = get_model()
    embeddings = model.encode([text_a, text_b], convert_to_tensor=True)
    return round(float(util.cos_sim(embeddings[0], embeddings[1])), 3)
