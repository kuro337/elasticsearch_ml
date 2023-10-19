# Semantic Search in Elasticsearch


## Generating Embeddings


- Transformers

```bash

pip install transformers
pip install torch
pip install -U  sentence-transformers

# For CPU Only Support
pip install 'transformers[torch]'

pip3 install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Cuda
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.4.0/local_installers/cuda-repo-wsl-ubuntu-11-4-local_11.4.0-1_amd64.deb
sudo dpkg -i cuda-repo-wsl-ubuntu-11-4-local_11.4.0-1_amd64.deb
sudo apt-key add /var/cuda-repo-wsl-ubuntu-11-4-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda

# Confirm
nvidia-smi

# Pytorch
python -m pip install torch==1.6.0 torchvision==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html


# Now try
pip install -U sentence-transformers

```

```python
from sentence_transformers import SentenceTransformer

# Load the SBERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Assume doc is your document and it has fields name, email, gender, country
doc = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "gender": "Male",
    "country": "USA"
}

# Combine the fields into a single string
doc_string = " ".join([str(value) for value in doc.values()])

# Generate the embedding for the document
embedding = model.encode(doc_string, convert_to_tensor=True)

```



- Finetuning the Model

- Unsupservised Finetuning (we don't have labels for the data)

  - More complex than supervised finetuning - due to the lack of labels, we need to use a proxy task to train the model

  - Here we use contrastive loss - to learn to distinguish between similar and dissimilar pairs of sentences


```python
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import torch
import torch.nn.functional as F

# Load pre-trained model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Assume you have the following data
texts = ['Text 1', 'Text 2', ...]

# Create DataLoader
examples = [InputExample(texts=[text]) for text in texts]
train_dataloader = DataLoader(examples, shuffle=True, batch_size=32)

# Define a hypothetical contrastive loss
class ContrastiveLoss(torch.nn.Module):
    def __init__(self, margin=1.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, output1, output2, label):
        euclidean_distance = F.pairwise_distance(output1, output2)
        loss_contrastive = torch.mean((1-label) * torch.pow(euclidean_distance, 2) +
                                       (label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))

        return loss_contrastive

# Define the training objective
train_loss = ContrastiveLoss()

# Assume a hypothetical method to fine-tune the model with contrastive loss
# This is a simplified and hypothetical method for illustration purposes only
def fine_tune(model, train_dataloader, train_loss, epochs=1):
    for epoch in range(epochs):
        for batch in train_dataloader:
            embeddings = model.encode(batch.texts[0])
            # Hypothetical pairs and labels generation
            output1, output2, labels = ...  # You would need to define how to obtain these
            loss = train_loss(output1, output2, labels)
            loss.backward()
            # Update model parameters
            ...

# Fine-tune the model
fine_tune(model, train_dataloader, train_loss)

```

- Supervised Finetuning (we have labels for the data denoting similarity)

```python
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# Load pre-trained model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Assume you have the following data
text_pairs = [('Text 1a', 'Text 1b'), ('Text 2a', 'Text 2b'), ...]
similarity_scores = [0.8, 0.3, ...]  # Assume similarity scores are in range [0, 1]

# Create InputExamples
examples = [InputExample(texts=pair, label=score) for pair, score in zip(text_pairs, similarity_scores)]
train_dataloader = DataLoader(examples, shuffle=True, batch_size=32)

# Define the training objective
train_loss = losses.CosineSimilarityLoss(model=model)

# Fine-tune the model
model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=1, warmup_steps=100)


```