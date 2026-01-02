"""
Vector store implementation using ChromaDB for similarity search.
Supports both OpenAI and local embeddings.
"""
import os
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import openai


class VectorStore:
    """Manages embeddings and similarity search using ChromaDB."""
    
    def __init__(
        self,
        collection_name: str = "rag_documents",
        persist_directory: str = "./chroma_db",
        embedding_provider: str = "openai",
        openai_model: str = "text-embedding-3-small",
        local_model: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize vector store.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the database
            embedding_provider: "openai" or "local"
            openai_model: OpenAI embedding model name
            local_model: Sentence transformer model name for local embeddings
        """
        self.embedding_provider = embedding_provider
        self.openai_model = openai_model
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize local embedding model if needed
        self.local_embedder = None
        if embedding_provider == "local":
            print(f"Loading local embedding model: {local_model}")
            self.local_embedder = SentenceTransformer(local_model)
            print("✓ Local embedding model loaded")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using configured provider.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if self.embedding_provider == "openai":
            response = openai.embeddings.create(
                model=self.openai_model,
                input=text
            )
            return response.data[0].embedding
        else:
            # Use local sentence transformer
            embedding = self.local_embedder.encode(text, convert_to_numpy=True)
            return embedding.tolist()
    
    def add_documents(self, chunks: List[Dict[str, str]], batch_size: int = 100):
        """
        Add document chunks to the vector store.
        
        Args:
            chunks: List of document chunks with 'content' and metadata
            batch_size: Number of chunks to process at once
        """
        print(f"Adding {len(chunks)} chunks to vector store...")
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            
            # Generate embeddings for batch
            texts = [chunk['content'] for chunk in batch]
            embeddings = []
            
            if self.embedding_provider == "openai":
                # Batch embedding with OpenAI
                response = openai.embeddings.create(
                    model=self.openai_model,
                    input=texts
                )
                embeddings = [data.embedding for data in response.data]
            else:
                # Batch embedding with local model
                embeddings = self.local_embedder.encode(
                    texts,
                    convert_to_numpy=True,
                    show_progress_bar=True
                ).tolist()
            
            # Prepare data for ChromaDB
            ids = [f"chunk_{i + j}" for j in range(len(batch))]
            metadatas = [
                {
                    'source': chunk.get('source', 'unknown'),
                    'chunk_index': str(chunk.get('chunk_index', 0)),
                    'start_token': str(chunk.get('start_token', 0)),
                    'end_token': str(chunk.get('end_token', 0))
                }
                for chunk in batch
            ]
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
            
            print(f"  Processed {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")
        
        print("✓ All chunks added to vector store")
    
    def search(
        self,
        query: str,
        n_results: int = 3
    ) -> List[Dict[str, any]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of search results with content and metadata
        """
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()
    
    def clear(self):
        """Clear all documents from the collection."""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"}
        )
        print("✓ Vector store cleared")


if __name__ == "__main__":
    # Demo the vector store
    from document_processor import DocumentChunker, create_sample_documents
    
    # Create sample documents
    create_sample_documents()
    
    # Process documents
    chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
    docs = chunker.load_documents_from_directory("./sample_docs")
    chunks = chunker.process_documents(docs)
    
    print(f"\nProcessed {len(docs)} documents into {len(chunks)} chunks")
    
    # Initialize vector store with local embeddings (no API key needed for demo)
    vector_store = VectorStore(
        collection_name="rag_demo",
        persist_directory="./chroma_db_demo",
        embedding_provider="local"
    )
    
    # Clear existing data
    vector_store.clear()
    
    # Add documents
    vector_store.add_documents(chunks)
    
    # Test search
    print("\n" + "="*70)
    print("Testing similarity search...")
    print("="*70)
    
    query = "How do I install Ollama?"
    print(f"\nQuery: {query}")
    results = vector_store.search(query, n_results=2)
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Source: {result['metadata']['source']}")
        print(f"Content: {result['content'][:300]}...")

