# Complete RAG Deployment Example

This file provides a fully working RAG (Retrieval Augmented Generation) system you can deploy.

---

## Real-World Scenario: HR Policy Chatbot

**Business Need:** A company wants employees to ask questions about HR policies, benefits, and procedures without waiting for HR staff.

**Requirements:**
- Answer questions from 500+ policy documents
- Response time < 3 seconds
- 95%+ accuracy on common questions
- Escalate complex/sensitive questions to HR

---

## Complete Implementation

### Project Structure

```
hr-policy-rag/
├── src/
│   ├── __init__.py
│   ├── app.py                 # FastAPI application
│   ├── ingestion.py           # Document processing
│   ├── embeddings.py          # Embedding generation
│   ├── retrieval.py           # Vector search
│   ├── generation.py          # LLM response generation
│   └── config.py              # Configuration
├── documents/                  # HR policy PDFs
├── tests/
│   └── test_rag.py
├── scripts/
│   ├── ingest_documents.py    # One-time ingestion
│   └── evaluate_rag.py        # Quality evaluation
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### requirements.txt

```
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.0
boto3==1.34.0
opensearch-py==2.4.0
requests-aws4auth==1.2.3
PyPDF2==3.0.1
python-docx==1.1.0
tiktoken==0.5.0
tenacity==8.2.0
```

### src/config.py

```python
"""Configuration for the RAG application"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # AWS
    aws_region: str = "us-east-1"
    
    # OpenSearch
    opensearch_host: str = os.getenv("OPENSEARCH_HOST", "")
    opensearch_index: str = "hr-policies"
    
    # Bedrock
    embedding_model: str = "amazon.titan-embed-text-v1"
    generation_model: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    # RAG parameters
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_results: int = 5
    
    # Safety
    max_input_length: int = 1000
    escalation_keywords: list = ["salary", "termination", "lawsuit", "harassment", "discrimination"]

settings = Settings()
```

### src/ingestion.py

```python
"""Document ingestion pipeline"""
import os
import hashlib
from typing import List, Dict
from PyPDF2 import PdfReader
from docx import Document
import tiktoken

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def load_document(self, file_path: str) -> str:
        """Load document based on file type"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self._load_pdf(file_path)
        elif ext == '.docx':
            return self._load_docx(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _load_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def _load_docx(self, file_path: str) -> str:
        """Extract text from Word document"""
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """Split text into overlapping chunks"""
        # Clean text
        text = " ".join(text.split())
        
        chunks = []
        tokens = self.tokenizer.encode(text)
        
        start = 0
        chunk_index = 0
        
        while start < len(tokens):
            # Get chunk tokens
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            
            # Decode back to text
            chunk_text = self.tokenizer.decode(chunk_tokens)
            
            # Create chunk with metadata
            chunk_id = hashlib.md5(chunk_text.encode()).hexdigest()[:12]
            
            chunks.append({
                'id': f"{metadata.get('doc_id', 'unknown')}_{chunk_index}_{chunk_id}",
                'text': chunk_text,
                'metadata': {
                    **(metadata or {}),
                    'chunk_index': chunk_index,
                    'token_count': len(chunk_tokens)
                }
            })
            
            # Move to next chunk with overlap
            start = end - self.overlap
            chunk_index += 1
        
        return chunks
    
    def process_directory(self, directory: str) -> List[Dict]:
        """Process all documents in a directory"""
        all_chunks = []
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if not os.path.isfile(file_path):
                continue
            
            try:
                print(f"Processing: {filename}")
                text = self.load_document(file_path)
                
                metadata = {
                    'doc_id': hashlib.md5(filename.encode()).hexdigest()[:8],
                    'filename': filename,
                    'source': file_path
                }
                
                chunks = self.chunk_text(text, metadata)
                all_chunks.extend(chunks)
                print(f"  Created {len(chunks)} chunks")
                
            except Exception as e:
                print(f"  Error processing {filename}: {e}")
        
        return all_chunks
```

### src/embeddings.py

```python
"""Embedding generation using AWS Bedrock"""
import boto3
import json
from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential

class BedrockEmbeddings:
    def __init__(self, model_id: str = "amazon.titan-embed-text-v1", region: str = "us-east-1"):
        self.client = boto3.client('bedrock-runtime', region_name=region)
        self.model_id = model_id
        self.dimension = 1536  # Titan embedding dimension
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        body = json.dumps({"inputText": text})
        
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body
        )
        
        result = json.loads(response['body'].read())
        return result['embedding']
    
    def embed_batch(self, texts: List[str], batch_size: int = 10) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            for text in batch:
                embedding = self.embed_text(text)
                embeddings.append(embedding)
            
            print(f"  Embedded {min(i + batch_size, len(texts))}/{len(texts)}")
        
        return embeddings
```

### src/retrieval.py

```python
"""Vector search using OpenSearch"""
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from typing import List, Dict
from src.embeddings import BedrockEmbeddings
from src.config import settings

class VectorStore:
    def __init__(self):
        # Setup AWS auth
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            settings.aws_region,
            'es',
            session_token=credentials.token
        )
        
        # Connect to OpenSearch
        self.client = OpenSearch(
            hosts=[{'host': settings.opensearch_host, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
        
        self.index_name = settings.opensearch_index
        self.embedder = BedrockEmbeddings()
    
    def create_index(self):
        """Create the vector index if it doesn't exist"""
        if self.client.indices.exists(index=self.index_name):
            print(f"Index {self.index_name} already exists")
            return
        
        index_body = {
            "settings": {
                "index": {
                    "knn": True,
                    "knn.algo_param.ef_search": 100
                }
            },
            "mappings": {
                "properties": {
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": 1536,
                        "method": {
                            "name": "hnsw",
                            "space_type": "cosinesimil",
                            "engine": "nmslib",
                            "parameters": {
                                "ef_construction": 128,
                                "m": 24
                            }
                        }
                    },
                    "text": {"type": "text"},
                    "metadata": {"type": "object"}
                }
            }
        }
        
        self.client.indices.create(index=self.index_name, body=index_body)
        print(f"Created index: {self.index_name}")
    
    def index_documents(self, documents: List[Dict]):
        """Index documents with their embeddings"""
        print(f"Indexing {len(documents)} documents...")
        
        # Generate embeddings
        texts = [doc['text'] for doc in documents]
        embeddings = self.embedder.embed_batch(texts)
        
        # Index each document
        for doc, embedding in zip(documents, embeddings):
            body = {
                'embedding': embedding,
                'text': doc['text'],
                'metadata': doc.get('metadata', {})
            }
            
            self.client.index(
                index=self.index_name,
                id=doc['id'],
                body=body
            )
        
        # Refresh index
        self.client.indices.refresh(index=self.index_name)
        print(f"Indexed {len(documents)} documents successfully")
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        # Get query embedding
        query_embedding = self.embedder.embed_text(query)
        
        # KNN search
        search_body = {
            "size": k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_embedding,
                        "k": k
                    }
                }
            }
        }
        
        response = self.client.search(
            index=self.index_name,
            body=search_body
        )
        
        results = []
        for hit in response['hits']['hits']:
            results.append({
                'id': hit['_id'],
                'text': hit['_source']['text'],
                'score': hit['_score'],
                'metadata': hit['_source'].get('metadata', {})
            })
        
        return results
```

### src/generation.py

```python
"""LLM response generation using Bedrock Claude"""
import boto3
import json
from typing import List, Dict
from src.config import settings

class ResponseGenerator:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime', region_name=settings.aws_region)
        self.model_id = settings.generation_model
    
    def generate(self, query: str, context_docs: List[Dict]) -> Dict:
        """Generate response using retrieved context"""
        
        # Check for escalation keywords
        should_escalate = self._check_escalation(query)
        
        # Format context
        context = self._format_context(context_docs)
        
        # Create prompt
        prompt = f"""You are an HR assistant helping employees understand company policies and benefits.

<context>
{context}
</context>

<question>
{query}
</question>

Instructions:
1. Answer based ONLY on the information provided in the context above
2. If the information is not in the context, say "I don't have information about that in my knowledge base. Please contact HR directly."
3. Be helpful and professional
4. For sensitive topics (salary negotiations, legal issues, complaints), suggest contacting HR directly
5. Cite which policy document you're referencing when possible

Answer:"""

        # Call Bedrock
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
        
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body
        )
        
        result = json.loads(response['body'].read())
        answer = result['content'][0]['text']
        
        # Add escalation notice if needed
        if should_escalate:
            answer += "\n\n⚠️ This topic may require personal attention. Consider reaching out to HR directly at hr@company.com or extension 1234."
        
        return {
            'answer': answer,
            'should_escalate': should_escalate,
            'sources': [
                {
                    'filename': doc['metadata'].get('filename', 'Unknown'),
                    'relevance': round(doc['score'], 3)
                }
                for doc in context_docs[:3]
            ]
        }
    
    def _format_context(self, docs: List[Dict]) -> str:
        """Format retrieved documents as context"""
        context_parts = []
        
        for i, doc in enumerate(docs):
            source = doc['metadata'].get('filename', 'Unknown document')
            context_parts.append(f"[Document {i+1}: {source}]\n{doc['text']}")
        
        return "\n\n".join(context_parts)
    
    def _check_escalation(self, query: str) -> bool:
        """Check if query should be escalated to human HR"""
        query_lower = query.lower()
        
        for keyword in settings.escalation_keywords:
            if keyword in query_lower:
                return True
        
        return False
```

### src/app.py

```python
"""FastAPI application for HR Policy RAG"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import time
import logging

from src.retrieval import VectorStore
from src.generation import ResponseGenerator
from src.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize
app = FastAPI(
    title="HR Policy Assistant",
    description="Ask questions about HR policies, benefits, and procedures",
    version="1.0.0"
)

vector_store = VectorStore()
generator = ResponseGenerator()

# Pydantic models
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "How many vacation days do I get per year?"
            }
        }

class Source(BaseModel):
    filename: str
    relevance: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    should_escalate: bool
    latency_ms: float

class HealthResponse(BaseModel):
    status: str
    index_exists: bool

# Endpoints
@app.get("/health", response_model=HealthResponse)
def health():
    """Check service health"""
    try:
        index_exists = vector_store.client.indices.exists(index=settings.opensearch_index)
        return HealthResponse(status="healthy", index_exists=index_exists)
    except Exception as e:
        return HealthResponse(status=f"unhealthy: {str(e)}", index_exists=False)

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Ask a question about HR policies.
    
    The system will search relevant policy documents and generate an answer.
    """
    start_time = time.time()
    
    try:
        # 1. Retrieve relevant documents
        logger.info(f"Searching for: {request.question[:50]}...")
        relevant_docs = vector_store.search(request.question, k=settings.top_k_results)
        
        if not relevant_docs:
            return QueryResponse(
                answer="I couldn't find any relevant policy documents. Please contact HR directly.",
                sources=[],
                should_escalate=True,
                latency_ms=round((time.time() - start_time) * 1000, 2)
            )
        
        # 2. Generate response
        result = generator.generate(request.question, relevant_docs)
        
        latency = (time.time() - start_time) * 1000
        logger.info(f"Generated response in {latency:.0f}ms")
        
        return QueryResponse(
            answer=result['answer'],
            sources=[Source(**s) for s in result['sources']],
            should_escalate=result['should_escalate'],
            latency_ms=round(latency, 2)
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {
        "message": "HR Policy Assistant API",
        "docs": "/docs",
        "health": "/health"
    }
```

### scripts/ingest_documents.py

```python
#!/usr/bin/env python3
"""
Ingest HR policy documents into the vector store.
Usage: python scripts/ingest_documents.py --documents-dir ./documents
"""

import argparse
from src.ingestion import DocumentProcessor
from src.retrieval import VectorStore

def main():
    parser = argparse.ArgumentParser(description="Ingest documents into vector store")
    parser.add_argument("--documents-dir", required=True, help="Directory containing documents")
    args = parser.parse_args()
    
    # Process documents
    print("Processing documents...")
    processor = DocumentProcessor(chunk_size=500, overlap=50)
    chunks = processor.process_directory(args.documents_dir)
    print(f"Created {len(chunks)} total chunks")
    
    # Create index and ingest
    print("\nIndexing documents...")
    vector_store = VectorStore()
    vector_store.create_index()
    vector_store.index_documents(chunks)
    
    print("\nDone! Documents are now searchable.")

if __name__ == "__main__":
    main()
```

---

## Deployment Commands

### Deploy to AWS

```bash
# 1. Create OpenSearch Serverless collection
aws opensearchserverless create-collection \
    --name hr-policies \
    --type VECTORSEARCH

# 2. Build and push Docker image
aws ecr create-repository --repository-name hr-rag-api

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker build -t hr-rag-api .
docker tag hr-rag-api:latest ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/hr-rag-api:latest
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/hr-rag-api:latest

# 3. Ingest documents (run once)
python scripts/ingest_documents.py --documents-dir ./documents

# 4. Deploy to ECS/Fargate
# Use the task definition from the ML API example, updating the image and env vars

# 5. Test
curl -X POST "https://your-api-url/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "How many vacation days do I get?"}'
```

### Deploy to GCP

```bash
# 1. Create Vertex AI Vector Search index
python scripts/create_gcp_index.py

# 2. Deploy to Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/hr-rag-api

gcloud run deploy hr-rag-api \
    --image gcr.io/PROJECT_ID/hr-rag-api \
    --platform managed \
    --region us-central1 \
    --memory 2Gi \
    --set-env-vars "GCP_PROJECT=PROJECT_ID,INDEX_ENDPOINT_ID=xxx"
```

---

## Example Conversations

**User:** "How many vacation days do I get per year?"

**Assistant:** "According to our PTO Policy (vacation_policy.pdf), full-time employees receive:
- 15 days of paid vacation in years 1-3
- 20 days in years 4-7  
- 25 days after 7+ years

Vacation days reset on January 1st each year. Unused days can be carried over up to 5 days maximum.

*Sources: vacation_policy.pdf (relevance: 0.92)*"

---

**User:** "I want to file a harassment complaint"

**Assistant:** "I understand you want to file a harassment complaint. According to our Employee Handbook (section 12.3), harassment of any kind is not tolerated.

To file a complaint:
1. Contact HR directly at hr@company.com
2. Or call the anonymous ethics hotline: 1-800-XXX-XXXX
3. Or speak with your manager's manager

All complaints are treated confidentially and investigated promptly.

⚠️ This topic may require personal attention. Consider reaching out to HR directly at hr@company.com or extension 1234.

*Sources: employee_handbook.pdf (relevance: 0.89)*"

---

## Evaluation Script

### scripts/evaluate_rag.py

```python
#!/usr/bin/env python3
"""Evaluate RAG system quality"""

import json
from src.retrieval import VectorStore
from src.generation import ResponseGenerator

# Test questions with expected answers
TEST_CASES = [
    {
        "question": "How many vacation days do new employees get?",
        "expected_keywords": ["15", "vacation", "days"],
        "expected_source": "vacation_policy"
    },
    {
        "question": "What is the dress code policy?",
        "expected_keywords": ["business", "casual", "dress"],
        "expected_source": "dress_code"
    },
    {
        "question": "How do I request parental leave?",
        "expected_keywords": ["parental", "leave", "weeks"],
        "expected_source": "parental_leave"
    }
]

def evaluate():
    vector_store = VectorStore()
    generator = ResponseGenerator()
    
    results = []
    
    for test in TEST_CASES:
        # Get response
        docs = vector_store.search(test["question"], k=5)
        response = generator.generate(test["question"], docs)
        
        # Check keyword presence
        answer_lower = response["answer"].lower()
        keywords_found = sum(1 for kw in test["expected_keywords"] if kw.lower() in answer_lower)
        keyword_score = keywords_found / len(test["expected_keywords"])
        
        # Check source relevance
        source_found = any(test["expected_source"] in s["filename"].lower() for s in response["sources"])
        
        results.append({
            "question": test["question"],
            "keyword_score": keyword_score,
            "source_correct": source_found,
            "answer_preview": response["answer"][:200]
        })
        
        print(f"Q: {test['question']}")
        print(f"  Keyword Score: {keyword_score:.0%}")
        print(f"  Source Found: {'✓' if source_found else '✗'}")
        print()
    
    # Summary
    avg_keyword = sum(r["keyword_score"] for r in results) / len(results)
    source_accuracy = sum(1 for r in results if r["source_correct"]) / len(results)
    
    print("=" * 50)
    print(f"Average Keyword Score: {avg_keyword:.0%}")
    print(f"Source Accuracy: {source_accuracy:.0%}")

if __name__ == "__main__":
    evaluate()
```

This complete example gives you everything needed to build and deploy a production RAG system!
