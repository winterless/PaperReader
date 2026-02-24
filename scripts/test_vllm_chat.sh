#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
MAX_TIME="${MAX_TIME:-120}"
MAX_TOKENS="${MAX_TOKENS:-1024}"
TEMPERATURE="${TEMPERATURE:-0.2}"
HISTORY_FILE="${HISTORY_FILE:-.rag_chat_history.jsonl}"
HISTORY_TURNS="${HISTORY_TURNS:-8}"
CONTEXT_FILE="${CONTEXT_FILE:-}"
SAVE_HISTORY="${SAVE_HISTORY:-1}"

SYSTEM_PROMPT="${SYSTEM_PROMPT:-你是一个用于论文学习与RAG管理的研究助手。\
你的目标是帮助用户高效学习大模型论文。\
请优先输出结构化内容：结论、关键点、方法对比、阅读建议。\
如果提供了检索上下文，只能基于上下文给出事实性结论；不确定时明确说明。\
回答尽量简洁，必要时给出下一步学习计划。}"

USER_PROMPT="${*:-${PROMPT:-帮我总结这篇论文的核心贡献，并给出下一步阅读建议。}}"

models_json="$(curl -s --max-time 120 "http://${HOST}:${PORT}/v1/models")"
MODEL_ID="$(python -c 'import json,sys; data=json.load(sys.stdin); items=data.get("data", []); print(items[0].get("id","") if items else "")' <<<"${models_json}")"

if [[ -z "${MODEL_ID}" ]]; then
  echo "No model id found from /v1/models on ${HOST}:${PORT}" >&2
  exit 1
fi

# Build current user message. If RAG context exists, inject it.
if [[ -n "${CONTEXT_FILE}" && -f "${CONTEXT_FILE}" ]]; then
  CONTEXT_TEXT="$(<"${CONTEXT_FILE}")"
  USER_MESSAGE="$(cat <<EOF
【用户问题】
${USER_PROMPT}

【RAG检索上下文】
${CONTEXT_TEXT}
EOF
)"
else
  USER_MESSAGE="${USER_PROMPT}"
fi

REQUEST_JSON="$(python - <<'PY' "${MODEL_ID}" "${SYSTEM_PROMPT}" "${USER_MESSAGE}" "${HISTORY_FILE}" "${HISTORY_TURNS}" "${MAX_TOKENS}" "${TEMPERATURE}"
import json
import pathlib
import sys

model_id, system_prompt, user_message, history_file, history_turns, max_tokens, temperature = sys.argv[1:]
history_turns = max(0, int(history_turns))

messages = [{"role": "system", "content": system_prompt}]

p = pathlib.Path(history_file)
if p.exists():
    # jsonl format: one chat message per line.
    lines = [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    history = []
    for line in lines:
        try:
            item = json.loads(line)
            if item.get("role") in {"user", "assistant"} and isinstance(item.get("content"), str):
                history.append({"role": item["role"], "content": item["content"]})
        except json.JSONDecodeError:
            continue
    if history_turns > 0:
        history = history[-(history_turns * 2):]
    else:
        history = []
    messages.extend(history)

messages.append({"role": "user", "content": user_message})

payload = {
    "model": model_id,
    "messages": messages,
    "max_tokens": int(max_tokens),
    "temperature": float(temperature),
}
print(json.dumps(payload, ensure_ascii=False))
PY
)"

resp="$(curl -sS --max-time "${MAX_TIME}" "http://${HOST}:${PORT}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d "${REQUEST_JSON}")"

ASSISTANT_CONTENT="$(python - <<'PY' "${resp}"
import json
import sys

try:
    data = json.loads(sys.argv[1])
except json.JSONDecodeError:
    print("")
    raise SystemExit(0)

choice = (data.get("choices") or [{}])[0]
msg = choice.get("message", {}) if isinstance(choice, dict) else {}
print((msg.get("content", "") or "").strip())
PY
)"

if [[ -z "${ASSISTANT_CONTENT}" ]]; then
  echo "Model reply is empty. Raw response:"
  echo "${resp}"
else
  echo "Model reply: ${ASSISTANT_CONTENT}"
fi

if [[ "${SAVE_HISTORY}" == "1" ]]; then
  python - <<'PY' "${HISTORY_FILE}" "${USER_MESSAGE}" "${ASSISTANT_CONTENT}"
import json
import pathlib
import sys

history_file, user_message, assistant_content = sys.argv[1:]
p = pathlib.Path(history_file)
p.parent.mkdir(parents=True, exist_ok=True)
with p.open("a", encoding="utf-8") as f:
    f.write(json.dumps({"role": "user", "content": user_message}, ensure_ascii=False) + "\n")
    f.write(json.dumps({"role": "assistant", "content": assistant_content}, ensure_ascii=False) + "\n")
PY
fi
#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

models_json="$(curl -s --max-time 120 "http://${HOST}:${PORT}/v1/models")"
MODEL_ID="$(python -c 'import json,sys; data=json.load(sys.stdin); items=data.get("data", []); print(items[0].get("id","") if items else "")' <<<"${models_json}")"

if [[ -z "${MODEL_ID}" ]]; then
  echo "No model id found from /v1/models on ${HOST}:${PORT}" >&2
  exit 1
fi

resp="$(curl -s --max-time 20 "http://${HOST}:${PORT}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "'"${MODEL_ID}"'",
    "messages": [{"role": "user", "content": "帮我写一段transformer基础代码"}],
    "max_tokens": 16000,
    "temperature": 0.2
  }')"

python -c 'import json,sys; data=json.load(sys.stdin); choice=data.get("choices",[{}])[0]; msg=choice.get("message",{}); print("Model reply:", (msg.get("content","") or "").strip())' <<<"${resp}"
