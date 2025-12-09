# Transformer Deep Dive: Complete Data Flow Analysis

## The Journey of a Single Input Through the Transformer

We'll trace **exactly** what happens to this input:
- **Source sentence**: "I love AI" (English)
- **Target sentence**: "J'aime l'IA" (French)

### Configuration (Original Paper)
```
d_model = 512       # Embedding dimension
d_k = d_v = 64      # Key/Value dimension per head
num_heads = 8       # Number of attention heads
d_ff = 2048         # Feed-forward inner dimension
num_layers = 6      # Encoder and Decoder layers
vocab_size = 37000  # Vocabulary size
```

---

# PART 1: INPUT PREPROCESSING (Before Encoder)

## Step 1.1: Tokenization

**Raw Input**: `"I love AI"`

**Tokenization Process**:
```
"I love AI" → Tokenizer → ["I", "love", "AI"]
```

**Token to ID mapping** (from vocabulary):
```
"I"    → 45
"love" → 2891
"AI"   → 15234
```

**Result**: `token_ids = [45, 2891, 15234]`
- Shape: `(3,)` → just 3 integers

**With batch dimension**:
```
token_ids = [[45, 2891, 15234]]
Shape: (batch_size=1, seq_len=3)
```

---

## Step 1.2: Token Embedding Lookup

### The Embedding Matrix

```
Embedding Matrix E: Shape (37000, 512)
                    ↑         ↑
              vocab_size   d_model

This is a LEARNED parameter matrix with 37000 × 512 = 18,944,000 parameters
```

**Visual of E**:
```
              d_model=512 columns
         ┌─────────────────────────────┐
Token 0  │ 0.023  -0.15   0.08  ...    │  ← 512 values for token 0
Token 1  │ 0.11   0.045  -0.23  ...    │  ← 512 values for token 1
Token 2  │ -0.08  0.19   0.002  ...    │
   ⋮     │   ⋮      ⋮      ⋮           │
Token 45 │ 0.34  -0.12   0.56  ...    │  ← This is "I"
   ⋮     │   ⋮      ⋮      ⋮           │
Token 2891│-0.21  0.78   0.11  ...    │  ← This is "love"
   ⋮     │   ⋮      ⋮      ⋮           │
Token 15234│0.44 -0.33   0.67  ...    │  ← This is "AI"
   ⋮     │   ⋮      ⋮      ⋮           │
Token 36999│0.01  0.09  -0.05  ...    │
         └─────────────────────────────┘
         37000 rows (one per vocabulary token)
```

### Embedding Lookup Operation

```python
# Input: token_ids = [[45, 2891, 15234]]
# Operation: E[token_ids]  (fancy indexing)

X_embed = E[[45, 2891, 15234]]  # Select rows 45, 2891, 15234
```

**Result**:
```
X_embed: Shape (1, 3, 512)
         ↑  ↑   ↑
      batch seq d_model

X_embed[0] = [
    [0.34, -0.12, 0.56, ..., 0.23],   # 512 values for "I"
    [-0.21, 0.78, 0.11, ..., -0.45],  # 512 values for "love"
    [0.44, -0.33, 0.67, ..., 0.89]    # 512 values for "AI"
]
```

### Scaling Factor

The paper multiplies embeddings by √d_model:
```python
X_embed = X_embed * sqrt(512)  # = X_embed * 22.627

# Why? To balance the magnitude with positional encodings
# Embeddings are initialized small (~N(0, 0.02))
# After scaling: ~N(0, 0.45) which matches PE magnitude
```

---

## Step 1.3: Positional Encoding

### Why Positional Encoding?

Self-attention has **no notion of order**. These produce identical outputs:
```
Attention("I love AI") == Attention("AI love I")  # Without PE!
```

### Sinusoidal Positional Encoding Formula

For position `pos` and dimension `i`:
```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

### Computing PE for Our 3 Positions

**For position 0 ("I")**:
```
PE[0, 0] = sin(0 / 10000^(0/512))   = sin(0)     = 0.0
PE[0, 1] = cos(0 / 10000^(0/512))   = cos(0)     = 1.0
PE[0, 2] = sin(0 / 10000^(2/512))   = sin(0)     = 0.0
PE[0, 3] = cos(0 / 10000^(2/512))   = cos(0)     = 1.0
... (continues for all 512 dimensions)
```

**For position 1 ("love")**:
```
PE[1, 0] = sin(1 / 10000^(0/512))   = sin(1)     = 0.841
PE[1, 1] = cos(1 / 10000^(0/512))   = cos(1)     = 0.540
PE[1, 2] = sin(1 / 10000^(2/512))   = sin(0.985) = 0.834
PE[1, 3] = cos(1 / 10000^(2/512))   = cos(0.985) = 0.551
...
```

**For position 2 ("AI")**:
```
PE[2, 0] = sin(2 / 10000^(0/512))   = sin(2)     = 0.909
PE[2, 1] = cos(2 / 10000^(0/512))   = cos(2)     = -0.416
PE[2, 2] = sin(2 / 10000^(2/512))   = sin(1.970) = 0.922
PE[2, 3] = cos(2 / 10000^(2/512))   = cos(1.970) = -0.387
...
```

### PE Matrix for seq_len=3
```
PE: Shape (3, 512)

PE = [
    [0.000, 1.000, 0.000, 1.000, ..., -0.023, 0.999],  # pos 0
    [0.841, 0.540, 0.834, 0.551, ...,  0.012, 0.998],  # pos 1
    [0.909,-0.416, 0.922,-0.387, ...,  0.047, 0.996]   # pos 2
]
```

### Adding PE to Embeddings

```python
# X_embed: (1, 3, 512) - scaled token embeddings
# PE:      (3, 512)    - positional encodings

X = X_embed + PE  # Broadcasting adds PE to each batch

# X: Shape (1, 3, 512)
```

**Concrete example for first position**:
```
X[0, 0, :] = X_embed[0, 0, :] + PE[0, :]

X[0, 0, :] = [7.69, -2.72, 12.67, ..., 5.20]    # Scaled "I" embedding
           + [0.00,  1.00,  0.00, ..., 0.999]   # PE for position 0
           = [7.69, -1.72, 12.67, ..., 6.20]    # Final representation
```

### Dropout on Input

```python
X = Dropout(X, p=0.1)  # Randomly zero out 10% of values during training
# Shape remains (1, 3, 512)
```

---

# PART 2: ENCODER (6 Identical Layers)

## Encoder Input
```
X: Shape (1, 3, 512)
   ↑  ↑   ↑
batch seq d_model

X = [
    [[7.69, -1.72, 12.67, ..., 6.20],    # "I" + pos 0
     [3.45,  8.12,  2.89, ..., -4.23],   # "love" + pos 1
     [9.01, -5.67, 14.34, ..., 11.56]]   # "AI" + pos 2
]
```

---

## ENCODER LAYER 1 (of 6)

### Step 2.1: Pre-Layer Normalization (Optional - Many implementations use this)

The original paper uses Post-LN, but Pre-LN is now more common:

**Post-LN (Original)**: `X + Sublayer(X)` then normalize
**Pre-LN (Modern)**: `X + Sublayer(Norm(X))`

We'll follow Post-LN as per the original paper.

---

### Step 2.2: Multi-Head Self-Attention

#### 2.2.1: Linear Projections to Create Q, K, V

**Weight matrices** (LEARNED parameters):
```
W_Q: Shape (512, 512) - 262,144 parameters
W_K: Shape (512, 512) - 262,144 parameters  
W_V: Shape (512, 512) - 262,144 parameters
W_O: Shape (512, 512) - 262,144 parameters

Total for attention: 1,048,576 parameters (+ biases)
```

**Computing Q, K, V**:
```python
Q = X @ W_Q  # (1, 3, 512) @ (512, 512) = (1, 3, 512)
K = X @ W_K  # (1, 3, 512) @ (512, 512) = (1, 3, 512)
V = X @ W_V  # (1, 3, 512) @ (512, 512) = (1, 3, 512)
```

**Detailed matrix multiplication for Q**:
```
X[0] @ W_Q:

[x_I, x_love, x_AI] @ W_Q

Where x_I = [7.69, -1.72, 12.67, ..., 6.20] (512 values)

q_I = x_I @ W_Q
    = 7.69*W_Q[0,:] + (-1.72)*W_Q[1,:] + ... + 6.20*W_Q[511,:]
    = [q_0, q_1, ..., q_511]  # 512 values
```

**Result**:
```
Q = [[[q_I_0, ..., q_I_511],      # Query for "I"
      [q_love_0, ..., q_love_511],# Query for "love"  
      [q_AI_0, ..., q_AI_511]]]   # Query for "AI"

Shape: (1, 3, 512)
```

Same process gives us K and V with the same shape.

#### 2.2.2: Split into 8 Heads

```python
# Reshape from (1, 3, 512) to (1, 3, 8, 64)
Q = Q.view(1, 3, 8, 64)
K = K.view(1, 3, 8, 64)
V = V.view(1, 3, 8, 64)

# Transpose to (1, 8, 3, 64) for parallel head computation
Q = Q.transpose(1, 2)  # (1, 8, 3, 64)
K = K.transpose(1, 2)  # (1, 8, 3, 64)
V = V.transpose(1, 2)  # (1, 8, 3, 64)
```

**Visual representation**:
```
Before reshape (1, 3, 512):
Token "I":    [q0, q1, ..., q63, q64, ..., q127, ..., q448, ..., q511]
              └─── head 1 ───┘└─── head 2 ───┘      └─── head 8 ───┘

After reshape and transpose (1, 8, 3, 64):
Head 1: ["I" queries 0-63,  "love" queries 0-63,  "AI" queries 0-63]
Head 2: ["I" queries 64-127, "love" queries 64-127, "AI" queries 64-127]
...
Head 8: ["I" queries 448-511, "love" queries 448-511, "AI" queries 448-511]
```

#### 2.2.3: Scaled Dot-Product Attention (Per Head)

**For Head 1** (same process for all 8 heads):

```
Q_h1: (1, 3, 64) - Queries for head 1
K_h1: (1, 3, 64) - Keys for head 1
V_h1: (1, 3, 64) - Values for head 1
```

**Step A: Compute Attention Scores**
```python
scores = Q_h1 @ K_h1.transpose(-2, -1)
# (1, 3, 64) @ (1, 64, 3) = (1, 3, 3)
```

**Detailed score computation**:
```
scores[0] = Q_h1[0] @ K_h1[0].T

         K_I    K_love   K_AI
       ┌──────┬────────┬──────┐
Q_I    │ 45.2 │  23.1  │ 31.5 │  ← "I" attends to all
       ├──────┼────────┼──────┤
Q_love │ 18.7 │  52.3  │ 28.9 │  ← "love" attends to all
       ├──────┼────────┼──────┤
Q_AI   │ 29.4 │  35.2  │ 48.6 │  ← "AI" attends to all
       └──────┴────────┴──────┘

Each entry = dot product of 64-dimensional vectors
Example: scores[0,0,0] = Q_I · K_I = Σ(q_i * k_i) for i=0..63
```

**Step B: Scale by √d_k**
```python
scores = scores / sqrt(64)  # = scores / 8.0

       K_I    K_love   K_AI
     ┌──────┬────────┬──────┐
Q_I  │ 5.65 │  2.89  │ 3.94 │
     ├──────┼────────┼──────┤
Q_love│2.34 │  6.54  │ 3.61 │
     ├──────┼────────┼──────┤
Q_AI │ 3.68 │  4.40  │ 6.08 │
     └──────┴────────┴──────┘

Why scale? Without scaling, dot products grow with d_k,
pushing softmax into saturation (very peaked distributions).
```

**Step C: Softmax (Row-wise)**
```python
attention_weights = softmax(scores, dim=-1)
```

**Softmax computation for row 0 (Q_I)**:
```
scores_I = [5.65, 2.89, 3.94]

exp_scores = [exp(5.65), exp(2.89), exp(3.94)]
           = [284.29, 18.00, 51.42]

sum_exp = 284.29 + 18.00 + 51.42 = 353.71

attention_I = [284.29/353.71, 18.00/353.71, 51.42/353.71]
            = [0.804, 0.051, 0.145]

Interpretation: "I" pays 80.4% attention to itself,
               5.1% to "love", 14.5% to "AI"
```

**Full attention matrix (Head 1)**:
```
                K_I    K_love   K_AI    (sum=1.0)
              ┌──────┬────────┬──────┐
Q_I           │ 0.804│  0.051 │ 0.145│  → 1.0
              ├──────┼────────┼──────┤
Q_love        │ 0.089│  0.712 │ 0.199│  → 1.0
              ├──────┼────────┼──────┤
Q_AI          │ 0.152│  0.234 │ 0.614│  → 1.0
              └──────┴────────┴──────┘
```

**Step D: Weighted Sum of Values**
```python
output_h1 = attention_weights @ V_h1
# (1, 3, 3) @ (1, 3, 64) = (1, 3, 64)
```

**Detailed for "I"**:
```
output_I = 0.804 * V_I + 0.051 * V_love + 0.145 * V_AI

Where V_I, V_love, V_AI are each 64-dimensional vectors

output_I[j] = 0.804*V_I[j] + 0.051*V_love[j] + 0.145*V_AI[j]
              for j = 0, 1, ..., 63
```

**Head 1 Output**:
```
output_h1: (1, 3, 64)
[
  [o_I_0, ..., o_I_63],      # Contextualized "I" from head 1
  [o_love_0, ..., o_love_63], # Contextualized "love" from head 1
  [o_AI_0, ..., o_AI_63]     # Contextualized "AI" from head 1
]
```

#### 2.2.4: Repeat for All 8 Heads (In Parallel)

Each head learns different attention patterns:
```
Head 1: Might focus on syntactic relationships
Head 2: Might focus on semantic similarity
Head 3: Might focus on positional proximity
...
Head 8: Might focus on coreference patterns
```

**All heads computed in parallel** (batched matrix multiplication):
```python
# All at once: (1, 8, 3, 64) @ (1, 8, 64, 3) = (1, 8, 3, 3)
scores_all = torch.matmul(Q, K.transpose(-2, -1)) / sqrt(64)
attn_all = softmax(scores_all, dim=-1)
output_all = torch.matmul(attn_all, V)  # (1, 8, 3, 64)
```

#### 2.2.5: Concatenate Heads

```python
# Transpose back: (1, 8, 3, 64) → (1, 3, 8, 64)
output_all = output_all.transpose(1, 2)

# Reshape to concatenate: (1, 3, 8, 64) → (1, 3, 512)
concat_output = output_all.reshape(1, 3, 512)
```

**Visual**:
```
"I" representation:
[head1_64_values | head2_64_values | ... | head8_64_values]
└────────────────────── 512 values ──────────────────────┘
```

#### 2.2.6: Output Projection

```python
attention_output = concat_output @ W_O  # (1, 3, 512) @ (512, 512) = (1, 3, 512)
```

This mixes information from all heads back together.

#### 2.2.7: Dropout on Attention Output

```python
attention_output = Dropout(attention_output, p=0.1)
```

---

### Step 2.3: Residual Connection #1

```python
X1 = X + attention_output  # (1, 3, 512)
```

**Why residual?**
- Allows gradients to flow directly during backpropagation
- Lets the model learn "modifications" rather than complete transformations
- Prevents vanishing gradients in deep networks

```
X1[0, 0, :] = X[0, 0, :] + attention_output[0, 0, :]

Original "I":       [7.69, -1.72, 12.67, ..., 6.20]
Attention output:   [1.23,  0.45, -2.10, ..., 0.89]
After residual:     [8.92, -1.27, 10.57, ..., 7.09]
```

---

### Step 2.4: Layer Normalization #1

**LayerNorm normalizes across the d_model dimension**:

```python
# For each position independently:
mean = X1.mean(dim=-1, keepdim=True)     # (1, 3, 1)
var = X1.var(dim=-1, keepdim=True)       # (1, 3, 1)
X1_norm = (X1 - mean) / sqrt(var + eps)  # (1, 3, 512)

# Learned scale (γ) and shift (β)
X1_norm = γ * X1_norm + β
# γ, β: (512,) - 1024 parameters
```

**Detailed for "I" position**:
```
X1[0, 0, :] = [8.92, -1.27, 10.57, 3.45, ..., 7.09]  # 512 values

mean_I = (8.92 + (-1.27) + 10.57 + ... + 7.09) / 512 = 2.34
var_I = Σ(x_i - mean_I)² / 512 = 15.67
std_I = sqrt(15.67 + 1e-5) = 3.96

X1_norm[0, 0, 0] = (8.92 - 2.34) / 3.96 = 1.66
X1_norm[0, 0, 1] = (-1.27 - 2.34) / 3.96 = -0.91
...

# Then apply learned parameters
X1_norm[0, 0, j] = γ[j] * X1_norm[0, 0, j] + β[j]
```

---

### Step 2.5: Feed-Forward Network

**Two linear transformations with ReLU**:

```
FFN(x) = max(0, x·W1 + b1)·W2 + b2
```

**Weight matrices**:
```
W1: (512, 2048)  - 1,048,576 parameters
b1: (2048,)      - 2,048 parameters
W2: (2048, 512)  - 1,048,576 parameters
b2: (512,)       - 512 parameters

Total FFN: 2,099,712 parameters
```

#### 2.5.1: First Linear Layer (Expansion)

```python
hidden = X1_norm @ W1 + b1  # (1, 3, 512) @ (512, 2048) = (1, 3, 2048)
```

**For "I" position**:
```
X1_norm[0, 0, :]: (512,) values
W1: (512, 2048)

hidden[0, 0, :] = X1_norm[0, 0, :] @ W1 + b1
                = [h0, h1, ..., h2047]  # 2048 values

Each output is a weighted combination of all 512 inputs:
h0 = Σ(X1_norm[0,0,j] * W1[j,0]) + b1[0] for j=0..511
```

#### 2.5.2: ReLU Activation

```python
hidden = ReLU(hidden)  # max(0, x) element-wise
# Shape: (1, 3, 2048)
```

```
hidden[0, 0, :] = [max(0, h0), max(0, h1), ..., max(0, h2047)]

Example:
Before ReLU: [2.3, -1.5, 0.8, -3.2, ...]
After ReLU:  [2.3,  0.0, 0.8,  0.0, ...]
```

#### 2.5.3: Dropout

```python
hidden = Dropout(hidden, p=0.1)
```

#### 2.5.4: Second Linear Layer (Compression)

```python
ffn_output = hidden @ W2 + b2  # (1, 3, 2048) @ (2048, 512) = (1, 3, 512)
```

**Why expand then compress?**
- More parameters = more capacity to learn complex patterns
- ReLU in the middle adds non-linearity
- Acts as a "memory" or "processing" step

---

### Step 2.6: Residual Connection #2

```python
X2 = X1_norm + ffn_output  # (1, 3, 512)
```

---

### Step 2.7: Layer Normalization #2

```python
X2_norm = LayerNorm(X2)  # (1, 3, 512)
```

---

### End of Encoder Layer 1

**Output of Layer 1**:
```
X_layer1: (1, 3, 512)

Now each token has been:
1. Contextualized via attention (knows about other tokens)
2. Processed through FFN (individual reasoning)
3. Normalized (stable activations)
```

---

## Encoder Layers 2-6

The output of Layer 1 becomes input to Layer 2, and so on.

```
X_input → Layer 1 → X_layer1 → Layer 2 → X_layer2 → ... → Layer 6 → X_encoder_out
```

**After all 6 layers**:
```
encoder_output: (1, 3, 512)

[
  [[e_I_0, ..., e_I_511],       # Deeply contextualized "I"
   [e_love_0, ..., e_love_511], # Deeply contextualized "love"
   [e_AI_0, ..., e_AI_511]]     # Deeply contextualized "AI"
]
```

**What has changed?**
- Each position now contains information about the ENTIRE sentence
- "I" knows it's the subject, followed by a verb, before "AI"
- "love" knows its subject is "I" and object is "AI"
- "AI" knows it's being loved by "I"

---

## Encoder Parameter Count (Per Layer)

```
Multi-Head Attention:
  W_Q, W_K, W_V, W_O: 4 × 512 × 512 = 1,048,576
  Biases: 4 × 512 = 2,048

Feed-Forward:
  W1: 512 × 2048 = 1,048,576
  b1: 2,048
  W2: 2048 × 512 = 1,048,576
  b2: 512

Layer Norms (×2):
  γ, β: 2 × 512 × 2 = 2,048

Per Layer Total: ~3,152,384 parameters

6 Layers: ~18,914,304 parameters
```

---

# PART 3: DECODER

## Decoder Input Preparation

**Target sentence**: "J'aime l'IA"
**Tokenized**: `["<BOS>", "J'", "aime", "l'", "IA"]` (BOS = Beginning of Sentence)
**Token IDs**: `[1, 892, 5621, 234, 9876]`

**During training** (teacher forcing), we feed the FULL target sequence.
**During inference**, we generate one token at a time.

Let's trace **training** first (simpler).

### Decoder Token Embeddings + Positional Encoding

```python
# Same process as encoder
tgt_embed = embedding_lookup(target_ids)  # (1, 5, 512)
tgt_embed = tgt_embed * sqrt(512)
tgt_input = tgt_embed + PE[:5]            # (1, 5, 512)
tgt_input = Dropout(tgt_input)
```

---

## DECODER LAYER 1 (of 6)

### Step 3.1: Masked Multi-Head Self-Attention

**CRITICAL DIFFERENCE**: The decoder cannot look at future tokens!

#### 3.1.1: Create Causal Mask

```python
def create_causal_mask(seq_len):
    mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1)
    mask = mask.masked_fill(mask == 1, float('-inf'))
    return mask

# For seq_len=5:
mask = [
    [0, -∞, -∞, -∞, -∞],  # Position 0 can only see position 0
    [0,  0, -∞, -∞, -∞],  # Position 1 can see 0, 1
    [0,  0,  0, -∞, -∞],  # Position 2 can see 0, 1, 2
    [0,  0,  0,  0, -∞],  # Position 3 can see 0, 1, 2, 3
    [0,  0,  0,  0,  0],  # Position 4 can see all
]
```

#### 3.1.2: Self-Attention with Mask

```python
Q = tgt_input @ W_Q  # (1, 5, 512)
K = tgt_input @ W_K  # (1, 5, 512)
V = tgt_input @ W_V  # (1, 5, 512)

# After splitting into heads: (1, 8, 5, 64)
scores = Q @ K.T / sqrt(64)  # (1, 8, 5, 5)

# Apply causal mask BEFORE softmax
scores = scores + mask  # Add -∞ to future positions

# Softmax converts -∞ to 0 probability
attention_weights = softmax(scores, dim=-1)
```

**Masked attention matrix (for one head)**:
```
                 K_BOS  K_J'  K_aime  K_l'  K_IA
              ┌───────┬──────┬───────┬─────┬─────┐
Q_BOS         │  0.95 │  0   │   0   │  0  │  0  │  ← Can only see BOS
              ├───────┼──────┼───────┼─────┼─────┤
Q_J'          │  0.30 │ 0.70 │   0   │  0  │  0  │  ← Can see BOS, J'
              ├───────┼──────┼───────┼─────┼─────┤
Q_aime        │  0.15 │ 0.45 │  0.40 │  0  │  0  │  ← Can see BOS, J', aime
              ├───────┼──────┼───────┼─────┼─────┤
Q_l'          │  0.10 │ 0.25 │  0.35 │0.30 │  0  │  ← Can see 0-3
              ├───────┼──────┼───────┼─────┼─────┤
Q_IA          │  0.08 │ 0.22 │  0.30 │0.15 │0.25 │  ← Can see all
              └───────┴──────┴───────┴─────┴─────┘
              
Note: Each row sums to 1.0, and zeros appear for future positions
```

**Why masking?**
- During inference, future tokens don't exist yet
- Training must simulate this constraint
- Prevents the model from "cheating" by looking ahead

#### 3.1.3: Compute Output (same as encoder)

```python
masked_self_attn_out = attention_weights @ V  # (1, 5, 512)
masked_self_attn_out = masked_self_attn_out @ W_O
masked_self_attn_out = Dropout(masked_self_attn_out)
```

### Step 3.2: Residual + LayerNorm #1

```python
Y1 = LayerNorm(tgt_input + masked_self_attn_out)  # (1, 5, 512)
```

---

### Step 3.3: Cross-Attention (Encoder-Decoder Attention)

**THIS IS WHERE ENCODER OUTPUT ENTERS THE DECODER!**

#### 3.3.1: Q from Decoder, K and V from Encoder

```python
# Q comes from decoder's current state
Q = Y1 @ W_Q_cross  # (1, 5, 512) @ (512, 512) = (1, 5, 512)

# K and V come from ENCODER OUTPUT!
K = encoder_output @ W_K_cross  # (1, 3, 512) @ (512, 512) = (1, 3, 512)
V = encoder_output @ W_V_cross  # (1, 3, 512) @ (512, 512) = (1, 3, 512)
```

**Shape analysis**:
```
Q: (1, 5, 512) → After split: (1, 8, 5, 64)  ← 5 decoder positions
K: (1, 3, 512) → After split: (1, 8, 3, 64)  ← 3 encoder positions
V: (1, 3, 512) → After split: (1, 8, 3, 64)  ← 3 encoder positions
```

#### 3.3.2: Cross-Attention Scores

```python
scores = Q @ K.T / sqrt(64)  # (1, 8, 5, 64) @ (1, 8, 64, 3) = (1, 8, 5, 3)
```

**Each decoder position attends to ALL encoder positions**:
```
                   K_I   K_love  K_AI   (encoder)
              ┌────────┬────────┬──────┐
Q_BOS         │  0.25  │  0.35  │ 0.40 │  ← BOS looks at source
              ├────────┼────────┼──────┤
Q_J'          │  0.70  │  0.15  │ 0.15 │  ← "J'" mainly attends to "I"
              ├────────┼────────┼──────┤
Q_aime        │  0.20  │  0.65  │ 0.15 │  ← "aime" attends to "love"!
              ├────────┼────────┼──────┤
Q_l'          │  0.15  │  0.25  │ 0.60 │  ← "l'" attends to "AI"
              ├────────┼────────┼──────┤
Q_IA          │  0.10  │  0.20  │ 0.70 │  ← "IA" strongly attends to "AI"
              └────────┴────────┴──────┘
              
This is the "translation alignment" the model learns!
```

**NO MASK in cross-attention** - decoder can see entire source sentence.

#### 3.3.3: Weighted Sum of Encoder Values

```python
cross_attn_out = attention_weights @ V  # (1, 8, 5, 3) @ (1, 8, 3, 64) = (1, 8, 5, 64)
```

**For "aime" position**:
```
cross_attn_out[aime] = 0.20 * V_I + 0.65 * V_love + 0.15 * V_AI

The representation of "aime" now contains:
- 20% information about "I"
- 65% information about "love" (its translation!)
- 15% information about "AI"
```

#### 3.3.4: Project Back

```python
cross_attn_out = concat_heads(cross_attn_out)  # (1, 5, 512)
cross_attn_out = cross_attn_out @ W_O_cross
cross_attn_out = Dropout(cross_attn_out)
```

### Step 3.4: Residual + LayerNorm #2

```python
Y2 = LayerNorm(Y1 + cross_attn_out)  # (1, 5, 512)
```

---

### Step 3.5: Feed-Forward Network (Same as Encoder)

```python
hidden = ReLU(Y2 @ W1 + b1)  # (1, 5, 2048)
hidden = Dropout(hidden)
ffn_out = hidden @ W2 + b2   # (1, 5, 512)
```

### Step 3.6: Residual + LayerNorm #3

```python
decoder_layer1_out = LayerNorm(Y2 + ffn_out)  # (1, 5, 512)
```

---

## Decoder Layers 2-6

Same as encoder layers, but each layer has:
1. Masked self-attention (decoder attends to itself)
2. Cross-attention (decoder attends to encoder)
3. Feed-forward network

**After all 6 decoder layers**:
```
decoder_output: (1, 5, 512)

Each position is now a rich representation combining:
- Its own token's meaning
- Context from previous target tokens (masked self-attn)
- Relevant source information (cross-attention)
- Deep non-linear processing (FFN)
```

---

# PART 4: OUTPUT GENERATION

## Step 4.1: Final Linear Projection

```python
# Project to vocabulary size
logits = decoder_output @ W_vocab + b_vocab
# (1, 5, 512) @ (512, 37000) = (1, 5, 37000)

# W_vocab: (512, 37000) - 18,944,000 parameters
# b_vocab: (37000,)     - 37,000 parameters
```

**What are logits?**
```
logits[0, 0, :] = [score for token 0, score for token 1, ..., score for token 36999]

Higher score = more likely to be the next token
```

## Step 4.2: Softmax for Probabilities

```python
probs = softmax(logits, dim=-1)  # (1, 5, 37000)
```

**For position 1 (predicting what comes after BOS)**:
```
probs[0, 0, :] = [0.00001, ..., 0.75, ..., 0.00002]
                           ↑
                    Token 892 = "J'"
                    
The model predicts "J'" with 75% probability
```

---

## Step 4.3: Loss Calculation (Training)

**Target labels** (shifted by 1):
```
Input:  ["<BOS>", "J'", "aime", "l'", "IA"]
Labels: ["J'", "aime", "l'", "IA", "<EOS>"]

Label IDs: [892, 5621, 234, 9876, 2]
```

**Cross-Entropy Loss**:
```python
loss = CrossEntropyLoss(logits.view(-1, 37000), labels.view(-1))
# logits: (5, 37000)
# labels: (5,)
```

**For each position**:
```
Loss_pos0 = -log(probs[0, 0, 892])   # Should predict "J'"
Loss_pos1 = -log(probs[0, 1, 5621])  # Should predict "aime"
Loss_pos2 = -log(probs[0, 2, 234])   # Should predict "l'"
Loss_pos3 = -log(probs[0, 3, 9876])  # Should predict "IA"
Loss_pos4 = -log(probs[0, 4, 2])     # Should predict "<EOS>"

Total Loss = (Loss_pos0 + Loss_pos1 + Loss_pos2 + Loss_pos3 + Loss_pos4) / 5
```

---

# PART 5: INFERENCE (Auto-regressive Generation)

During inference, we don't have the target sequence. We generate one token at a time.

## Step 5.1: Encode Source Once

```python
encoder_output = encoder("I love AI")  # (1, 3, 512)
# This is computed ONCE and reused for all decoding steps
```

## Step 5.2: Start with BOS

```python
generated = [BOS_TOKEN]  # [1]
```

## Step 5.3: Generate Loop

```python
for step in range(max_length):
    # 1. Embed current sequence
    tgt_input = embed(generated) + PE[:len(generated)]  # (1, step+1, 512)
    
    # 2. Decode with cross-attention to encoder
    decoder_out = decoder(tgt_input, encoder_output)  # (1, step+1, 512)
    
    # 3. Get logits for LAST position only
    last_logits = decoder_out[0, -1, :] @ W_vocab + b_vocab  # (37000,)
    
    # 4. Sample or argmax
    next_token = argmax(last_logits)  # or sample from softmax(last_logits)
    
    # 5. Append to generated sequence
    generated.append(next_token)
    
    # 6. Stop if EOS
    if next_token == EOS_TOKEN:
        break
```

**Trace through**:
```
Step 0: generated = [BOS]
        decoder output for BOS position
        predict: "J'" (token 892)
        generated = [BOS, J']

Step 1: generated = [BOS, J']
        decoder attends to [BOS, J'] (masked) and encoder
        predict at position 1: "aime"
        generated = [BOS, J', aime]

Step 2: generated = [BOS, J', aime]
        predict: "l'"
        generated = [BOS, J', aime, l']

Step 3: generated = [BOS, J', aime, l', IA]
        predict: EOS
        STOP
```

---

# PART 6: DETAILED DATA FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ENCODER                                         │
│                                                                             │
│  "I love AI"                                                                │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────┐    ┌──────────────┐    ┌──────────────────────────────────┐   │
│  │Tokenize │───▶│Embed + Scale │───▶│      Add Positional Encoding     │   │
│  └─────────┘    └──────────────┘    └──────────────────────────────────┘   │
│       │              (512)                         (512)                    │
│       ▼                                              │                      │
│  [45, 2891, 15234]                                   ▼                      │
│                                              ┌──────────────┐               │
│                                              │   Dropout    │               │
│                                              └──────────────┘               │
│                                                      │                      │
│                                                      ▼                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     ENCODER LAYER 1                                   │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │  │
│  │  │  Multi-Head Self-Attention                                       │ │  │
│  │  │  ┌─────┐     ┌─────────────┐     ┌──────────┐     ┌──────────┐  │ │  │
│  │  │  │Q=XWq│────▶│ Split into  │────▶│  Scaled  │────▶│ Softmax  │  │ │  │
│  │  │  │K=XWk│     │  8 heads    │     │ Dot-Prod │     │          │  │ │  │
│  │  │  │V=XWv│     │ (3,512)→    │     │ QK^T/√64 │     │ (3,3)×8  │  │ │  │
│  │  │  └─────┘     │ (8,3,64)    │     │ (3,3)×8  │     └────┬─────┘  │ │  │
│  │  │              └─────────────┘     └──────────┘          │        │ │  │
│  │  │                                                        ▼        │ │  │
│  │  │  ┌──────────┐     ┌──────────────┐     ┌─────────────────────┐  │ │  │
│  │  │  │Concat    │◀────│   Attn×V     │◀────│   Attention Weights │  │ │  │
│  │  │  │Heads     │     │  (8,3,64)    │     │       × Values      │  │ │  │
│  │  │  │(3,512)   │     └──────────────┘     └─────────────────────┘  │ │  │
│  │  │  └────┬─────┘                                                   │ │  │
│  │  │       │                                                         │ │  │
│  │  │       ▼                                                         │ │  │
│  │  │  ┌──────────┐     ┌──────────┐                                  │ │  │
│  │  │  │  Wo Proj │────▶│ Dropout  │                                  │ │  │
│  │  │  │ (3,512)  │     │          │                                  │ │  │
│  │  │  └──────────┘     └────┬─────┘                                  │ │  │
│  │  └────────────────────────│────────────────────────────────────────┘ │  │
│  │                           │                                          │  │
│  │                           ▼                                          │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │              X_res1 = X + Attention_Output                    │   │  │
│  │  │                     (Residual Connection)                     │   │  │
│  │  └────────────────────────────┬─────────────────────────────────┘   │  │
│  │                               │                                      │  │
│  │                               ▼                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                    LayerNorm(X_res1)                          │   │  │
│  │  │              mean=0, var=1 across d_model                     │   │  │
│  │  └────────────────────────────┬─────────────────────────────────┘   │  │
│  │                               │                                      │  │
│  │                               ▼                                      │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐│  │
│  │  │  Feed-Forward Network                                           ││  │
│  │  │  ┌────────────┐   ┌──────┐   ┌─────────┐   ┌─────────────────┐  ││  │
│  │  │  │Linear      │──▶│ ReLU │──▶│ Dropout │──▶│ Linear          │  ││  │
│  │  │  │512→2048    │   │      │   │         │   │ 2048→512        │  ││  │
│  │  │  └────────────┘   └──────┘   └─────────┘   └────────┬────────┘  ││  │
│  │  └─────────────────────────────────────────────────────│───────────┘│  │
│  │                                                        │            │  │
│  │                                                        ▼            │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │              X_res2 = X_norm1 + FFN_Output                    │   │  │
│  │  │                     (Residual Connection)                     │   │  │
│  │  └────────────────────────────┬─────────────────────────────────┘   │  │
│  │                               │                                      │  │
│  │                               ▼                                      │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                    LayerNorm(X_res2)                          │   │  │
│  │  └────────────────────────────┬─────────────────────────────────┘   │  │
│  └───────────────────────────────│──────────────────────────────────────┘  │
│                                  │                                         │
│                                  ▼                                         │
│                         ENCODER LAYERS 2-6                                 │
│                         (Same structure)                                   │
│                                  │                                         │
│                                  ▼                                         │
│                    ┌─────────────────────────┐                             │
│                    │    ENCODER OUTPUT       │                             │
│                    │      (1, 3, 512)        │                             │
│                    └───────────┬─────────────┘                             │
│                                │                                           │
└────────────────────────────────│───────────────────────────────────────────┘
                                 │
                                 │ ◀══════════════════════════════════════╗
                                 │                                         ║
                                 ▼                                         ║
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DECODER                                         │
│                                                                             │
│  Target: "<BOS> J' aime l' IA"                                              │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────┐    ┌──────────────┐    ┌──────────────────────────────────┐   │
│  │Tokenize │───▶│Embed + Scale │───▶│      Add Positional Encoding     │   │
│  └─────────┘    └──────────────┘    └──────────────────────────────────┘   │
│                                                      │                      │
│                                                      ▼                      │
│                                              ┌──────────────┐               │
│                                              │   Dropout    │               │
│                                              └──────────────┘               │
│                                                      │                      │
│                                                      ▼                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     DECODER LAYER 1                                   │  │
│  │                                                                       │  │
│  │  ╔═══════════════════════════════════════════════════════════════╗   │  │
│  │  ║  MASKED Multi-Head Self-Attention                             ║   │  │
│  │  ║  ┌─────┐                                                      ║   │  │
│  │  ║  │Q=YWq│    ┌────────────────────────────────────────────┐   ║   │  │
│  │  ║  │K=YWk│───▶│ Causal Mask: Can't attend to future tokens │   ║   │  │
│  │  ║  │V=YWv│    │                                            │   ║   │  │
│  │  ║  └─────┘    │  [0, -∞, -∞, -∞, -∞]  position 0 sees 0    │   ║   │  │
│  │  ║             │  [0,  0, -∞, -∞, -∞]  position 1 sees 0,1  │   ║   │  │
│  │  ║             │  [0,  0,  0, -∞, -∞]  position 2 sees 0-2  │   ║   │  │
│  │  ║             │  [0,  0,  0,  0, -∞]  position 3 sees 0-3  │   ║   │  │
│  │  ║             │  [0,  0,  0,  0,  0]  position 4 sees all  │   ║   │  │
│  │  ║             └────────────────────────────────────────────┘   ║   │  │
│  │  ║                                                              ║   │  │
│  │  ║  Scores = QK^T/√64 + Mask  →  Softmax  →  × V  →  Wo       ║   │  │
│  │  ╚══════════════════════════════════════════════════════════════╝   │  │
│  │                               │                                      │  │
│  │                               ▼                                      │  │
│  │           Add & Norm (Y_res1 = Y + MaskedAttn, then LN)             │  │
│  │                               │                                      │  │
│  │                               ▼                                      │  │
│  │  ╔═══════════════════════════════════════════════════════════════╗   │  │
│  │  ║  CROSS-ATTENTION (Encoder-Decoder Attention)                  ║   │  │
│  │  ║                                                               ║   │  │
│  │  ║  ┌─────────────┐         ┌──────────────────────────────┐    ║   │  │
│  │  ║  │ Q = Y × Wq  │         │      ENCODER OUTPUT          │    ║   │  │
│  │  ║  │ (from       │         │        (1, 3, 512)           │════╬═══╝
│  │  ║  │  decoder)   │         │                              │    ║
│  │  ║  │ (1,5,512)   │         │  K = Encoder_out × Wk        │    ║
│  │  ║  └──────┬──────┘         │  V = Encoder_out × Wv        │    ║
│  │  ║         │                │  Both: (1, 3, 512)           │    ║
│  │  ║         │                └────────────┬─────────────────┘    ║
│  │  ║         │                             │                      ║
│  │  ║         ▼                             ▼                      ║
│  │  ║  ┌─────────────────────────────────────────────────────┐    ║
│  │  ║  │  Attention Scores: Q(5×512) × K^T(512×3) = (5×3)    │    ║
│  │  ║  │                                                      │    ║
│  │  ║  │  Each decoder position attends to ALL encoder pos:  │    ║
│  │  ║  │                                                      │    ║
│  │  ║  │           "I"    "love"   "AI"                       │    ║
│  │  ║  │  "BOS"  [ 0.25    0.35    0.40 ]                    │    ║
│  │  ║  │  "J'"   [ 0.70    0.15    0.15 ]  ◀─ aligns to "I"  │    ║
│  │  ║  │  "aime" [ 0.20    0.65    0.15 ]  ◀─ aligns to "love"│   ║
│  │  ║  │  "l'"   [ 0.15    0.25    0.60 ]  ◀─ aligns to "AI" │    ║
│  │  ║  │  "IA"   [ 0.10    0.20    0.70 ]  ◀─ aligns to "AI" │    ║
│  │  ║  │                                                      │    ║
│  │  ║  │  NO MASK - decoder sees entire source sentence      │    ║
│  │  ║  └─────────────────────────────────────────────────────┘    ║
│  │  ║                          │                                   ║
│  │  ║                          ▼                                   ║
│  │  ║      CrossAttn_Out = Softmax(Scores) × V  →  Wo             ║
│  │  ║             (1, 5, 512)                                      ║
│  │  ╚═══════════════════════════════════════════════════════════════╝
│  │                               │
│  │                               ▼
│  │           Add & Norm (Y_res2 = Y_norm1 + CrossAttn, then LN)
│  │                               │
│  │                               ▼
│  │  ┌─────────────────────────────────────────────────────────────────┐
│  │  │  Feed-Forward Network (same as encoder)                         │
│  │  │  Linear(512→2048) → ReLU → Dropout → Linear(2048→512)          │
│  │  └─────────────────────────────────────────────────────────────────┘
│  │                               │
│  │                               ▼
│  │           Add & Norm (Y_res3 = Y_norm2 + FFN, then LN)
│  │                               │
│  └───────────────────────────────│──────────────────────────────────────┘
│                                  │
│                                  ▼
│                         DECODER LAYERS 2-6
│                         (Same structure, with cross-attention)
│                                  │
│                                  ▼
│                    ┌─────────────────────────┐
│                    │    DECODER OUTPUT       │
│                    │      (1, 5, 512)        │
│                    └───────────┬─────────────┘
│                                │
│                                ▼
│  ┌──────────────────────────────────────────────────────────────────────┐
│  │              OUTPUT PROJECTION                                        │
│  │                                                                       │
│  │   Decoder_Output × W_vocab + b_vocab                                  │
│  │   (1, 5, 512) × (512, 37000) = (1, 5, 37000)                         │
│  │                                                                       │
│  │   Each position: 37000 scores (one per vocab token)                  │
│  └──────────────────────────────────────────────────────────────────────┘
│                                │
│                                ▼
│  ┌──────────────────────────────────────────────────────────────────────┐
│  │              SOFTMAX → PROBABILITIES                                  │
│  │                                                                       │
│  │   Position 0: Predict "J'"   → prob("J'") = 0.75                     │
│  │   Position 1: Predict "aime" → prob("aime") = 0.82                   │
│  │   Position 2: Predict "l'"   → prob("l'") = 0.68                     │
│  │   Position 3: Predict "IA"   → prob("IA") = 0.91                     │
│  │   Position 4: Predict "<EOS>"→ prob("<EOS>") = 0.95                  │
│  └──────────────────────────────────────────────────────────────────────┘
│                                │
│                                ▼
│  ┌──────────────────────────────────────────────────────────────────────┐
│  │              LOSS CALCULATION (Training)                              │
│  │                                                                       │
│  │   Target Labels: ["J'", "aime", "l'", "IA", "<EOS>"]                 │
│  │                                                                       │
│  │   Loss = -Σ log(P(correct_token))                                    │
│  │        = -log(0.75) - log(0.82) - log(0.68) - log(0.91) - log(0.95) │
│  │        = 0.29 + 0.20 + 0.39 + 0.09 + 0.05                           │
│  │        = 1.02                                                        │
│  └──────────────────────────────────────────────────────────────────────┘
│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# PART 7: GRADIENT FLOW (Backpropagation)

Understanding how gradients flow helps understand why each component exists.

```
Loss
  │
  ▼
∂Loss/∂logits
  │
  ▼
∂logits/∂W_vocab ──────▶ Update W_vocab
  │
  ▼
∂logits/∂decoder_out
  │
  ├──▶ Through Layer Norm
  │         │
  │         ▼
  │    Through FFN
  │         │
  │         ├──▶ ∂/∂W2 ──▶ Update W2
  │         ├──▶ ∂/∂W1 ──▶ Update W1
  │         │
  │         ▼
  │    Through Residual (gradient flows directly!)
  │         │
  │         ▼
  │    Through Cross-Attention
  │         │
  │         ├──▶ ∂/∂W_Q_cross ──▶ Update
  │         ├──▶ ∂/∂W_K_cross ──▶ Update (gradient to encoder!)
  │         ├──▶ ∂/∂W_V_cross ──▶ Update (gradient to encoder!)
  │         │
  │         ▼
  │    Through Residual
  │         │
  │         ▼
  │    Through Masked Self-Attention
  │         │
  │         ├──▶ ∂/∂W_Q, W_K, W_V, W_O ──▶ Update
  │         │
  │         ▼
  │    Through Residual
  │         │
  │         ▼
  │    Through Embedding (decoder)
  │         │
  │         ▼
  │    ∂/∂E_target ──▶ Update target embeddings
  │
  │
  │ (Gradients from Cross-Attention K, V)
  │         │
  │         ▼
  │    ∂/∂encoder_output
  │         │
  │         ▼
  │    Back through Encoder Layers 6→1
  │         │
  │         ▼
  │    ∂/∂E_source ──▶ Update source embeddings
  │
  ▼
All parameters updated via Adam optimizer
```

**Key insight**: Residual connections allow gradients to flow directly from loss to early layers, preventing vanishing gradients.

---

# PART 8: TENSOR SHAPES SUMMARY

## Encoder Shapes

| Stage | Tensor | Shape |
|-------|--------|-------|
| Input tokens | `token_ids` | `(B, S_src)` = `(1, 3)` |
| After embedding | `X_embed` | `(B, S_src, d)` = `(1, 3, 512)` |
| After PE | `X` | `(1, 3, 512)` |
| Q, K, V (before split) | | `(1, 3, 512)` |
| Q, K, V (after split) | | `(1, 8, 3, 64)` |
| Attention scores | | `(1, 8, 3, 3)` |
| Attention output | | `(1, 8, 3, 64)` |
| After concat | | `(1, 3, 512)` |
| FFN hidden | | `(1, 3, 2048)` |
| FFN output | | `(1, 3, 512)` |
| Encoder output | `enc_out` | `(1, 3, 512)` |

## Decoder Shapes

| Stage | Tensor | Shape |
|-------|--------|-------|
| Target tokens | `tgt_ids` | `(B, S_tgt)` = `(1, 5)` |
| After embedding | `Y_embed` | `(1, 5, 512)` |
| Masked self-attn Q, K, V | | `(1, 8, 5, 64)` |
| Masked self-attn scores | | `(1, 8, 5, 5)` |
| Cross-attn Q (from decoder) | | `(1, 8, 5, 64)` |
| Cross-attn K, V (from encoder) | | `(1, 8, 3, 64)` |
| Cross-attn scores | | `(1, 8, 5, 3)` |
| Cross-attn output | | `(1, 8, 5, 64)` |
| Decoder output | | `(1, 5, 512)` |
| Logits | | `(1, 5, 37000)` |
| Probabilities | | `(1, 5, 37000)` |

---

# PART 9: KEY INTERVIEW QUESTIONS (DEEP)

## Q1: Why do we need both encoder and decoder?

**Encoder**: Processes the **entire** source sequence in parallel. Each position can attend to all other positions. Creates a rich, bidirectional representation of the input.

**Decoder**: Generates output **autoregressively** (one token at a time). Uses causal masking because future tokens don't exist during generation. Cross-attention allows it to "look at" the encoded source while generating.

```
Encoder: Understands the question
Decoder: Generates the answer
```

## Q2: Why can't we just use the encoder for generation?

The encoder processes all positions simultaneously. For generation:
- We don't know how long the output will be
- Each generated token depends on previous generated tokens
- We need the causal structure of the decoder

## Q3: What exactly happens in cross-attention?

```python
# Decoder position "aime" wants to know what English word it should translate

# Query from decoder: "I am the French verb for 'like/love', what should I attend to?"
Q_aime = decoder_representation["aime"]

# Keys from encoder: "Here are the representations of 'I', 'love', 'AI'"
K_encoder = [K_I, K_love, K_AI]

# Attention scores: Q_aime · K_encoder
# "aime" finds high similarity with "love"

# Values from encoder: retrieve information from "love"
V_encoder = [V_I, V_love, V_AI]

# Output: weighted sum, mostly from "love"
output_aime = 0.20*V_I + 0.65*V_love + 0.15*V_AI
```

## Q4: Why scale by √d_k?

Without scaling:
```
d_k = 64
Q[i] and K[j] are 64-dimensional vectors
dot_product(Q[i], K[j]) = Σ(Q[i][k] * K[j][k]) for k=0..63

If Q and K entries ~ N(0, 1):
Expected dot product variance = d_k = 64
Standard deviation = √64 = 8

Large values push softmax to extremes:
softmax([8, 1, 1]) ≈ [0.999, 0.0005, 0.0005]  # Nearly one-hot!
```

With scaling:
```
scaled_dot_product = dot_product / √64 = dot_product / 8
Variance ≈ 1
softmax([1, 0.125, 0.125]) ≈ [0.57, 0.21, 0.21]  # Smoother!
```

**Smooth distributions** allow gradient flow and learning multiple attention patterns.

## Q5: What's the computational complexity?

**Self-Attention**: O(n² · d)
- n² attention scores for n positions
- Each score requires d operations (dot product)

**FFN**: O(n · d · d_ff)
- For each of n positions
- Matrix multiplication: d × d_ff

**For very long sequences (n >> d)**:
- Attention becomes the bottleneck (quadratic in n)
- This motivates efficient attention variants (Linformer, Performer, etc.)

## Q6: How do positional encodings let the model know position?

```python
# Position 0 and Position 100 have different PE values
PE[0] = [sin(0), cos(0), sin(0), cos(0), ...]
       = [0, 1, 0, 1, ...]

PE[100] = [sin(100), cos(100), sin(100/10000^(2/512)), cos(100/10000^(2/512)), ...]
         = [−0.506, 0.862, 0.981, 0.192, ...]

# The model learns: "if this dimension pattern appears, it's position 100"
# More importantly: PE[pos+k] can be computed as linear transform of PE[pos]
# This helps the model learn relative positions!
```

## Q7: Walk through what happens when I type "Hello" and GPT generates a response

1. **Tokenization**: "Hello" → [15496]

2. **Embedding lookup**: token 15496 → 768-dim vector

3. **Add positional encoding**: vector + PE[0]

4. **Through decoder layers** (GPT has no encoder, just decoder):
   - Masked self-attention (only looks at "Hello")
   - FFN
   - Repeat for all layers

5. **Output projection**: Get 50257 logits (GPT-2 vocab size)

6. **Sampling**: Pick next token, e.g., "!" (token 0)

7. **Repeat**: Now input is ["Hello", "!"], generate next...

8. **Continue until**: Max length or EOS token

---

# PART 10: COMPLETE NUMERICAL EXAMPLE

Let's trace **one number** through the entire network.

**Setup**: Token "love" at position 1, dimension 0

## Input
```
token_id = 2891  ("love")
position = 1
dimension = 0
```

## Embedding
```
E[2891, 0] = -0.0234  (random initialization, learned)
Scaled: -0.0234 * √512 = -0.0234 * 22.627 = -0.529
```

## Positional Encoding
```
PE[1, 0] = sin(1 / 10000^(0/512)) = sin(1) = 0.841
```

## Input to Encoder
```
X[0, 1, 0] = -0.529 + 0.841 = 0.312
```

## After Self-Attention
Let's say attention weights for position 1 are [0.15, 0.70, 0.15] and V values at dim 0 are [0.5, 0.3, 0.8]:
```
attention_output[0, 1, 0] = 0.15*0.5 + 0.70*0.3 + 0.15*0.8 
                         = 0.075 + 0.21 + 0.12 = 0.405
After W_O projection (say multiplies by 1.2): 0.405 * 1.2 = 0.486
```

## After Residual
```
X1[0, 1, 0] = X[0, 1, 0] + attention_output[0, 1, 0]
            = 0.312 + 0.486 = 0.798
```

## After LayerNorm
```
mean across dim=512: say 0.2
std across dim=512: say 1.5
γ[0] = 1.0, β[0] = 0.0  (typical initialization)

X1_norm[0, 1, 0] = (0.798 - 0.2) / 1.5 * 1.0 + 0.0 = 0.399
```

## After FFN
```
First linear: 0.399 * W1[0, :] + ... = say 1.234
After ReLU: max(0, 1.234) = 1.234
Second linear: 1.234 * W2[:, 0] + ... = say 0.567
```

## After Residual + LayerNorm
```
X2 = X1_norm + FFN_out = 0.399 + 0.567 = 0.966
After LayerNorm: say 0.512
```

**This value continues through 5 more encoder layers, then into decoder via cross-attention!**

---

This deep dive should give you a complete understanding of every operation in the Transformer. Each concept builds on the previous, and the architecture is designed to enable:
1. **Parallel processing** (unlike RNNs)
2. **Long-range dependencies** (attention mechanism)
3. **Stable training** (residuals + layer norm)
4. **High capacity** (multi-head attention + FFN)
