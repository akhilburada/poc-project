# Real-World Client Project Examples for ML/AI Engineers (2 Years Experience)

This document describes realistic client projects that ML/AI engineers typically work on in service companies like Virtusa, TCS, Infosys, Wipro, etc. These are based on common industry patterns.

---

## Project 1: Intelligent Document Processing (IDP) Platform

### Client Domain: Insurance / Banking / Healthcare
### Duration: 8-12 months
### Team Size: 5-8 members

### Business Problem
Client receives 10,000+ documents daily (claims, invoices, KYC documents, medical records). Manual processing takes 15-20 minutes per document. They want to automate extraction and classification.

### What You Built

```
Architecture:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Document  │────▶│   AWS S3    │────▶│  Lambda     │────▶│  Textract/  │
│   Upload    │     │   Bucket    │     │  Trigger    │     │  OCR Engine │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Response  │◀────│  DynamoDB   │◀────│  Post-      │◀────│  ML Model   │
│   API       │     │  Storage    │     │  Processing │     │  Inference  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Technical Implementation

**1. Document Classification Model**
```python
# You built a document classifier using transfer learning
from transformers import LayoutLMv3ForSequenceClassification, LayoutLMv3Processor

class DocumentClassifier:
    def __init__(self, model_path):
        self.model = LayoutLMv3ForSequenceClassification.from_pretrained(model_path)
        self.processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base")
        self.labels = ["invoice", "claim_form", "id_proof", "medical_report", "contract"]
    
    def classify(self, image, ocr_text, bboxes):
        encoding = self.processor(
            image, 
            ocr_text, 
            boxes=bboxes,
            return_tensors="pt",
            truncation=True
        )
        outputs = self.model(**encoding)
        predicted_class = outputs.logits.argmax(-1).item()
        confidence = torch.softmax(outputs.logits, dim=-1).max().item()
        return self.labels[predicted_class], confidence
```

**2. Named Entity Extraction using Fine-tuned BERT**
```python
# Fine-tuned NER model for extracting key fields
from transformers import AutoModelForTokenClassification, AutoTokenizer

class EntityExtractor:
    def __init__(self):
        self.model = AutoModelForTokenClassification.from_pretrained(
            "your-company/insurance-ner-model"  # Fine-tuned on client data
        )
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.label_map = {
            0: "O",
            1: "B-POLICY_NUMBER",
            2: "I-POLICY_NUMBER", 
            3: "B-CLAIM_AMOUNT",
            4: "I-CLAIM_AMOUNT",
            5: "B-DATE",
            6: "I-DATE",
            7: "B-NAME",
            8: "I-NAME"
        }
    
    def extract_entities(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=2)
        
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        entities = self._group_entities(tokens, predictions[0])
        return entities
```

**3. AWS Lambda Handler**
```python
import boto3
import json

s3_client = boto3.client('s3')
textract_client = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Get document from S3
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Call Textract for OCR
    response = textract_client.analyze_document(
        Document={'S3Object': {'Bucket': bucket, 'Name': key}},
        FeatureTypes=['FORMS', 'TABLES']
    )
    
    # Extract text and bounding boxes
    extracted_data = process_textract_response(response)
    
    # Call SageMaker endpoint for classification
    classification_result = invoke_classification_endpoint(extracted_data)
    
    # Call SageMaker endpoint for entity extraction
    entities = invoke_ner_endpoint(extracted_data['text'])
    
    # Store results in DynamoDB
    table = dynamodb.Table('DocumentProcessingResults')
    table.put_item(Item={
        'document_id': key,
        'classification': classification_result,
        'extracted_entities': entities,
        'processed_at': datetime.now().isoformat()
    })
    
    return {'statusCode': 200, 'body': json.dumps('Processing complete')}
```

### Your Role & Responsibilities
- Developed document classification model using LayoutLMv3
- Fine-tuned BERT-based NER model on 5000 labeled documents
- Built data preprocessing pipeline for handling various document formats (PDF, images, scanned docs)
- Deployed models on AWS SageMaker with auto-scaling
- Integrated with AWS Textract for OCR
- Achieved 94% classification accuracy and 89% entity extraction F1-score

### Challenges You Faced
1. **Poor quality scanned documents** - Implemented image preprocessing (deskewing, denoising, contrast enhancement)
2. **Handwritten text** - Used AWS Textract's handwriting feature + custom post-processing
3. **Model latency** - Optimized using ONNX runtime, reduced inference from 2s to 300ms
4. **Class imbalance** - Used weighted loss function and oversampling for rare document types

### Business Impact
- Reduced processing time from 15 minutes to 45 seconds per document
- 85% documents processed without human intervention
- Saved client $2M annually in operational costs

---

## Project 2: Customer Support Chatbot with RAG (Retrieval Augmented Generation)

### Client Domain: E-commerce / Telecom
### Duration: 6 months
### Team Size: 4 members

### Business Problem
Client's customer support handles 50,000 queries daily. 60% are repetitive questions about products, policies, orders. They want an AI chatbot to handle L1 queries automatically.

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │────▶│   API       │────▶│   Query     │
│   Query     │     │   Gateway   │     │   Router    │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
            ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
            │   FAQ/      │           │   Order     │           │   Product   │
            │   Policy    │           │   Status    │           │   Info      │
            │   (RAG)     │           │   (API)     │           │   (RAG)     │
            └─────────────┘           └─────────────┘           └─────────────┘
                    │                          │                          │
                    └──────────────────────────┼──────────────────────────┘
                                               │
                                               ▼
                                      ┌─────────────┐
                                      │   LLM       │
                                      │   Response  │
                                      │   Generator │
                                      └─────────────┘
```

### Technical Implementation

**1. Document Ingestion & Embedding Pipeline**
```python
from langchain.document_loaders import PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

class KnowledgeBaseBuilder:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " "]
        )
        
        pinecone.init(api_key=os.environ["PINECONE_API_KEY"])
        self.index_name = "customer-support-kb"
    
    def ingest_documents(self, file_paths):
        all_chunks = []
        
        for path in file_paths:
            if path.endswith('.pdf'):
                loader = PyPDFLoader(path)
            elif path.endswith('.csv'):
                loader = CSVLoader(path)
            
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            
            # Add metadata
            for chunk in chunks:
                chunk.metadata['source'] = path
                chunk.metadata['doc_type'] = self._classify_doc_type(path)
            
            all_chunks.extend(chunks)
        
        # Create vector store
        Pinecone.from_documents(
            all_chunks, 
            self.embeddings, 
            index_name=self.index_name
        )
        
        return len(all_chunks)
```

**2. RAG Chain with Query Classification**
```python
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class CustomerSupportBot:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
        self.vectorstore = Pinecone.from_existing_index(
            "customer-support-kb",
            HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        )
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",  # Maximum Marginal Relevance
            search_kwargs={"k": 5, "fetch_k": 10}
        )
        
        self.qa_prompt = PromptTemplate(
            template="""You are a helpful customer support assistant. 
            Use the following context to answer the question. 
            If you cannot find the answer in the context, say "I'll connect you with a human agent."
            
            Context: {context}
            
            Chat History: {chat_history}
            
            Question: {question}
            
            Answer in a friendly, professional tone. Be concise but complete.""",
            input_variables=["context", "chat_history", "question"]
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            combine_docs_chain_kwargs={"prompt": self.qa_prompt},
            return_source_documents=True
        )
    
    def get_response(self, query, chat_history=[]):
        # First, classify the query intent
        intent = self._classify_intent(query)
        
        if intent == "order_status":
            return self._handle_order_query(query)
        elif intent == "escalate":
            return self._escalate_to_human(query)
        else:
            # Use RAG for general queries
            result = self.chain({
                "question": query,
                "chat_history": chat_history
            })
            
            return {
                "answer": result["answer"],
                "sources": [doc.metadata["source"] for doc in result["source_documents"]],
                "confidence": self._calculate_confidence(result)
            }
    
    def _classify_intent(self, query):
        # Simple intent classification
        order_keywords = ["order", "tracking", "delivery", "shipping", "where is my"]
        escalate_keywords = ["speak to human", "agent", "manager", "complaint"]
        
        query_lower = query.lower()
        if any(kw in query_lower for kw in order_keywords):
            return "order_status"
        elif any(kw in query_lower for kw in escalate_keywords):
            return "escalate"
        return "general"
```

**3. FastAPI Backend**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import redis

app = FastAPI()
bot = CustomerSupportBot()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    session_id: str
    escalated: bool = False

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Get chat history from Redis
    session_id = request.session_id or f"{request.user_id}_{int(time.time())}"
    chat_history = get_chat_history(session_id)
    
    # Get response
    result = bot.get_response(request.message, chat_history)
    
    # Store in chat history
    store_chat_history(session_id, request.message, result["answer"])
    
    return ChatResponse(
        response=result["answer"],
        sources=result.get("sources", []),
        session_id=session_id,
        escalated=result.get("escalated", False)
    )

def get_chat_history(session_id):
    history = redis_client.lrange(f"chat:{session_id}", 0, -1)
    return [json.loads(h) for h in history]

def store_chat_history(session_id, user_msg, bot_msg):
    redis_client.rpush(f"chat:{session_id}", json.dumps({"human": user_msg, "ai": bot_msg}))
    redis_client.expire(f"chat:{session_id}", 3600)  # 1 hour TTL
```

### Your Role & Responsibilities
- Built RAG pipeline using LangChain and Pinecone vector database
- Implemented query intent classification to route queries appropriately
- Developed conversation memory management using Redis
- Fine-tuned embedding model on domain-specific data for better retrieval
- Set up evaluation metrics (RAGAS) for measuring RAG quality
- Deployed on AWS ECS with auto-scaling

### Challenges You Faced
1. **Hallucination** - Implemented strict grounding prompts and confidence scoring
2. **Slow retrieval** - Used hybrid search (semantic + keyword) with re-ranking
3. **Context window limits** - Implemented smart chunking and summarization
4. **Multilingual queries** - Added language detection and translation layer

### Business Impact
- Handled 65% of queries without human intervention
- Reduced average response time from 8 minutes to 15 seconds
- Customer satisfaction score improved from 3.2 to 4.1 (out of 5)

---

## Project 3: Predictive Maintenance for Manufacturing

### Client Domain: Manufacturing / Industrial
### Duration: 10 months
### Team Size: 6 members

### Business Problem
Client has 200+ industrial machines (CNC machines, pumps, compressors). Unplanned downtime costs $50,000/hour. They want to predict failures 24-48 hours in advance.

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   IoT       │────▶│   AWS IoT   │────▶│   Kinesis   │────▶│   Lambda    │
│   Sensors   │     │   Core      │     │   Stream    │     │   Process   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Alert     │◀────│  SNS        │◀────│  Anomaly    │◀────│  Feature    │
│   Dashboard │     │  Notify     │     │  Detection  │     │  Store      │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                      ┌─────────────┐
                                      │  SageMaker  │
                                      │  ML Model   │
                                      └─────────────┘
```

### Technical Implementation

**1. Feature Engineering Pipeline**
```python
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler

class FeatureEngineer:
    def __init__(self, window_sizes=[60, 300, 900]):  # 1min, 5min, 15min windows
        self.window_sizes = window_sizes
        self.scaler = StandardScaler()
    
    def extract_features(self, sensor_df):
        """
        sensor_df columns: timestamp, machine_id, temperature, vibration, 
                          pressure, current, rpm
        """
        features = []
        
        for machine_id in sensor_df['machine_id'].unique():
            machine_data = sensor_df[sensor_df['machine_id'] == machine_id].copy()
            machine_data = machine_data.sort_values('timestamp')
            
            feature_row = {'machine_id': machine_id}
            
            for col in ['temperature', 'vibration', 'pressure', 'current', 'rpm']:
                for window in self.window_sizes:
                    rolling = machine_data[col].rolling(window=window)
                    
                    # Statistical features
                    feature_row[f'{col}_mean_{window}'] = rolling.mean().iloc[-1]
                    feature_row[f'{col}_std_{window}'] = rolling.std().iloc[-1]
                    feature_row[f'{col}_min_{window}'] = rolling.min().iloc[-1]
                    feature_row[f'{col}_max_{window}'] = rolling.max().iloc[-1]
                    feature_row[f'{col}_skew_{window}'] = rolling.skew().iloc[-1]
                    
                    # Rate of change
                    feature_row[f'{col}_roc_{window}'] = (
                        machine_data[col].iloc[-1] - machine_data[col].iloc[-window]
                    ) / window
                
                # Frequency domain features (for vibration)
                if col == 'vibration':
                    fft_vals = np.fft.fft(machine_data[col].values[-1024:])
                    feature_row['vibration_fft_peak'] = np.max(np.abs(fft_vals))
                    feature_row['vibration_fft_mean'] = np.mean(np.abs(fft_vals))
            
            # Cross-sensor features
            feature_row['temp_vibration_corr'] = machine_data['temperature'].corr(
                machine_data['vibration']
            )
            feature_row['power_factor'] = (
                machine_data['current'].iloc[-1] * machine_data['rpm'].iloc[-1]
            )
            
            features.append(feature_row)
        
        return pd.DataFrame(features)
```

**2. Anomaly Detection Model**
```python
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
import xgboost as xgb
import joblib

class FailurePredictionModel:
    def __init__(self):
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.failure_classifier = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            scale_pos_weight=10,  # Handle class imbalance
            random_state=42
        )
        self.feature_engineer = FeatureEngineer()
    
    def train(self, historical_data, failure_labels):
        """
        historical_data: sensor readings
        failure_labels: 1 if failure occurred within 24 hours, 0 otherwise
        """
        # Extract features
        features = self.feature_engineer.extract_features(historical_data)
        
        # Train anomaly detector (unsupervised)
        self.anomaly_detector.fit(features.drop('machine_id', axis=1))
        
        # Add anomaly score as feature
        features['anomaly_score'] = self.anomaly_detector.decision_function(
            features.drop('machine_id', axis=1)
        )
        
        # Train classifier
        X = features.drop('machine_id', axis=1)
        y = failure_labels
        
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )
        
        self.failure_classifier.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=20,
            verbose=False
        )
        
        # Feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.failure_classifier.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return self.evaluate(X_val, y_val)
    
    def predict(self, sensor_data):
        features = self.feature_engineer.extract_features(sensor_data)
        features['anomaly_score'] = self.anomaly_detector.decision_function(
            features.drop('machine_id', axis=1)
        )
        
        X = features.drop('machine_id', axis=1)
        
        failure_prob = self.failure_classifier.predict_proba(X)[:, 1]
        
        results = []
        for idx, machine_id in enumerate(features['machine_id']):
            results.append({
                'machine_id': machine_id,
                'failure_probability': failure_prob[idx],
                'risk_level': self._get_risk_level(failure_prob[idx]),
                'anomaly_score': features['anomaly_score'].iloc[idx]
            })
        
        return results
    
    def _get_risk_level(self, prob):
        if prob > 0.8:
            return 'CRITICAL'
        elif prob > 0.5:
            return 'HIGH'
        elif prob > 0.3:
            return 'MEDIUM'
        return 'LOW'
```

**3. Real-time Processing with AWS Lambda**
```python
import boto3
import json
from datetime import datetime

sagemaker_runtime = boto3.client('sagemaker-runtime')
sns_client = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Parse Kinesis records
    sensor_readings = []
    for record in event['Records']:
        payload = json.loads(
            base64.b64decode(record['kinesis']['data']).decode('utf-8')
        )
        sensor_readings.append(payload)
    
    # Group by machine
    machine_data = group_by_machine(sensor_readings)
    
    predictions = []
    for machine_id, readings in machine_data.items():
        # Call SageMaker endpoint
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName='predictive-maintenance-endpoint',
            ContentType='application/json',
            Body=json.dumps({'readings': readings})
        )
        
        prediction = json.loads(response['Body'].read().decode())
        predictions.append(prediction)
        
        # Store prediction
        store_prediction(machine_id, prediction)
        
        # Send alert if high risk
        if prediction['risk_level'] in ['CRITICAL', 'HIGH']:
            send_alert(machine_id, prediction)
    
    return {'statusCode': 200, 'predictions': len(predictions)}

def send_alert(machine_id, prediction):
    sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:xxx:maintenance-alerts',
        Message=json.dumps({
            'machine_id': machine_id,
            'risk_level': prediction['risk_level'],
            'failure_probability': prediction['failure_probability'],
            'recommended_action': get_recommended_action(prediction),
            'timestamp': datetime.now().isoformat()
        }),
        Subject=f'[{prediction["risk_level"]}] Maintenance Alert - {machine_id}'
    )
```

### Your Role & Responsibilities
- Built feature engineering pipeline for time-series sensor data
- Developed hybrid model (Isolation Forest + XGBoost) for failure prediction
- Implemented real-time streaming pipeline using AWS Kinesis and Lambda
- Created monitoring dashboard using CloudWatch metrics
- Achieved 87% precision and 82% recall in predicting failures 24 hours ahead

### Challenges You Faced
1. **Severe class imbalance** - Only 2% positive samples; used SMOTE and adjusted class weights
2. **Sensor noise** - Implemented Kalman filtering for sensor data smoothing
3. **Concept drift** - Set up model retraining pipeline triggered by performance degradation
4. **Missing sensors** - Built imputation logic for handling sensor failures

### Business Impact
- Reduced unplanned downtime by 40%
- Saved $3.2M annually in emergency repairs
- Increased equipment lifespan by 15%

---

## Project 4: GenAI-Powered Code Review Assistant

### Client Domain: IT Services / Software Development
### Duration: 4 months
### Team Size: 3 members

### Business Problem
Development team spends 30% of time on code reviews. They want an AI assistant to do initial review, catch common issues, and suggest improvements.

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   GitHub    │────▶│   Webhook   │────▶│   Queue     │
│   PR Event  │     │   Handler   │     │   (SQS)     │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                      ┌─────────────┐
                                      │   Review    │
                                      │   Worker    │
                                      └─────────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
            ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
            │   Static    │           │   LLM       │           │   Security  │
            │   Analysis  │           │   Review    │           │   Scan      │
            └─────────────┘           └─────────────┘           └─────────────┘
                    │                          │                          │
                    └──────────────────────────┼──────────────────────────┘
                                               │
                                               ▼
                                      ┌─────────────┐
                                      │   GitHub    │
                                      │   Comment   │
                                      └─────────────┘
```

### Technical Implementation

**1. Code Analysis with Fine-tuned Model**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, LoraConfig
import torch

class CodeReviewAgent:
    def __init__(self, base_model="codellama/CodeLlama-7b-hf", lora_path="./code-review-lora"):
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        
        # Load base model with 4-bit quantization
        base = AutoModelForCausalLM.from_pretrained(
            base_model,
            load_in_4bit=True,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        # Load LoRA adapter
        self.model = PeftModel.from_pretrained(base, lora_path)
        
        self.system_prompt = """You are an expert code reviewer. Analyze the code and provide:
1. Bug identification with line numbers
2. Security vulnerabilities
3. Performance issues
4. Code style and best practice violations
5. Suggested improvements with code examples

Be specific and actionable. Format as markdown."""

    def review_code(self, code_diff, file_path, context=""):
        prompt = f"""<s>[INST] <<SYS>>
{self.system_prompt}
<</SYS>>

File: {file_path}

Code changes:
```
{code_diff}
```

Additional context:
{context}

Provide a detailed code review. [/INST]"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1024,
                temperature=0.2,
                top_p=0.9,
                do_sample=True
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self._parse_review(response)
    
    def _parse_review(self, response):
        # Extract the assistant's response after [/INST]
        review = response.split("[/INST]")[-1].strip()
        
        # Parse into structured format
        return {
            "full_review": review,
            "issues": self._extract_issues(review),
            "suggestions": self._extract_suggestions(review)
        }
```

**2. Fine-tuning with LoRA**
```python
from datasets import load_dataset
from transformers import TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

def fine_tune_code_reviewer():
    # Load training data (code review pairs)
    dataset = load_dataset("json", data_files="code_review_dataset.json")
    
    # LoRA configuration
    lora_config = LoraConfig(
        r=16,  # Rank
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        "codellama/CodeLlama-7b-hf",
        load_in_4bit=True,
        torch_dtype=torch.float16
    )
    
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, lora_config)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir="./code-review-lora",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        warmup_steps=100,
        logging_steps=10,
        save_steps=200,
        fp16=True
    )
    
    # Trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        tokenizer=tokenizer,
        dataset_text_field="text",
        max_seq_length=2048
    )
    
    trainer.train()
    trainer.save_model("./code-review-lora")
```

**3. GitHub Integration**
```python
from github import Github
import os

class GitHubReviewBot:
    def __init__(self):
        self.github = Github(os.environ["GITHUB_TOKEN"])
        self.reviewer = CodeReviewAgent()
    
    def process_pull_request(self, repo_name, pr_number):
        repo = self.github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        
        all_reviews = []
        
        for file in pr.get_files():
            if not self._should_review(file.filename):
                continue
            
            # Get diff
            diff = file.patch
            
            # Get full file content for context
            try:
                content = repo.get_contents(file.filename, ref=pr.head.sha)
                full_content = content.decoded_content.decode('utf-8')
            except:
                full_content = ""
            
            # Get AI review
            review = self.reviewer.review_code(
                code_diff=diff,
                file_path=file.filename,
                context=full_content[:2000]  # First 2000 chars for context
            )
            
            all_reviews.append({
                "file": file.filename,
                "review": review
            })
            
            # Post inline comments for specific issues
            for issue in review["issues"]:
                if issue.get("line_number"):
                    pr.create_review_comment(
                        body=issue["description"],
                        commit=pr.get_commits().reversed[0],
                        path=file.filename,
                        line=issue["line_number"]
                    )
        
        # Post summary comment
        summary = self._create_summary(all_reviews)
        pr.create_issue_comment(summary)
        
        return all_reviews
    
    def _should_review(self, filename):
        reviewable_extensions = ['.py', '.js', '.ts', '.java', '.go', '.rs']
        return any(filename.endswith(ext) for ext in reviewable_extensions)
    
    def _create_summary(self, reviews):
        total_issues = sum(len(r["review"]["issues"]) for r in reviews)
        
        summary = f"""## 🤖 AI Code Review Summary

**Files Reviewed:** {len(reviews)}
**Issues Found:** {total_issues}

### Detailed Findings:

"""
        for review in reviews:
            summary += f"#### `{review['file']}`\n"
            summary += review["review"]["full_review"][:500] + "\n\n"
        
        summary += "\n---\n*This review was generated by AI. Please verify suggestions before applying.*"
        
        return summary
```

### Your Role & Responsibilities
- Fine-tuned CodeLlama model using LoRA on 10,000 code review examples
- Built GitHub webhook integration for automatic PR reviews
- Implemented context-aware review using RAG for coding standards
- Set up CI/CD pipeline for model deployment
- Achieved 78% acceptance rate for AI suggestions

### Challenges You Faced
1. **Context length limits** - Implemented smart chunking to review large files in pieces
2. **False positives** - Added confidence scoring and filtering
3. **Language-specific rules** - Created separate prompts for different programming languages
4. **Latency** - Used quantization (QLoRA) to reduce inference time

---

## Project 5: Multi-Agent Research Assistant

### Client Domain: Consulting / Research
### Duration: 3 months
### Team Size: 3 members

### Business Problem
Research analysts spend 2-3 days gathering information for market research reports. Client wants an AI system to automate initial research and draft reports.

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Orchestrator Agent                          │
│                   (Plans and coordinates)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │   Search    │     │   Analysis  │     │   Writer    │
   │   Agent     │     │   Agent     │     │   Agent     │
   └─────────────┘     └─────────────┘     └─────────────┘
          │                   │                   │
          ▼                   ▼                   ▼
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │  Web Search │     │  Data       │     │  Document   │
   │  Tools      │     │  Processing │     │  Generation │
   └─────────────┘     └─────────────┘     └─────────────┘
```

### Technical Implementation

**1. Agent Framework Setup**
```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun

class ResearchAgentSystem:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.1)
        self.search_tool = DuckDuckGoSearchRun()
        
        # Define agents
        self.research_agent = Agent(
            role='Research Analyst',
            goal='Find comprehensive and accurate information on the given topic',
            backstory="""You are an expert research analyst with 10 years of experience
            in market research. You excel at finding relevant information from multiple
            sources and identifying key trends.""",
            tools=[self._create_search_tool(), self._create_news_tool()],
            llm=self.llm,
            verbose=True
        )
        
        self.analysis_agent = Agent(
            role='Data Analyst',
            goal='Analyze research findings and extract actionable insights',
            backstory="""You are a senior data analyst specializing in synthesizing
            information from multiple sources. You identify patterns, trends, and
            provide data-driven recommendations.""",
            llm=self.llm,
            verbose=True
        )
        
        self.writer_agent = Agent(
            role='Report Writer',
            goal='Create well-structured, professional research reports',
            backstory="""You are an experienced business writer who creates clear,
            concise, and compelling research reports for executive audiences.""",
            llm=self.llm,
            verbose=True
        )
    
    def _create_search_tool(self):
        return Tool(
            name="Web Search",
            func=self.search_tool.run,
            description="Search the web for current information on any topic"
        )
    
    def _create_news_tool(self):
        def search_news(query):
            # Custom news search implementation
            return self.search_tool.run(f"{query} news latest 2024")
        
        return Tool(
            name="News Search",
            func=search_news,
            description="Search for recent news articles on a topic"
        )
    
    def run_research(self, topic, specific_questions=None):
        # Define tasks
        research_task = Task(
            description=f"""Research the following topic thoroughly: {topic}
            
            Specific areas to cover:
            1. Market size and growth trends
            2. Key players and market share
            3. Recent developments and news
            4. Challenges and opportunities
            5. Future outlook
            
            Additional questions to answer: {specific_questions or 'None'}
            
            Provide detailed findings with sources.""",
            agent=self.research_agent,
            expected_output="Comprehensive research findings with sources"
        )
        
        analysis_task = Task(
            description="""Analyze the research findings and:
            1. Identify key trends and patterns
            2. Compare different data points
            3. Highlight opportunities and risks
            4. Provide data-driven recommendations
            
            Create a structured analysis with clear insights.""",
            agent=self.analysis_agent,
            expected_output="Structured analysis with insights and recommendations",
            context=[research_task]
        )
        
        writing_task = Task(
            description="""Create a professional research report with:
            1. Executive Summary
            2. Market Overview
            3. Key Findings
            4. Competitive Landscape
            5. Trends and Opportunities
            6. Recommendations
            7. Appendix with sources
            
            Format in clean markdown. Be concise but comprehensive.""",
            agent=self.writer_agent,
            expected_output="Professional research report in markdown format",
            context=[research_task, analysis_task]
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[self.research_agent, self.analysis_agent, self.writer_agent],
            tasks=[research_task, analysis_task, writing_task],
            process=Process.sequential,
            verbose=2
        )
        
        result = crew.kickoff()
        return result
```

**2. Custom Tools with Memory**
```python
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import chromadb

class ResearchMemory:
    def __init__(self):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection("research_memory")
        self.short_term_memory = ConversationBufferWindowMemory(k=10)
    
    def store_finding(self, finding, source, topic):
        self.collection.add(
            documents=[finding],
            metadatas=[{"source": source, "topic": topic}],
            ids=[f"{topic}_{hash(finding)}"]
        )
    
    def retrieve_relevant(self, query, n_results=5):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

class FactCheckerTool:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = PromptTemplate(
            input_variables=["claim", "sources"],
            template="""Verify the following claim against the provided sources:
            
            Claim: {claim}
            
            Sources: {sources}
            
            Provide:
            1. Verification status (Verified/Partially Verified/Unverified)
            2. Supporting evidence
            3. Contradicting evidence (if any)
            4. Confidence level (High/Medium/Low)
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def verify(self, claim, sources):
        return self.chain.run(claim=claim, sources=sources)
```

**3. Report Generation with Structured Output**
```python
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain.output_parsers import PydanticOutputParser

class MarketInsight(BaseModel):
    insight: str
    supporting_data: str
    confidence: str
    source: str

class CompetitorInfo(BaseModel):
    name: str
    market_share: Optional[str]
    strengths: List[str]
    weaknesses: List[str]

class ResearchReport(BaseModel):
    title: str
    executive_summary: str
    market_size: str
    growth_rate: str
    key_insights: List[MarketInsight]
    competitors: List[CompetitorInfo]
    opportunities: List[str]
    risks: List[str]
    recommendations: List[str]
    sources: List[str]

class StructuredReportGenerator:
    def __init__(self, llm):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=ResearchReport)
    
    def generate_report(self, research_data, analysis_data):
        prompt = f"""Based on the following research and analysis, create a structured report.

Research Data:
{research_data}

Analysis:
{analysis_data}

{self.parser.get_format_instructions()}
"""
        
        response = self.llm.predict(prompt)
        report = self.parser.parse(response)
        
        return report
    
    def export_to_markdown(self, report: ResearchReport):
        md = f"""# {report.title}

## Executive Summary
{report.executive_summary}

## Market Overview
- **Market Size:** {report.market_size}
- **Growth Rate:** {report.growth_rate}

## Key Insights
"""
        for insight in report.key_insights:
            md += f"\n### {insight.insight}\n"
            md += f"- **Supporting Data:** {insight.supporting_data}\n"
            md += f"- **Confidence:** {insight.confidence}\n"
            md += f"- **Source:** {insight.source}\n"
        
        md += "\n## Competitive Landscape\n"
        for comp in report.competitors:
            md += f"\n### {comp.name}\n"
            md += f"- **Market Share:** {comp.market_share}\n"
            md += f"- **Strengths:** {', '.join(comp.strengths)}\n"
            md += f"- **Weaknesses:** {', '.join(comp.weaknesses)}\n"
        
        md += "\n## Opportunities\n"
        for opp in report.opportunities:
            md += f"- {opp}\n"
        
        md += "\n## Risks\n"
        for risk in report.risks:
            md += f"- {risk}\n"
        
        md += "\n## Recommendations\n"
        for rec in report.recommendations:
            md += f"- {rec}\n"
        
        md += "\n## Sources\n"
        for source in report.sources:
            md += f"- {source}\n"
        
        return md
```

### Your Role & Responsibilities
- Designed multi-agent architecture using CrewAI framework
- Implemented custom tools for web search, news aggregation, and fact-checking
- Built memory system using ChromaDB for cross-session research continuity
- Created structured output generation for consistent report format
- Deployed as API service on AWS ECS

### Challenges You Faced
1. **Agent hallucination** - Implemented fact-checking tool and source verification
2. **Coordination between agents** - Used hierarchical process with clear task dependencies
3. **Rate limiting** - Added retry logic and caching for API calls
4. **Output consistency** - Used Pydantic models for structured outputs

### Business Impact
- Reduced research time from 2-3 days to 4-6 hours
- Research analysts now focus on validation and insights rather than gathering
- 40% increase in research report throughput

---

## How to Discuss These Projects in Interviews

### Technical Depth Questions & Sample Answers

**Q: "Explain the architecture of your document processing system."**

A: "We built a serverless architecture on AWS. Documents uploaded to S3 trigger a Lambda function. This calls AWS Textract for OCR, then invokes our SageMaker endpoints - first for document classification using a fine-tuned LayoutLMv3 model, then for entity extraction using a BERT-based NER model. Results are stored in DynamoDB and exposed via API Gateway. We used Step Functions to orchestrate the workflow and handle retries."

**Q: "How did you handle class imbalance in the predictive maintenance project?"**

A: "We had only 2% failure cases. We used multiple techniques: SMOTE for synthetic oversampling during training, adjusted class weights in XGBoost (scale_pos_weight=10), and used precision-recall AUC instead of accuracy as our metric. We also implemented stratified k-fold cross-validation to ensure each fold had representative samples."

**Q: "What challenges did you face with RAG and how did you solve them?"**

A: "Main challenges were hallucination, retrieval quality, and latency. For hallucination, we added strict grounding prompts and implemented confidence scoring - if retrieved chunks had low similarity scores, we'd escalate to human. For retrieval, we used hybrid search combining semantic embeddings with BM25 keyword search, plus a re-ranking step using a cross-encoder. For latency, we cached frequent queries and used async processing."

**Q: "How did you fine-tune the model and why LoRA?"**

A: "We used LoRA because full fine-tuning of a 7B parameter model would need multiple high-end GPUs. LoRA only trains small adapter layers - about 0.1% of parameters - making it feasible on a single GPU. We used rank 16, alpha 32, targeted the attention layers, and trained for 3 epochs with learning rate 2e-4. This gave us 85% of full fine-tuning performance at 10% of the cost."

### Red Flags to Avoid

1. **Don't claim to have done everything alone** - Always mention team members
2. **Know your metrics** - Be ready with specific numbers (accuracy, latency, cost savings)
3. **Understand trade-offs** - Be ready to explain why you chose one approach over alternatives
4. **Know failure cases** - Discuss what didn't work and how you fixed it
5. **Business context matters** - Always connect technical work to business outcomes

---

## Next Steps for You

1. **Pick 2-3 projects** from above that match your interests
2. **Build simplified versions** - You don't need full scale, just working prototypes
3. **Document everything** - Create GitHub repos with proper READMEs
4. **Practice explaining** - Record yourself explaining architecture and decisions
5. **Prepare for deep dives** - Interviewers will probe specific areas

Would you like me to help you build any of these projects step by step?
