---
title: "EXP-59 — Upload routes accept oversized files — buffer.byteLength not re-checked after arrayBuffer()"
date: "2026-05-21"
status: resolved
resolution: fixed — PR #312 (commit e30cde8a)
tags: [bug, security, dos, upload, file-size, project/experts]
linear: "https://linear.app/experts/issue/EXP-59"
fingerprint: "07157ef04386"
---

## Summary

Upload routes trusted `file.size` from the multipart envelope without re-verifying after materializing the buffer with `arrayBuffer()`. A client could lie about file size in the multipart metadata to bypass `MAX_FILE_SIZE`.

## Repro

1. Craft a multipart request with `Content-Length` / `size` field set to a small value but actual body exceeding `MAX_FILE_SIZE`
2. POST to any upload route
3. Observe: upload succeeds past the size check

## Agent fingerprint

`<!-- agent-fp: 07157ef04386 -->`

## Status

`resolved` — PR #312 adds `buffer.byteLength` re-check after `arrayBuffer()` call.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
