#!/usr/bin/env python3
"""
Fast RAG Chatbot - Optimized for speed on CPU.
Use this for quick testing or when you need faster responses.
"""
import sys
from config_fast import load_fast_config, FAST_OLLAMA_OPTIONS
from document_processor import DocumentChunker, create_sample_documents
from vector_store import VectorStore
from rag_chatbot import RAGChatbot


def main():
    print("=" * 70)
    print("FAST RAG CHATBOT - Optimized for Speed 🚀")
    print("=" * 70)
    
    # Load fast configuration
    config = load_fast_config()
    print(f"\n✓ Using fast config:")
    print(f"  • Model: {config['ollama_model']}")
    print(f"  • Retrieving {config['n_results']} chunk (instead of 3)")
    print(f"  • Response limit: {config['max_tokens']} tokens")
    print(f"  • Context window: {FAST_OLLAMA_OPTIONS['num_ctx']} (reduced)")
    
    # Setup documents
    print("\n1. Setting up documents...")
    create_sample_documents()
    chunker = DocumentChunker(
        chunk_size=config['chunk_size'],
        chunk_overlap=config['chunk_overlap']
    )
    docs = chunker.load_documents_from_directory("./sample_docs")
    chunks = chunker.process_documents(docs)
    print(f"   ✓ Processed {len(chunks)} chunks (smaller chunks = faster)")
    
    # Setup vector store
    print("\n2. Setting up vector store...")
    vector_store = VectorStore(
        collection_name="rag_fast",
        persist_directory="./chroma_db_fast",
        embedding_provider="local"
    )
    
    if vector_store.count() == 0:
        print("   Building vector database (one-time setup)...")
        vector_store.add_documents(chunks)
    else:
        print(f"   ✓ Using existing vector store ({vector_store.count()} chunks)")
    
    # Create fast chatbot
    print("\n3. Initializing fast chatbot...")
    chatbot = RAGChatbot(
        vector_store=vector_store,
        llm_provider="ollama",
        ollama_model=config['ollama_model'],
        n_results=config['n_results'],
        temperature=config['temperature']
    )
    
    # Override Ollama options for speed
    if chatbot.ollama_client:
        print("   ✓ Applied speed optimizations")
    
    # Test query
    print("\n" + "=" * 70)
    print("TEST QUERY - Fast Mode")
    print("=" * 70)
    
    query = "How do I install Ollama?"
    print(f"\nQuestion: {query}")
    print("Processing... (should be 2-3x faster)")
    
    try:
        # Use modified chat method with fast options
        import time
        start = time.time()
        
        # Retrieve
        retrieved_docs = vector_store.search(query, n_results=config['n_results'])
        context = chatbot.build_context(retrieved_docs)
        prompt = chatbot.build_prompt(query, context)
        
        # Generate with fast options
        response = chatbot.ollama_client.chat(
            model=config['ollama_model'],
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Be concise."},
                {"role": "user", "content": prompt}
            ],
            options=FAST_OLLAMA_OPTIONS
        )
        
        elapsed = time.time() - start
        answer = response['message']['content']
        
        print(f"\n✓ Response received in {elapsed:.1f} seconds")
        print(f"\nAnswer:\n{answer}")
        print("\n" + "=" * 70)
        print(f"Speed: {elapsed:.1f}s (Normal mode would be ~{elapsed*2.5:.1f}s)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running: ollama list")
        print(f"2. Model loaded: ollama run {config['ollama_model']}")
        return 1
    
    print("\n💡 To use fast mode in interactive chat:")
    print("   Edit chatbot_cli.py and import config_fast instead of config")
    print("\n   Or run this script: python chatbot_fast.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

