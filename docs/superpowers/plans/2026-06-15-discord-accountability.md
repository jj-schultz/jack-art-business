# Discord Accountability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first repo-native Discord accountability loop that prompts Jack directly and logs structured summaries in this repository.

**Architecture:** Use a dependency-free Python helper script for adaptive prompt generation, webhook sending, and CSV response logging. Keep strategy and operating guidance in Markdown docs, and keep the durable interaction log in `data/discord_accountability_log.csv`.

**Tech Stack:** Python standard library, CSV, Discord incoming webhook, Markdown docs.

---

### Task 1: Adaptive Prompt Script

**Files:**
- Create: `scripts/discord_accountability.py`
- Test: `tests/test_discord_accountability.py`

- [x] **Step 1: Write failing tests for voice selection**

Run: `python3 -m unittest tests/test_discord_accountability.py`
Expected before implementation: failure because `scripts/discord_accountability.py` does not exist.

- [x] **Step 2: Implement adaptive voice selection**

Implement `choose_voice(entries)` with these rules:

- Three recent `response_received=no` rows choose `gentle_coach`.
- A recent response with `productive_progress=yes` chooses `game_challenge`.
- A recent response with a blocker chooses `gentle_coach`.
- Otherwise choose `direct_teammate`.

- [x] **Step 3: Verify tests pass**

Run: `python3 -m unittest tests/test_discord_accountability.py`
Expected: all tests pass.

### Task 2: Adaptive Timing And Logging

**Files:**
- Modify: `scripts/discord_accountability.py`
- Create: `data/discord_accountability_log.csv`
- Test: `tests/test_discord_accountability.py`

- [x] **Step 1: Write tests for recommended response hour and prompt logging**

Run: `python3 -m unittest tests/test_discord_accountability.py`
Expected before implementation: failure for missing functions.

- [x] **Step 2: Implement response-hour recommendation and CSV append**

Implement:

- `recommended_send_hour(entries)`
- `append_prompt_log(...)`
- `update_response_log(...)`

- [x] **Step 3: Add the initial CSV header**

Create `data/discord_accountability_log.csv` with the stable field names used by the script.

- [x] **Step 4: Verify tests pass**

Run: `python3 -m unittest tests/test_discord_accountability.py`
Expected: all tests pass.

### Task 3: Discord Webhook Send Path

**Files:**
- Modify: `scripts/discord_accountability.py`

- [x] **Step 1: Add dependency-free webhook sending**

Use `urllib.request` to POST JSON with `content`, `username`, and `allowed_mentions` to the URL from `JACK_DISCORD_WEBHOOK_URL`.

- [x] **Step 2: Add dry-run mode**

Allow `send --dry-run` to print the selected prompt without posting to Discord or appending to the log.

- [x] **Step 3: Verify script help works**

Run: `python3 scripts/discord_accountability.py --help`
Expected: help text exits with code 0.

### Task 4: Operating Documentation

**Files:**
- Create: `docs/discord-accountability-loop.md`
- Modify: `README.md`
- Modify: `docs/agentic-support-layer.md`
- Modify: `docs/dashboard-layer.md`

- [x] **Step 1: Document the loop**

Explain the goal, adaptive voice, adaptive timing, repo logging, script commands, and future upgrade path.

- [x] **Step 2: Link it into the existing strategy docs**

Add the Discord accountability loop to the README planning docs, agentic support layer, and dashboard layer.

- [x] **Step 3: Verify documentation references resolve**

Run: `test -f docs/discord-accountability-loop.md && test -f data/discord_accountability_log.csv && test -f scripts/discord_accountability.py`
Expected: exit code 0.
