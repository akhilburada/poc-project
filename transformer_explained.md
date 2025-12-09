# Transformer Architecture: Complete Guide
## "Attention Is All You Need" - From Basics to Advanced

---

## Table of Contents
1. [Why Transformers?](#1-why-transformers---the-motivation)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Embedding Layer & Static Embedding Matrix](#3-embedding-layer--static-embedding-matrix)
4. [Positional Encoding](#4-positional-encoding)
5. [Self-Attention Mechanism](#5-self-attention-mechanism)
6. [Multi-Head Attention](#6-multi-head-attention)
7. [Feed-Forward Network](#7-feed-forward-network)
8. [Layer Normalization & Residual Connections](#8-layer-normalization--residual-connections)
9. [Encoder Stack](#9-encoder-stack)
10. [Decoder Stack](#10-decoder-stack)
11. [Training Process](#11-training-process)
12. [Interview Questions & Key Points](#12-interview-questions--key-points)

---

## 1. Why Transformers? - The Motivation

### Problems with Previous Architectures (RNN/LSTM)

```
RNN Processing (Sequential):
Word1 → Word2 → Word3 → Word4 → Word5
  ↓       ↓       ↓       ↓       ↓
  h1  →   h2  →   h3  →   h4  →   h5

Problems:
1. Sequential processing = slow (can't parallelize)
2. Long-range dependencies vanish (vanishing gradient)
3. Information bottleneck at each step
```

### Transformer Solution

```
Transformer Processing (Parallel):
Word1   Word2   Word3   Word4   Word5
  ↓       ↓       ↓       ↓       ↓
  ↔       ↔       ↔       ↔       ↔   ← All words attend to all others
  ↓       ↓       ↓       ↓       ↓
 Out1    Out2    Out3    Out4    Out5

Benefits:
1. Parallel processing = fast training
2. Direct connections between any two positions
3. No information bottleneck
```

---

## 2. High-Level Architecture

```
                    ┌─────────────────────────────────────────────────────┐
                    │              TRANSFORMER ARCHITECTURE                │
                    └─────────────────────────────────────────────────────┘

     ENCODER (Nx)                                    DECODER (Nx)
┌─────────────────────┐                      ┌─────────────────────────┐
│                     │                      │                         │
│  ┌───────────────┐  │                      │  ┌───────────────────┐  │
│  │ Feed Forward  │  │                      │  │   Feed Forward    │  │
│  │    Network    │  │                      │  │     Network       │  │
│  └───────┬───────┘  │                      │  └─────────┬─────────┘  │
│          │          │                      │            │            │
│    Add & Norm       │                      │      Add & Norm         │
│          │          │                      │            │            │
│  ┌───────┴───────┐  │                      │  ┌─────────┴─────────┐  │
│  │  Multi-Head   │  │   ─────────────────► │  │ Encoder-Decoder   │  │
│  │  Self-Attn    │  │   (K, V from Encoder)│  │    Attention      │  │
│  └───────┬───────┘  │                      │  └─────────┬─────────┘  │
│          │          │                      │            │            │
│    Add & Norm       │                      │      Add & Norm         │
│          ▲          │                      │            │            │
└──────────┼──────────┘                      │  ┌─────────┴─────────┐  │
           │                                 │  │  Masked Multi-Head│  │
    ┌──────┴──────┐                          │  │   Self-Attention  │  │
    │  Positional │                          │  └─────────┬─────────┘  │
    │  Encoding   │                          │            │            │
    │      +      │                          │      Add & Norm         │
    │  Input      │                          │            ▲            │
    │  Embedding  │                          └────────────┼────────────┘
    └─────────────┘                                       │
           ▲                                    ┌─────────┴─────────┐
           │                                    │    Positional     │
      Input Tokens                              │    Encoding +     │
      "The cat sat"                             │ Output Embedding  │
                                                └───────────────────┘
                                                         ▲
                                                         │
                                                   Output Tokens
                                                   (shifted right)
                                                   "<start> Le chat"
```

---

## 3. Embedding Layer & Static Embedding Matrix

### What is an Embedding?

An embedding converts discrete tokens (words) into continuous vector representations.

```
Vocabulary Size: V = 30,000 words
Embedding Dimension: d_model = 512

Embedding Matrix E: Shape = (V × d_model) = (30,000 × 512)

┌─────────────────────────────────────────────────────────────┐
│                    EMBEDDING MATRIX E                        │
│                    (30,000 × 512)                            │
├─────────────────────────────────────────────────────────────┤
│ Word Index │              512-dimensional vector             │
├────────────┼────────────────────────────────────────────────┤
│     0      │  [0.12, -0.34, 0.56, ..., 0.78]  ← "the"       │
│     1      │  [0.45, 0.23, -0.67, ..., 0.12]  ← "cat"       │
│     2      │  [-0.89, 0.34, 0.12, ..., -0.45] ← "sat"       │
│    ...     │  ...                                            │
│   29,999   │  [0.34, -0.56, 0.78, ..., 0.23]  ← "zebra"     │
└────────────┴────────────────────────────────────────────────┘
```

### How Embedding Matrix is Trained

```python
# The embedding matrix is a LEARNABLE PARAMETER
# It's trained via backpropagation along with the rest of the model

class Embedding:
    def __init__(self, vocab_size, d_model):
        # Initialize randomly (Xavier/He initialization)
        self.E = nn.Parameter(torch.randn(vocab_size, d_model) * 0.02)
    
    def forward(self, token_ids):
        # Simple lookup operation
        # token_ids: [batch_size, seq_len] e.g., [[45, 123, 67], [89, 234, 12]]
        # Returns: [batch_size, seq_len, d_model]
        return self.E[token_ids]  # Fancy indexing
```

### Training Process for Embeddings

```
Step 1: Random Initialization
┌──────────────────────────────────────────────────────────────┐
│ "cat" → [0.1, -0.3, 0.5, ...]   (random, meaningless)       │
│ "dog" → [0.8, 0.2, -0.1, ...]   (random, meaningless)       │
└──────────────────────────────────────────────────────────────┘

Step 2: Forward Pass
Input: "The cat sat on the mat"
         ↓
    Embeddings → Transformer → Output Prediction
                                     ↓
                              Loss Calculation
                              (Cross-Entropy)

Step 3: Backward Pass (Backpropagation)
                              Loss
                                ↓
    Gradients flow back through entire network
                                ↓
    ∂Loss/∂E computed for embedding matrix
                                ↓
    E_new = E_old - learning_rate × gradient

Step 4: After Training (Semantically Meaningful)
┌──────────────────────────────────────────────────────────────┐
│ "cat" → [0.7, 0.3, 0.9, ...]   Similar vectors!             │
│ "dog" → [0.6, 0.4, 0.8, ...]   ← semantically similar       │
│                                                              │
│ "car" → [-0.5, 0.8, -0.2, ...] Different vector             │
└──────────────────────────────────────────────────────────────┘
```

### Key Interview Points about Embeddings

1. **Embeddings are trained end-to-end** with the model
2. **Sparse to Dense**: One-hot (30,000 dims) → Dense (512 dims)
3. **Scaling**: Paper multiplies embeddings by √d_model for stability
4. **Tied Weights**: Some models share embedding & output projection weights

```python
# In the Transformer paper:
embedded = self.embedding(tokens) * math.sqrt(d_model)  # Scaling!
```

---

## 4. Positional Encoding

### The Problem

```
"Dog bites man" vs "Man bites dog"
        ↓                  ↓
Same words, different meanings!

Self-attention is PERMUTATION INVARIANT:
Attention("dog", "bites", "man") = Attention("man", "bites", "dog")

We need to inject position information!
```

### Sinusoidal Positional Encoding (Original Paper)

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

Where:
- pos = position in sequence (0, 1, 2, ...)
- i = dimension index (0, 1, 2, ..., d_model/2)
- d_model = 512
```

### Visual Representation

```
Position →     0        1        2        3        4
            ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
Dim 0 (sin) │ 0.0 │  │ 0.84│  │ 0.91│  │ 0.14│  │-0.76│
Dim 1 (cos) │ 1.0 │  │ 0.54│  │-0.42│  │-0.99│  │-0.65│
Dim 2 (sin) │ 0.0 │  │ 0.02│  │ 0.03│  │ 0.05│  │ 0.06│  ← Lower frequency
Dim 3 (cos) │ 1.0 │  │ 0.99│  │ 0.99│  │ 0.99│  │ 0.99│
    ...     │ ... │  │ ... │  │ ... │  │ ... │  │ ... │
            └─────┘  └─────┘  └─────┘  └─────┘  └─────┘

Final Input = Embedding + Positional Encoding
```

### Why Sinusoidal?

```python
# 1. Unique encoding for each position
# 2. Relative positions can be learned (PE[pos+k] is linear function of PE[pos])
# 3. Extrapolates to longer sequences than seen in training
# 4. No additional parameters to learn

def positional_encoding(seq_len, d_model):
    PE = torch.zeros(seq_len, d_model)
    position = torch.arange(0, seq_len).unsqueeze(1)  # [seq_len, 1]
    
    div_term = torch.exp(
        torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model)
    )
    
    PE[:, 0::2] = torch.sin(position * div_term)  # Even indices
    PE[:, 1::2] = torch.cos(position * div_term)  # Odd indices
    
    return PE  # [seq_len, d_model]
```

### Learned vs Fixed Positional Encoding

| Fixed (Sinusoidal) | Learned |
|-------------------|---------|
| No extra parameters | Adds V × d_model parameters |
| Extrapolates to longer sequences | Limited to training length |
| Used in original Transformer | Used in BERT, GPT |

---

## 5. Self-Attention Mechanism

### The Core Intuition

```
"The animal didn't cross the street because it was too tired"
                                          ↑
                                    What does "it" refer to?

Self-attention helps model learn: "it" → "animal" (high attention weight)
                                 "it" → "street" (low attention weight)
```

### Query, Key, Value Analogy

```
Think of it like a search/retrieval system:

Query (Q): "What am I looking for?"
Key (K):   "What information do I have?"  
Value (V): "What do I return?"

Example: Library search
─────────────────────────────────────────────────────────
Your Query: "machine learning book"

Book Keys (titles/tags):         | Book Values (actual content):
─────────────────────────────────|─────────────────────────────
"Deep Learning Basics"      →    │ [Full book content...]
"Cooking Italian Food"      →    │ [Full book content...]
"Neural Networks Guide"     →    │ [Full book content...]

Attention Scores:
"Deep Learning Basics"   : 0.7  (high similarity to query)
"Cooking Italian Food"   : 0.05 (low similarity)
"Neural Networks Guide"  : 0.25 (medium similarity)

Output = Weighted sum of Values based on attention scores
```

### Mathematical Formulation

```
Input: X ∈ ℝ^(seq_len × d_model)   e.g., (10 × 512)

Step 1: Create Q, K, V using linear projections
─────────────────────────────────────────────────
Q = X × W_Q    where W_Q ∈ ℝ^(d_model × d_k)     → Q ∈ ℝ^(seq_len × d_k)
K = X × W_K    where W_K ∈ ℝ^(d_model × d_k)     → K ∈ ℝ^(seq_len × d_k)
V = X × W_V    where W_V ∈ ℝ^(d_model × d_v)     → V ∈ ℝ^(seq_len × d_v)

In original paper: d_k = d_v = d_model / num_heads = 512/8 = 64

Step 2: Compute Attention Scores
─────────────────────────────────────────────────
                    Q × K^T
Attention(Q,K,V) = softmax(─────────) × V
                           √d_k

Why √d_k scaling?
- Q × K^T produces values with variance ≈ d_k
- Large values → softmax saturates → vanishing gradients
- Dividing by √d_k normalizes variance back to 1
```

### Step-by-Step Example

```
Sentence: "I love AI" (3 tokens)
d_model = 4, d_k = 4 (simplified)

Step 1: Input Embeddings X (3 × 4)
┌─────────────────────────────┐
│ "I"    → [1.0, 0.5, 0.3, 0.8] │
│ "love" → [0.2, 0.9, 0.7, 0.1] │
│ "AI"   → [0.8, 0.3, 0.6, 0.9] │
└─────────────────────────────┘

Step 2: Linear Projections (learned weights)
Q = X × W_Q    K = X × W_K    V = X × W_V

Example Q (after projection):
┌─────────────────────────────┐
│ q_I    = [0.5, 0.8, 0.2, 0.3] │
│ q_love = [0.7, 0.1, 0.9, 0.4] │
│ q_AI   = [0.3, 0.6, 0.5, 0.7] │
└─────────────────────────────┘

Step 3: Compute Q × K^T (3 × 3 attention scores)
                     k_I   k_love  k_AI
              ┌─────────────────────────┐
    q_I       │ 1.2    0.8     0.9      │  ← How much "I" attends to each
    q_love    │ 0.6    1.5     0.7      │  ← How much "love" attends to each
    q_AI      │ 0.8    0.7     1.3      │  ← How much "AI" attends to each
              └─────────────────────────┘

Step 4: Scale by √d_k = √4 = 2
              ┌─────────────────────────┐
              │ 0.6    0.4     0.45     │
              │ 0.3    0.75    0.35     │
              │ 0.4    0.35    0.65     │
              └─────────────────────────┘

Step 5: Apply Softmax (row-wise)
              ┌─────────────────────────┐
              │ 0.38   0.30    0.32     │  Each row sums to 1.0
              │ 0.27   0.43    0.30     │
              │ 0.32   0.29    0.39     │
              └─────────────────────────┘
              
Step 6: Multiply by V
Output = Attention_weights × V

For "I": output_I = 0.38 × v_I + 0.30 × v_love + 0.32 × v_AI
                  = weighted combination of all value vectors
```

### Self-Attention Code

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q, K, V: [batch_size, seq_len, d_k]
    mask: [batch_size, 1, seq_len] or [batch_size, seq_len, seq_len]
    """
    d_k = Q.size(-1)
    
    # Step 1: Q × K^T → [batch, seq_len, seq_len]
    scores = torch.matmul(Q, K.transpose(-2, -1))
    
    # Step 2: Scale
    scores = scores / math.sqrt(d_k)
    
    # Step 3: Mask (optional, for decoder)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))
    
    # Step 4: Softmax
    attention_weights = F.softmax(scores, dim=-1)
    
    # Step 5: Weighted sum with V
    output = torch.matmul(attention_weights, V)
    
    return output, attention_weights
```

---

## 6. Multi-Head Attention

### Why Multiple Heads?

```
Single attention head might focus on one aspect:
- Head 1 might learn: syntax (subject-verb agreement)
- Head 2 might learn: coreference (pronouns → nouns)
- Head 3 might learn: semantic similarity
- Head 4 might learn: positional patterns

Multiple heads allow model to attend to different aspects simultaneously!
```

### Multi-Head Attention Architecture

```
                           Input X
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
      ┌─────────┐        ┌─────────┐        ┌─────────┐
      │ Head 1  │        │ Head 2  │   ...  │ Head h  │
      │ (Q,K,V) │        │ (Q,K,V) │        │ (Q,K,V) │
      │ d_k=64  │        │ d_k=64  │        │ d_k=64  │
      └────┬────┘        └────┬────┘        └────┬────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                        Concatenate
                              │
                       [seq_len, h × d_k]
                       [seq_len, 8 × 64]
                       [seq_len, 512]
                              │
                        ┌─────┴─────┐
                        │  Linear   │
                        │   W_O     │
                        └─────┬─────┘
                              │
                        Output (d_model)
```

### Mathematical Formulation

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) × W_O

where head_i = Attention(Q × W_Q^i, K × W_K^i, V × W_V^i)

Parameters:
- h = 8 heads (in original paper)
- d_model = 512
- d_k = d_v = d_model / h = 64

Learnable Parameters:
- W_Q^i ∈ ℝ^(d_model × d_k) = (512 × 64) × 8 heads
- W_K^i ∈ ℝ^(d_model × d_k) = (512 × 64) × 8 heads
- W_V^i ∈ ℝ^(d_model × d_v) = (512 × 64) × 8 heads
- W_O ∈ ℝ^(h×d_v × d_model) = (512 × 512)
```

### Multi-Head Attention Code

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, num_heads=8):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads  # 64
        
        # Linear projections for all heads (combined for efficiency)
        self.W_Q = nn.Linear(d_model, d_model)  # 512 → 512
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)
        
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # 1. Linear projection and split into heads
        # [batch, seq_len, d_model] → [batch, seq_len, num_heads, d_k]
        Q = self.W_Q(Q).view(batch_size, -1, self.num_heads, self.d_k)
        K = self.W_K(K).view(batch_size, -1, self.num_heads, self.d_k)
        V = self.W_V(V).view(batch_size, -1, self.num_heads, self.d_k)
        
        # 2. Transpose for attention: [batch, num_heads, seq_len, d_k]
        Q = Q.transpose(1, 2)
        K = K.transpose(1, 2)
        V = V.transpose(1, 2)
        
        # 3. Compute attention for all heads in parallel
        attn_output, attn_weights = scaled_dot_product_attention(Q, K, V, mask)
        
        # 4. Concatenate heads
        # [batch, num_heads, seq_len, d_k] → [batch, seq_len, d_model]
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.view(batch_size, -1, self.d_model)
        
        # 5. Final linear projection
        output = self.W_O(attn_output)
        
        return output
```

---

## 7. Feed-Forward Network

### Position-wise Feed-Forward Network

```
Applied to each position INDEPENDENTLY and IDENTICALLY.

FFN(x) = max(0, x × W_1 + b_1) × W_2 + b_2
       = ReLU(x × W_1 + b_1) × W_2 + b_2

Dimensions:
- Input:  d_model = 512
- Hidden: d_ff = 2048 (4× expansion)
- Output: d_model = 512

This is essentially two linear layers with ReLU in between.
```

### Visual Representation

```
Input: [batch, seq_len, 512]
              │
              ▼
    ┌─────────────────────┐
    │   Linear (512→2048) │
    │       + ReLU        │
    └──────────┬──────────┘
               │
    [batch, seq_len, 2048]
               │
               ▼
    ┌─────────────────────┐
    │  Linear (2048→512)  │
    └──────────┬──────────┘
               │
Output: [batch, seq_len, 512]
```

### Why FFN?

1. **Non-linearity**: Attention is essentially linear (weighted sums)
2. **Capacity**: Adds more parameters and representational power
3. **Per-position processing**: Different transformation at each position
4. **Memory**: Can store factual knowledge in weights

### FFN Code

```python
class FeedForward(nn.Module):
    def __init__(self, d_model=512, d_ff=2048, dropout=0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        # x: [batch, seq_len, d_model]
        x = self.linear1(x)           # [batch, seq_len, d_ff]
        x = F.relu(x)                 # ReLU activation
        x = self.dropout(x)
        x = self.linear2(x)           # [batch, seq_len, d_model]
        return x
```

---

## 8. Layer Normalization & Residual Connections

### Residual Connections (Skip Connections)

```
                    ┌───────────────┐
        x ─────────►│   Sublayer    │──────► Sublayer(x)
        │           │ (Attention or │              │
        │           │     FFN)      │              │
        │           └───────────────┘              │
        │                                          │
        └──────────────────────────────────────────┤
                                                   ▼
                                            x + Sublayer(x)
                                            (Residual Add)

Benefits:
1. Helps with gradient flow in deep networks
2. Allows easier optimization
3. Model can learn identity function if needed
```

### Layer Normalization

```
LayerNorm normalizes across the feature dimension (not batch!)

Input x: [batch, seq_len, d_model]

For each position independently:
μ = mean(x)           # across d_model dimension
σ = std(x)            # across d_model dimension
x_norm = (x - μ) / (σ + ε)
output = γ × x_norm + β    # γ, β are learnable parameters

Why LayerNorm (not BatchNorm)?
- Works with variable sequence lengths
- Independent of batch size
- More stable for transformers
```

### Pre-LN vs Post-LN

```
Original Paper (Post-LN):
    x → Sublayer → Add(x, ·) → LayerNorm

Modern Practice (Pre-LN):
    x → LayerNorm → Sublayer → Add(x, ·)

Pre-LN is more stable for training deep transformers!
```

### Complete Sublayer with Residual + LayerNorm

```python
class SublayerConnection(nn.Module):
    """
    Residual connection + Layer normalization
    """
    def __init__(self, d_model, dropout=0.1):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x, sublayer_fn):
        # Post-LN (original): 
        # return self.norm(x + self.dropout(sublayer_fn(x)))
        
        # Pre-LN (better):
        return x + self.dropout(sublayer_fn(self.norm(x)))
```

---

## 9. Encoder Stack

### Single Encoder Layer

```
                        Input
                          │
                          ▼
              ┌───────────────────────┐
              │    Layer Norm         │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │   Multi-Head          │
              │   Self-Attention      │
              └───────────┬───────────┘
                          │
           ┌──────────────┼──────────────┐
           │              │              │
           │              ▼              │
           │        Dropout              │
           │              │              │
           │              ▼              │
           └─────────►   Add   ◄─────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │    Layer Norm         │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │   Feed-Forward        │
              │   Network             │
              └───────────┬───────────┘
                          │
           ┌──────────────┼──────────────┐
           │              │              │
           │              ▼              │
           │        Dropout              │
           │              │              │
           │              ▼              │
           └─────────►   Add   ◄─────────┘
                          │
                        Output
```

### Encoder Code

```python
class EncoderLayer(nn.Module):
    def __init__(self, d_model=512, num_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.ffn = FeedForward(d_model, d_ff, dropout)
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        
    def forward(self, x, mask=None):
        # Self-attention with residual
        attn_output = self.self_attn(x, x, x, mask)  # Q=K=V=x
        x = x + self.dropout1(attn_output)
        x = self.norm1(x)
        
        # FFN with residual
        ffn_output = self.ffn(x)
        x = x + self.dropout2(ffn_output)
        x = self.norm2(x)
        
        return x


class Encoder(nn.Module):
    def __init__(self, num_layers=6, d_model=512, num_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        self.layers = nn.ModuleList([
            EncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(d_model)  # Final normalization
        
    def forward(self, x, mask=None):
        for layer in self.layers:
            x = layer(x, mask)
        return self.norm(x)
```

---

## 10. Decoder Stack

### Key Differences from Encoder

1. **Masked Self-Attention**: Prevents attending to future tokens
2. **Cross-Attention**: Attends to encoder output (encoder-decoder attention)
3. **Three sub-layers** instead of two

### Masked Self-Attention

```
For autoregressive generation, position i can only attend to positions ≤ i

Attention Mask (for sequence length 5):
     Position:  0    1    2    3    4
            ┌─────────────────────────┐
Position 0  │  1    0    0    0    0  │  Can only see itself
Position 1  │  1    1    0    0    0  │  Can see 0, 1
Position 2  │  1    1    1    0    0  │  Can see 0, 1, 2
Position 3  │  1    1    1    1    0  │  Can see 0, 1, 2, 3
Position 4  │  1    1    1    1    1  │  Can see all
            └─────────────────────────┘

1 = can attend, 0 = cannot attend (masked with -inf before softmax)
```

### Cross-Attention (Encoder-Decoder Attention)

```
In cross-attention:
- Query (Q): comes from DECODER
- Key (K), Value (V): come from ENCODER output

This allows decoder to "look at" the input sequence while generating.

Example: Translation
Encoder Input: "I love you"
Encoder Output: Contextual representations

Decoder generating "Je t'aime":
- When generating "t'" → Q from decoder, K,V from encoder
- High attention on "love" to generate "t'aime"
```

### Decoder Layer Code

```python
class DecoderLayer(nn.Module):
    def __init__(self, d_model=512, num_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        # Masked self-attention
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        # Cross-attention (encoder-decoder)
        self.cross_attn = MultiHeadAttention(d_model, num_heads)
        # Feed-forward
        self.ffn = FeedForward(d_model, d_ff, dropout)
        
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        self.dropout3 = nn.Dropout(dropout)
        
    def forward(self, x, encoder_output, src_mask=None, tgt_mask=None):
        # 1. Masked self-attention
        attn1 = self.self_attn(x, x, x, tgt_mask)  # Q=K=V from decoder
        x = x + self.dropout1(attn1)
        x = self.norm1(x)
        
        # 2. Cross-attention
        attn2 = self.cross_attn(x, encoder_output, encoder_output, src_mask)
        # Q from decoder, K,V from encoder
        x = x + self.dropout2(attn2)
        x = self.norm2(x)
        
        # 3. Feed-forward
        ffn_out = self.ffn(x)
        x = x + self.dropout3(ffn_out)
        x = self.norm3(x)
        
        return x


def generate_square_subsequent_mask(sz):
    """Generate causal mask for decoder self-attention"""
    mask = torch.triu(torch.ones(sz, sz), diagonal=1)
    mask = mask.masked_fill(mask == 1, float('-inf'))
    return mask
```

---

## 11. Training Process

### Training Objective

```
For Machine Translation (Original Task):

Input (Encoder):  "The cat sat on the mat"
Target (Decoder): "<sos> Le chat est assis sur le tapis <eos>"

Loss: Cross-Entropy between predicted and actual next tokens

              Encoder                    Decoder
        "The cat sat..."          "<sos> Le chat est..."
              │                           │
              ▼                           ▼
         [Encoding]    ──────────►    [Decoding]
                                          │
                                          ▼
                                    Predictions
                                    P(Le|<sos>)
                                    P(chat|<sos> Le)
                                    P(est|<sos> Le chat)
                                          │
                                          ▼
                          Cross-Entropy Loss with Targets
```

### Teacher Forcing

```
During Training:
- Decoder receives GROUND TRUTH previous tokens
- Not its own predictions
- This accelerates training

Input to Decoder:  <sos> Le   chat  est   assis
Target Output:     Le    chat est   assis sur

During Inference:
- Decoder receives its OWN previous predictions
- Autoregressive generation
```

### Label Smoothing

```
Instead of hard targets [0, 0, 1, 0, 0], use soft targets:
[0.0167, 0.0167, 0.9, 0.0167, 0.0167]

ε = 0.1 (smoothing factor)
Confidence = 1 - ε = 0.9
Others = ε / (vocab_size - 1)

Benefits:
- Prevents overconfidence
- Better generalization
- Improves BLEU score
```

### Optimizer: Adam with Warmup

```
Learning Rate Schedule:

lrate = d_model^(-0.5) × min(step^(-0.5), step × warmup_steps^(-1.5))

          │
Learning  │    /\
Rate      │   /  \____________________
          │  /
          │ /
          └──────────────────────────────
                      Steps
            ↑
        Warmup Period (4000 steps)
        
Linear warmup then decay
```

### Training Hyperparameters (Original Paper)

```
┌────────────────────────────────────────────┐
│ Parameter              │ Value             │
├────────────────────────┼───────────────────┤
│ d_model                │ 512               │
│ d_ff                   │ 2048              │
│ num_heads              │ 8                 │
│ num_layers (encoder)   │ 6                 │
│ num_layers (decoder)   │ 6                 │
│ d_k = d_v             │ 64                │
│ Dropout                │ 0.1               │
│ Label Smoothing        │ 0.1               │
│ Batch Size             │ ~25,000 tokens    │
│ Warmup Steps           │ 4,000             │
│ Training Steps         │ 100,000           │
└────────────────────────┴───────────────────┘

Total Parameters: ~65 million (base model)
                  ~213 million (big model)
```

### Training Code Snippet

```python
class Transformer(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, d_model=512, num_heads=8, 
                 num_encoder_layers=6, num_decoder_layers=6, d_ff=2048, dropout=0.1):
        super().__init__()
        
        # Embeddings
        self.src_embed = nn.Embedding(src_vocab, d_model)
        self.tgt_embed = nn.Embedding(tgt_vocab, d_model)
        self.pos_encoding = PositionalEncoding(d_model, dropout)
        
        # Encoder & Decoder
        self.encoder = Encoder(num_encoder_layers, d_model, num_heads, d_ff, dropout)
        self.decoder = Decoder(num_decoder_layers, d_model, num_heads, d_ff, dropout)
        
        # Output projection
        self.output_proj = nn.Linear(d_model, tgt_vocab)
        
        # Initialize parameters
        self._init_parameters()
        
    def _init_parameters(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
                
    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        # Encode
        src_emb = self.pos_encoding(self.src_embed(src) * math.sqrt(self.d_model))
        enc_output = self.encoder(src_emb, src_mask)
        
        # Decode
        tgt_emb = self.pos_encoding(self.tgt_embed(tgt) * math.sqrt(self.d_model))
        dec_output = self.decoder(tgt_emb, enc_output, src_mask, tgt_mask)
        
        # Project to vocabulary
        logits = self.output_proj(dec_output)
        return logits


# Training Loop
def train_step(model, src, tgt, optimizer, criterion):
    model.train()
    optimizer.zero_grad()
    
    # Shift target for teacher forcing
    tgt_input = tgt[:, :-1]   # <sos> Le chat est
    tgt_output = tgt[:, 1:]   # Le chat est <eos>
    
    # Create masks
    tgt_mask = generate_square_subsequent_mask(tgt_input.size(1))
    
    # Forward pass
    logits = model(src, tgt_input, tgt_mask=tgt_mask)
    
    # Compute loss
    loss = criterion(logits.view(-1, logits.size(-1)), tgt_output.view(-1))
    
    # Backward pass
    loss.backward()
    optimizer.step()
    
    return loss.item()
```

---

## 12. Interview Questions & Key Points

### Frequently Asked Questions

#### Q1: Why is it called "Self-Attention"?
```
"Self" because Q, K, V all come from the SAME sequence.
The sequence attends to itself.

In cross-attention (encoder-decoder), Q comes from one sequence
and K, V come from another.
```

#### Q2: What is the complexity of self-attention?
```
Time Complexity: O(n² × d)
- n = sequence length
- d = dimension
- n² from Q × K^T matrix multiplication

Space Complexity: O(n²) for attention matrix

This is why Transformers struggle with very long sequences!
Solutions: Sparse attention, Linear attention, etc.
```

#### Q3: Why multiple heads instead of one large head?
```
1. Multiple heads can attend to different positions/aspects
2. Computationally efficient (parallel processing)
3. Richer representation learning

With d_model=512 and 8 heads:
- Each head: d_k = 64
- Total computation similar to single 512-dim attention
- But more expressive!
```

#### Q4: Why scale by √d_k?
```
Without scaling:
- Q and K have values with variance 1
- Q × K^T has variance d_k (sum of d_k independent products)
- Large values → softmax saturates → small gradients

With scaling by √d_k:
- Q × K^T / √d_k has variance 1
- Softmax works in good gradient region
```

#### Q5: Difference between Pre-LN and Post-LN?
```
Post-LN (Original):  x → Sublayer → Add → LN
Pre-LN (Better):     x → LN → Sublayer → Add

Pre-LN advantages:
- More stable training
- Easier to train deep models
- Gradients flow more easily
```

#### Q6: How does Transformer handle variable-length sequences?
```
1. Padding: Add <pad> tokens to make batch same length
2. Padding Mask: Prevent attention to <pad> tokens
3. Positional Encoding: Provides position info regardless of length
```

#### Q7: Why is FFN important?
```
1. Attention is essentially linear (weighted sums)
2. FFN adds non-linearity (ReLU/GeLU)
3. Increases model capacity
4. Acts as "memory" storing factual knowledge
```

### Key Formulas to Remember

```
1. Attention:
   Attention(Q,K,V) = softmax(QK^T / √d_k) × V

2. Multi-Head:
   MultiHead(Q,K,V) = Concat(head_1,...,head_h) × W_O
   head_i = Attention(Q×W_Q^i, K×W_K^i, V×W_V^i)

3. FFN:
   FFN(x) = ReLU(x×W_1 + b_1) × W_2 + b_2

4. Positional Encoding:
   PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
   PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

5. Learning Rate:
   lr = d_model^(-0.5) × min(step^(-0.5), step × warmup^(-1.5))
```

### Parameter Count

```
For base Transformer (d_model=512, d_ff=2048, vocab=30000):

Embeddings: 30000 × 512 = 15.36M (×2 for src & tgt if not shared)
Per Encoder Layer:
  - Self-Attn: 4 × (512 × 512) = 1.05M
  - FFN: (512 × 2048) + (2048 × 512) = 2.1M
  - LayerNorm: 2 × 512 = negligible
  Total per layer: ~3.15M
  
6 Encoder Layers: 6 × 3.15M = 18.9M
6 Decoder Layers: 6 × (3.15M + 1.05M cross-attn) = 25.2M
Output Projection: 512 × 30000 = 15.36M

Total: ~65M parameters
```

### Evolution of Transformers

```
Original Transformer (2017)
    │
    ├── BERT (2018): Encoder-only, bidirectional
    │
    ├── GPT (2018-2023): Decoder-only, autoregressive
    │
    ├── T5 (2019): Encoder-decoder, text-to-text
    │
    └── Modern LLMs: GPT-4, Claude, LLaMA, etc.

Key innovations since original:
1. Pre-training on massive data
2. Scaling laws
3. RLHF (Reinforcement Learning from Human Feedback)
4. Sparse attention for long sequences
5. Rotary position embeddings (RoPE)
6. Flash Attention (efficient implementation)
7. Mixture of Experts (MoE)
```

---

## Quick Reference Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRANSFORMER AT A GLANCE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Input: "Hello world"                                                        │
│         ↓                                                                    │
│  ┌──────────────────┐                                                        │
│  │ 1. Tokenization  │ → [101, 7592, 2088, 102]                              │
│  └────────┬─────────┘                                                        │
│           ↓                                                                  │
│  ┌──────────────────┐                                                        │
│  │ 2. Embedding     │ → [4, 512] float vectors                              │
│  │    × √d_model    │                                                        │
│  └────────┬─────────┘                                                        │
│           ↓                                                                  │
│  ┌──────────────────┐                                                        │
│  │ 3. + Position    │ → [4, 512] with position info                         │
│  │    Encoding      │                                                        │
│  └────────┬─────────┘                                                        │
│           ↓                                                                  │
│  ┌──────────────────────────────────────────────────────────────┐           │
│  │ 4. ENCODER (×6)                                               │           │
│  │    ┌─────────────────────────────────────────────────────┐   │           │
│  │    │ Multi-Head Self-Attention + Add&Norm                │   │           │
│  │    │ Feed-Forward Network + Add&Norm                     │   │           │
│  │    └─────────────────────────────────────────────────────┘   │           │
│  └────────┬─────────────────────────────────────────────────────┘           │
│           ↓                                                                  │
│  ┌──────────────────────────────────────────────────────────────┐           │
│  │ 5. DECODER (×6)                                               │           │
│  │    ┌─────────────────────────────────────────────────────┐   │           │
│  │    │ Masked Multi-Head Self-Attention + Add&Norm         │   │           │
│  │    │ Cross-Attention (Q:dec, K,V:enc) + Add&Norm         │   │           │
│  │    │ Feed-Forward Network + Add&Norm                     │   │           │
│  │    └─────────────────────────────────────────────────────┘   │           │
│  └────────┬─────────────────────────────────────────────────────┘           │
│           ↓                                                                  │
│  ┌──────────────────┐                                                        │
│  │ 6. Linear +      │ → Vocabulary probabilities                            │
│  │    Softmax       │                                                        │
│  └──────────────────┘                                                        │
│                                                                              │
│  Output: "Bonjour monde" (translation example)                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Good Luck with Your Interview! 🚀

Remember:
1. Understand the intuition, not just formulas
2. Be able to explain Q, K, V clearly
3. Know the complexity trade-offs
4. Understand why each component exists
5. Be familiar with modern variants (GPT, BERT)
