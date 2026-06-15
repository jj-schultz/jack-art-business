# Discord Accountability Loop

This document defines the first Discord-based accountability system for keeping
Jack moving toward earning money through his art while also building the durable
habits and assets that support a long-term creative career.

## Goal

Jack should get one lightweight Discord prompt on days when the system runs. The
prompt should ask for a tiny productive next step toward art income, then the
repo should preserve a structured summary of the interaction.

The system should talk to Jack directly. Parent/guardian or agent review happens
through the repo log, not by adding extra people to the Discord conversation.

## Why Discord

Jack uses Discord more reliably than email or text. This makes Discord the best
place for daily accountability nudges, especially if the prompt feels like a
teammate helping him make one concrete move instead of an adult assigning
homework.

## Operating Principles

- Keep prompts low-pressure, short, and actionable.
- Count broad productive progress, not only sales.
- Preserve summaries, not full Discord transcripts.
- Avoid guilt, streak shame, or public pressure.
- Use the repo as the durable record of what was tried and how Jack responded.
- Keep the loop pointed at recurring creative revenue and Jack's longer-term
  creative career.

## Productive Progress

Any of these count as progress:

- Making or finishing art.
- Photographing, scanning, or organizing a finished piece.
- Cataloging a piece with title, medium, size, or notes.
- Choosing a price or product path.
- Picking one piece to test as an original, print, sticker, card, zine, or
  digital product.
- Sharing available work with a trusted person.
- Replying to buyer or supporter interest.
- Learning something practical about printing, selling, packaging, shipping, or
  platform rules.
- Removing a blocker that made the next business action harder.

## Adaptive Voice

The prompt voice should change based on Jack's recent responses.

### Gentle Coach

Use this when Jack has not responded recently, seems stuck, names a blocker, or
only has enough energy for a very small check-in.

Example:

```text
Hey Jack, tiny art-business check-in. No guilt if today was packed. Did you
make, photograph, catalog, price, share, or unblock one thing that helps your
art earn money? If yes, what was it? If not, what would make the next step
easier?
```

### Direct Teammate

Use this as the default when there is a clear next business action.

Example:

```text
Daily art-business check-in: what is the smallest productive step today? A good
candidate is: photograph one finished piece. Reply with what you did, what is
blocked, or the next tiny action.
```

### Game Challenge

Use this when Jack has recently responded and completed productive progress.

Example:

```text
Today's art-money mission: finish one tiny move in 15 minutes or less.
Suggested mission: photograph one finished piece. Reply with 'done', 'blocked',
or the move you chose instead.
```

## Adaptive Timing

The first version adapts timing from the repo log, not from surveillance of
Discord activity. Each logged response can include `response_received_at_local`.
The script recommends the hour when Jack has most often responded.

If there is no response history, the fallback send hour is 16:00 local time.
After enough responses are logged, an external scheduler can call the send
command near the recommended hour.

## Repo Log

The durable log lives at:

- `data/discord_accountability_log.csv`

The specific task queue lives at:

- `data/next_actions.csv`

Daily prompts should prefer the first `ready` or `open` action assigned to Jack
in `data/next_actions.csv`. Each action should be small enough to finish in one
short sitting and should include a concrete done condition. If there is no ready
action, the script falls back to the most recent `next_step` from the Discord
accountability log.

The log records:

- Check-in id.
- Local send time.
- Recommended send hour.
- Voice used.
- Prompt sent.
- Discord message id, if available.
- Whether Jack responded.
- Local response time.
- Short response summary.
- Whether productive progress happened.
- Next step.
- Blocker.
- Follow-up owner and due date.
- Notes.

Do not paste full Discord transcripts into the log. Summaries should preserve
business context and accountability without making the repo feel like
surveillance.

## Script

The helper script is:

- `scripts/discord_accountability.py`

It has three commands:

```bash
python3 scripts/discord_accountability.py suggest
python3 scripts/discord_accountability.py send --dry-run
python3 scripts/discord_accountability.py log-response --response-received yes --summary "Picked one finished piece to photograph." --productive-progress yes --next-step "Photograph it tomorrow."
```

`send` posts through the `JACK_DISCORD_WEBHOOK_URL` environment variable unless
`--dry-run` is used. This should be a webhook for a private Discord channel that
Jack uses directly. The repo must not store the webhook URL.

Discord webhooks can post messages to channels without a bot user. If the system
later needs to read replies automatically, that should become a separate Discord
bot implementation with its own token handling and privacy review.

## Initial Automation Shape

Version one can be operated by a scheduler that runs the script once per day:

1. Read `data/discord_accountability_log.csv`.
2. Read `data/next_actions.csv`.
3. Choose the first ready, specific, small action assigned to Jack.
4. Choose the adaptive voice.
5. Recommend the active hour from previous response times.
6. Send the prompt to Jack's private Discord channel.
7. Append the prompt to the repo log.
8. Later, summarize Jack's reply into the same log row.

This is intentionally small. The important behavior is the daily nudge, adaptive
voice, adaptive timing, and durable repo summary.

## Future Upgrade Path

Possible later improvements:

- Add a Discord bot that can read replies and update the repo log automatically.
- Use Linear to create or update the smallest next business action after Jack
  responds.
- Generate weekly check-in notes from the Discord log.
- Feed completed actions into the dashboard layer.
- Track which voice and prompt types produce the most useful responses.
