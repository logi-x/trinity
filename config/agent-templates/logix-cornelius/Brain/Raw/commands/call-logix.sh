#!/bin/bash

set -a;

. ~/.config/logix/config;
set+a;
echo "ep=$LOGIX_ENDPOINT model=$LOGIX_MODEL tok=${LOGIX_TOKEN:+present}";
PROMPT='Give ONE witty, original aphorism (max 16 words) about building software with AI coding agents. Output ONLY the aphorism. No quotes, no attribution, no preamble, no thinking.';
BODY=$(python3 -c "import json,sys;print(json.dumps({'model':sys.argv[1],'max_tokens':80,'messages':[{'role':'user','content':sys.argv[2]}]}))" "$LOGIX_MODEL" "$PROMPT"); echo "=== /v1/messages ===";
time curl -s -m 60 "$LOGIX_ENDPOINT/v1/messages" -H "Authorization: Bearer $LOGIX_TOKEN" -H "anthropic-version: 2023-06-01" -H "Content-Type: application/json" -d "$BODY" 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);c=d.get('content');print(c[0]['text'].strip() if isinstance(c,list) and c else '(raw) '+json.dumps(d)[:400])" 2>/dev/null





# === /v1/messages ===
# Code with AI assistants like hiring interns—exciting until you realize they're just as lazy as you thought you'd be spared.

# real       0m1.862s
# user       0m0.031s
# sys        0m0.004s