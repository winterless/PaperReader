---
paper_id: shoeybi_2019_megatron_lm
title: Megatron-LM Training Multi-Billion Parameter Language Models Using Model Parallelism
year: 2019
topic_tags: [training_infra, parallelism, transformer]
capability_tags: [tp_pp_design, large_scale_training, gpu_parallelism]
prerequisites: [[vaswani_2017_attention_is_all_you_need]]
related: [[narayanan_2021_efficient_large_scale_lm_training]]
source_url: https://arxiv.org/abs/1909.08053
---

# Megatron-LM (2019)

## Problem

Single-GPU memory limits prevent training very large Transformer models efficiently.

## Method Summary

The paper introduces tensor model parallelism for Transformer layers:

- Split GEMM operations across GPUs (column/row parallel linear layers).
- Minimize synchronization points in attention and MLP blocks.
- Combine with data parallelism to scale training throughput.

## TP/PP Relevance

This paper mainly formalizes **tensor parallelism (TP)** at layer level.  
Pipeline parallelism (PP) design is expanded in later work (Megatron-DeepSpeed and follow-ups).

## Practical Takeaways

- TP reduces per-device memory footprint.
- Communication cost becomes dominant at higher TP degrees.
- Efficient collective operations are critical for scaling efficiency.

## Common Confusions

- TP is not a substitute for data parallelism; they are usually composed.
- Larger TP does not always mean faster training due to all-reduce overhead.

## Prerequisite / Next Reading

- Prerequisite: [[vaswani_2017_attention_is_all_you_need]]
- Next: Megatron + PP/ZeRO integration papers (to be added).
