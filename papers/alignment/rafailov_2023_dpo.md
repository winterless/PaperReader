---
paper_id: rafailov_2023_dpo
title: Direct Preference Optimization Your Language Model is Secretly a Reward Model
year: 2023
topic_tags: [alignment, preference_optimization, post_training]
capability_tags: [alignment_basics, objective_design, preference_learning]
prerequisites: [[vaswani_2017_attention_is_all_you_need]]
related: [[ouyang_2022_instructgpt]]
source_url: https://arxiv.org/abs/2305.18290
---

# DPO (2023)

## Problem

RLHF pipelines are often complex due to separate reward model training and RL optimization.

## Core Formulation

DPO directly optimizes policy preference pairs \((x, y_w, y_l)\) using a closed-form objective derived from a KL-constrained reward maximization perspective.

Simplified intuition:

- Increase likelihood of preferred response \(y_w\)
- Decrease likelihood of dispreferred response \(y_l\)
- Use reference model regularization to control drift

## Why It Matters

- Removes explicit RL loop in many alignment settings.
- Lower implementation complexity than classic PPO-based RLHF.
- Strong practical baseline for instruction tuning with preference data.

## Practical Caveats

- Quality strongly depends on preference data quality.
- Hyperparameter \(\beta\) controls alignment-vs-divergence balance.
- Not a universal replacement for all online RLHF scenarios.

## Prerequisite / Next Reading

- Background: [[ouyang_2022_instructgpt]] (to be added)
- Compare with IPO/ORPO and other preference objectives (to be added)
