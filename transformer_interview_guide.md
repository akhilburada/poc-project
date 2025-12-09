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

# 3. UNDERSTANDING QUERY, KEY, VALUE (Q, K, V)

**This is the CORE of attention - understand this first!**

---

## The Real-World Analogy: Library Search

```
Imagine you're in a library looking for information:

YOU have a QUESTION (Query):
   "I want to learn about machine learning"

Each BOOK has a LABEL (Key):
   Book 1: "Cooking recipes"
   Book 2: "Machine learning basics"
   Book 3: "History of France"
   Book 4: "Deep learning guide"

Each BOOK has CONTENT (Value):
   Book 1: [recipes, ingredients, cooking tips...]
   Book 2: [ML algorithms, neural networks, training...]
   Book 3: [French revolution, Napoleon, Paris...]
   Book 4: [backprop, transformers, GPT...]

PROCESS:
1. Compare your Question with each Label → Get relevance scores
   - "Cooking recipes" vs your question → Low match (0.1)
   - "Machine learning basics" vs your question → High match (0.8)
   - "History of France" vs your question → Low match (0.05)
   - "Deep learning guide" vs your question → High match (0.7)

2. Normalize scores (softmax) → They sum to 1
   - Cooking: 0.05
   - ML basics: 0.50  ← Most relevant!
   - History: 0.02
   - Deep learning: 0.43

3. Get weighted mix of Content
   - Your answer = 0.05×(Cooking content) + 0.50×(ML content) + 
                   0.02×(History content) + 0.43×(DL content)
   
   Result: Mostly ML and DL information!
```

---

## In Transformers: Every Word Searches Every Other Word

```
Sentence: "The cat sat on the mat"

When processing "sat":
- "sat" has a QUERY: "What information do I need?"
- Every word has a KEY: "Here's what I offer"
- Every word has a VALUE: "Here's my actual information"

"sat" compares its Query with all Keys:
- Query_sat vs Key_the  → Low relevance (article, not important)
- Query_sat vs Key_cat  → HIGH relevance (who is sitting!)
- Query_sat vs Key_sat  → Medium relevance (myself)
- Query_sat vs Key_on   → Low relevance
- Query_sat vs Key_the  → Low relevance  
- Query_sat vs Key_mat  → HIGH relevance (where sitting!)

Result: "sat" gathers information mostly from "cat" and "mat"
        Now "sat" knows WHO sat and WHERE!
```

---

## How Are Q, K, V Created?

### Step 1: Start with Word Embeddings

```
Each word starts as a vector (from embedding matrix):

"I"    → [0.2, -0.5, 0.8, ..., 0.3]   (512 numbers)
"love" → [0.6, 0.1, -0.4, ..., 0.7]   (512 numbers)
"AI"   → [-0.3, 0.9, 0.2, ..., -0.1]  (512 numbers)

These are the raw word representations.
```

### Step 2: Transform into Q, K, V using Learned Weights

```
The model has THREE weight matrices (learned during training):

W_Q (Query weights):  512 × 512 matrix
W_K (Key weights):    512 × 512 matrix
W_V (Value weights):  512 × 512 matrix

For each word, we create THREE different vectors:

┌─────────────────────────────────────────────────────────────────┐
│  For word "love":                                                │
│                                                                  │
│  Q_love = embedding_love × W_Q                                  │
│         = [0.6, 0.1, -0.4, ..., 0.7] × [512×512 matrix]         │
│         = [0.3, -0.2, 0.9, ..., 0.1]  ← Query vector            │
│                                                                  │
│  K_love = embedding_love × W_K                                  │
│         = [0.6, 0.1, -0.4, ..., 0.7] × [512×512 matrix]         │
│         = [0.5, 0.4, -0.1, ..., 0.8]  ← Key vector              │
│                                                                  │
│  V_love = embedding_love × W_V                                  │
│         = [0.6, 0.1, -0.4, ..., 0.7] × [512×512 matrix]         │
│         = [-0.2, 0.7, 0.3, ..., 0.6]  ← Value vector            │
└─────────────────────────────────────────────────────────────────┘

Same process for every word in the sentence!
```

### Step 3: Result - Every Word Has Q, K, V

```
After transformation:

Word "I":
   Q_I = [...]    "What am I looking for?"
   K_I = [...]    "What do I offer to others?"
   V_I = [...]    "What information do I contain?"

Word "love":
   Q_love = [...]  "What am I looking for?"
   K_love = [...]  "What do I offer to others?"
   V_love = [...]  "What information do I contain?"

Word "AI":
   Q_AI = [...]   "What am I looking for?"
   K_AI = [...]   "What do I offer to others?"
   V_AI = [...]   "What information do I contain?"
```

---

## Why Three DIFFERENT Vectors?

```
Q, K, V serve different purposes:

QUERY (Q): "What am I searching for?"
   - Represents what this word NEEDS from other words
   - A verb might query for its subject/object
   - A pronoun might query for what it refers to

KEY (K): "What can others find in me?"
   - Represents what this word OFFERS to other words
   - Like a label or index for the word
   - Used to match against queries

VALUE (V): "What information will I give?"
   - The actual CONTENT to pass along
   - When a word is attended to, its Value is retrieved
   - Contains the useful information

───────────────────────────────────────────────────
ANALOGY: Dating App

Query = "What am I looking for in a partner?"
Key = "How do I describe myself?"
Value = "My actual personality/information"

Matching process:
1. Compare my Query with everyone's Key
2. Find high matches (compatibility scores)
3. Get their Values (learn about them)
───────────────────────────────────────────────────
```

---

## Why Use Weight Matrices (W_Q, W_K, W_V)?

```
Q1: Why not just use the embedding directly?

The raw embedding is the SAME for all purposes.
But we need DIFFERENT representations for different roles:

- When QUERYING: Word needs to express what it's looking for
- When being a KEY: Word needs to express what it offers
- When being a VALUE: Word needs to provide actual content

Weight matrices TRANSFORM the embedding into specialized versions!

───────────────────────────────────────────────────
Q2: How are W_Q, W_K, W_V learned?

Same as all neural network weights:
- Start with random values
- During training, backpropagation adjusts them
- They learn to create useful Q, K, V representations
- After training, they know how to transform words properly
───────────────────────────────────────────────────
```

---

## The Complete Attention Process (Summary)

```
INPUT: 3 word embeddings (each 512-dim)
       "I", "love", "AI"

STEP 1: Create Q, K, V for each word
        Q = embeddings × W_Q  → 3 query vectors
        K = embeddings × W_K  → 3 key vectors
        V = embeddings × W_V  → 3 value vectors

STEP 2: Calculate attention scores
        For each word, compare its Q with ALL Ks
        scores = Q × K^T (dot product)
        
        Result: 3×3 matrix (every word to every word)
        
                    K_I    K_love   K_AI
               ┌─────────┬─────────┬─────────┐
        Q_I    │  score  │  score  │  score  │
               ├─────────┼─────────┼─────────┤
        Q_love │  score  │  score  │  score  │
               ├─────────┼─────────┼─────────┤
        Q_AI   │  score  │  score  │  score  │
               └─────────┴─────────┴─────────┘

STEP 3: Scale scores
        Divide by √(dimension) to keep values manageable

STEP 4: Softmax (per row)
        Convert scores to probabilities (sum to 1)
        
                    K_I    K_love   K_AI    SUM
               ┌─────────┬─────────┬─────────┐
        Q_I    │  0.50   │  0.30   │  0.20   │ = 1.0
               ├─────────┼─────────┼─────────┤
        Q_love │  0.25   │  0.55   │  0.20   │ = 1.0
               ├─────────┼─────────┼─────────┤
        Q_AI   │  0.15   │  0.25   │  0.60   │ = 1.0
               └─────────┴─────────┴─────────┘

STEP 5: Weighted sum of Values
        For each word, mix all Values using attention weights
        
        new_I    = 0.50×V_I + 0.30×V_love + 0.20×V_AI
        new_love = 0.25×V_I + 0.55×V_love + 0.20×V_AI
        new_AI   = 0.15×V_I + 0.25×V_love + 0.60×V_AI

OUTPUT: 3 NEW vectors (each 512-dim)
        Each word now contains information from ALL words!
        "love" knows about "I" (subject) and "AI" (object)
```

---

## Interview Quick Answers

**Q: What are Q, K, V?**
> Query is what a word is searching for. Key is what a word offers. Value is the information retrieved. Each word has all three, created by multiplying embedding with learned weight matrices.

**Q: How are Q, K, V calculated?**
> Q = embedding × W_Q, K = embedding × W_K, V = embedding × W_V. The weight matrices are learned during training.

**Q: Why do we need separate Q, K, V? Why not use embedding directly?**
> A word needs different representations for different purposes - what it's looking for (Q) vs what it offers (K) vs what information it contains (V). Weight matrices create these specialized versions.

**Q: What do the attention scores mean?**
> How relevant each word is to each other word. High score = high relevance = more information will be retrieved from that word's Value.

---

# 4. COMPLETE DATA FLOW

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

X = [
    [0.12, -0.34, 0.56, ..., 0.23],   ← "I" (512 numbers)
    [0.45, 0.12, -0.78, ..., -0.11],  ← "love" (512 numbers)
    [-0.23, 0.89, 0.34, ..., 0.67]    ← "AI" (512 numbers)
]
```

### Inside Each Encoder Layer (6 layers total)

Each layer has 2 main parts:

---

#### Part A: Self-Attention (DETAILED)

**Step 1: Create Query, Key, Value**

The model has 3 learned weight matrices: W_Q, W_K, W_V (each is 512 × 512)

```
For EACH word, we create 3 different vectors:

Q (Query) = "What am I looking for?"
K (Key)   = "What do I contain that others might want?"
V (Value) = "What information will I give if someone attends to me?"

How to calculate:
┌─────────────────────────────────────────────────────────────────┐
│  Q = X × W_Q    (input × weight matrix)                         │
│  K = X × W_K                                                     │
│  V = X × W_V                                                     │
│                                                                  │
│  X shape: (3 words, 512)                                        │
│  W_Q shape: (512, 512)                                          │
│  Q shape: (3 words, 512)                                        │
└─────────────────────────────────────────────────────────────────┘

Result for our 3 words:
Q = [Q_I, Q_love, Q_AI]       ← 3 query vectors
K = [K_I, K_love, K_AI]       ← 3 key vectors  
V = [V_I, V_love, V_AI]       ← 3 value vectors
```

**Step 2: Calculate Attention Scores**

Each word compares its Query with ALL Keys:

```
"How relevant is each word to me?"

For word "love":
┌─────────────────────────────────────────────────────────────────┐
│  score(love→I)    = Q_love · K_I    (dot product)              │
│  score(love→love) = Q_love · K_love                             │
│  score(love→AI)   = Q_love · K_AI                               │
└─────────────────────────────────────────────────────────────────┘

Dot product = multiply matching dimensions and sum
If Q_love and K_I point in similar direction → HIGH score
If they point in different directions → LOW score

Full attention score matrix (all words):
              K_I    K_love   K_AI
         ┌─────────┬─────────┬─────────┐
Q_I      │   1.2   │   0.8   │   0.5   │
         ├─────────┼─────────┼─────────┤
Q_love   │   2.1   │   1.8   │   0.9   │
         ├─────────┼─────────┼─────────┤
Q_AI     │   0.6   │   1.1   │   1.5   │
         └─────────┴─────────┴─────────┘
```

**Step 3: Scale the Scores**

```
Divide by √64 (square root of dimension per head)

Why? Large dot products → softmax becomes too "sharp" (nearly one-hot)
Scaling keeps gradients healthy

Scaled scores = scores / 8
```

**Step 4: Softmax → Attention Weights**

```
Convert scores to probabilities (each row sums to 1)

              K_I    K_love   K_AI     SUM
         ┌─────────┬─────────┬─────────┐
Q_I      │  0.50   │  0.30   │  0.20   │ = 1.0
         ├─────────┼─────────┼─────────┤
Q_love   │  0.30   │  0.50   │  0.20   │ = 1.0
         ├─────────┼─────────┼─────────┤
Q_AI     │  0.20   │  0.35   │  0.45   │ = 1.0
         └─────────┴─────────┴─────────┘

Reading: "love" pays 30% attention to "I", 50% to itself, 20% to "AI"
```

**Step 5: Weighted Sum of Values**

```
For each word, mix the Values based on attention weights:

new_love = 0.30 × V_I + 0.50 × V_love + 0.20 × V_AI
           └─────────────────────────────────────────┘
           "love" now contains info from ALL words!

new_I    = 0.50 × V_I + 0.30 × V_love + 0.20 × V_AI
new_AI   = 0.20 × V_I + 0.35 × V_love + 0.45 × V_AI
```

**Step 6: Output Projection**

```
Final step: multiply by another weight matrix W_O (512 × 512)

attention_output = weighted_values × W_O

This mixes all the information together
```

**Multi-Head Attention: Do This 8 Times in Parallel**

```
Instead of one attention with 512 dimensions:
→ Split into 8 heads, each with 64 dimensions

Head 1: Uses W_Q1, W_K1, W_V1 (each 512 → 64)
Head 2: Uses W_Q2, W_K2, W_V2 (each 512 → 64)
...
Head 8: Uses W_Q8, W_K8, W_V8 (each 512 → 64)

Each head learns DIFFERENT patterns:
- Head 1: Might learn "who is the subject?"
- Head 2: Might learn "what is the object?"
- Head 3: Might learn "what words are nearby?"
- Head 4: Might learn "what's the main verb?"
- etc.

Finally: Concatenate all 8 heads → 8 × 64 = 512 dimensions
         Then multiply by W_O to mix them
```

**After Self-Attention + Residual + LayerNorm**:
```
output = LayerNorm(X + attention_output)

Residual (X +): Gradient flows directly, prevents vanishing gradient
LayerNorm: Normalizes values for stability
```

---

#### Part B: Feed-Forward Network (DETAILED)

After attention, each position is processed INDEPENDENTLY (no mixing between positions).

**Structure**:
```
┌─────────────────────────────────────────────────────────────────┐
│  FFN has 2 linear layers with ReLU activation between them      │
│                                                                  │
│  Step 1: Expand                                                  │
│  hidden = X × W1 + b1                                           │
│  (3, 512) × (512, 2048) = (3, 2048)                             │
│                                                                  │
│  Step 2: ReLU activation                                        │
│  hidden = ReLU(hidden)                                          │
│  ReLU(x) = max(0, x)  ← keeps positive, zeros negative          │
│                                                                  │
│  Step 3: Compress back                                          │
│  output = hidden × W2 + b2                                      │
│  (3, 2048) × (2048, 512) = (3, 512)                             │
└─────────────────────────────────────────────────────────────────┘
```

**Why Expand then Compress?**
```
512 → 2048 → 512

- More parameters = more learning capacity
- ReLU adds non-linearity (network can learn complex patterns)
- Think of it as "thinking space" - expand to process, compress to output
- 2048 = 4× expansion is standard (can be adjusted)
```

**What FFN Does**:
```
- Processes each position's representation
- Adds non-linear transformation
- NO interaction between positions (unlike attention)
- Attention = "gather information from others"
- FFN = "process the gathered information"
```

**After FFN + Residual + LayerNorm**:
```
output = LayerNorm(attention_output + ffn_output)
```

---

#### Complete Encoder Layer Flow
```
Input X (3 words × 512 dim)
    │
    ▼
┌─────────────────────────┐
│ Self-Attention          │
│ Q, K, V → Scores →      │
│ Softmax → Weighted Sum  │
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    │   + (Residual)│ ← Add original input
    └───────┬───────┘
            │
    ┌───────┴───────┐
    │  LayerNorm    │
    └───────┬───────┘
            │
            ▼
┌─────────────────────────┐
│ Feed-Forward Network    │
│ Linear → ReLU → Linear  │
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    │   + (Residual)│ ← Add attention output
    └───────┬───────┘
            │
    ┌───────┴───────┐
    │  LayerNorm    │
    └───────┬───────┘
            │
            ▼
Output (3 words × 512 dim) → Goes to next encoder layer
```

---

### What Comes Out of Encoder (After 6 Layers)
```
3 vectors (same shape as input: 3 × 512)

But now each vector is DEEPLY CONTEXTUALIZED:

Original "I":   Just knew "I am the word I"
After Encoder:  "I am the subject, I am doing the loving, 
                 the object is AI, I come first in sentence"

Original "love": Just knew "I am the word love"
After Encoder:   "I am a verb, my subject is I, my object is AI,
                  I express positive emotion, I'm in middle position"

Original "AI":   Just knew "I am the word AI"  
After Encoder:   "I am the object being loved, the lover is I,
                  I come at the end, I'm a technology term"

This rich encoder output goes to the decoder!
```

---

## STAGE 4: DECODER (Generating the Output)

The decoder's job: **Generate the target sentence one token at a time**

### Where Does the Target Come From?

**THIS IS IMPORTANT**: During training, we have a **parallel corpus** (dataset of paired sentences):

```
Training Dataset (millions of pairs):
┌────────────────────────────────────────────────────────┐
│  Source (English)     │  Target (French)              │
├───────────────────────┼───────────────────────────────┤
│  "I love AI"          │  "J'aime l'IA"                │
│  "Hello world"        │  "Bonjour monde"              │
│  "The cat is black"   │  "Le chat est noir"          │
│  "How are you?"       │  "Comment allez-vous?"       │
│  ... millions more    │  ...                          │
└───────────────────────┴───────────────────────────────┘

The model learns from these pairs!
- Source goes into Encoder
- Target is used by Decoder (during training)
- Model learns to predict target given source
```

**Where do parallel corpora come from?**
- Human translators (UN documents, EU parliament)
- Existing bilingual websites
- Books translated to multiple languages
- Crowdsourced translations

---

### Training vs Inference

**Training (Teacher Forcing)**:
```
We KNOW the correct target from our dataset!

Source: "I love AI"           → Encoder
Target: "J'aime l'IA"         → Decoder uses this!

Decoder Input (shifted right):
[<BOS>, "J'", "aime", "l'", "IA"]

What model should predict (labels):
["J'", "aime", "l'", "IA", <EOS>]

Teacher forcing = We give the model the CORRECT previous tokens
                 (not its own predictions)
Why? Faster, more stable training
```

**Inference (Auto-regressive)**:
```
We DON'T know the target - we're generating it!

Step 1: Input [<BOS>]               → Model predicts "J'"
Step 2: Input [<BOS>, "J'"]         → Model predicts "aime"
Step 3: Input [<BOS>, "J'", "aime"] → Model predicts "l'"
Step 4: Input [<BOS>, "J'", "aime", "l'"] → Model predicts "IA"
Step 5: Input [<BOS>, "J'", "aime", "l'", "IA"] → Model predicts <EOS>
STOP!

Each step uses the model's OWN previous predictions
```

---

### Inside Each Decoder Layer (6 layers)

Each layer has 3 main parts:

---

#### Part A: Masked Self-Attention (DETAILED)

**Same as encoder self-attention, BUT with a crucial difference: CAUSAL MASK**

**Step 1: Create Q, K, V from Decoder Input**

```
Decoder input: [<BOS>, "J'", "aime", "l'", "IA"]
                 pos0   pos1   pos2   pos3  pos4

Same as encoder:
Q = decoder_input × W_Q  → 5 query vectors
K = decoder_input × W_K  → 5 key vectors
V = decoder_input × W_V  → 5 value vectors
```

**Step 2: Calculate Attention Scores**

```
Same as encoder: Q × K^T to get scores

              K_BOS  K_J'  K_aime  K_l'  K_IA
         ┌────────┬───────┬───────┬──────┬──────┐
Q_BOS    │  2.1   │  1.5  │  0.8  │  0.6 │  0.4 │
Q_J'     │  1.8   │  2.3  │  1.2  │  0.7 │  0.5 │
Q_aime   │  1.1   │  1.9  │  2.0  │  1.3 │  0.9 │
Q_l'     │  0.9   │  1.4  │  1.6  │  1.8 │  1.1 │
Q_IA     │  0.7   │  1.2  │  1.4  │  1.5 │  2.2 │
         └────────┴───────┴───────┴──────┴──────┘
```

**Step 3: Apply the Causal Mask (THE KEY DIFFERENCE!)**

```
MASK future positions with -infinity:

              K_BOS  K_J'  K_aime  K_l'  K_IA
         ┌────────┬───────┬───────┬──────┬──────┐
Q_BOS    │  2.1   │  -∞   │  -∞   │  -∞  │  -∞  │  ← Can only see itself
Q_J'     │  1.8   │  2.3  │  -∞   │  -∞  │  -∞  │  ← Can see BOS, itself
Q_aime   │  1.1   │  1.9  │  2.0  │  -∞  │  -∞  │  ← Can see BOS, J', itself
Q_l'     │  0.9   │  1.4  │  1.6  │  1.8 │  -∞  │  ← Can see first 4
Q_IA     │  0.7   │  1.2  │  1.4  │  1.5 │  2.2 │  ← Can see all
         └────────┴───────┴───────┴──────┴──────┘

The mask is a upper triangular matrix of -infinity values
```

**Step 4: Softmax (with mask)**

```
softmax(-∞) = 0  ← Future positions get ZERO attention!

After softmax:
              K_BOS  K_J'  K_aime  K_l'  K_IA   SUM
         ┌────────┬───────┬───────┬──────┬──────┐
Q_BOS    │  1.00  │  0    │  0    │  0   │  0   │ = 1.0
Q_J'     │  0.38  │  0.62 │  0    │  0   │  0   │ = 1.0
Q_aime   │  0.22  │  0.39 │  0.39 │  0   │  0   │ = 1.0
Q_l'     │  0.15  │  0.25 │  0.28 │  0.32│  0   │ = 1.0
Q_IA     │  0.10  │  0.18 │  0.22 │  0.23│  0.27│ = 1.0
         └────────┴───────┴───────┴──────┴──────┘

Notice: Each row only has non-zero values for current and past positions!
```

**Step 5: Weighted Sum of Values**

```
For "aime" (position 2):
new_aime = 0.22 × V_BOS + 0.39 × V_J' + 0.39 × V_aime + 0 × V_l' + 0 × V_IA
         = 0.22 × V_BOS + 0.39 × V_J' + 0.39 × V_aime
         
"aime" CANNOT see "l'" or "IA" - they're masked out!
```

**Why is Masking Necessary?**
```
During INFERENCE:
- When generating "aime", the words "l'" and "IA" DON'T EXIST YET
- We can't look at something that hasn't been generated

During TRAINING:
- We have the full target, but we MUST simulate inference conditions
- If model could see future tokens, it would just copy them (cheating!)
- Mask ensures model learns to predict based only on past
```

**After Masked Self-Attention + Residual + LayerNorm**:
```
output = LayerNorm(decoder_input + masked_attention_output)
```

---

#### Part B: Cross-Attention (DETAILED) - THE BRIDGE!

**This is where the ENCODER OUTPUT enters the decoder!**

**Key Insight**:
```
Q (Query)  → comes from DECODER (current target state)
K (Key)    → comes from ENCODER (source sentence info)
V (Value)  → comes from ENCODER (source sentence info)

Decoder asks: "What information from the source do I need?"
Encoder provides: "Here's what each source word contains"
```

**Step 1: Create Q from Decoder, K and V from Encoder**

```
┌─────────────────────────────────────────────────────────────────┐
│  Q = decoder_state × W_Q_cross                                   │
│      (5 decoder positions × 512)                                 │
│                                                                  │
│  K = encoder_output × W_K_cross                                  │
│      (3 encoder positions × 512)                                 │
│                                                                  │
│  V = encoder_output × W_V_cross                                  │
│      (3 encoder positions × 512)                                 │
│                                                                  │
│  Note: W_Q_cross, W_K_cross, W_V_cross are DIFFERENT weights    │
│        from the self-attention weights!                          │
└─────────────────────────────────────────────────────────────────┘

Result:
Q = [Q_BOS, Q_J', Q_aime, Q_l', Q_IA]   ← 5 decoder queries
K = [K_I, K_love, K_AI]                  ← 3 encoder keys
V = [V_I, V_love, V_AI]                  ← 3 encoder values
```

**Step 2: Calculate Cross-Attention Scores**

```
Each DECODER position attends to ALL ENCODER positions

Scores = Q × K^T
(5 decoder, 512) × (512, 3 encoder) = (5, 3)

            K_I    K_love   K_AI   (ENCODER)
       ┌─────────┬─────────┬─────────┐
Q_BOS  │   0.8   │   1.2   │   0.9   │  ← BOS looks at source
Q_J'   │   2.5   │   0.7   │   0.6   │  ← "J'" looks at source
Q_aime │   0.9   │   2.8   │   0.8   │  ← "aime" looks at source
Q_l'   │   0.6   │   1.1   │   2.4   │  ← "l'" looks at source
Q_IA   │   0.5   │   0.9   │   2.9   │  ← "IA" looks at source
       └─────────┴─────────┴─────────┘
(DECODER)

Notice: EVERY decoder position can see ALL encoder positions
        NO MASK here - we want full access to source!
```

**Step 3: Softmax → Cross-Attention Weights**

```
            K_I    K_love   K_AI    SUM
       ┌─────────┬─────────┬─────────┐
Q_BOS  │  0.28   │  0.42   │  0.30   │ = 1.0  (general attention)
Q_J'   │  0.70   │  0.18   │  0.12   │ = 1.0  ← "J'" attends to "I"!
Q_aime │  0.18   │  0.68   │  0.14   │ = 1.0  ← "aime" attends to "love"!
Q_l'   │  0.15   │  0.25   │  0.60   │ = 1.0  ← "l'" attends to "AI"
Q_IA   │  0.12   │  0.20   │  0.68   │ = 1.0  ← "IA" attends to "AI"!
       └─────────┴─────────┴─────────┘

THIS IS THE TRANSLATION ALIGNMENT!
- "J'" (French "I") strongly attends to "I" (English) ✓
- "aime" (French "love") strongly attends to "love" (English) ✓
- "IA" (French "AI") strongly attends to "AI" (English) ✓

The model LEARNS these alignments during training!
```

**Step 4: Weighted Sum of Encoder Values**

```
For "aime" position:
new_aime = 0.18 × V_I + 0.68 × V_love + 0.14 × V_AI
                        └─────────────┘
                        Mostly "love" information!

"aime" now contains:
- 18% information about "I"
- 68% information about "love" (its translation!)
- 14% information about "AI"
```

**Step 5: Output Projection**

```
cross_attention_output = weighted_values × W_O_cross
```

**After Cross-Attention + Residual + LayerNorm**:
```
output = LayerNorm(masked_attn_output + cross_attention_output)
```

---

#### Part C: Feed-Forward Network (DETAILED)

**Same structure as encoder FFN, applied to each decoder position independently**

```
Input: (5 decoder positions × 512)

┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Expand to higher dimension                             │
│  hidden = input × W1 + b1                                       │
│  (5, 512) × (512, 2048) = (5, 2048)                             │
│                                                                  │
│  Step 2: Non-linear activation                                  │
│  hidden = ReLU(hidden)                                          │
│  - Negative values → 0                                          │
│  - Positive values → unchanged                                  │
│  - Adds non-linearity so network can learn complex patterns     │
│                                                                  │
│  Step 3: Compress back                                          │
│  output = hidden × W2 + b2                                      │
│  (5, 2048) × (2048, 512) = (5, 512)                             │
└─────────────────────────────────────────────────────────────────┘
```

**What FFN Does in Decoder**:
```
After attention layers, each position has:
- Information from previous target tokens (masked self-attn)
- Information from source sentence (cross-attn)

FFN processes this combined information:
- Applies learned transformations
- Prepares representation for next layer or output
- Adds capacity to learn complex mappings

Important: FFN is applied INDEPENDENTLY to each position
           No mixing between positions (that's attention's job)
```

**After FFN + Residual + LayerNorm**:
```
output = LayerNorm(cross_attn_output + ffn_output)

This output either:
- Goes to the next decoder layer (layers 1-5)
- Goes to output projection (after layer 6)
```

---

#### Complete Decoder Layer Flow
```
Decoder Input (5 positions × 512)
    │
    ▼
┌─────────────────────────┐
│ Masked Self-Attention   │
│ Q, K, V from decoder    │
│ + Causal mask           │
│ (can't see future)      │
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    │   + Residual  │
    └───────┬───────┘
    ┌───────┴───────┐
    │   LayerNorm   │
    └───────┬───────┘
            │
            ▼
┌─────────────────────────┐
│ Cross-Attention         │
│ Q from decoder          │
│ K, V from ENCODER ◀─────┼──── Encoder Output (3 × 512)
│ (sees full source)      │
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    │   + Residual  │
    └───────┬───────┘
    ┌───────┴───────┐
    │   LayerNorm   │
    └───────┬───────┘
            │
            ▼
┌─────────────────────────┐
│ Feed-Forward Network    │
│ 512 → 2048 → 512        │
└───────────┬─────────────┘
            │
    ┌───────┴───────┐
    │   + Residual  │
    └───────┬───────┘
    ┌───────┴───────┐
    │   LayerNorm   │
    └───────┬───────┘
            │
            ▼
Output (5 positions × 512) → Next decoder layer
```

---

### What Comes Out of Decoder (After 6 Layers)
```
5 vectors (one per target position), each 512-dimensional

Each vector now contains:
┌─────────────────────────────────────────────────────────────────┐
│  Position 0 (after BOS):                                        │
│  - Knows it's the start of French sentence                      │
│  - Has info from encoder about "I love AI"                      │
│  - Ready to predict first word "J'"                             │
│                                                                  │
│  Position 1 (after J'):                                         │
│  - Knows "J'" was generated                                     │
│  - Strongly connected to "I" from source                        │
│  - Ready to predict "aime"                                      │
│                                                                  │
│  Position 2 (after aime):                                       │
│  - Knows "J' aime" so far                                       │
│  - Strongly connected to "love" from source                     │
│  - Ready to predict "l'"                                        │
│                                                                  │
│  ... and so on                                                  │
└─────────────────────────────────────────────────────────────────┘
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

# 5. THE THREE TYPES OF ATTENTION

| Attention Type | Where | Q From | K,V From | Mask? | Purpose |
|---------------|-------|--------|----------|-------|---------|
| **Encoder Self-Attention** | Encoder | Encoder | Encoder | No | Let source words see each other |
| **Decoder Masked Self-Attention** | Decoder | Decoder | Decoder | Yes (causal) | Let target words see previous target words only |
| **Cross-Attention** | Decoder | Decoder | Encoder | No | Let target words see ALL source words |

---

# 6. HOW ATTENTION ACTUALLY WORKS (Simple Version)

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

# 7. LAYER NORMALIZATION & RESIDUAL CONNECTIONS

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

# 8. KEY DIMENSIONS

| Parameter | Original Paper | Meaning |
|-----------|---------------|---------|
| d_model | 512 | Embedding/hidden dimension |
| d_ff | 2048 | Feed-forward inner dimension (4× d_model) |
| num_heads | 8 | Number of attention heads |
| d_k = d_v | 64 | Dimension per head (d_model / num_heads) |
| num_layers | 6 | Encoder layers (6) + Decoder layers (6) |
| vocab_size | 37000 | Vocabulary size |

---

# 9. INTERVIEW QUESTIONS & ANSWERS

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

# 10. VISUAL SUMMARY

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

# 11. QUICK FACTS FOR INTERVIEWS

- **Parameters in base model**: ~65 million
- **Embedding parameters**: vocab_size × d_model = 37000 × 512 = 19M
- **Attention parameters per layer**: 4 × d_model² = 4 × 512² = 1M
- **FFN parameters per layer**: 2 × d_model × d_ff = 2 × 512 × 2048 = 2M
- **Training time (original)**: 3.5 days on 8 P100 GPUs
- **Sequence length limit**: Fixed (usually 512 or 2048) due to positional encoding
- **Main innovation**: Replaced recurrence with attention - enables parallelization

---

# 12. COMMON MISCONCEPTIONS

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
