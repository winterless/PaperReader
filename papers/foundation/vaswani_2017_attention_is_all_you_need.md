---
paper_id: vaswani_2017_attention_is_all_you_need
title: Attention Is All You Need
year: 2017
topic_tags: [foundation, transformer, architecture]
capability_tags: [transformer_basics, sequence_modeling]
prerequisites: []
related: [[shoeybi_2019_megatron_lm]]
source_url: https://arxiv.org/abs/1706.03762
---

# Attention Is All You Need

## Core Idea

The paper replaces recurrence/convolution with pure attention to model sequence transduction.  
The key operator is scaled dot-product attention:

$$
\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

Multi-head attention runs multiple attention projections in parallel and concatenates outputs.

## Key Contributions

1. Introduces full Transformer encoder-decoder architecture.
2. Establishes self-attention as the primary sequence modeling primitive.
3. Uses positional encoding to inject order information without recurrence.

## Why It Matters For LLMs

- Defines the base architecture for GPT/BERT/T5 style models.
- Makes large-scale parallel training feasible due to non-recurrent structure.

## Common Confusions

- Self-attention complexity grows with sequence length (\(O(n^2)\)).
- Positional encoding is not optional for order-sensitive tasks.

## Prerequisite / Next Reading

- Next: [[shoeybi_2019_megatron_lm]] for scaling Transformer training.
