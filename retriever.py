def retrieve_chunks(vector_store, question):

    documents = vector_store.similarity_search(
        question,
        k=3
    )

    relevant_chunks = [
        doc.page_content
        for doc in documents
    ]

    return relevant_chunks