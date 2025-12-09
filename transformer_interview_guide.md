# Transformer Interview Guide
## Complete Flow Explanation (Interview Level)

---

# 1. THE BIG PICTURE

## What is a Transformer?

A **sequence-to-sequence** model that processes input in **parallel** (unlike RNNs which process word by word). It uses **attention** to let each word "look at" all other words directly.

**Used in**: BERT, GPT, T5, ChatGPT, all modern LLMs

## Why Transformer over RNN/LSTM?

| Problem with RNN | How Transformer Solves It |
|------------------|---------------------------|
| Sequential processing (slow) | Parallel processing (fast) |
| Long sequences = vanishing gradients | Direct connections via attention |
| Hard to capture long-range dependencies | Any word can attend to any other word |
| Can't leverage GPU parallelism | Fully parallelizable |

---

# 2. THE STATIC EMBEDDING MATRIX

## What is it?

A **lookup table** that converts words (tokens) into vectors of numbers that the model can process.

```
Vocabulary: ["the", "cat", "sat", "on", "mat", ..., "transformer"]
             ↓      ↓      ↓     ↓     ↓              ↓
Token IDs:   [0,     1,     2,    3,    4,   ...,    36999]
```

**Embedding Matrix E**: A table with one row per word in vocabulary

```
             Dimension 0   Dim 1    Dim 2   ...   Dim 511
           ┌─────────────┬────────┬────────┬─────┬────────┐
Word 0     │    0.23     │ -0.15  │  0.08  │ ... │  0.42  │  ← 512 numbers for "the"
Word 1     │    0.11     │  0.45  │ -0.23  │ ... │ -0.31  │  ← 512 numbers for "cat"
Word 2     │   -0.08     │  0.19  │  0.02  │ ... │  0.67  │  ← 512 numbers for "sat"
  ⋮        │     ⋮       │   ⋮    │   ⋮    │  ⋮  │   ⋮    │
Word 36999 │    0.34     │ -0.12  │  0.56  │ ... │  0.19  │  ← 512 numbers for "transformer"
           └─────────────┴────────┴────────┴─────┴────────┘

Size: 37,000 words × 512 dimensions = 18.9 million parameters
```

## How is the Embedding Matrix Created/Trained?

### Step 1: Random Initialization
```
At the start of training:
- Every value in E is randomly initialized (small random numbers)
- "cat" vector has NO meaning yet
- "dog" vector has NO meaning yet
- They're just random numbers!
```

### Step 2: Training Updates the Embeddings

During training, the model:
1. Makes a prediction (e.g., translate "I love cats")
2. Compares with correct answer
3. Calculates loss (how wrong it was)
4. **Backpropagation updates ALL parameters, including E**

```
Example during training:

Input: "The cat sat"
Model predicts next word: "jumped" (wrong!)
Correct answer: "down"

Loss is calculated → Gradients flow backward → 
Embedding for "cat", "sat", "the" all get slightly adjusted

After millions of examples:
- "cat" embedding becomes similar to "dog" embedding (both are animals)
- "sat" embedding becomes similar to "stood" embedding (both are verbs)
- Words with similar meanings cluster together!
```

### Step 3: What the Trained Embeddings Capture

After training, the embedding matrix captures:
- **Semantic similarity**: "king" and "queen" are close
- **Relationships**: king - man + woman ≈ queen
- **Context patterns**: Words that appear in similar contexts have similar vectors

### Key Interview Points About Embeddings

**Q: Is the embedding matrix fixed or learned?**
> It's LEARNED during training. Starts random, gets meaningful through backpropagation.

**Q: Why is it called "static"?**
> Because each word has ONE fixed vector regardless of context. "bank" (river) and "bank" (money) have the SAME embedding. This is different from contextual embeddings (like BERT outputs) where meaning changes based on context.

**Q: What's the embedding dimension (512)?**
> It's a hyperparameter. Larger = more capacity but more parameters. 512 was used in original paper. GPT-3 uses 12,288!

**Q: How does lookup work?**
> Simple indexing: If "cat" = token ID 1, just grab row 1 from the matrix. No computation needed - just memory access!

---

# 3. COMPLETE DATA FLOW

## Input: "I love AI" → Output: "J'aime l'IA"

---

## STAGE 1: TOKENIZATION

```
"I love AI" → Tokenizer → ["I", "love", "AI"] → [45, 2891, 15234]

The tokenizer:
- Splits text into tokens (can be words, subwords, or characters)
- Maps each token to its ID from vocabulary
- Common tokenizers: BPE (GPT), WordPiece (BERT), SentencePiece
```

---

## STAGE 2: EMBEDDING + POSITIONAL ENCODING

### Embedding Lookup
```
Token IDs [45, 2891, 15234]
                ↓
        Look up each row in E
                ↓
3 vectors, each with 512 numbers

"I"    → [0.12, -0.34, 0.56, ..., 0.23]   (512 values)
"love" → [0.45, 0.12, -0.78, ..., -0.11]  (512 values)
"AI"   → [-0.23, 0.89, 0.34, ..., 0.67]   (512 values)
```

### Why Positional Encoding?

**Problem**: Attention treats input as a SET, not a SEQUENCE. It doesn't know word order!
- "I love AI" would be same as "AI love I" without position info

**Solution**: Add position information to each embedding

```
Position 0 ("I"):    Add a specific pattern for "position 0"
Position 1 ("love"): Add a specific pattern for "position 1"  
Position 2 ("AI"):   Add a specific pattern for "position 2"

Final input = Token Embedding + Positional Encoding
```

**How is PE created?**
- Original paper: Fixed sine/cosine waves (not learned)
- Modern models (GPT, BERT): Learned positional embeddings
- Both work! Learned is slightly better but uses more parameters

---

## STAGE 3: ENCODER (Understanding the Input)

The encoder's job: **Build a rich understanding of the source sentence**

### What Goes Into Encoder
```
3 vectors (one per word), each 512-dimensional
Shape: (3 words, 512 dimensions)
```

### Inside Each Encoder Layer (6 layers total)

Each layer has 2 main parts:

#### Part A: Self-Attention
```
"I" looks at:     "I" (itself), "love", "AI"
"love" looks at:  "I", "love" (itself), "AI"  
"AI" looks at:    "I", "love", "AI" (itself)

Each word decides: "How much should I pay attention to each other word?"

Example attention for "love":
- "I": 30% attention (it's the subject doing the loving)
- "love": 50% attention (the word itself is important)
- "AI": 20% attention (it's what's being loved)

Result: "love" now contains information from all 3 words!
```

**Multi-Head Attention**: We do this 8 times in parallel, each "head" learning different patterns:
- Head 1: Might learn grammatical relationships
- Head 2: Might learn semantic relationships
- Head 3: Might learn positional patterns
- etc.

#### Part B: Feed-Forward Network
```
Each position goes through:
Linear layer (512 → 2048) → ReLU → Linear layer (2048 → 512)

This is individual processing - no interaction between positions
Adds computational power and non-linearity
```

#### Residual Connections + Layer Norm
```
After each part:
output = LayerNorm(input + sublayer_output)

Residual: Helps gradients flow (prevents vanishing gradient)
LayerNorm: Keeps values stable (mean=0, variance=1)
```

### What Comes Out of Encoder
```
3 vectors (same shape as input: 3 × 512)

But now each vector is CONTEXTUALIZED:
- "I" vector now knows it's the subject
- "love" vector knows it has subject "I" and object "AI"
- "AI" vector knows it's being loved

This encoder output is used by the decoder!
```

---

## STAGE 4: DECODER (Generating the Output)

The decoder's job: **Generate the target sentence one token at a time**

### Training vs Inference

**Training (Teacher Forcing)**:
```
We know the target: "J'aime l'IA"
Feed the WHOLE target (shifted) at once:
Input:  [<BOS>, "J'", "aime", "l'", "IA"]
Labels: ["J'", "aime", "l'", "IA", <EOS>]
```

**Inference (Auto-regressive)**:
```
Step 1: Input [<BOS>]           → Predict "J'"
Step 2: Input [<BOS>, "J'"]     → Predict "aime"
Step 3: Input [<BOS>, "J'", "aime"] → Predict "l'"
... continue until <EOS>
```

### Inside Each Decoder Layer (6 layers)

Each layer has 3 main parts:

#### Part A: Masked Self-Attention
```
SAME as encoder self-attention BUT with a mask!

When generating "aime", the model can only see:
- <BOS> ✓
- "J'"  ✓
- "aime" ✓ (current position)
- "l'"  ✗ (MASKED - can't see future!)
- "IA"  ✗ (MASKED - can't see future!)

Why mask? During inference, future tokens don't exist!
Training must simulate this constraint.
```

#### Part B: Cross-Attention (THE KEY COMPONENT!)
```
This is where ENCODER OUTPUT enters the decoder!

Query (Q): From decoder - "What am I looking for?"
Key (K):   From encoder - "What does the source have?"
Value (V): From encoder - "What information to retrieve?"

Example for "aime" position:
Q_aime asks: "I need to generate a French word, what English word should I translate?"

Attention scores (how much to look at each source word):
- "I":    20%  
- "love": 65%  ← Highest! "aime" is the translation of "love"
- "AI":   15%

Result: "aime" representation now contains mostly "love" information!

This is the TRANSLATION ALIGNMENT the model learns!
```

#### Part C: Feed-Forward Network
Same as encoder - individual position processing.

### What Comes Out of Decoder
```
5 vectors (one per target position), each 512-dimensional
Each vector contains:
- Information from previous target tokens (masked self-attention)
- Information from source sentence (cross-attention)
- Processed representations (FFN)
```

---

## STAGE 5: OUTPUT GENERATION

### Linear Projection
```
Each 512-dim vector → Project to vocabulary size (37,000)

decoder_output @ W_vocab = logits
(5, 512) @ (512, 37000) = (5, 37000)

Each position now has 37,000 scores - one per possible word
```

### Softmax → Probabilities
```
For position 0:
logits: [2.3, -1.2, 0.5, ..., 8.9, ..., 0.1]
                              ↑
                        Token for "J'"

softmax → probabilities: [0.01, 0.001, 0.002, ..., 0.75, ..., 0.0001]

"J'" has 75% probability - model predicts "J'"!
```

### Loss Calculation (Training)
```
Cross-entropy loss:
- Compare predicted probabilities with actual target
- Loss = -log(probability of correct answer)

If model predicts "J'" with 75% probability:
Loss = -log(0.75) = 0.29

Goal: Minimize loss = Maximize probability of correct tokens
```

---

# 4. THE THREE TYPES OF ATTENTION

| Attention Type | Where | Q From | K,V From | Mask? | Purpose |
|---------------|-------|--------|----------|-------|---------|
| **Encoder Self-Attention** | Encoder | Encoder | Encoder | No | Let source words see each other |
| **Decoder Masked Self-Attention** | Decoder | Decoder | Decoder | Yes (causal) | Let target words see previous target words only |
| **Cross-Attention** | Decoder | Decoder | Encoder | No | Let target words see ALL source words |

---

# 5. HOW ATTENTION ACTUALLY WORKS (Simple Version)

## The Q, K, V Concept

Think of it like a **search engine**:

```
Query (Q):  "What am I looking for?"
Key (K):    "What does each item have to offer?"
Value (V):  "What information does each item contain?"

Process:
1. Compare my Query with all Keys → Get relevance scores
2. Convert scores to weights (softmax) → Weights sum to 1
3. Weighted average of Values → My new representation
```

## Concrete Example

```
Sentence: "The cat sat on the mat"

When processing "sat":
Q_sat = "I'm a verb, what should I pay attention to?"

Comparing with all Keys:
- K_the:  Score = 0.5  (just an article)
- K_cat:  Score = 2.1  (the subject!)
- K_sat:  Score = 1.8  (myself)
- K_on:   Score = 0.3  (preposition)
- K_the2: Score = 0.2  (article)
- K_mat:  Score = 1.2  (location)

After softmax:
- "the":  5%
- "cat":  35%  ← Highest (subject of verb)
- "sat":  25%
- "on":   3%
- "the2": 2%
- "mat":  30%  ← Second highest (location)

New representation for "sat":
new_sat = 0.05×V_the + 0.35×V_cat + 0.25×V_sat + 0.03×V_on + 0.02×V_the2 + 0.30×V_mat

Now "sat" knows who did the sitting (cat) and where (mat)!
```

## Multi-Head Attention

```
Instead of one attention, do 8 in parallel:

Head 1: Might learn "who is the subject?"
Head 2: Might learn "what is the object?"
Head 3: Might learn "what's the next word?"
Head 4: Might learn "what's nearby?"
... etc

Each head has its own Q, K, V projections
Results are concatenated and mixed together
```

---

# 6. LAYER NORMALIZATION & RESIDUAL CONNECTIONS

## Residual Connection (Skip Connection)

```
output = input + sublayer(input)

Why?
- Gradients flow directly through the skip connection
- Prevents vanishing gradient in deep networks
- Model learns "what to add" rather than "complete transformation"
- If sublayer learns nothing useful, output ≈ input (safe default)
```

## Layer Normalization

```
For each position independently:
1. Calculate mean across all 512 dimensions
2. Calculate standard deviation
3. Normalize: (x - mean) / std
4. Scale and shift with learned parameters

Why?
- Keeps values in reasonable range
- Stabilizes training
- Each layer gets consistent input distribution
```

---

# 7. KEY DIMENSIONS

| Parameter | Original Paper | Meaning |
|-----------|---------------|---------|
| d_model | 512 | Embedding/hidden dimension |
| d_ff | 2048 | Feed-forward inner dimension (4× d_model) |
| num_heads | 8 | Number of attention heads |
| d_k = d_v | 64 | Dimension per head (d_model / num_heads) |
| num_layers | 6 | Encoder layers (6) + Decoder layers (6) |
| vocab_size | 37000 | Vocabulary size |

---

# 8. INTERVIEW QUESTIONS & ANSWERS

## Architecture Questions

**Q: Explain the Transformer architecture in 30 seconds.**
> Transformer has an encoder that reads the input sentence using self-attention (each word can see all other words), and a decoder that generates output one token at a time using masked self-attention (can't see future) and cross-attention (can see encoder output).

**Q: What's the difference between encoder and decoder?**
> Encoder: Bidirectional - each position sees ALL other positions. Processes whole input at once.
> Decoder: Causal/autoregressive - each position only sees PREVIOUS positions. Generates one token at a time. Also has cross-attention to look at encoder output.

**Q: Why is cross-attention needed?**
> It's the bridge between encoder and decoder. Decoder queries ask "what source information do I need?" and retrieve relevant information from encoder. This is how translation alignment is learned.

**Q: What would happen without positional encoding?**
> Model would treat input as a bag of words - "I love you" would be same as "you love I". No word order information.

## Attention Questions

**Q: Why multi-head instead of single-head attention?**
> Different heads learn different patterns (syntactic, semantic, positional, etc.). More expressive than single attention. Also cheaper computationally for same d_model.

**Q: Why scale by √d_k in attention?**
> Prevents dot products from getting too large, which would push softmax into saturation (outputting near one-hot vectors). Scaling keeps gradients healthy.

**Q: What's the complexity of self-attention?**
> O(n² × d) where n is sequence length. Quadratic in sequence length - problematic for very long sequences. This motivated efficient transformers (Linformer, Performer, etc.).

## Training Questions

**Q: How are embeddings trained?**
> Initialized randomly. During training, gradients from the loss flow back through the entire network. Embeddings are updated to minimize loss. After training, similar words have similar embeddings.

**Q: What is teacher forcing?**
> During training, we feed the CORRECT previous tokens to the decoder, not the model's own predictions. Faster and more stable training. During inference, we use the model's own predictions.

**Q: Why use label smoothing?**
> Instead of one-hot targets (100% on correct token), use soft targets (90% correct, 0.1% spread on others). Prevents overconfidence, improves generalization.

## Practical Questions

**Q: BERT vs GPT - what's the difference?**
> BERT: Encoder-only. Bidirectional (sees all words). Good for understanding tasks (classification, QA).
> GPT: Decoder-only. Unidirectional (can't see future). Good for generation tasks.

**Q: Why do modern LLMs use decoder-only?**
> Generation is the primary task. Simpler architecture. Can still do "understanding" tasks by framing them as generation. Scale better.

**Q: How does the model know when to stop generating?**
> Special <EOS> (end of sequence) token. Model predicts <EOS> when it thinks the sentence is complete. Also usually have a max length limit.

---

# 9. VISUAL SUMMARY

```
INPUT: "I love AI"
         │
         ▼
    ┌─────────────┐
    │ TOKENIZE    │  "I love AI" → [45, 2891, 15234]
    └─────────────┘
         │
         ▼
    ┌─────────────┐
    │ EMBED       │  Look up vectors from embedding matrix
    └─────────────┘
         │
         ▼
    ┌─────────────┐
    │ + POSITION  │  Add positional encoding
    └─────────────┘
         │
         ▼
    ┌─────────────────────────────────────────┐
    │            ENCODER (×6 layers)          │
    │  ┌────────────────────────────────────┐ │
    │  │ Self-Attention                     │ │
    │  │ Each word attends to ALL words     │ │
    │  └────────────────────────────────────┘ │
    │  ┌────────────────────────────────────┐ │
    │  │ Feed-Forward Network               │ │
    │  │ Process each position individually │ │
    │  └────────────────────────────────────┘ │
    └─────────────────────────────────────────┘
         │
         │ ENCODER OUTPUT (rich representations)
         │
         ▼
    ┌─────────────────────────────────────────┐
    │            DECODER (×6 layers)          │
    │  ┌────────────────────────────────────┐ │
    │  │ Masked Self-Attention              │ │
    │  │ Each word attends to PREVIOUS only │ │
    │  └────────────────────────────────────┘ │
    │  ┌────────────────────────────────────┐ │
    │  │ Cross-Attention                    │ │
    │  │ Attend to ENCODER OUTPUT      ◀────┼─┘
    │  └────────────────────────────────────┘
    │  ┌────────────────────────────────────┐
    │  │ Feed-Forward Network               │
    │  └────────────────────────────────────┘
    └─────────────────────────────────────────┘
         │
         ▼
    ┌─────────────┐
    │ LINEAR      │  Project to vocabulary size
    └─────────────┘
         │
         ▼
    ┌─────────────┐
    │ SOFTMAX     │  Get probabilities
    └─────────────┘
         │
         ▼
    OUTPUT: "J'aime l'IA"
```

---

# 10. QUICK FACTS FOR INTERVIEWS

- **Parameters in base model**: ~65 million
- **Embedding parameters**: vocab_size × d_model = 37000 × 512 = 19M
- **Attention parameters per layer**: 4 × d_model² = 4 × 512² = 1M
- **FFN parameters per layer**: 2 × d_model × d_ff = 2 × 512 × 2048 = 2M
- **Training time (original)**: 3.5 days on 8 P100 GPUs
- **Sequence length limit**: Fixed (usually 512 or 2048) due to positional encoding
- **Main innovation**: Replaced recurrence with attention - enables parallelization

---

# 11. COMMON MISCONCEPTIONS

❌ "Embeddings are pre-trained separately"
✓ Embeddings are trained together with the whole model (end-to-end)

❌ "Attention replaces everything"
✓ FFN is equally important - provides capacity and non-linearity

❌ "Position is encoded in embeddings"
✓ Position is ADDED to embeddings as a separate signal

❌ "Cross-attention goes both ways"
✓ Cross-attention only flows decoder→encoder (decoder queries, encoder provides K,V)

❌ "Encoder and decoder share parameters"
✓ They have separate parameters (except sometimes the embedding matrix)
