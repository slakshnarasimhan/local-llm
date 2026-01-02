# Retrieval Augmented Generation (RAG)

RAG is a technique that enhances large language models by providing them with relevant
context from a knowledge base. Instead of relying solely on the model's training data,
RAG retrieves relevant documents and includes them in the prompt.

## How RAG Works

1. **Document Chunking**: Break documents into smaller, manageable pieces
2. **Embedding Generation**: Convert chunks into vector representations
3. **Vector Storage**: Store embeddings in a vector database
4. **Query Processing**: When a question comes in, embed it as a vector
5. **Similarity Search**: Find the most relevant document chunks
6. **Context Injection**: Include retrieved chunks in the LLM prompt
7. **Response Generation**: LLM generates answer grounded in the context

## Benefits of RAG

- **Reduced Hallucinations**: Answers are grounded in actual documents
- **Up-to-date Information**: Knowledge base can be updated without retraining
- **Source Attribution**: Can cite which documents informed the answer
- **Domain Specificity**: Works well for specialized knowledge
- **Cost Effective**: No need for expensive fine-tuning

## RAG vs Fine-tuning

RAG is ideal when:
- You need frequently updated information
- You want source attribution
- You have limited compute resources

Fine-tuning is better when:
- You need specific tone or format
- Domain knowledge needs to be internalized
- You want faster inference

## Implementation Considerations

- Chunk size affects retrieval quality (typically 500-1000 tokens)
- Embedding model choice matters for semantic search
- Number of retrieved chunks balances context vs relevance
- Vector database selection impacts performance at scale
