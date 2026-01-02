"""
RAG Chatbot with support for both OpenAI (cloud) and Ollama (local) LLMs.
This demonstrates how easy it is to switch between cloud and local inference.
"""
import os
from typing import List, Dict, Optional
import openai
import requests
import json


class RAGChatbot:
    """RAG chatbot that can use either OpenAI or Ollama for inference."""
    
    def __init__(
        self,
        vector_store,
        llm_provider: str = "openai",
        openai_model: str = "gpt-3.5-turbo",
        ollama_model: str = "llama3",
        ollama_base_url: str = "http://localhost:11434",
        n_results: int = 3,
        temperature: float = 0.7
    ):
        """
        Initialize RAG chatbot.
        
        Args:
            vector_store: VectorStore instance for document retrieval
            llm_provider: "openai" or "ollama"
            openai_model: OpenAI model name
            ollama_model: Ollama model name
            ollama_base_url: Ollama server URL
            n_results: Number of documents to retrieve
            temperature: LLM temperature for response generation
        """
        self.vector_store = vector_store
        self.llm_provider = llm_provider
        self.openai_model = openai_model
        self.ollama_model = ollama_model
        self.n_results = n_results
        self.temperature = temperature
        
        # Store Ollama connection info
        self.ollama_base_url = ollama_base_url
        if llm_provider == "ollama":
            print(f"✓ Using Ollama at {ollama_base_url}")
    
    def build_context(self, retrieved_docs: List[Dict[str, any]]) -> str:
        """
        Build context string from retrieved documents.
        
        Args:
            retrieved_docs: List of retrieved document chunks
            
        Returns:
            Formatted context string
        """
        if not retrieved_docs:
            return "No relevant documents found."
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            source = doc['metadata'].get('source', 'Unknown')
            content = doc['content']
            context_parts.append(f"[Document {i} - {source}]\n{content}")
        
        return "\n\n".join(context_parts)
    
    def build_prompt(self, query: str, context: str) -> str:
        """
        Build the RAG prompt with query and context.
        
        Args:
            query: User's question
            context: Retrieved context
            
        Returns:
            Complete prompt
        """
        prompt = f"""You are a helpful AI assistant. Answer the user's question based on the provided context.

Context:
{context}

Question: {query}

Instructions:
- Answer based primarily on the provided context
- If the context doesn't contain enough information, say so
- Be concise but thorough
- Cite which document sections support your answer when relevant

Answer:"""
        return prompt
    
    def query_openai(self, prompt: str) -> str:
        """
        Query OpenAI API.
        
        Args:
            prompt: Complete prompt with context
            
        Returns:
            Generated response
        """
        response = openai.chat.completions.create(
            model=self.openai_model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that answers questions based on provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    def query_ollama(self, prompt: str) -> str:
        """
        Query Ollama API using requests library with streaming.
        
        Args:
            prompt: Complete prompt with context
            
        Returns:
            Generated response
        """
        url = f"{self.ollama_base_url}/api/chat"
        data = {
            "model": self.ollama_model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that answers questions based on provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": True,
            "options": {
                "temperature": self.temperature,
                "num_predict": 500
            }
        }
        
        try:
            full_response = ""
            response = requests.post(url, json=data, stream=True, timeout=120)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'message' in chunk and 'content' in chunk['message']:
                        full_response += chunk['message']['content']
                    if chunk.get('done', False):
                        break
            
            return full_response
        except requests.Timeout:
            raise Exception(f"Ollama request timed out after 120s. Is the model loaded?")
        except requests.HTTPError as e:
            raise Exception(f"Ollama API error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Error calling Ollama: {str(e)}")
    
    def chat(self, query: str, verbose: bool = False) -> Dict[str, any]:
        """
        Process a query using RAG.
        
        Args:
            query: User's question
            verbose: Whether to return detailed information
            
        Returns:
            Dictionary with answer and optional debug info
        """
        # Step 1: Retrieve relevant documents
        retrieved_docs = self.vector_store.search(query, n_results=self.n_results)
        
        # Step 2: Build context from retrieved documents
        context = self.build_context(retrieved_docs)
        
        # Step 3: Build complete prompt
        prompt = self.build_prompt(query, context)
        
        # Step 4: Generate response using selected LLM
        if self.llm_provider == "openai":
            answer = self.query_openai(prompt)
        elif self.llm_provider == "ollama":
            answer = self.query_ollama(prompt)
        else:
            raise ValueError(f"Unknown LLM provider: {self.llm_provider}")
        
        # Prepare response
        response = {
            "answer": answer,
            "llm_provider": self.llm_provider,
            "model": self.openai_model if self.llm_provider == "openai" else self.ollama_model
        }
        
        if verbose:
            response["retrieved_docs"] = retrieved_docs
            response["context"] = context
            response["full_prompt"] = prompt
        
        return response
    
    def switch_provider(self, new_provider: str):
        """
        Switch between OpenAI and Ollama.
        
        Args:
            new_provider: "openai" or "ollama"
        """
        if new_provider not in ["openai", "ollama"]:
            raise ValueError(f"Invalid provider: {new_provider}. Must be 'openai' or 'ollama'")
        
        self.llm_provider = new_provider
        print(f"✓ Switched to {new_provider.upper()} for LLM inference")


if __name__ == "__main__":
    # Demo the RAG chatbot
    from document_processor import DocumentChunker, create_sample_documents
    from vector_store import VectorStore
    import sys
    
    print("="*70)
    print("RAG Chatbot Demo - Local Embeddings + Local LLM")
    print("="*70)
    
    # Create sample documents
    create_sample_documents()
    
    # Process documents
    print("\n1. Processing documents...")
    chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
    docs = chunker.load_documents_from_directory("./sample_docs")
    chunks = chunker.process_documents(docs)
    print(f"   ✓ Processed {len(docs)} documents into {len(chunks)} chunks")
    
    # Initialize vector store (using local embeddings for demo)
    print("\n2. Setting up vector store...")
    vector_store = VectorStore(
        collection_name="rag_demo",
        persist_directory="./chroma_db_demo",
        embedding_provider="local"
    )
    
    # Check if we need to add documents
    if vector_store.count() == 0:
        print("   Adding documents to vector store...")
        vector_store.add_documents(chunks)
    else:
        print(f"   ✓ Vector store already contains {vector_store.count()} chunks")
    
    # Initialize chatbot with Ollama (local LLM)
    print("\n3. Initializing RAG chatbot with Ollama...")
    try:
        chatbot = RAGChatbot(
            vector_store=vector_store,
            llm_provider="ollama",
            ollama_model="llama3"
        )
        
        # Test query
        print("\n4. Testing RAG chatbot...")
        print("-"*70)
        query = "How do I install and run Ollama?"
        print(f"Query: {query}\n")
        
        response = chatbot.chat(query)
        print(f"Answer ({response['model']}):\n{response['answer']}")
        print("-"*70)
        
    except Exception as e:
        print(f"   ⚠ Ollama not available: {e}")
        print("   To run this demo, install Ollama from https://ollama.com")
        print("   Then run: ollama pull llama3")

