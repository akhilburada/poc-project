# Chapter 3: GenAI Application Deployment (LLM & RAG)

## Overview

This chapter covers deploying Generative AI applications including:
- Simple LLM applications (chatbots, text generation)
- RAG (Retrieval Augmented Generation) systems
- Production-ready architectures on AWS and GCP

---

## Understanding GenAI Application Types

### Type 1: Simple LLM Application

Direct API calls to an LLM with prompt engineering.

```
┌─────────────────────────────────────────────────────────────────┐
│                 SIMPLE LLM APPLICATION                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User Input: "Explain quantum computing"                       │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │   Prompt Template                                        │  │
│   │   "You are an expert teacher. Explain {topic} in        │  │
│   │    simple terms for a beginner."                        │  │
│   └─────────────────────┬───────────────────────────────────┘  │
│                         │                                       │
│                         ▼                                       │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │   LLM API (Bedrock/Vertex AI/OpenAI)                    │  │
│   │   - Process prompt                                       │  │
│   │   - Generate response                                    │  │
│   └─────────────────────┬───────────────────────────────────┘  │
│                         │                                       │
│                         ▼                                       │
│   Response: "Quantum computing is like..."                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Use Cases:** Chatbots, content generation, summarization, translation

### Type 2: RAG (Retrieval Augmented Generation)

LLM enhanced with external knowledge from your documents.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RAG SYSTEM ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ═══════════════════════ INDEXING PIPELINE (Offline) ═══════════════════════│
│                                                                             │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌───────────┐ │
│  │Documents│──►│  Loader  │──►│ Chunker  │──►│ Embedder │──►│Vector DB  │ │
│  │(PDF,etc)│   │          │   │(split)   │   │          │   │(store)    │ │
│  └─────────┘   └──────────┘   └──────────┘   └──────────┘   └───────────┘ │
│                                                                             │
│  ═══════════════════════ QUERY PIPELINE (Online) ═══════════════════════════│
│                                                                             │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐                                 │
│  │  User   │──►│  Embed   │──►│  Search  │                                 │
│  │  Query  │   │  Query   │   │ Top-K    │                                 │
│  └─────────┘   └──────────┘   └────┬─────┘                                 │
│                                    │                                        │
│                    ┌───────────────┴───────────────┐                       │
│                    │     Retrieved Documents       │                        │
│                    │  "Doc1: ...", "Doc2: ..."     │                        │
│                    └───────────────┬───────────────┘                        │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        AUGMENTED PROMPT                               │  │
│  │                                                                       │  │
│  │  System: You are a helpful assistant. Answer based on the context.   │  │
│  │                                                                       │  │
│  │  Context:                                                             │  │
│  │  {retrieved_documents}                                                │  │
│  │                                                                       │  │
│  │  Question: {user_query}                                               │  │
│  │                                                                       │  │
│  └──────────────────────────────────┬───────────────────────────────────┘  │
│                                     │                                       │
│                                     ▼                                       │
│                            ┌───────────────┐                                │
│                            │   LLM API     │──► Generated Answer            │
│                            └───────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Use Cases:** Q&A over documents, customer support, knowledge bases, enterprise search

---

## AWS GenAI Services

### AWS Bedrock

Amazon Bedrock provides access to foundation models from multiple providers:

| Model Provider | Models Available | Best For |
|---------------|------------------|----------|
| Anthropic | Claude 3 (Opus, Sonnet, Haiku) | General tasks, reasoning |
| Meta | Llama 2, Llama 3 | Open-source, customizable |
| Amazon | Titan Text, Titan Embeddings | Cost-effective |
| Cohere | Command, Embed | Enterprise search |
| AI21 Labs | Jurassic | Text generation |

### AWS RAG Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AWS RAG ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────┐     ┌──────────────┐     ┌─────────────────────────┐    │
│   │  Client  │────►│ API Gateway  │────►│   Lambda / ECS          │    │
│   │  (App)   │     │              │     │   (Application Logic)   │    │
│   └──────────┘     └──────────────┘     └───────────┬─────────────┘    │
│                                                     │                   │
│                     ┌───────────────────────────────┼───────────────┐   │
│                     │                               │               │   │
│                     ▼                               ▼               │   │
│              ┌─────────────┐              ┌─────────────────┐       │   │
│              │   Bedrock   │              │   OpenSearch    │       │   │
│              │ (Embeddings)│              │   Serverless    │       │   │
│              │  Titan      │              │  (Vector DB)    │       │   │
│              └──────┬──────┘              └────────┬────────┘       │   │
│                     │                              │                │   │
│                     │      ┌───────────────────────┘                │   │
│                     │      │                                        │   │
│                     ▼      ▼                                        │   │
│              ┌─────────────────┐                                    │   │
│              │    Bedrock      │                                    │   │
│              │    (Claude)     │                                    │   │
│              │   Generation    │                                    │   │
│              └────────┬────────┘                                    │   │
│                       │                                             │   │
│                       ▼                                             │   │
│              ┌─────────────────┐                                    │   │
│              │    Response     │                                    │   │
│              └─────────────────┘                                    │   │
│                                                                         │
│   ══════════════════ Document Ingestion Pipeline ══════════════════     │
│                                                                         │
│   ┌──────┐    ┌──────────┐    ┌──────────────┐    ┌─────────────┐      │
│   │  S3  │───►│  Lambda  │───►│   Bedrock    │───►│ OpenSearch  │      │
│   │(Docs)│    │(Chunking)│    │ (Embedding)  │    │  (Index)    │      │
│   └──────┘    └──────────┘    └──────────────┘    └─────────────┘      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### AWS Bedrock Code Examples

#### Basic LLM Call

```python
# bedrock_basic.py
import boto3
import json

# Initialize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

def call_claude(prompt: str, max_tokens: int = 1000) -> str:
    """Call Claude model on Bedrock"""
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=body
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

# Example usage
response = call_claude("Explain machine learning in 3 sentences.")
print(response)
```

#### Embeddings with Titan

```python
# bedrock_embeddings.py
import boto3
import json
import numpy as np

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def get_embedding(text: str) -> list:
    """Get embeddings using Amazon Titan"""
    
    body = json.dumps({
        "inputText": text
    })
    
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body=body
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['embedding']

# Example
embedding = get_embedding("Hello, world!")
print(f"Embedding dimension: {len(embedding)}")  # 1536 dimensions
```

#### Complete RAG Implementation on AWS

```python
# aws_rag.py
import boto3
import json
from typing import List, Dict
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

class AWSRAGSystem:
    def __init__(self, opensearch_host: str, index_name: str, region: str = 'us-east-1'):
        self.bedrock = boto3.client('bedrock-runtime', region_name=region)
        self.index_name = index_name
        
        # Setup OpenSearch connection
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            region,
            'es',
            session_token=credentials.token
        )
        
        self.opensearch = OpenSearch(
            hosts=[{'host': opensearch_host, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding using Titan"""
        response = self.bedrock.invoke_model(
            modelId='amazon.titan-embed-text-v1',
            body=json.dumps({'inputText': text})
        )
        return json.loads(response['body'].read())['embedding']
    
    def index_document(self, doc_id: str, text: str, metadata: Dict = None):
        """Index a document with its embedding"""
        embedding = self.get_embedding(text)
        
        document = {
            'text': text,
            'embedding': embedding,
            'metadata': metadata or {}
        }
        
        self.opensearch.index(
            index=self.index_name,
            id=doc_id,
            body=document
        )
    
    def search_similar(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        query_embedding = self.get_embedding(query)
        
        search_query = {
            'size': k,
            'query': {
                'knn': {
                    'embedding': {
                        'vector': query_embedding,
                        'k': k
                    }
                }
            }
        }
        
        response = self.opensearch.search(index=self.index_name, body=search_query)
        return [
            {
                'text': hit['_source']['text'],
                'score': hit['_score'],
                'metadata': hit['_source'].get('metadata', {})
            }
            for hit in response['hits']['hits']
        ]
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """Generate response using Claude with retrieved context"""
        
        context = "\n\n".join([doc['text'] for doc in context_docs])
        
        prompt = f"""Based on the following context, answer the user's question.
If the answer cannot be found in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {query}

Answer:"""
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=body
        )
        
        return json.loads(response['body'].read())['content'][0]['text']
    
    def query(self, question: str, k: int = 5) -> str:
        """Complete RAG query pipeline"""
        # 1. Retrieve relevant documents
        relevant_docs = self.search_similar(question, k=k)
        
        # 2. Generate response with context
        response = self.generate_response(question, relevant_docs)
        
        return response

# Example usage
if __name__ == "__main__":
    rag = AWSRAGSystem(
        opensearch_host='your-domain.us-east-1.es.amazonaws.com',
        index_name='documents'
    )
    
    # Index some documents
    rag.index_document("doc1", "Python is a programming language created by Guido van Rossum.")
    rag.index_document("doc2", "Machine learning is a subset of artificial intelligence.")
    
    # Query
    answer = rag.query("Who created Python?")
    print(answer)
```

---

## GCP GenAI Services

### Vertex AI for GenAI

| Service | Description |
|---------|-------------|
| **Gemini** | Google's most capable model (multimodal) |
| **PaLM 2** | Text generation and chat |
| **Embeddings API** | Text embeddings for RAG |
| **Vector Search** | Managed vector database |
| **Vertex AI Search** | Enterprise search with RAG built-in |

### GCP RAG Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        GCP RAG ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────┐     ┌──────────────┐     ┌─────────────────────────┐    │
│   │  Client  │────►│Cloud Endpoints│───►│   Cloud Run / GKE       │    │
│   │  (App)   │     │or API Gateway │     │   (Application)         │    │
│   └──────────┘     └──────────────┘     └───────────┬─────────────┘    │
│                                                     │                   │
│                     ┌───────────────────────────────┼───────────────┐   │
│                     │                               │               │   │
│                     ▼                               ▼               │   │
│              ┌─────────────┐              ┌─────────────────┐       │   │
│              │  Vertex AI  │              │   Vertex AI     │       │   │
│              │ Embeddings  │              │  Vector Search  │       │   │
│              └──────┬──────┘              └────────┬────────┘       │   │
│                     │                              │                │   │
│                     │      ┌───────────────────────┘                │   │
│                     │      │                                        │   │
│                     ▼      ▼                                        │   │
│              ┌─────────────────┐                                    │   │
│              │   Vertex AI     │                                    │   │
│              │   (Gemini)      │                                    │   │
│              │   Generation    │                                    │   │
│              └────────┬────────┘                                    │   │
│                       │                                             │   │
│                       ▼                                             │   │
│              ┌─────────────────┐                                    │   │
│              │    Response     │                                    │   │
│              └─────────────────┘                                    │   │
│                                                                         │
│   ══════════════════ Document Ingestion Pipeline ══════════════════     │
│                                                                         │
│   ┌──────────┐  ┌────────────┐  ┌──────────────┐  ┌──────────────┐     │
│   │  Cloud   │─►│Cloud Func/ │─►│  Vertex AI   │─►│ Vector Search│     │
│   │ Storage  │  │  Dataflow  │  │ (Embedding)  │  │   (Index)    │     │
│   └──────────┘  └────────────┘  └──────────────┘  └──────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### GCP Vertex AI Code Examples

#### Basic Gemini Call

```python
# vertex_basic.py
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(project='your-project-id', location='us-central1')

def call_gemini(prompt: str) -> str:
    """Call Gemini model on Vertex AI"""
    model = GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    return response.text

# Example usage
response = call_gemini("Explain quantum computing in simple terms.")
print(response)
```

#### Gemini with Chat History

```python
# vertex_chat.py
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession

vertexai.init(project='your-project-id', location='us-central1')

class GeminiChat:
    def __init__(self):
        self.model = GenerativeModel('gemini-1.5-pro')
        self.chat = self.model.start_chat()
    
    def send_message(self, message: str) -> str:
        response = self.chat.send_message(message)
        return response.text
    
    def get_history(self):
        return self.chat.history

# Usage
chat = GeminiChat()
print(chat.send_message("Hi! What's machine learning?"))
print(chat.send_message("Give me an example."))
```

#### Embeddings with Vertex AI

```python
# vertex_embeddings.py
from vertexai.language_models import TextEmbeddingModel

def get_embeddings(texts: list) -> list:
    """Get embeddings using Vertex AI"""
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]

# Example
texts = ["Hello world", "Machine learning is awesome"]
embeddings = get_embeddings(texts)
print(f"Embedding dimension: {len(embeddings[0])}")
```

#### Complete RAG Implementation on GCP

```python
# gcp_rag.py
import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel
from google.cloud import aiplatform
from typing import List, Dict
import numpy as np

class GCPRAGSystem:
    def __init__(self, project_id: str, location: str, index_endpoint_id: str):
        vertexai.init(project=project_id, location=location)
        
        self.embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
        self.generation_model = GenerativeModel('gemini-1.5-pro')
        
        # Connect to Vector Search index
        aiplatform.init(project=project_id, location=location)
        self.index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_id)
        
        self.documents = {}  # In production, use a proper document store
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding"""
        embeddings = self.embedding_model.get_embeddings([text])
        return embeddings[0].values
    
    def index_document(self, doc_id: str, text: str):
        """Store document and its embedding"""
        embedding = self.get_embedding(text)
        self.documents[doc_id] = {
            'text': text,
            'embedding': embedding
        }
        # In production: upsert to Vector Search index
    
    def search_similar(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents using Vector Search"""
        query_embedding = self.get_embedding(query)
        
        # Query the index endpoint
        response = self.index_endpoint.find_neighbors(
            deployed_index_id="your_deployed_index_id",
            queries=[query_embedding],
            num_neighbors=k
        )
        
        results = []
        for neighbor in response[0]:
            doc_id = neighbor.id
            if doc_id in self.documents:
                results.append({
                    'id': doc_id,
                    'text': self.documents[doc_id]['text'],
                    'score': neighbor.distance
                })
        
        return results
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """Generate response with Gemini"""
        context = "\n\n".join([doc['text'] for doc in context_docs])
        
        prompt = f"""Based on the following context, answer the user's question accurately.
If the answer is not in the context, say so.

Context:
{context}

Question: {query}

Answer:"""
        
        response = self.generation_model.generate_content(prompt)
        return response.text
    
    def query(self, question: str, k: int = 5) -> str:
        """Complete RAG query"""
        relevant_docs = self.search_similar(question, k=k)
        response = self.generate_response(question, relevant_docs)
        return response

# Example usage
if __name__ == "__main__":
    rag = GCPRAGSystem(
        project_id='your-project',
        location='us-central1',
        index_endpoint_id='your-index-endpoint-id'
    )
    
    # Index documents
    rag.index_document("doc1", "Google Cloud Platform offers many AI services.")
    rag.index_document("doc2", "Vertex AI is Google's unified ML platform.")
    
    # Query
    answer = rag.query("What is Vertex AI?")
    print(answer)
```

---

## Production RAG Deployment

### FastAPI RAG Service

```python
# app.py - Production RAG API
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import logging
import time

app = FastAPI(title="RAG API", version="1.0.0")
logger = logging.getLogger(__name__)

# Initialize RAG system (use your AWS or GCP implementation)
# rag_system = AWSRAGSystem(...) or GCPRAGSystem(...)

class QueryRequest(BaseModel):
    question: str
    max_docs: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    latency_ms: float

class IngestRequest(BaseModel):
    documents: List[dict]  # [{"id": "doc1", "text": "...", "metadata": {...}}]

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    start_time = time.time()
    
    try:
        # Search for relevant documents
        relevant_docs = rag_system.search_similar(request.question, k=request.max_docs)
        
        # Generate response
        answer = rag_system.generate_response(request.question, relevant_docs)
        
        latency_ms = (time.time() - start_time) * 1000
        
        return QueryResponse(
            answer=answer,
            sources=relevant_docs,
            latency_ms=round(latency_ms, 2)
        )
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest(request: IngestRequest, background_tasks: BackgroundTasks):
    """Ingest documents in background"""
    background_tasks.add_task(ingest_documents, request.documents)
    return {"message": f"Ingesting {len(request.documents)} documents", "status": "processing"}

async def ingest_documents(documents: List[dict]):
    """Background task to ingest documents"""
    for doc in documents:
        try:
            rag_system.index_document(
                doc_id=doc['id'],
                text=doc['text'],
                metadata=doc.get('metadata', {})
            )
        except Exception as e:
            logger.error(f"Failed to ingest document {doc['id']}: {str(e)}")
```

### Dockerfile for RAG Service

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

### requirements.txt

```
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.0
boto3==1.34.0
opensearch-py==2.4.0
requests-aws4auth==1.2.0
google-cloud-aiplatform==1.38.0
vertexai==1.38.0
langchain==0.1.0
```

---

## Advanced RAG Patterns

### 1. Hybrid Search (Keyword + Semantic)

```python
def hybrid_search(query: str, k: int = 5) -> List[Dict]:
    """Combine keyword and semantic search"""
    
    # Semantic search
    semantic_results = vector_db.search(get_embedding(query), k=k)
    
    # Keyword search (BM25)
    keyword_results = elasticsearch.search(query, k=k)
    
    # Combine with Reciprocal Rank Fusion
    combined = reciprocal_rank_fusion(semantic_results, keyword_results)
    
    return combined[:k]
```

### 2. Re-ranking

```python
def rerank_results(query: str, documents: List[str], k: int = 5) -> List[str]:
    """Re-rank documents using a cross-encoder"""
    from sentence_transformers import CrossEncoder
    
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    pairs = [[query, doc] for doc in documents]
    scores = model.predict(pairs)
    
    # Sort by score
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    
    return [doc for doc, score in ranked[:k]]
```

### 3. Query Expansion

```python
def expand_query(query: str) -> str:
    """Use LLM to expand/rephrase the query"""
    
    prompt = f"""Given the query: "{query}"
    
Generate 3 alternative phrasings that might help find relevant information.
Return only the alternatives, one per line."""
    
    response = call_llm(prompt)
    alternatives = response.strip().split('\n')
    
    return query + " " + " ".join(alternatives)
```

---

## Deployment Checklist

### Security
- [ ] API authentication (API keys, OAuth)
- [ ] Rate limiting
- [ ] Input validation and sanitization
- [ ] Secrets management (AWS Secrets Manager / GCP Secret Manager)
- [ ] VPC configuration for vector database

### Scalability
- [ ] Auto-scaling configured
- [ ] Caching for embeddings (Redis/ElastiCache)
- [ ] Async document ingestion
- [ ] Connection pooling

### Monitoring
- [ ] Request latency tracking
- [ ] Token usage monitoring
- [ ] Error rate alerts
- [ ] Cost monitoring

### Cost Optimization
- [ ] Use smaller models for simple queries
- [ ] Cache frequent queries
- [ ] Batch embedding requests
- [ ] Use spot instances for batch jobs

---

## Interview Tips for GenAI Deployment

**Q: How would you design a RAG system for enterprise documents?**

Answer structure:
1. **Ingestion Pipeline**: "I'd build an async pipeline that processes documents from S3/GCS, chunks them appropriately (500-1000 tokens with overlap), generates embeddings using Titan/Vertex AI, and stores in a vector database."

2. **Query Pipeline**: "For queries, I'd embed the query, retrieve top-k relevant chunks, optionally re-rank them, then pass to an LLM with the context."

3. **Operational concerns**: "I'd add caching for repeated queries, monitoring for latency and costs, and implement feedback loops to improve retrieval quality."

---

## Next Steps

Continue to [Chapter 4: Agentic AI Deployment](../04-agentic-ai-deployment/README.md) to learn about deploying AI agents and multi-agent systems.
