import os
import logging
import shutil

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

_vector_store = None


def _get_index_path() -> str:
    from django.conf import settings
    return str(settings.FAISS_INDEX_PATH)


def get_vector_store():
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    index_path = _get_index_path()
    if os.path.exists(index_path):
        try:
            _vector_store = FAISS.load_local(
                index_path,
                embedding_model,
                allow_dangerous_deserialization=True,
            )
            logger.info("Vector store loaded from disk")
        except Exception as e:
            logger.error(f"Failed to load vector store from disk: {e}")
            _vector_store = None

    return _vector_store


def rebuild_vector_store():
    global _vector_store

    from documents.models import Document

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_chunks = []
    metadata = []

    for doc in Document.objects.exclude(extracted_text=''):
        chunks = splitter.split_text(doc.extracted_text)
        all_chunks.extend(chunks)
        metadata.extend([
            {"document_id": doc.id, "title": doc.title}
            for _ in chunks
        ])

    index_path = _get_index_path()

    if all_chunks:
        _vector_store = FAISS.from_texts(
            texts=all_chunks,
            embedding=embedding_model,
            metadatas=metadata,
        )
        _vector_store.save_local(index_path)
        logger.info(f"Vector store rebuilt with {len(all_chunks)} chunks from {Document.objects.count()} documents")
    else:
        _vector_store = None
        if os.path.exists(index_path):
            shutil.rmtree(index_path)
        logger.info("Vector store cleared — no documents with extracted text")
