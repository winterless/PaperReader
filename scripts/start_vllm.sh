#!/usr/bin/env bash
set -euo pipefail

# Start vLLM OpenAI-compatible API server with a local HF model.
HF_MODEL_DIR="/home/unlimitediw/workspace/models/Qwen3-30B-A3B-Thinking-2507-FP8"

# 30B FP8 在 32GB 显存上：模型 ~29GiB。--swap-space 为 CPU 侧 KV cache 容量，加大可把更多 cache 换到 CPU，减轻显存压力（用时会略慢）
CMD=(python -m vllm.entrypoints.openai.api_server \
  --model "${HF_MODEL_DIR}" \
  --dtype auto \
  --tensor-parallel-size 1 \
  --max-model-len 1024 \
  --gpu-memory-utilization 0.94 \
  --swap-space 16 \
  --enforce-eager \
  --port 8000)

printf '%q ' "${CMD[@]}"
echo
exec "${CMD[@]}"
