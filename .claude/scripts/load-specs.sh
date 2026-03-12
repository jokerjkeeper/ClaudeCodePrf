#!/bin/bash
# Auto-load all specification files from .claude/claude_specs/
# Called by SessionStart hook

SPECS_DIR=".claude/claude_specs"

if [ -d "$SPECS_DIR" ]; then
  shopt -s nullglob
  files=("$SPECS_DIR"/*.md)
  shopt -u nullglob

  if [ ${#files[@]} -gt 0 ]; then
    echo "=== 自動載入規格文件 (${#files[@]} 個) ==="
    for spec_file in "${files[@]}"; do
      echo ""
      echo "--- $(basename "$spec_file") ---"
      cat "$spec_file"
    done
    echo ""
    echo "=== 規格文件載入完成 ==="
  fi
fi

exit 0
