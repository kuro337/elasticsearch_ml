# SBERT 

- Setup

```bash
sudo apt install python3.10
python3.10 --version 
sudo apt install python3.10-venv

# Create Project and Activate Environment
python3.10 -m venv myenv310
source myenv310/bin/activate  

source myenv310/bin/deactivate  




# To return to System Interpretor
deactivate

pip install -U  sentence-transformers
pip install pylint pydantic elasticsearch 

# Run tests - unittest part of stdlib
python -m unittest test_module.py

# Setting up Linting
which pylint
# Ctrl + , -> pylint import strategy = from env

# Make sure .env file is set at Root with
# PYTHONPATH=/home/chin/projects/Search/Elasticsearch/SBERT/ml_app

# Also Set the Pylint Binary path 
# /home/chin/projects/Search/Elasticsearch/SBERT/myenv310/bin/pylint

# Run App
python3 sbert.py

# Disabling Auto Import
# pylint: disable=unused-import

```

- Embeddings Index ES

```json
{
  "mappings": {
    "properties": {
      "embedding": {
        "type": "dense_vector",
        "dims": 384  // match the dimensionality of your embeddings
      }
    }
  }
}


```

- Dense Vectors:

  - Max Dimensions - 2048​1​.

  - Dimensionality has to be defined at Index Creation Time​.

  - All dense vectors within an index must have the same dimensionality​.

- Sparse Vectors:

  - Max Dimensions - 1024​4​.

  - In terms of setting a specific dimensionality, it is done at the time of index creation for dense vectors, whereas sparse vectors do not require the dimensionality to be specified upon index creation as they are designed to handle high-dimensional data with lots of zero values efficiently.

  - Therefore, while you have to set the dimensionality when dealing with dense vectors, sparse vectors allow for a more flexible handling of vector data, albeit with a limitation on the maximum number of dimensions.