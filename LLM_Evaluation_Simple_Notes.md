# LLM & Agent Evaluation - Simple Interview Notes

---

## 1. Why Do We Evaluate LLMs?

| Reason | Explanation |
|--------|-------------|
| **Quality Check** | Is the model output good enough? |
| **Model Comparison** | Which model is better for my task? |
| **Find Problems** | Detect hallucinations, bias, errors |
| **Track Improvements** | Did my changes make it better? |
| **Cost vs Performance** | Is expensive model worth it? |

---

## 2. Two Types of Evaluation

### Offline Evaluation (Before Deployment)
- Test on prepared datasets
- Compare against ground truth
- Use benchmarks

### Online Evaluation (After Deployment)
- Monitor real user interactions
- Collect user feedback
- A/B testing

---

## 3. Most Important Metrics

### For Text Generation

| Metric | What It Measures | Simple Explanation |
|--------|------------------|-------------------|
| **BLEU** | Word overlap (precision) | "How many words in output match reference?" |
| **ROUGE** | Word overlap (recall) | "How many reference words appear in output?" |
| **BERTScore** | Semantic similarity | "Is the meaning similar?" (uses embeddings) |
| **Perplexity** | Model confidence | Lower = model is more confident |

**When to use what:**
- Translation → BLEU
- Summarization → ROUGE
- Paraphrasing → BERTScore

### For Classification

| Metric | When to Use |
|--------|-------------|
| **Accuracy** | Balanced classes |
| **Precision** | False positives are costly (spam detection) |
| **Recall** | False negatives are costly (disease detection) |
| **F1 Score** | Imbalanced classes, need balance |

### For Code Generation

| Metric | Meaning |
|--------|---------|
| **Pass@1** | Does first attempt pass all tests? |
| **Pass@k** | Does at least 1 of k attempts pass? |

---

## 4. Key Benchmarks (Know These!)

### General Knowledge
| Benchmark | What It Tests |
|-----------|---------------|
| **MMLU** | 57 subjects - tests breadth of knowledge |
| **HellaSwag** | Common sense reasoning |
| **TruthfulQA** | Avoiding false information |

### Reasoning
| Benchmark | What It Tests |
|-----------|---------------|
| **GSM8K** | Grade school math word problems |
| **MATH** | Advanced mathematics |
| **BIG-Bench** | 200+ diverse reasoning tasks |

### Code
| Benchmark | What It Tests |
|-----------|---------------|
| **HumanEval** | 164 Python coding problems |
| **MBPP** | 1000 basic Python problems |
| **SWE-Bench** | Real GitHub issue fixing |

### Agents
| Benchmark | What It Tests |
|-----------|---------------|
| **AgentBench** | Multi-step tasks with tools |
| **WebArena** | Web browsing tasks |
| **GAIA** | Real-world assistant tasks |

---

## 5. RAG Evaluation (Very Important!)

### What is RAG?
```
Question → Retrieve Documents → Generate Answer
```

### Key RAG Metrics

| Metric | Question It Answers |
|--------|---------------------|
| **Faithfulness** | Is answer based ONLY on retrieved context? (No hallucination) |
| **Answer Relevancy** | Does answer actually address the question? |
| **Context Precision** | Are retrieved documents relevant? |
| **Context Recall** | Did we retrieve all needed information? |

### Retrieval Metrics

| Metric | Meaning |
|--------|---------|
| **Recall@k** | % of relevant docs found in top k |
| **MRR** | How high is first relevant result ranked? |
| **NDCG** | Quality of ranking order |

**Tool to use:** RAGAS framework

---

## 6. Agent Evaluation

### How Agents Differ from LLMs

| LLM | Agent |
|-----|-------|
| Single response | Multiple steps |
| Text only | Uses tools (search, code, APIs) |
| No actions | Takes actions |
| Stateless | Has memory |

### Agent Metrics

| Metric | What It Measures |
|--------|------------------|
| **Task Success Rate** | Did agent complete the task? |
| **Steps to Complete** | How efficient? (fewer = better) |
| **Tool Selection Accuracy** | Did it pick the right tool? |
| **Error Recovery** | Can it fix its mistakes? |

### Evaluation Approaches

1. **End-to-End**: Just check final result
2. **Trajectory**: Check each step was correct
3. **Checkpoint**: Verify key milestones

---

## 7. LLM-as-a-Judge

### What Is It?
Use a powerful LLM (like GPT-4) to evaluate outputs of other models.

### Three Ways to Use It

**1. Single Rating**
```
"Rate this response 1-5 for helpfulness"
```

**2. Pairwise Comparison**
```
"Which response is better: A or B?"
```

**3. Reference-Based**
```
"Compare response to this correct answer"
```

### Common Biases (Interview Favorite!)

| Bias | Problem | Solution |
|------|---------|----------|
| **Position Bias** | Prefers first/last option | Randomize order |
| **Verbosity Bias** | Prefers longer answers | Penalize unnecessary length |
| **Self-Enhancement** | Prefers its own outputs | Use different model as judge |

---

## 8. Human vs Automated Evaluation

| Aspect | Human | Automated |
|--------|-------|-----------|
| **Cost** | Expensive | Cheap |
| **Scale** | Limited | Unlimited |
| **Speed** | Slow | Fast |
| **Nuance** | Catches subtlety | May miss nuance |
| **Consistency** | Varies | Always same |

### When to Use Human Evaluation
- Subjective quality (creativity, humor)
- Final validation before launch
- When automated metrics don't correlate with quality

### Inter-Annotator Agreement
- **Cohen's Kappa**: Agreement between 2 raters
- **Fleiss' Kappa**: Agreement among 3+ raters
- Goal: κ > 0.8 (excellent agreement)

---

## 9. Production Monitoring

### Key Metrics to Track

| Category | Metrics |
|----------|---------|
| **Latency** | Time to first token, total response time |
| **Cost** | Tokens per request, cost per user |
| **Quality** | User thumbs up/down, regeneration rate |
| **Reliability** | Error rate, timeout rate |

### A/B Testing
- Split users between old and new model
- Compare metrics
- Need enough users for statistical significance

---

## 10. Popular Tools

| Tool | Best For |
|------|----------|
| **RAGAS** | RAG evaluation |
| **LangSmith** | LangChain apps, tracing |
| **DeepEval** | Unit testing LLMs |
| **Promptfoo** | Comparing prompts/models |
| **LM Eval Harness** | Running benchmarks |

---

## 11. Top Interview Questions & Answers

### Q1: How do you evaluate if an LLM is hallucinating?

**Answer:**
1. Check if claims are in the source/context (faithfulness)
2. Verify facts against knowledge base
3. Ask same question multiple times - inconsistent = hallucination
4. Use LLM-as-judge to verify claims

---

### Q2: BLEU vs ROUGE - what's the difference?

**Answer:**
- **BLEU** = Precision focused → "How much of OUTPUT is in reference?"
- **ROUGE** = Recall focused → "How much of REFERENCE is in output?"
- Use BLEU for translation, ROUGE for summarization

---

### Q3: How would you evaluate a RAG system?

**Answer:**
1. **Retrieval**: Recall@k, MRR - are we getting right documents?
2. **Faithfulness**: Is answer grounded in context?
3. **Relevancy**: Does answer address the question?
4. Use RAGAS framework

---

### Q4: What are limitations of automated metrics?

**Answer:**
- Don't always match human preference
- Can be gamed by models
- Miss subjective qualities (creativity, tone)
- Only measure what they're designed for

---

### Q5: How do you evaluate an AI agent?

**Answer:**
1. **Success Rate**: Does it complete tasks?
2. **Efficiency**: Steps/tokens used
3. **Tool Accuracy**: Picks right tools?
4. **Error Recovery**: Handles failures?
5. Can evaluate end-to-end or step-by-step

---

### Q6: What is LLM-as-a-Judge and its problems?

**Answer:**
Using strong LLM to evaluate other models.

**Problems:**
- Position bias (prefers first option)
- Verbosity bias (prefers longer)
- Self-enhancement (prefers own outputs)

**Solutions:** Randomize order, use different judge model, require reasoning

---

### Q7: When would you use human evaluation?

**Answer:**
- Subjective quality assessment
- When automated metrics don't correlate
- Final validation before production
- Complex tasks needing domain expertise

---

### Q8: How do you evaluate in production?

**Answer:**
- Track latency, error rate, cost
- Collect user feedback (thumbs up/down)
- Monitor regeneration rate (user asked again = bad)
- A/B test new models
- Set up alerts for quality drops

---

### Q9: What is Pass@k?

**Answer:**
Probability that at least 1 of k code samples passes all tests.
- Pass@1: First try works
- Pass@10: At least 1 of 10 tries works
- Higher k = more forgiving

---

### Q10: How to compare two models for your use case?

**Answer:**
1. Create test dataset matching your use case
2. Run both models on same inputs
3. Measure relevant metrics (accuracy, latency, cost)
4. Do human evaluation on sample
5. A/B test with real users

---

## Quick Cheat Sheet

```
┌─────────────────────────────────────────────────────┐
│           EVALUATION QUICK REFERENCE                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  TEXT QUALITY     → BLEU, ROUGE, BERTScore          │
│  CLASSIFICATION   → Accuracy, F1, Precision/Recall  │
│  CODE             → Pass@k                          │
│  RAG              → Faithfulness, Relevancy, Recall │
│  AGENTS           → Success Rate, Efficiency        │
│                                                     │
│  HALLUCINATION    → Faithfulness check              │
│  BIAS             → BBQ benchmark                   │
│  KNOWLEDGE        → MMLU benchmark                  │
│  REASONING        → GSM8K, BIG-Bench                │
│                                                     │
│  FRAMEWORKS       → RAGAS, LangSmith, DeepEval      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

**Good luck with your interview! 🎯**
