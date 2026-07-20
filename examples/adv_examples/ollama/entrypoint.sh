#!/bin/sh
set -eu

OLLAMA_HOST=127.0.0.1 ollama serve &
ollama_pid=$!

cleanup() {
    kill "$ollama_pid" 2>/dev/null || true
    wait "$ollama_pid" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

attempt=1
while ! ollama list >/dev/null 2>&1; do
    if [ "$attempt" -eq 30 ]; then
        echo "Ollama did not start within 30 seconds." >&2
        exit 1
    fi
    attempt=$((attempt + 1))
    sleep 1
done

python3 -u /app/download_models.py
kill "$ollama_pid"
wait "$ollama_pid"
trap - EXIT INT TERM

OLLAMA_HOST=0.0.0.0 exec ollama serve
