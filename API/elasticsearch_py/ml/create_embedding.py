from sentence_transformers import SentenceTransformer

# Load the SBERT model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Assume doc is your document and it has fields name, email, gender, country
doc = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "gender": "Male",
    "country": "USA",
}

# Combine the fields into a single string
doc_string = " ".join([str(value) for value in doc.values()])

# Generate the embedding for the document
embedding = model.encode(doc_string, convert_to_tensor=True)

print(embedding)
