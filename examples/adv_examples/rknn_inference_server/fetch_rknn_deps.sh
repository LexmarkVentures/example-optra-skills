#!/usr/bin/env bash
# fetch_rknn_deps.sh
#
# Downloads Rockchip-proprietary files that cannot be redistributed in this
# repository.  Files are pulled from the official airockchip/rknn-toolkit2
# release at the tag pinned below.
#
# Usage (run from the rknn_inference_server/ directory):
#   ./fetch_rknn_deps.sh          # skip files that already exist
#   ./fetch_rknn_deps.sh --force  # overwrite existing files

set -euo pipefail

RKNN_TOOLKIT2_TAG="v2.2.0"
BASE_URL="https://raw.githubusercontent.com/airockchip/rknn-toolkit2/${RKNN_TOOLKIT2_TAG}/rknpu2/runtime/Linux/librknn_api"

FORCE=false
if [[ "${1:-}" == "--force" ]]; then
  FORCE=true
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

download() {
  local remote_path="$1"
  local local_path="${SCRIPT_DIR}/$2"

  if [[ "$FORCE" == false && -f "$local_path" ]]; then
    echo "  [skip] $2 (already exists; use --force to overwrite)"
    return
  fi

  echo "  [fetch] $2"
  mkdir -p "$(dirname "$local_path")"
  curl -fsSL "${BASE_URL}/${remote_path}" -o "$local_path"
}

echo "Fetching RKNN runtime deps from airockchip/rknn-toolkit2 @ ${RKNN_TOOLKIT2_TAG} ..."

download "include/rknn_api.h"       "inference_server/include/rknn_api.h"
download "include/rknn_custom_op.h"  "inference_server/include/rknn_custom_op.h"
download "include/rknn_matmul_api.h" "inference_server/include/rknn_matmul_api.h"
download "aarch64/librknnrt.so"      "inference_server/lib/librknnrt.so"

echo "Done. All required files are in place."
