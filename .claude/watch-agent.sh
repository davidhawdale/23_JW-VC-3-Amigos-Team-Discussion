#!/bin/bash
# Usage: .claude/watch-agent.sh <label> <output-file-path>
# Shows readable Claude Code agent output in real time.
#
# Example:
#   .claude/watch-agent.sh "Quality Reviewer" /tmp/claude-501/.../tasks/abc123.output

LABEL="${1:-Agent}"
FILE="$2"

if [ -z "$FILE" ]; then
  echo "Usage: watch-agent.sh <label> <output-file-path>"
  exit 1
fi

echo "Waiting for $FILE ..."
while [ ! -f "$FILE" ]; do sleep 0.5; done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  $LABEL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

tail -f "$FILE" | jq -rR '
  try (
    fromjson |
    if .message.role == "assistant" then
      .message.content[]? |
      if .type == "text" and (.text | length) > 0 then .text
      elif .type == "tool_use" then "[\(.name)] \(.input | to_entries | map("\(.key)=\(.value | tostring | .[0:80])") | join(", "))"
      else empty
      end
    else empty
    end
  ) catch empty
'
