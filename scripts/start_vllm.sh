#!/usr/bin/env bash
set -euo pipefail

# Start vLLM OpenAI-compatible API server with a local HF model.
HF_MODEL_DIR="/home/unlimitediw/workspace/models/Qwen3-30B-A3B-Thinking-2507-FP8"

CMD=(python -m vllm.entrypoints.openai.api_server \
  --model "${HF_MODEL_DIR}" \
  --dtype auto \
  --tensor-parallel-size 1 \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.9 \
  --swap-space 8 \
  --port 8000)

printf '%q ' "${CMD[@]}"
echo
exec "${CMD[@]}"
