#!/bin/bash
set -e

cd ~/.claude && CLAUDE_5H_TOKEN_BUDGET=44000000 CLAUDE_WEEK_TOKEN_BUDGET=2080000000 CLAUDE_USAGE_CACHE=/tmp/v.json node usage-burn.js && node -e '
  const c=require("/tmp/v.json");
  const B5=44e6,BW=2.08e9;
  console.log("=== SESSION (5h) ===");
  console.log("weighted tokens:",Math.round(c.tokens).toLocaleString());
  console.log("script %:",(c.tokens/B5*100).toFixed(1)+"%   | /usage: 29%");
  console.log("budget to hit 29%:",Math.round(c.tokens/0.29).toLocaleString());
  console.log("script reset (UTC):",c.blockEndAt,"=",new Date(c.blockEnd).toLocaleString("en-US",{timeZone:"Asia/Riyadh"}),"Riyadh");
  console.log("           /usage reset: 8:10pm Riyadh (17:10 UTC)");
  console.log("=== WEEK ===");
  console.log("weighted tokens:",Math.round(c.weekTokens).toLocaleString());
  console.log("script %:",(c.weekTokens/BW*100).toFixed(1)+"%   | /usage: 27%");
  console.log("budget to hit 27%:",Math.round(c.weekTokens/0.27).toLocaleString());
'