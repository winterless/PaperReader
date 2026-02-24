#!/usr/bin/env bash
set -euo pipefail

# Start vLLM OpenAI-compatible API server with a local HF model.
HF_MODEL_DIR="/home/unlimitediw/workspace/LLMRunner/datapool/experiments/qwen3-1.7b_megatron_full/model/base/Qwen3-1.7B"

CMD=(python -m vllm.entrypoints.openai.api_server \
  --model "${HF_MODEL_DIR}" \
  --dtype auto \
  --tensor-parallel-size 1 \
  --max-model-len 32384 \
  --gpu-memory-utilization 0.85 \
  --swap-space 8 \
  --port 8000)

printf '%q ' "${CMD[@]}"
echo
exec "${CMD[@]}"
#!/usr/bin/env bash
set -euo pipefail

# Start vLLM OpenAI-compatible API server with a local HF model.
HF_MODEL_DIR="/home/unlimitediw/workspace/models/Qwen2.5-32B-Instruct-AWQ"

CMD=(python -m vllm.entrypoints.openai.api_server \
  --model "${HF_MODEL_DIR}" \
  --dtype auto \
  --tensor-parallel-size 1 \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.85 \
  --swap-space 8 \
  --port 8000)

printf '%q ' "${CMD[@]}"
echo
exec "${CMD[@]}"
