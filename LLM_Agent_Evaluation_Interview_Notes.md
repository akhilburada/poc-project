# LLM & Agent Evaluation - Interview Preparation Notes

## Table of Contents
1. [Why Evaluation Matters](#1-why-evaluation-matters)
2. [LLM Evaluation Fundamentals](#2-llm-evaluation-fundamentals)
3. [Key Evaluation Metrics](#3-key-evaluation-metrics)
4. [Popular Benchmarks](#4-popular-benchmarks)
5. [Agent Evaluation](#5-agent-evaluation)
6. [Evaluation Frameworks & Tools](#6-evaluation-frameworks--tools)
7. [RAG Evaluation](#7-rag-evaluation)
8. [Human Evaluation vs Automated Evaluation](#8-human-evaluation-vs-automated-evaluation)
9. [LLM-as-a-Judge](#9-llm-as-a-judge)
10. [Production Monitoring & Online Evaluation](#10-production-monitoring--online-evaluation)
11. [Common Interview Questions](#11-common-interview-questions)
12. [Key Terms Glossary](#12-key-terms-glossary)

---

## 1. Why Evaluation Matters

### Business Perspective
- **Quality Assurance**: Ensure LLM outputs meet quality standards before deployment
- **Cost Optimization**: Compare models to find best cost-performance ratio
- **Risk Mitigation**: Identify harmful, biased, or incorrect outputs
- **Continuous Improvement**: Track model performance over time

### Technical Perspective
- **Model Selection**: Choose the right model for specific use cases
- **Prompt Engineering**: Measure effectiveness of different prompts
- **Fine-tuning Validation**: Verify fine-tuned models improve on base models
- **Regression Testing**: Ensure updates don't degrade performance

---

## 2. LLM Evaluation Fundamentals

### Types of Evaluation

#### A. Intrinsic Evaluation
Measures model's internal capabilities independent of downstream tasks.

| Metric | What it Measures |
|--------|------------------|
| Perplexity | How well model predicts next token |
| Cross-entropy Loss | Difference between predicted and actual distribution |
| Embedding Quality | Semantic representation capability |

#### B. Extrinsic Evaluation
Measures performance on specific downstream tasks.

| Task Type | Examples |
|-----------|----------|
| Classification | Sentiment analysis, intent detection |
| Generation | Summarization, translation, code generation |
| Reasoning | Math problems, logical inference |
| Knowledge | Q&A, fact retrieval |

### Evaluation Dimensions

```
┌─────────────────────────────────────────────────────────┐
│                 LLM EVALUATION DIMENSIONS               │
├─────────────────────────────────────────────────────────┤
│  1. ACCURACY        - Correctness of outputs            │
│  2. FLUENCY         - Grammatical & linguistic quality  │
│  3. COHERENCE       - Logical flow and consistency      │
│  4. RELEVANCE       - Alignment with input/query        │
│  5. SAFETY          - Harmful content detection         │
│  6. FACTUALITY      - Truthfulness of claims            │
│  7. HELPFULNESS     - Utility to the user               │
│  8. HARMLESSNESS    - Avoiding negative impacts         │
│  9. HONESTY         - Acknowledging uncertainty         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Key Evaluation Metrics

### 3.1 Text Generation Metrics

#### BLEU (Bilingual Evaluation Understudy)
- **Purpose**: Measures n-gram overlap between generated and reference text
- **Range**: 0 to 1 (higher is better)
- **Use Case**: Machine translation, summarization
- **Formula**: 
  ```
  BLEU = BP × exp(∑ wn × log pn)
  BP = Brevity Penalty
  pn = Modified n-gram precision
  ```
- **Limitations**: Doesn't capture semantic similarity, penalizes valid paraphrases

#### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
- **Variants**:
  - ROUGE-N: N-gram overlap (ROUGE-1, ROUGE-2)
  - ROUGE-L: Longest Common Subsequence
  - ROUGE-S: Skip-bigram
- **Use Case**: Summarization evaluation
- **Focus**: Recall-oriented (how much of reference is captured)

#### METEOR
- **Improvement over BLEU**: Considers synonyms, stemming, paraphrasing
- **Features**: Word-level alignment, penalty for fragmentation

#### BERTScore
- **Method**: Uses BERT embeddings to compute semantic similarity
- **Advantage**: Captures semantic meaning beyond surface-level matching
- **Components**: Precision, Recall, F1 based on cosine similarity

#### Perplexity
- **Definition**: Exponential of average negative log-likelihood
- **Formula**: PPL = exp(-1/N × ∑ log P(wi|w1...wi-1))
- **Interpretation**: Lower perplexity = better model
- **Limitation**: Only measures likelihood, not quality

### 3.2 Classification Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| **Accuracy** | (TP + TN) / Total | Balanced datasets |
| **Precision** | TP / (TP + FP) | When FP is costly |
| **Recall** | TP / (TP + FN) | When FN is costly |
| **F1 Score** | 2 × (P × R) / (P + R) | Imbalanced datasets |
| **AUC-ROC** | Area under ROC curve | Binary classification |

### 3.3 Semantic Similarity Metrics

#### Embedding-Based Metrics
```python
# Cosine Similarity
def cosine_similarity(emb1, emb2):
    return dot(emb1, emb2) / (norm(emb1) * norm(emb2))

# Common ranges: -1 to 1 (1 = identical, 0 = orthogonal)
```

#### Semantic Textual Similarity (STS)
- Measures degree of semantic equivalence
- Scale: 0 (unrelated) to 5 (equivalent)

### 3.4 Task-Specific Metrics

| Task | Metrics |
|------|---------|
| **Code Generation** | Pass@k, Execution accuracy, CodeBLEU |
| **Question Answering** | Exact Match (EM), F1, Recall@k |
| **Dialogue** | Engagement, Coherence, Informativeness |
| **Summarization** | ROUGE, Factual consistency, Compression ratio |
| **Translation** | BLEU, COMET, chrF |

---

## 4. Popular Benchmarks

### 4.1 General Language Understanding

#### MMLU (Massive Multitask Language Understanding)
- **Tasks**: 57 subjects across STEM, humanities, social sciences
- **Format**: Multiple choice questions
- **Difficulty Levels**: Elementary to professional
- **Key Insight**: Tests breadth of knowledge

#### HellaSwag
- **Task**: Sentence completion with commonsense reasoning
- **Format**: Choose correct ending from 4 options
- **Challenge**: Requires understanding context and plausibility

#### ARC (AI2 Reasoning Challenge)
- **Versions**: ARC-Easy, ARC-Challenge
- **Task**: Science questions from standardized tests
- **Focus**: Reasoning and world knowledge

#### WinoGrande
- **Task**: Pronoun resolution requiring commonsense
- **Format**: Fill-in-the-blank
- **Example**: "The trophy doesn't fit in the suitcase because it's too [big/small]"

### 4.2 Reasoning Benchmarks

#### GSM8K (Grade School Math 8K)
- **Task**: Multi-step math word problems
- **Difficulty**: Grade school level
- **Evaluation**: Final answer accuracy
- **Key**: Tests chain-of-thought reasoning

#### MATH
- **Task**: Competition-level mathematics
- **Subjects**: Algebra, geometry, calculus, etc.
- **Difficulty**: High school to olympiad level

#### BIG-Bench
- **Scale**: 200+ diverse tasks
- **Categories**: Logic, math, language, creativity
- **Notable Subset**: BIG-Bench Hard (BBH) - most challenging tasks

#### DROP (Discrete Reasoning Over Paragraphs)
- **Task**: Reading comprehension with discrete reasoning
- **Operations**: Counting, sorting, arithmetic

### 4.3 Code Generation Benchmarks

#### HumanEval
- **Creator**: OpenAI
- **Tasks**: 164 Python programming problems
- **Metric**: Pass@k (pass rate with k attempts)
- **Format**: Function completion with test cases

#### MBPP (Mostly Basic Python Problems)
- **Tasks**: ~1000 crowd-sourced Python problems
- **Difficulty**: Basic programming tasks

#### CodeContests
- **Source**: Competitive programming platforms
- **Difficulty**: Higher than HumanEval

### 4.4 Safety & Alignment Benchmarks

#### TruthfulQA
- **Purpose**: Measures truthfulness and avoidance of misconceptions
- **Format**: Questions designed to elicit false answers
- **Categories**: Health, law, finance, conspiracies

#### BBQ (Bias Benchmark for QA)
- **Purpose**: Measures social biases
- **Categories**: Age, disability, gender, race, religion, etc.

#### RealToxicityPrompts
- **Purpose**: Measures toxic generation
- **Method**: Prompts that may elicit toxic completions

### 4.5 Agent & Tool Use Benchmarks

#### GAIA (General AI Assistants)
- **Purpose**: Real-world assistant tasks
- **Features**: Multi-step reasoning, tool use, web browsing

#### AgentBench
- **Tasks**: OS interaction, database, web browsing, coding
- **Focus**: End-to-end agent capabilities

#### WebArena
- **Environment**: Simulated web environment
- **Tasks**: Complex web-based tasks

#### SWE-Bench
- **Task**: Real GitHub issues from popular repos
- **Evaluation**: Whether generated patches pass tests

---

## 5. Agent Evaluation

### 5.1 What Makes Agent Evaluation Different?

```
┌─────────────────────────────────────────────────────────────┐
│              LLM vs AGENT EVALUATION                        │
├──────────────────────────┬──────────────────────────────────┤
│         LLM              │            AGENT                 │
├──────────────────────────┼──────────────────────────────────┤
│ Single response          │ Multi-step trajectories         │
│ Static evaluation        │ Dynamic environment interaction │
│ Text output only         │ Actions + tool calls + text     │
│ No state management      │ Memory and context management   │
│ Direct output            │ Planning → Execution → Feedback │
└──────────────────────────┴──────────────────────────────────┘
```

### 5.2 Agent Evaluation Dimensions

#### Task Completion
- **Success Rate**: Did agent complete the task?
- **Partial Success**: Degree of task completion
- **Error Recovery**: Can agent recover from mistakes?

#### Efficiency
- **Steps**: Number of actions to complete task
- **Tokens**: Total tokens used
- **Time**: Wall-clock time
- **Cost**: API costs incurred

#### Trajectory Quality
- **Action Accuracy**: Correct tool selection
- **Argument Accuracy**: Correct parameters passed
- **Plan Quality**: Logical action sequence
- **Unnecessary Actions**: Steps that didn't contribute

#### Safety & Reliability
- **Guardrail Adherence**: Stays within boundaries
- **Hallucination Rate**: Makes up information
- **Confidential Leakage**: Protects sensitive data

### 5.3 Agent Evaluation Approaches

#### A. End-to-End Evaluation
```python
# Evaluate final outcome only
success = final_state == expected_state
```
- Pros: Simple, task-focused
- Cons: No insight into process quality

#### B. Trajectory Evaluation
```python
# Evaluate each step
for step in trajectory:
    evaluate_action_correctness(step)
    evaluate_reasoning(step)
    evaluate_efficiency(step)
```
- Pros: Detailed insights, debugging
- Cons: Requires ground truth trajectories

#### C. Checkpoint Evaluation
- Define intermediate checkpoints
- Verify agent passes each checkpoint
- Balance between end-to-end and trajectory

### 5.4 Key Agent Metrics

| Metric | Description | Formula |
|--------|-------------|---------|
| **Task Success Rate** | % of tasks completed | Successful / Total |
| **Step Accuracy** | Correct actions per step | Correct Steps / Total Steps |
| **Tool Selection Accuracy** | Correct tool chosen | Correct Tools / Tool Calls |
| **Average Steps** | Efficiency measure | Total Steps / Tasks |
| **Recovery Rate** | Bounce back from errors | Recovered / Errors |
| **Goal Progress** | Partial completion score | Achieved Sub-goals / Total |

### 5.5 Multi-Agent Evaluation

Additional considerations:
- **Communication Efficiency**: Quality of inter-agent messages
- **Coordination**: How well agents work together
- **Load Distribution**: Balanced task allocation
- **Conflict Resolution**: Handling conflicting goals

---

## 6. Evaluation Frameworks & Tools

### 6.1 Popular Frameworks

#### LangSmith (LangChain)
```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Run evaluation
results = evaluate(
    experiment_name="my-experiment",
    data="dataset-name",
    evaluators=[
        "correctness",
        "helpfulness",
        "custom_evaluator"
    ]
)
```
- **Features**: Tracing, datasets, custom evaluators
- **Best For**: LangChain-based applications

#### RAGAS (RAG Assessment)
```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
)
```
- **Focus**: RAG pipeline evaluation
- **Key Metrics**: Faithfulness, relevancy, context quality

#### DeepEval
```python
from deepeval import evaluate
from deepeval.metrics import GEval, AnswerRelevancyMetric

metric = GEval(
    name="Correctness",
    criteria="Determine if the actual output is correct"
)

evaluate(test_cases, metrics=[metric])
```
- **Features**: Unit test framework for LLMs
- **Integration**: pytest compatible

#### OpenAI Evals
```yaml
# eval_spec.yaml
evals:
  my_eval:
    class: evals.basic_eval:Match
    args:
      samples_jsonl: data/samples.jsonl
```
- **Creator**: OpenAI
- **Extensible**: Custom eval creation

#### Promptfoo
```yaml
# promptfooconfig.yaml
prompts:
  - "Answer: {{question}}"
providers:
  - openai:gpt-4
  - anthropic:claude-3
tests:
  - vars:
      question: "What is 2+2?"
    assert:
      - type: contains
        value: "4"
```
- **Focus**: Prompt testing and comparison
- **Features**: Multi-provider, CI/CD integration

#### Eleuther AI LM Evaluation Harness
```bash
lm_eval --model hf --model_args pretrained=gpt2 \
        --tasks hellaswag,mmlu --batch_size 8
```
- **Use Case**: Benchmark evaluation
- **Supported**: 200+ benchmarks

### 6.2 Framework Comparison

| Framework | Best For | Strengths |
|-----------|----------|-----------|
| **LangSmith** | LangChain apps | Tracing, debugging |
| **RAGAS** | RAG pipelines | Specialized metrics |
| **DeepEval** | Testing/CI | pytest integration |
| **Promptfoo** | Prompt comparison | Multi-provider |
| **LM Eval Harness** | Benchmarking | Comprehensive benchmarks |
| **Weights & Biases** | Experiment tracking | Visualization |

---

## 7. RAG Evaluation

### 7.1 RAG Pipeline Components to Evaluate

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG PIPELINE                             │
│                                                             │
│  Query → [Retriever] → Context → [Generator] → Response    │
│              ↓              ↓           ↓                   │
│         Retrieval       Context    Generation              │
│         Quality         Quality    Quality                 │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Retrieval Metrics

| Metric | Description | Formula |
|--------|-------------|---------|
| **Recall@k** | Relevant docs in top-k | Relevant ∩ Retrieved@k / Relevant |
| **Precision@k** | Precision of top-k | Relevant ∩ Retrieved@k / k |
| **MRR** | Mean Reciprocal Rank | 1/N × Σ(1/rank_i) |
| **NDCG** | Normalized DCG | DCG / Ideal DCG |
| **Hit Rate** | At least one relevant in top-k | Queries with hit / Total queries |

### 7.3 Generation Quality Metrics

#### Faithfulness (Groundedness)
- Does the answer use only information from context?
- Detects hallucinations
- Score: 0-1

```python
# RAGAS Faithfulness approach
# 1. Extract claims from answer
# 2. Verify each claim against context
faithfulness = supported_claims / total_claims
```

#### Answer Relevancy
- Is the answer relevant to the question?
- Penalizes incomplete or off-topic answers

#### Answer Correctness
- Does the answer match ground truth?
- Combination of semantic and factual similarity

### 7.4 Context Metrics

#### Context Precision
- Are retrieved contexts relevant to the question?
- Higher = less noise in retrieved documents

#### Context Recall
- Do retrieved contexts contain information needed for ground truth answer?
- Higher = better coverage

#### Context Utilization
- How much of the context was actually used?
- Important for efficiency

### 7.5 End-to-End RAG Metrics

```python
# Example: RAGAS evaluation
from ragas.metrics import (
    faithfulness,         # Generation grounded in context
    answer_relevancy,     # Answer addresses the question
    context_precision,    # Retrieved context is relevant
    context_recall,       # Context contains needed info
    answer_correctness    # Answer matches ground truth
)
```

---

## 8. Human Evaluation vs Automated Evaluation

### 8.1 Comparison

| Aspect | Human Evaluation | Automated Evaluation |
|--------|------------------|----------------------|
| **Cost** | High (time, money) | Low (compute only) |
| **Scale** | Limited | Unlimited |
| **Consistency** | Variable | Highly consistent |
| **Nuance** | Captures subtlety | May miss nuance |
| **Speed** | Slow | Fast |
| **Bias** | Human biases | Model biases |

### 8.2 Human Evaluation Methods

#### Absolute Rating
- Rate output on fixed scale (1-5, Likert)
- Simple but calibration varies across raters

#### Pairwise Comparison
- "Which response is better: A or B?"
- More reliable than absolute rating
- Harder to aggregate

#### Ranking
- Rank multiple outputs
- Good for comparing many systems
- Computationally expensive to analyze

#### Multi-dimensional Rating
- Rate on multiple criteria separately
- More informative but more effort

### 8.3 Inter-Annotator Agreement

Measure consistency among human raters:

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **Cohen's Kappa** | 2 raters | >0.8 = excellent |
| **Fleiss' Kappa** | 3+ raters | 0.6-0.8 = substantial |
| **Krippendorff's Alpha** | Any number, any scale | >0.8 = reliable |

### 8.4 Best Practices for Human Evaluation

1. **Clear Guidelines**: Detailed rubrics with examples
2. **Training**: Calibrate raters before evaluation
3. **Blind Evaluation**: Hide model identity
4. **Randomization**: Randomize order of presentations
5. **Quality Control**: Include attention checks
6. **Sufficient Sample Size**: Statistical significance

---

## 9. LLM-as-a-Judge

### 9.1 Concept

Use a powerful LLM to evaluate outputs of other LLMs.

```
┌─────────────────────────────────────────────────────────┐
│                  LLM-AS-A-JUDGE                         │
│                                                         │
│  Input: Question + Response (+ Reference)               │
│           ↓                                             │
│  [Judge LLM] → Evaluation Score + Reasoning             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 9.2 Evaluation Modes

#### Single-Answer Grading
```python
prompt = """
Rate the following response on a scale of 1-5.

Question: {question}
Response: {response}

Criteria:
- Accuracy: Is the information correct?
- Completeness: Does it fully answer the question?
- Clarity: Is it well-written and easy to understand?

Provide your rating and explanation.
"""
```

#### Pairwise Comparison
```python
prompt = """
Compare these two responses and pick the better one.

Question: {question}
Response A: {response_a}
Response B: {response_b}

Which response is better? Explain your reasoning.
"""
```

#### Reference-Based Grading
```python
prompt = """
Compare the response to the reference answer.

Question: {question}
Reference Answer: {reference}
Model Response: {response}

Score the response for correctness (0-100).
"""
```

### 9.3 G-Eval Framework

1. **Define Criteria**: What aspects to evaluate
2. **Create Evaluation Steps**: Chain-of-thought for evaluation
3. **Score**: Generate probability-weighted scores

```python
# G-Eval example
evaluation_steps = """
1. Read the source document carefully
2. Read the generated summary
3. Check if all key information is included
4. Check for any hallucinated facts
5. Assign a score from 1-5
"""
```

### 9.4 Biases in LLM-as-a-Judge

| Bias | Description | Mitigation |
|------|-------------|------------|
| **Position Bias** | Prefers first/last response | Randomize order |
| **Verbosity Bias** | Prefers longer responses | Normalize by length |
| **Self-Enhancement** | Prefers own outputs | Use different judge |
| **Style Bias** | Prefers certain writing styles | Clear criteria |
| **Sycophancy** | Agrees with user perspective | Blind evaluation |

### 9.5 Best Practices

1. **Use Strong Models**: GPT-4, Claude 3 as judges
2. **Structured Output**: JSON for consistent parsing
3. **Chain-of-Thought**: Require reasoning before score
4. **Multiple Judges**: Ensemble for reliability
5. **Calibration**: Test against human judgments
6. **Bias Mitigation**: Swap positions, blind evaluation

---

## 10. Production Monitoring & Online Evaluation

### 10.1 Key Production Metrics

#### Latency Metrics
- **Time to First Token (TTFT)**: Initial response time
- **Tokens per Second**: Generation speed
- **Total Response Time**: End-to-end latency
- **P50, P95, P99**: Latency percentiles

#### Reliability Metrics
- **Error Rate**: Failed requests
- **Availability**: Uptime percentage
- **Timeout Rate**: Requests exceeding time limit

#### Cost Metrics
- **Tokens per Request**: Average usage
- **Cost per Request**: API spend
- **Cost per User/Session**: Unit economics

#### Quality Metrics (Online)
- **User Feedback**: Thumbs up/down, ratings
- **Completion Rate**: Task completion
- **Regeneration Rate**: User requested new response
- **Edit Rate**: User modified response

### 10.2 Online Evaluation Techniques

#### A/B Testing
```
┌─────────────────────────────────────────┐
│            A/B TESTING                  │
│                                         │
│  Users ─┬─→ Model A (Control)   ──→ ?   │
│         │                               │
│         └─→ Model B (Treatment) ──→ ?   │
│                                         │
│  Compare metrics between groups         │
└─────────────────────────────────────────┘
```

- **Key Metrics**: Engagement, task success, user satisfaction
- **Statistical Significance**: Ensure sufficient sample size
- **Duration**: Run long enough for representative data

#### Interleaving
- Show results from both models in same session
- User choices indicate preference
- More efficient than A/B testing

#### Shadow Mode
- Run new model in parallel without serving
- Compare outputs offline
- Zero user impact during testing

### 10.3 Observability Stack

```
┌─────────────────────────────────────────────────────────┐
│              LLM OBSERVABILITY                          │
├─────────────────────────────────────────────────────────┤
│  TRACING         │  Track request through pipeline     │
│  LOGGING         │  Structured logs for debugging      │
│  METRICS         │  Quantitative measurements          │
│  ALERTING        │  Notify on anomalies                │
│  DASHBOARDS      │  Visualize trends                   │
└─────────────────────────────────────────────────────────┘
```

### 10.4 Tools for Production Monitoring

| Tool | Focus |
|------|-------|
| **LangSmith** | LangChain tracing |
| **Langfuse** | Open-source observability |
| **Helicone** | LLM gateway with analytics |
| **Arize Phoenix** | ML observability |
| **Weights & Biases** | Experiment tracking |
| **Datadog / New Relic** | General APM |

---

## 11. Common Interview Questions

### Conceptual Questions

**Q1: How would you evaluate an LLM's factual accuracy?**
> **Answer**: 
> 1. Use datasets like TruthfulQA for known misconceptions
> 2. Create domain-specific fact-checking datasets
> 3. Implement LLM-as-a-judge with web search for verification
> 4. Check against knowledge bases/databases
> 5. Use multiple models and check consensus

**Q2: What's the difference between BLEU and ROUGE?**
> **Answer**:
> - BLEU: Precision-focused, measures how much of generated text appears in reference
> - ROUGE: Recall-focused, measures how much of reference appears in generated text
> - BLEU better for translation, ROUGE better for summarization

**Q3: How do you evaluate an agent that uses tools?**
> **Answer**:
> 1. Task completion rate (end-to-end success)
> 2. Tool selection accuracy (right tool for job)
> 3. Argument correctness (valid parameters)
> 4. Efficiency (steps/tokens to complete)
> 5. Trajectory analysis (quality of reasoning)
> 6. Error recovery (handling failures)

**Q4: What are the limitations of automated metrics?**
> **Answer**:
> - May not correlate with human preferences
> - Miss nuanced quality aspects
> - Gaming: models can optimize for metrics
> - Limited coverage of possible good responses
> - Can't assess subjective qualities (humor, creativity)

**Q5: How would you set up evaluation for a RAG system?**
> **Answer**:
> 1. Retrieval metrics: Recall@k, MRR, NDCG
> 2. Faithfulness: Is answer grounded in context?
> 3. Answer relevancy: Does it address the question?
> 4. End-to-end accuracy: Compare to ground truth
> 5. Use frameworks like RAGAS

### Practical/Scenario Questions

**Q6: Your LLM-powered chatbot is getting negative user feedback but automated metrics look good. What do you do?**
> **Answer**:
> 1. Analyze feedback qualitatively - identify themes
> 2. Audit specific failing conversations
> 3. Check if metrics capture what users care about
> 4. Set up human evaluation on sample
> 5. Add new metrics for identified issues
> 6. Consider implicit signals (regeneration rate, conversation abandonment)

**Q7: How would you compare two LLMs for your production use case?**
> **Answer**:
> 1. Define success criteria for specific use case
> 2. Create representative test dataset
> 3. Run both models on same inputs
> 4. Use multiple metrics (accuracy, latency, cost)
> 5. Conduct human evaluation on subset
> 6. A/B test in production with real users
> 7. Consider edge cases and failure modes

**Q8: Design an evaluation pipeline for a code generation model.**
> **Answer**:
> 1. Functional correctness: Pass@k with test cases
> 2. Code quality: Linting, static analysis
> 3. Similarity metrics: CodeBLEU for structure
> 4. Security: Check for vulnerabilities
> 5. Efficiency: Runtime performance
> 6. Human review for readability
> 7. Use HumanEval, MBPP benchmarks

**Q9: How do you handle evaluation when there's no ground truth?**
> **Answer**:
> 1. LLM-as-a-Judge with clear criteria
> 2. Pairwise comparisons (easier than absolute rating)
> 3. Human evaluation sampling
> 4. Proxy metrics (engagement, task completion)
> 5. Expert review for specialized domains
> 6. Self-consistency checks across multiple samples

**Q10: What's your approach to detecting hallucinations?**
> **Answer**:
> 1. Factual verification against knowledge base
> 2. Consistency checks (multiple samples)
> 3. Claim extraction + verification
> 4. Confidence calibration
> 5. Retrieval-based grounding
> 6. Source attribution requirements

### Technical Deep-Dive Questions

**Q11: Explain how BERTScore works and when to use it.**
> **Answer**:
> - Computes embeddings for each token in candidate and reference
> - Uses cosine similarity for pairwise token matching
> - Greedy matching to maximize total similarity
> - Produces precision, recall, F1
> - Better than BLEU for paraphrases
> - Use when semantic similarity matters more than exact wording

**Q12: What is Pass@k and how is it calculated?**
> **Answer**:
> - Probability that at least 1 of k samples passes tests
> - Unbiased estimator: Pass@k = 1 - C(n-c, k) / C(n, k)
> - n = total samples, c = correct samples
> - Common values: Pass@1, Pass@10, Pass@100
> - Higher k compensates for non-determinism

**Q13: How would you implement LLM-as-a-Judge without position bias?**
> **Answer**:
> 1. Run evaluation twice with swapped positions
> 2. Take average or require agreement
> 3. Use randomized presentation order
> 4. Track and report position bias metrics
> 5. Use structured output format

**Q14: Explain the RAGAS faithfulness metric.**
> **Answer**:
> 1. Extract atomic claims from generated answer
> 2. For each claim, verify if it can be inferred from context
> 3. Faithfulness = supported claims / total claims
> 4. Uses NLI or LLM for entailment checking
> 5. Score of 1.0 means fully grounded

---

## 12. Key Terms Glossary

| Term | Definition |
|------|------------|
| **Benchmark** | Standardized test suite for model comparison |
| **Ground Truth** | Correct/expected output for evaluation |
| **Hallucination** | Model generating false or unsupported information |
| **Inter-annotator Agreement** | Consistency among human evaluators |
| **Intrinsic Evaluation** | Measuring internal model properties |
| **Extrinsic Evaluation** | Measuring task-specific performance |
| **Perplexity** | Measure of model's prediction uncertainty |
| **Recall@k** | Fraction of relevant items in top-k results |
| **NDCG** | Normalized Discounted Cumulative Gain |
| **Faithfulness** | Degree to which output is grounded in source |
| **Calibration** | Alignment between confidence and accuracy |
| **A/B Testing** | Comparing variants with live traffic |
| **Pass@k** | Probability of correct solution in k attempts |
| **TTFT** | Time to First Token |
| **Trajectory** | Sequence of actions taken by an agent |
| **G-Eval** | LLM evaluation with chain-of-thought |

---

## Quick Reference Card

### Essential Metrics by Task

| Task | Primary Metrics |
|------|-----------------|
| Text Generation | BLEU, ROUGE, BERTScore, Human eval |
| Classification | Accuracy, F1, Precision, Recall |
| Code Generation | Pass@k, Execution accuracy |
| RAG | Faithfulness, Answer relevancy, Recall@k |
| Agents | Success rate, Efficiency, Trajectory accuracy |
| Summarization | ROUGE, Factual consistency |
| Q&A | Exact Match, F1, Accuracy |

### Evaluation Checklist

- [ ] Define success criteria aligned with business goals
- [ ] Create representative test dataset
- [ ] Select appropriate metrics for task
- [ ] Implement automated evaluation pipeline
- [ ] Include human evaluation for quality checks
- [ ] Test for safety and bias
- [ ] Set up production monitoring
- [ ] Plan for continuous evaluation

---

*Last Updated: January 2026*
*Good luck with your interviews! 🚀*
