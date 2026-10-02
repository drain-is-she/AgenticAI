import numpy as np


class VectorStore:

    def __init__(self):

        self.vectors = []
        self.documents = []
        self.metadata = []

    def add(
        self,
        vector,
        document,
        metadata
    ):

        self.vectors.append(vector)
        self.documents.append(document)
        self.metadata.append(metadata)

    def search(
        self,
        query_vector,
        top_k=5
    ):

        results = []

        for i, vector in enumerate(self.vectors):

            dot_product = np.dot(
                query_vector,
                vector
            )

            magnitude_query = np.linalg.norm(
                query_vector
            )

            magnitude_vector = np.linalg.norm(
                vector
            )

            if (
                magnitude_query == 0
                or magnitude_vector == 0
            ):
                score = 0

            else:

                score = (
                    dot_product
                    / (
                        magnitude_query
                        * magnitude_vector
                    )
                )

            results.append({
                "score": score,
                "document": self.documents[i],
                "metadata": self.metadata[i]
            })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:top_k]