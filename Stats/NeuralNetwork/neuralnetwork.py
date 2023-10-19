import tensorflow as tf
import numpy as np

# Numpy Array contained SBERT embeddings
SBERT_EMBEDDINGS = np.load("SBERT_EMBEDDINGS.npy")


# Define the neural network model
class RecommenderNetwork(tf.keras.Model):
    def __init__(self):
        super(RecommenderNetwork, self).__init__()
        self.embedding_layer = tf.keras.layers.Embedding(
            input_dim=SBERT_EMBEDDINGS.shape[0],  # number of unique categories
            output_dim=SBERT_EMBEDDINGS.shape[1],  # embedding dimension
            weights=[SBERT_EMBEDDINGS],  # pre-trained embeddings
            trainable=False,  # set to True if you want to fine-tune the embeddings
        )
        self.dense1 = tf.keras.layers.Dense(128, activation="relu")
        self.dense2 = tf.keras.layers.Dense(1, activation="sigmoid")

    def call(self, inputs):
        """
        Forward pass of the neural network
        """
        x = self.embedding_layer(inputs)
        x = self.dense1(x)
        x = self.dense2(x)
        return x


# Instantiate and compile the model
model = RecommenderNetwork()
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
