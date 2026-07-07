#!/usr/bin/env bash
set -e

BASE_URL="http://localhost:8000"
PASS=0
FAIL=0

echo "=== Ops Assistant Smoke Test ==="

# 1. Health check
echo -n "Health check... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/health)
if [ "$STATUS" = "200" ]; then echo "PASS"; PASS=$((PASS+1)); else echo "FAIL ($STATUS)"; FAIL=$((FAIL+1)); fi

# 2. Login
echo -n "Login... "
TOKEN=$(curl -s -X POST ${BASE_URL}/api/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
if [ -n "$TOKEN" ]; then echo "PASS"; PASS=$((PASS+1)); else echo "FAIL"; FAIL=$((FAIL+1)); fi

# 3. Get me
echo -n "Get me... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/api/auth/me -H "Authorization: Bearer ${TOKEN}")
if [ "$STATUS" = "200" ]; then echo "PASS"; PASS=$((PASS+1)); else echo "FAIL ($STATUS)"; FAIL=$((FAIL+1)); fi

# 4. Create module
echo -n "Create module... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/api/modules -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"name":"test-module","description":"Smoke test"}')
if [ "$STATUS" = "200" ]; then echo "PASS"; PASS=$((PASS+1)); else echo "FAIL ($STATUS)"; FAIL=$((FAIL+1)); fi

# 5. List modules
echo -n "List modules... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/api/modules)
if [ "$STATUS" = "200" ]; then echo "PASS"; PASS=$((PASS+1)); else echo "FAIL ($STATUS)"; FAIL=$((FAIL+1)); fi

# 6. AI locate (fallback mode, no LLM key)
echo -n "AI locate (fallback)... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/api/ai/locate -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"description":"test error in module"}')
if [ "$STATUS" = "200" ]; then echo "PASS"; PASS=$((PASS+1)); else echo "FAIL ($STATUS)"; FAIL=$((FAIL+1)); fi

# 7. Stats dashboard
echo -n "Stats dashboard... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/api/stats/dashboard -H "Authorization: Bearer ${TOKEN}")
if [ "$STATUS" = "200" ]; then echo "PASS"; PASS=$((PASS+1)); else echo "FAIL ($STATUS)"; FAIL=$((FAIL+1)); fi

echo ""
echo "=== Results: ${PASS} passed, ${FAIL} failed ==="
if [ $FAIL -gt 0 ]; then exit 1; fi
