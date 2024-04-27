from transformers import AutoModel, AutoTokenizer
import torch
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_clinicalbert_embeddings(text):
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
    model = AutoModel.from_pretrained("medicalai/ClinicalBERT")
    
    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    # Get embeddings
    with torch.no_grad(): # Disable gradient calculation for inference
        outputs = model(**inputs)
    
    # The embeddings can be taken from the last hidden state
    embeddings = outputs.last_hidden_state
    
    # You might want to pool the embeddings for the entire input
    # Here, we simply average them to get a single vector for the input text
    pooled_embeddings = torch.mean(embeddings, dim=1)

    vector_list = pooled_embeddings[0].detach().cpu().numpy().tolist()
    
    return vector_list

# Example usage
# text = "Aspirin can be used to reduce fever and relieve mild to moderate pain."
# embeddings = get_clinicalbert_embeddings(text)

# print(len(embeddings[0]))




def batch_generator(data, batch_size):
    """Yield successive n-sized batches from data."""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

def get_embeddings_for_batch(batch):
    tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
    model = AutoModel.from_pretrained("medicalai/ClinicalBERT")
    texts = [d['embed_text'] for d in batch]
    
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    embeddings = outputs.last_hidden_state
    pooled_embeddings = torch.mean(embeddings, dim=1)
    embeddings_list = pooled_embeddings.detach().cpu().numpy()
    
    # Returning a list of dictionaries with id, embed_text, and embeddings
    return [
        {"id": item["id"], "embed_text": item["embed_text"], "embedding": embedding.tolist()}
        for item, embedding in zip(batch, embeddings_list)
    ]

def get_clinicalbert_embeddings_parallel(data, batch_size=10):
    results = []
    with ThreadPoolExecutor() as executor:
        future_to_batch = {executor.submit(get_embeddings_for_batch, batch): batch for batch in batch_generator(data, batch_size)}
        for future in as_completed(future_to_batch):
            results.extend(future.result())
    return results

# Example usage:
# data = [{'id': 1, 'embed_text': 'Sample text 1'}, {'id': 2, 'embed_text': 'Sample text 2'}, ...]
# enriched_data = get_clinicalbert_embeddings_parallel(data, batch_size=10)
