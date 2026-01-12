# LLM & Agent Evaluation - Complete Interview Guide

---

## 1. Introduction to LLM Evaluation

### What is LLM Evaluation?
LLM Evaluation is the process of measuring how well a language model performs on specific tasks. It helps us understand model capabilities, limitations, and suitability for production use.

### Why is Evaluation Important?

| Purpose | Description |
|---------|-------------|
| **Model Selection** | Choose the best model for your use case |
| **Quality Assurance** | Ensure outputs meet required standards |
| **Identify Weaknesses** | Find hallucinations, biases, errors |
| **Compare Models** | Benchmark different models objectively |
| **Track Improvements** | Measure impact of fine-tuning or prompt changes |
| **Cost Optimization** | Balance performance vs API costs |

### Types of Evaluation

**1. Offline Evaluation**
- Done before deployment using test datasets
- Controlled environment with known answers
- Examples: Running benchmarks, testing on held-out data

**2. Online Evaluation**
- Done after deployment with real users
- Measures actual production performance
- Examples: A/B testing, user feedback analysis

---

## 2. Evaluation Metrics - Detailed Explanation

### 2.1 Text Generation Metrics

#### BLEU (Bilingual Evaluation Understudy)
- **Purpose**: Measures n-gram overlap between generated text and reference
- **Focus**: Precision-oriented (how much of generated text matches reference)
- **Range**: 0 to 1 (higher is better)
- **Best for**: Machine translation

**How it works:**
```
Generated: "The cat sat on the mat"
Reference: "The cat is on the mat"

Unigram matches: the, cat, on, the, mat = 5/6 = 0.83
Bigram matches: the cat, on the, the mat = 3/5 = 0.60

BLEU combines n-gram precisions with brevity penalty
```

**Limitations:**
- Doesn't understand meaning (synonyms scored as wrong)
- Penalizes valid paraphrases
- Requires exact word matches

---

#### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
- **Purpose**: Measures overlap focusing on recall
- **Focus**: How much of the reference appears in generated text
- **Best for**: Summarization

**Variants:**
| Variant | What it Measures |
|---------|------------------|
| ROUGE-1 | Unigram (single word) overlap |
| ROUGE-2 | Bigram (two word) overlap |
| ROUGE-L | Longest Common Subsequence |

**Example:**
```
Reference: "The quick brown fox jumps over the lazy dog"
Generated: "A quick fox jumps over a dog"

ROUGE-1 Recall = matched words / reference words
               = 6/9 = 0.67
```

---

#### BERTScore
- **Purpose**: Measures semantic similarity using embeddings
- **How it works**: 
  1. Get BERT embeddings for each token
  2. Compute cosine similarity between tokens
  3. Find best matching pairs
  4. Calculate precision, recall, F1

**Advantage over BLEU/ROUGE:**
- Understands meaning, not just exact words
- "Happy" and "joyful" get high similarity
- Better for evaluating paraphrases

---

#### Perplexity
- **Purpose**: Measures how "surprised" the model is by text
- **Formula**: PPL = exp(average negative log likelihood)
- **Interpretation**: Lower perplexity = model predicts text better
- **Use case**: Comparing language models on same dataset

**Example:**
```
Model A perplexity on test set: 15.2
Model B perplexity on test set: 22.8

Model A is better (lower perplexity)
```

**Limitation**: Only measures prediction ability, not output quality

---

### 2.2 Classification Metrics

| Metric | Formula | When to Use |
|--------|---------|-------------|
| **Accuracy** | (TP + TN) / Total | Balanced classes |
| **Precision** | TP / (TP + FP) | When false positives are costly |
| **Recall** | TP / (TP + FN) | When false negatives are costly |
| **F1 Score** | 2 × (P × R) / (P + R) | Imbalanced classes |

**Example Scenarios:**
- **Spam Detection**: High precision (don't mark real emails as spam)
- **Disease Detection**: High recall (don't miss any cases)
- **General Classification**: F1 score for balance

---

### 2.3 Retrieval Metrics (Important for RAG)

#### Recall@k
- **Definition**: Fraction of relevant documents found in top-k results
- **Formula**: Relevant docs in top-k / Total relevant docs
- **Example**: If 3 relevant docs exist and 2 are in top-5 → Recall@5 = 0.67

#### Precision@k
- **Definition**: Fraction of top-k results that are relevant
- **Formula**: Relevant docs in top-k / k

#### MRR (Mean Reciprocal Rank)
- **Definition**: Average of 1/rank of first relevant result
- **Example**: 
  - Query 1: First relevant at position 2 → 1/2 = 0.5
  - Query 2: First relevant at position 1 → 1/1 = 1.0
  - MRR = (0.5 + 1.0) / 2 = 0.75

#### NDCG (Normalized Discounted Cumulative Gain)
- **Purpose**: Measures ranking quality considering position
- **Key idea**: Relevant documents ranked higher = better score
- **Range**: 0 to 1

---

### 2.4 Code Generation Metrics

#### Pass@k
- **Definition**: Probability that at least 1 of k generated samples passes all test cases
- **Formula**: Pass@k = 1 - C(n-c, k) / C(n, k)
  - n = total samples generated
  - c = samples that passed tests

**Common values:**
| Metric | Meaning |
|--------|---------|
| Pass@1 | First attempt passes (strictest) |
| Pass@10 | At least 1 of 10 attempts passes |
| Pass@100 | At least 1 of 100 attempts passes |

**Why not just accuracy?**
- LLMs are non-deterministic
- Pass@k accounts for variability
- Higher k is more forgiving

---

## 3. Important Benchmarks

### 3.1 General Knowledge & Understanding

#### MMLU (Massive Multitask Language Understanding)
- **What**: 57 subjects from STEM to humanities
- **Format**: Multiple choice questions
- **Levels**: Elementary to professional
- **Purpose**: Tests breadth and depth of knowledge
- **Example subjects**: Math, history, law, medicine, computer science

#### HellaSwag
- **What**: Sentence completion with common sense
- **Format**: Choose correct ending from 4 options
- **Purpose**: Tests common sense reasoning
- **Example**: "A woman is washing dishes. She..." → picks most logical continuation

#### ARC (AI2 Reasoning Challenge)
- **Versions**: ARC-Easy, ARC-Challenge
- **What**: Science questions from grade school exams
- **Purpose**: Tests scientific reasoning

#### WinoGrande
- **What**: Pronoun resolution problems
- **Purpose**: Tests understanding of context
- **Example**: "The trophy doesn't fit in the suitcase because it is too [big/small]" - which refers to trophy vs suitcase?

---

### 3.2 Reasoning Benchmarks

#### GSM8K (Grade School Math 8K)
- **What**: 8,500 grade school math word problems
- **Purpose**: Tests multi-step mathematical reasoning
- **Why important**: Requires chain-of-thought reasoning
- **Example**: "If John has 5 apples and gives 2 to Mary, then buys 3 more..."

#### MATH
- **What**: Competition-level mathematics
- **Difficulty**: High school to olympiad level
- **Topics**: Algebra, geometry, number theory, probability

#### BIG-Bench
- **What**: 200+ diverse tasks
- **Categories**: Logic, math, language understanding, creativity
- **BIG-Bench Hard (BBH)**: Subset of most challenging tasks

---

### 3.3 Code Benchmarks

#### HumanEval
- **Creator**: OpenAI
- **What**: 164 Python programming problems
- **Format**: Function signature + docstring → complete the function
- **Evaluation**: Run against test cases, measure Pass@k

#### MBPP (Mostly Basic Python Problems)
- **What**: ~1000 crowd-sourced Python problems
- **Difficulty**: Easier than HumanEval
- **Use**: Testing basic coding ability

#### SWE-Bench
- **What**: Real GitHub issues from popular repositories
- **Task**: Generate patches that fix the issue
- **Evaluation**: Patches must pass repository tests
- **Why important**: Tests real-world software engineering ability

---

### 3.4 Safety & Truthfulness

#### TruthfulQA
- **Purpose**: Tests if model avoids generating false information
- **Format**: Questions designed to elicit common misconceptions
- **Categories**: Health, law, conspiracies, fiction
- **Example**: Questions where popular but wrong answers exist

#### BBQ (Bias Benchmark for QA)
- **Purpose**: Measures social biases
- **Categories**: Age, disability, gender, race, religion, socioeconomic status
- **Format**: Ambiguous questions that shouldn't be answered with stereotypes

---

### 3.5 Agent Benchmarks

#### AgentBench
- **What**: Tests agent capabilities across environments
- **Environments**: Operating system, database, web browsing, coding
- **Purpose**: Measures multi-step task completion with tools

#### WebArena
- **What**: Web-based tasks in realistic environment
- **Tasks**: E-commerce, forums, content management
- **Purpose**: Tests web navigation and interaction

#### GAIA (General AI Assistants)
- **What**: Real-world assistant tasks
- **Features**: Requires reasoning, web search, tool use
- **Levels**: Different difficulty tiers

---

## 4. RAG (Retrieval-Augmented Generation) Evaluation

### What is RAG?
```
User Query → Retrieve Relevant Documents → Generate Answer using Context
```

### Why Special Evaluation for RAG?
RAG has two components that can fail:
1. **Retrieval**: Wrong documents retrieved
2. **Generation**: Wrong answer from correct documents

### RAG Evaluation Metrics

#### 1. Faithfulness (Groundedness)
- **Question**: Is the answer based ONLY on the retrieved context?
- **Purpose**: Detects hallucinations
- **Score**: 0 to 1 (1 = fully faithful)

**How it's measured:**
1. Extract individual claims from the answer
2. Check if each claim can be found in context
3. Faithfulness = supported claims / total claims

**Example:**
```
Context: "Paris is the capital of France. It has the Eiffel Tower."
Question: "What is the capital of France?"
Answer: "Paris is the capital of France. It was founded in 250 BC."

Claims: 
1. "Paris is capital of France" ✓ (in context)
2. "Founded in 250 BC" ✗ (not in context - hallucination!)

Faithfulness = 1/2 = 0.5
```

---

#### 2. Answer Relevancy
- **Question**: Does the answer actually address the question asked?
- **Purpose**: Ensures answer is on-topic
- **Penalizes**: Off-topic information, incomplete answers

**How it's measured:**
- Generate questions that the answer would address
- Compare with original question
- Higher similarity = more relevant

---

#### 3. Context Precision
- **Question**: Are the retrieved documents relevant to the question?
- **Purpose**: Measures retrieval quality
- **High precision**: Less noise in retrieved context

---

#### 4. Context Recall
- **Question**: Did we retrieve all documents needed to answer correctly?
- **Purpose**: Ensures nothing important was missed
- **How measured**: Compare retrieved context against ground truth answer

---

### RAG Evaluation Framework: RAGAS

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# Prepare your dataset
dataset = {
    "question": [...],
    "answer": [...],
    "contexts": [...],
    "ground_truth": [...]
}

# Run evaluation
result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)

print(result)
# {'faithfulness': 0.85, 'answer_relevancy': 0.92, ...}
```

---

## 5. Agent Evaluation

### How Agents Differ from Simple LLMs

| Aspect | LLM | Agent |
|--------|-----|-------|
| Output | Single response | Multiple steps/actions |
| Interaction | Text in → Text out | Uses tools, APIs, environment |
| State | Stateless | Maintains memory/context |
| Evaluation | Output quality | Task completion + process quality |

### Agent Evaluation Dimensions

#### 1. Task Success
- **Success Rate**: Percentage of tasks completed correctly
- **Partial Success**: How much of the task was completed
- **Binary vs Graded**: Pass/fail or percentage completion

#### 2. Efficiency
| Metric | What it Measures |
|--------|------------------|
| **Steps** | Number of actions taken |
| **Tokens** | Total tokens consumed |
| **Time** | Wall-clock time |
| **Cost** | API costs incurred |

*Fewer steps/tokens/cost for same outcome = better agent*

#### 3. Trajectory Quality
- **Action Accuracy**: Did agent choose correct tools?
- **Argument Accuracy**: Were tool inputs correct?
- **Reasoning Quality**: Was the thinking logical?
- **Unnecessary Actions**: Wasted steps that didn't help

#### 4. Error Handling
- **Error Recovery**: Can agent fix its mistakes?
- **Graceful Degradation**: Does it fail safely?
- **Self-Correction**: Recognizes and corrects errors

---

### Agent Evaluation Approaches

#### Approach 1: End-to-End Evaluation
- Only check if final outcome is correct
- Simple to implement
- Doesn't tell you where things went wrong

```
Task: "Book a flight from NYC to LA for tomorrow"
Evaluation: Did the flight get booked correctly? Yes/No
```

#### Approach 2: Trajectory Evaluation
- Evaluate each step in the agent's process
- Requires ground truth trajectories
- More detailed insights

```
Step 1: Search flights ✓
Step 2: Select cheapest option ✓
Step 3: Enter passenger details ✓
Step 4: Complete payment ✓
```

#### Approach 3: Checkpoint Evaluation
- Define key milestones
- Verify agent passes each checkpoint
- Balance between end-to-end and trajectory

```
Checkpoint 1: Found available flights ✓
Checkpoint 2: Selected appropriate flight ✓
Checkpoint 3: Booking confirmed ✓
```

---

### Key Agent Metrics Summary

| Metric | Formula | Good Value |
|--------|---------|------------|
| Task Success Rate | Completed / Total | > 80% |
| Average Steps | Total Steps / Tasks | Lower is better |
| Tool Accuracy | Correct Tool Calls / Total | > 90% |
| Recovery Rate | Recovered Errors / Total Errors | > 70% |

---

## 6. LLM-as-a-Judge

### What is LLM-as-a-Judge?
Using a powerful LLM (like GPT-4, Claude) to evaluate outputs from other models or systems.

### Why Use LLM-as-a-Judge?
- Scales better than human evaluation
- Cheaper than human annotators
- Can evaluate subjective qualities
- Consistent evaluation criteria

### Evaluation Modes

#### Mode 1: Single Answer Scoring
```
Prompt to Judge:
"Rate this response on a scale of 1-5 for helpfulness.

Question: {question}
Response: {response}

Consider:
- Does it answer the question?
- Is it accurate?
- Is it clear?

Score (1-5): "
```

#### Mode 2: Pairwise Comparison
```
Prompt to Judge:
"Which response is better?

Question: {question}
Response A: {response_a}
Response B: {response_b}

Choose A or B and explain why."
```

*Pairwise is often more reliable than absolute scoring*

#### Mode 3: Reference-Based Grading
```
Prompt to Judge:
"Compare this response to the reference answer.

Question: {question}
Reference: {correct_answer}
Response: {model_response}

Score correctness (0-100):"
```

---

### G-Eval Framework

G-Eval uses chain-of-thought prompting for more reliable evaluation:

1. **Define criteria**: What aspects to evaluate
2. **Create evaluation steps**: Detailed rubric
3. **Chain-of-thought**: Judge reasons before scoring
4. **Probability weighting**: Use token probabilities for scores

```
Evaluation Steps:
1. Read the source document carefully
2. Read the generated summary
3. Check if main points are covered
4. Check for any factual errors
5. Assign score 1-5 based on criteria
```

---

### Biases in LLM-as-a-Judge (Important for Interviews!)

| Bias | Description | Mitigation |
|------|-------------|------------|
| **Position Bias** | Prefers response shown first or last | Randomize order, evaluate both orders |
| **Verbosity Bias** | Prefers longer responses | Control for length, penalize unnecessary content |
| **Self-Enhancement Bias** | Prefers outputs similar to its own | Use different model as judge |
| **Style Bias** | Prefers certain writing styles | Focus criteria on content, not style |
| **Sycophancy** | Agrees with apparent user preference | Blind evaluation |

### Best Practices for LLM-as-a-Judge

1. **Use strong models**: GPT-4, Claude 3.5 as judges
2. **Structured output**: Request JSON for consistent parsing
3. **Require reasoning**: Ask for explanation before score
4. **Multiple evaluations**: Run multiple times, average
5. **Calibrate**: Compare with human judgments
6. **Mitigate biases**: Swap positions, blind evaluation

---

## 7. Human Evaluation

### When is Human Evaluation Necessary?
- Subjective qualities (creativity, humor, empathy)
- High-stakes decisions
- When automated metrics don't correlate with quality
- Final validation before production launch
- Evaluating safety and harmfulness

### Human Evaluation Methods

#### Method 1: Absolute Rating (Likert Scale)
- Rate on scale (1-5 or 1-7)
- Simple to collect
- Raters may have different calibrations

#### Method 2: Pairwise Comparison
- "Which is better: A or B?"
- More reliable than absolute rating
- Harder to aggregate across many items

#### Method 3: Ranking
- Rank multiple outputs from best to worst
- Good for comparing many systems
- Time-consuming for raters

### Inter-Annotator Agreement

**Why it matters**: Ensures evaluation is reliable and not random

| Metric | Use Case | Interpretation |
|--------|----------|----------------|
| **Cohen's Kappa** | 2 raters | > 0.8 excellent, 0.6-0.8 good |
| **Fleiss' Kappa** | 3+ raters | Same scale as Cohen's |
| **Krippendorff's Alpha** | Any raters, any scale | > 0.8 reliable |

**Formula intuition for Kappa:**
```
Kappa = (Observed Agreement - Chance Agreement) / (1 - Chance Agreement)
```

### Best Practices for Human Evaluation

1. **Clear guidelines**: Detailed rubrics with examples
2. **Training**: Calibrate raters before main evaluation
3. **Blind evaluation**: Hide which model generated output
4. **Randomize order**: Prevent position effects
5. **Attention checks**: Include easy items to verify attention
6. **Sufficient samples**: Ensure statistical significance

---

## 8. Production Monitoring & Online Evaluation

### Key Production Metrics

#### Performance Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| **TTFT** | Time to First Token | < 500ms |
| **Tokens/second** | Generation speed | > 30 |
| **Total latency** | End-to-end response time | < 3s |
| **P95/P99 latency** | Tail latencies | Monitor for spikes |

#### Reliability Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| **Error rate** | Failed requests | < 1% |
| **Timeout rate** | Requests exceeding limit | < 0.5% |
| **Availability** | Uptime percentage | > 99.9% |

#### Quality Metrics (Online)
| Metric | What it Indicates |
|--------|-------------------|
| **User feedback** | Direct thumbs up/down ratings |
| **Regeneration rate** | Users asking for new response (high = bad) |
| **Edit rate** | Users modifying response (high = needs improvement) |
| **Task completion** | Users completing intended task |
| **Session length** | Engagement indicator |

#### Cost Metrics
| Metric | Purpose |
|--------|---------|
| **Tokens per request** | Usage tracking |
| **Cost per request** | Budget monitoring |
| **Cost per user** | Unit economics |

---

### A/B Testing for LLMs

**Process:**
1. Split users randomly between Model A and Model B
2. Collect metrics for both groups
3. Statistically compare results
4. Choose winner

**Key considerations:**
- Need sufficient sample size for significance
- Run long enough for representative data
- Control for confounding variables
- Track multiple metrics (quality, latency, cost)

---

### Monitoring Tools

| Tool | Strength |
|------|----------|
| **LangSmith** | LangChain integration, tracing |
| **Langfuse** | Open-source, detailed tracing |
| **Helicone** | API gateway with analytics |
| **Weights & Biases** | Experiment tracking |
| **Arize Phoenix** | ML observability |

---

## 9. Evaluation Frameworks & Tools

### Framework Comparison

| Framework | Best For | Key Features |
|-----------|----------|--------------|
| **RAGAS** | RAG evaluation | Faithfulness, relevancy metrics |
| **LangSmith** | LangChain apps | Tracing, datasets, custom evaluators |
| **DeepEval** | Unit testing | pytest integration, CI/CD |
| **Promptfoo** | Prompt comparison | Multi-provider, easy config |
| **LM Eval Harness** | Benchmarking | 200+ benchmarks supported |

### RAGAS Example
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

result = evaluate(dataset, metrics=[faithfulness, answer_relevancy])
```

### DeepEval Example
```python
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="What is the capital of France?",
    actual_output="Paris is the capital of France.",
    expected_output="Paris"
)

metric = AnswerRelevancyMetric()
evaluate([test_case], [metric])
```

### Promptfoo Example
```yaml
# promptfooconfig.yaml
prompts:
  - "Answer concisely: {{question}}"
  - "Provide a detailed answer: {{question}}"

providers:
  - openai:gpt-4
  - openai:gpt-3.5-turbo

tests:
  - vars:
      question: "What is machine learning?"
    assert:
      - type: contains
        value: "algorithm"
```

---

## 10. Common Interview Questions with Answers

### Q1: How would you evaluate an LLM for production deployment?

**Answer:**
I would take a multi-stage approach:

1. **Benchmark Testing**: Run standard benchmarks (MMLU, HumanEval) to understand general capabilities

2. **Task-Specific Evaluation**: Create test dataset matching our actual use case with ground truth answers

3. **Metric Selection**: Choose appropriate metrics based on task
   - Generation: ROUGE, BERTScore
   - Classification: F1, Precision/Recall
   - RAG: Faithfulness, Answer Relevancy

4. **Safety Testing**: Check for hallucinations, biases, harmful outputs using TruthfulQA, BBQ

5. **Human Evaluation**: Sample-based human review for subjective quality

6. **A/B Testing**: Deploy to small user percentage, compare metrics

7. **Production Monitoring**: Set up dashboards for latency, errors, user feedback

---

### Q2: What's the difference between BLEU and ROUGE?

**Answer:**

| Aspect | BLEU | ROUGE |
|--------|------|-------|
| Focus | Precision | Recall |
| Question answered | How much of output is in reference? | How much of reference is in output? |
| Best for | Machine translation | Summarization |
| Penalty | Brevity penalty (too short) | None standard |

**Example:**
```
Reference: "The quick brown fox jumps"
Generated: "The quick brown"

BLEU: High (all generated words match)
ROUGE: Low (missing "fox jumps")
```

---

### Q3: How do you detect and evaluate hallucinations?

**Answer:**

**Detection methods:**
1. **Faithfulness scoring**: Check if claims are grounded in source
2. **Fact verification**: Cross-check against knowledge bases
3. **Self-consistency**: Ask multiple times, inconsistency = potential hallucination
4. **Claim extraction + verification**: Extract atomic claims, verify each

**Evaluation metrics:**
- Faithfulness score (RAGAS)
- Factual accuracy rate
- Hallucination rate = hallucinated responses / total responses

**Prevention:**
- Use RAG to ground responses
- Ask model to cite sources
- Lower temperature for factual tasks
- Include "I don't know" as valid response

---

### Q4: How would you evaluate a RAG system?

**Answer:**

I would evaluate both components separately and together:

**Retrieval Evaluation:**
- Recall@k: Are relevant documents being retrieved?
- MRR: How high are relevant documents ranked?
- Precision@k: Are retrieved documents actually relevant?

**Generation Evaluation:**
- Faithfulness: Is answer grounded in retrieved context?
- Answer Relevancy: Does answer address the question?
- Correctness: Does answer match ground truth?

**End-to-End:**
- Overall accuracy on test questions
- User satisfaction scores

**Tool**: RAGAS framework provides all these metrics

---

### Q5: Explain LLM-as-a-Judge and its limitations.

**Answer:**

**What it is:** Using a powerful LLM (GPT-4, Claude) to evaluate outputs from other models.

**Advantages:**
- Scales much better than human evaluation
- Cheaper than hiring annotators
- Consistent application of criteria
- Can evaluate subjective qualities

**Limitations/Biases:**

| Bias | Problem |
|------|---------|
| Position bias | Prefers first or last option |
| Verbosity bias | Prefers longer responses |
| Self-enhancement | Prefers outputs similar to its own |
| Style bias | Prefers certain writing styles |

**Mitigation strategies:**
- Randomize presentation order
- Evaluate same pair twice with swapped positions
- Use different model as judge than model being evaluated
- Require chain-of-thought reasoning before score
- Calibrate against human judgments

---

### Q6: What metrics would you use to evaluate an AI agent?

**Answer:**

**Primary metrics:**

1. **Task Success Rate**: % of tasks completed correctly
   - Most important metric
   - Can be binary or graded

2. **Efficiency**: 
   - Steps to completion (fewer = better)
   - Tokens used
   - Time taken
   - Cost incurred

3. **Tool Use Accuracy**:
   - Correct tool selection rate
   - Correct argument rate

4. **Error Recovery**:
   - Can agent recover from mistakes?
   - Recovery rate = recovered / total errors

**Evaluation approach:**
- End-to-end: Just check final outcome
- Trajectory: Evaluate each step
- Checkpoint: Verify key milestones

---

### Q7: How do you ensure human evaluation is reliable?

**Answer:**

**Key practices:**

1. **Clear guidelines**: 
   - Detailed rubric with scoring criteria
   - Examples of each score level

2. **Rater training**:
   - Practice rounds with feedback
   - Calibration sessions

3. **Quality measures**:
   - Inter-annotator agreement (Cohen's Kappa > 0.8)
   - Attention check questions
   - Gold standard items with known answers

4. **Bias prevention**:
   - Blind evaluation (hide model identity)
   - Randomize presentation order
   - Multiple raters per item

5. **Statistical rigor**:
   - Sufficient sample size
   - Calculate confidence intervals

---

### Q8: What's Pass@k and why is it used for code evaluation?

**Answer:**

**Definition:** Pass@k is the probability that at least one of k generated code samples passes all test cases.

**Why it's needed:**
- LLMs are non-deterministic (same prompt → different outputs)
- Pass@1 is too strict (penalizes randomness)
- Pass@k accounts for variability

**Common values:**
| Metric | Meaning | Difficulty |
|--------|---------|------------|
| Pass@1 | First try passes | Hardest |
| Pass@10 | At least 1 of 10 passes | Medium |
| Pass@100 | At least 1 of 100 passes | Easiest |

**Calculation:**
```
Pass@k = 1 - (ways to choose k failures) / (ways to choose k from n)
       = 1 - C(n-c, k) / C(n, k)

n = total samples, c = correct samples
```

---

### Q9: How would you set up evaluation for a chatbot?

**Answer:**

**Automated metrics:**
- Response relevance (BERTScore against expected)
- Coherence (does response follow conversation)
- Task completion rate (for task-oriented bots)

**LLM-as-Judge:**
- Helpfulness rating
- Appropriateness
- Tone consistency

**Human evaluation:**
- User satisfaction surveys
- Pairwise comparisons between versions

**Production metrics:**
- User engagement (session length, return rate)
- Thumbs up/down ratio
- Escalation rate (transfer to human)
- Task completion rate

**Safety evaluation:**
- Test for harmful responses
- Test for personal information leakage
- Adversarial prompt testing

---

### Q10: Compare offline and online evaluation.

**Answer:**

| Aspect | Offline | Online |
|--------|---------|--------|
| **When** | Before deployment | After deployment |
| **Data** | Test datasets | Real user interactions |
| **Control** | High (controlled conditions) | Low (real-world variability) |
| **Scale** | Limited by dataset size | Unlimited (all users) |
| **Metrics** | Accuracy, ROUGE, etc. | Engagement, satisfaction |
| **Risk** | None (no users affected) | Real impact on users |
| **Insights** | Model capabilities | Actual user experience |

**Best practice:** Use both
- Offline: Validate before deployment
- Online: Verify in real conditions

---

## Quick Reference Summary

### Metrics by Task
| Task | Primary Metrics |
|------|-----------------|
| Translation | BLEU, COMET |
| Summarization | ROUGE, Faithfulness |
| Classification | F1, Precision, Recall |
| Code Generation | Pass@k |
| RAG | Faithfulness, Relevancy, Recall@k |
| Agents | Success Rate, Efficiency |
| General Quality | BERTScore, LLM-as-Judge |

### Key Benchmarks
| Capability | Benchmark |
|------------|-----------|
| Knowledge | MMLU |
| Reasoning | GSM8K, BIG-Bench |
| Coding | HumanEval, SWE-Bench |
| Truthfulness | TruthfulQA |
| Common Sense | HellaSwag |
| Agents | AgentBench, WebArena |

### Evaluation Tools
| Tool | Use Case |
|------|----------|
| RAGAS | RAG evaluation |
| LangSmith | LangChain tracing |
| DeepEval | Unit testing |
| Promptfoo | Prompt comparison |
| LM Eval Harness | Benchmarking |

---

**Good luck with your interviews! 🎯**
