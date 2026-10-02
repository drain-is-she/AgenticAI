import numpy as np
from pypdf import PdfReader
import os


PDF_FOLDER = "knowledge"
WINDOW_SIZE = 2
CHUNK_SIZE = 200
OVERLAP = 40
EMBEDDING_DIMENSIONS = 50


def load_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def load_documents(folder):

    documents = []

    for filename in os.listdir(folder):

        if filename.lower().endswith(".pdf"):

            path = os.path.join(folder, filename)

            text = load_pdf(path)

            documents.append({
                "source": filename,
                "text": text
            })

    return documents


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks(documents):

    chunks = []

    for document in documents:

        document_chunks = chunk_text(
            document["text"]
        )

        for chunk in document_chunks:

            chunks.append({
                "source": document["source"],
                "text": chunk
            })

    return chunks


def tokenize(text):

    return text.lower().split()


def build_vocabulary(chunks):

    vocabulary = set()

    for chunk in chunks:

        words = tokenize(chunk["text"])

        for word in words:
            vocabulary.add(word)

    vocabulary = sorted(vocabulary)

    word_to_id = {
        word: i
        for i, word in enumerate(vocabulary)
    }

    id_to_word = {
        i: word
        for word, i in word_to_id.items()
    }

    return vocabulary, word_to_id, id_to_word


def build_cooccurrence_matrix(
    chunks,
    word_to_id
):

    vocab_size = len(word_to_id)

    co_matrix = np.zeros(
        (vocab_size, vocab_size),
        dtype=np.float64
    )

    for chunk in chunks:

        words = tokenize(chunk["text"])

        for i, word in enumerate(words):

            if word not in word_to_id:
                continue

            word_id = word_to_id[word]

            start = max(
                0,
                i - WINDOW_SIZE
            )

            end = min(
                len(words),
                i + WINDOW_SIZE + 1
            )

            for j in range(start, end):

                if i == j:
                    continue

                context_word = words[j]

                if context_word not in word_to_id:
                    continue

                context_id = word_to_id[
                    context_word
                ]

                co_matrix[
                    word_id,
                    context_id
                ] += 1

    return co_matrix


def create_word_embeddings(co_matrix):

    U, S, Vt = np.linalg.svd(
        co_matrix,
        full_matrices=False
    )

    k = min(
        EMBEDDING_DIMENSIONS,
        len(S)
    )

    embeddings = (
        U[:, :k]
        @ np.diag(S[:k])
    )

    return embeddings


def sentence_embedding(
    text,
    word_to_id,
    embeddings
):

    words = tokenize(text)

    vectors = []

    for word in words:

        if word in word_to_id:

            vectors.append(
                embeddings[
                    word_to_id[word]
                ]
            )

    if not vectors:

        return np.zeros(
            embeddings.shape[1]
        )

    return np.mean(
        vectors,
        axis=0
    )


def create_chunk_embeddings(
    chunks,
    word_to_id,
    embeddings
):

    vectors = []

    for chunk in chunks:

        vector = sentence_embedding(
            chunk["text"],
            word_to_id,
            embeddings
        )

        vectors.append(vector)

    return np.array(vectors)


def cosine_similarity(a, b):

    dot_product = np.dot(a, b)

    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return (
        dot_product
        / (magnitude_a * magnitude_b)
    )


def semantic_search(
    query,
    chunks,
    chunk_embeddings,
    word_to_id,
    word_embeddings,
    top_k=5
):

    query_vector = sentence_embedding(
        query,
        word_to_id,
        word_embeddings
    )

    results = []

    for i, chunk_vector in enumerate(
        chunk_embeddings
    ):

        score = cosine_similarity(
            query_vector,
            chunk_vector
        )

        results.append({
            "score": score,
            "source": chunks[i]["source"],
            "text": chunks[i]["text"]
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


def main():

    documents = load_documents(
        PDF_FOLDER
    )

    print(
        "Documents:",
        len(documents)
    )

    chunks = create_chunks(
        documents
    )

    print(
        "Chunks:",
        len(chunks)
    )

    vocabulary, word_to_id, id_to_word = (
        build_vocabulary(chunks)
    )

    print(
        "Vocabulary size:",
        len(vocabulary)
    )

    co_matrix = build_cooccurrence_matrix(
        chunks,
        word_to_id
    )

    print(
        "Co-occurrence matrix:",
        co_matrix.shape
    )

    word_embeddings = create_word_embeddings(
        co_matrix
    )

    print(
        "Word embeddings:",
        word_embeddings.shape
    )

    chunk_embeddings = create_chunk_embeddings(
        chunks,
        word_to_id,
        word_embeddings
    )

    print(
        "Chunk embeddings:",
        chunk_embeddings.shape
    )

    while True:

        query = input(
            "\nEnter query: "
        )

        if query.lower() == "exit":
            break

        results = semantic_search(
            query,
            chunks,
            chunk_embeddings,
            word_to_id,
            word_embeddings,
            top_k=5
        )

        print(
            "\nTop results:\n"
        )

        for result in results:

            print(
                f"Score: {result['score']:.4f}"
            )

            print(
                f"Source: {result['source']}"
            )

            print(
                result["text"]
            )

            print(
                "-" * 80
            )


if __name__ == "__main__":
    main()