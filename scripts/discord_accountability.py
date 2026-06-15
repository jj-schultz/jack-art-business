#!/usr/bin/env python3
"""Generate and log Jack's Discord accountability check-ins."""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from urllib import request
from urllib.error import HTTPError, URLError


DEFAULT_LOG_PATH = Path("data/discord_accountability_log.csv")
DEFAULT_SEND_HOUR = 16
FIELDNAMES = [
    "checkin_id",
    "sent_at_local",
    "recommended_send_hour",
    "voice",
    "prompt_text",
    "discord_message_id",
    "response_received",
    "response_received_at_local",
    "response_summary",
    "productive_progress",
    "next_step",
    "blocker",
    "follow_up_owner",
    "follow_up_due",
    "notes",
]


def load_entries(log_path: Path) -> list[dict[str, str]]:
    if not log_path.exists():
        return []

    with log_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def choose_voice(entries: list[dict[str, str]]) -> str:
    recent = entries[-3:]
    if len(recent) == 3 and all(row.get("response_received") == "no" for row in recent):
        return "gentle_coach"

    last_response = next(
        (row for row in reversed(entries) if row.get("response_received") == "yes"),
        None,
    )
    if not last_response:
        return "direct_teammate"

    if last_response.get("blocker"):
        return "gentle_coach"

    if last_response.get("productive_progress") == "yes":
        return "game_challenge"

    return "direct_teammate"


def recommended_send_hour(entries: list[dict[str, str]]) -> int:
    hours = []
    for row in entries:
        value = row.get("response_received_at_local", "")
        if not value:
            continue
        try:
            hours.append(datetime.fromisoformat(value).hour)
        except ValueError:
            continue

    if not hours:
        return DEFAULT_SEND_HOUR

    return Counter(hours).most_common(1)[0][0]


def latest_next_step(entries: list[dict[str, str]]) -> str:
    for row in reversed(entries):
        next_step = row.get("next_step", "").strip()
        if next_step:
            return next_step
    return "pick one tiny art-money step"


def build_prompt(voice: str, entries: list[dict[str, str]]) -> str:
    next_step = latest_next_step(entries)

    prompts = {
        "gentle_coach": (
            "Hey Jack, tiny art-business check-in. No guilt if today was packed. "
            "Did you make, photograph, catalog, price, share, or unblock one thing "
            "that helps your art earn money? If yes, what was it? If not, what "
            "would make the next step easier?"
        ),
        "direct_teammate": (
            "Daily art-business check-in: what is the smallest productive step "
            f"today? A good candidate is: {next_step}. Reply with what you did, "
            "what is blocked, or the next tiny action."
        ),
        "game_challenge": (
            "Today's art-money mission: finish one tiny move in 15 minutes or less. "
            f"Suggested mission: {next_step}. Reply with 'done', 'blocked', or "
            "the move you chose instead."
        ),
    }
    return prompts[voice]


def append_prompt_log(
    log_path: Path,
    *,
    checkin_id: str,
    sent_at_local: str,
    voice: str,
    prompt: str,
    recommended_send_hour: int,
    discord_message_id: str = "",
) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not log_path.exists()
    row = {
        "checkin_id": checkin_id,
        "sent_at_local": sent_at_local,
        "recommended_send_hour": str(recommended_send_hour),
        "voice": voice,
        "prompt_text": prompt,
        "discord_message_id": discord_message_id,
        "response_received": "",
        "response_received_at_local": "",
        "response_summary": "",
        "productive_progress": "",
        "next_step": "",
        "blocker": "",
        "follow_up_owner": "",
        "follow_up_due": "",
        "notes": "",
    }

    with log_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def update_response_log(
    log_path: Path,
    *,
    checkin_id: str,
    response_received: str,
    response_received_at_local: str,
    response_summary: str = "",
    productive_progress: str = "",
    next_step: str = "",
    blocker: str = "",
    follow_up_owner: str = "",
    follow_up_due: str = "",
    notes: str = "",
) -> None:
    entries = load_entries(log_path)
    if not entries:
        raise SystemExit(f"No log entries found at {log_path}")

    target_index = None
    if checkin_id == "latest":
        target_index = len(entries) - 1
    else:
        for index, row in enumerate(entries):
            if row.get("checkin_id") == checkin_id:
                target_index = index
                break

    if target_index is None:
        raise SystemExit(f"No check-in found for id: {checkin_id}")

    entries[target_index].update(
        {
            "response_received": response_received,
            "response_received_at_local": response_received_at_local,
            "response_summary": response_summary,
            "productive_progress": productive_progress,
            "next_step": next_step,
            "blocker": blocker,
            "follow_up_owner": follow_up_owner,
            "follow_up_due": follow_up_due,
            "notes": notes,
        }
    )
    write_entries(log_path, entries)


def write_entries(log_path: Path, entries: list[dict[str, str]]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in entries:
            writer.writerow({field: row.get(field, "") for field in FIELDNAMES})


def send_webhook(webhook_url: str, prompt: str) -> str:
    webhook_url = webhook_url.strip()
    parsed = urlparse(webhook_url)
    if parsed.scheme != "https" or parsed.netloc not in {"discord.com", "discordapp.com"}:
        raise SystemExit("Discord webhook URL is invalid.")
    if not parsed.path.startswith("/api/webhooks/"):
        raise SystemExit("Discord webhook URL is invalid.")

    payload = json.dumps(
        {
            "content": prompt,
            "username": "Jack Art Business",
            "allowed_mentions": {"parse": []},
        }
    ).encode("utf-8")
    separator = "&" if "?" in webhook_url else "?"
    url = f"{webhook_url}{separator}wait=true"
    webhook_request = request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Jack Art Business Discord Accountability/1.0",
        },
        method="POST",
    )

    try:
        with request.urlopen(webhook_request, timeout=20) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Discord webhook failed with HTTP {exc.code}: {details}") from exc
    except URLError as exc:
        raise SystemExit(f"Discord webhook failed: {exc.reason}") from exc

    if not body:
        return ""

    try:
        return json.loads(body).get("id", "")
    except json.JSONDecodeError:
        return ""


def current_local_timestamp() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def current_checkin_id(now: str) -> str:
    return now[:10]


def command_suggest(args: argparse.Namespace) -> None:
    log_path = Path(args.log)
    entries = load_entries(log_path)
    voice = choose_voice(entries)
    hour = recommended_send_hour(entries)
    prompt = build_prompt(voice, entries)
    print(f"voice: {voice}")
    print(f"recommended_send_hour: {hour}")
    print(f"prompt: {prompt}")


def command_send(args: argparse.Namespace) -> None:
    log_path = Path(args.log)
    entries = load_entries(log_path)
    now = current_local_timestamp()
    voice = args.voice or choose_voice(entries)
    hour = recommended_send_hour(entries)
    prompt = args.prompt or build_prompt(voice, entries)
    checkin_id = args.checkin_id or current_checkin_id(now)
    message_id = ""

    if args.dry_run:
        print(prompt)
        return
    else:
        webhook_url = os.environ.get("JACK_DISCORD_WEBHOOK_URL", "")
        if not webhook_url:
            raise SystemExit("Set JACK_DISCORD_WEBHOOK_URL or use --dry-run.")
        message_id = send_webhook(webhook_url, prompt)
        print(f"sent check-in {checkin_id}")

    append_prompt_log(
        log_path,
        checkin_id=checkin_id,
        sent_at_local=now,
        voice=voice,
        prompt=prompt,
        recommended_send_hour=hour,
        discord_message_id=message_id,
    )


def command_log_response(args: argparse.Namespace) -> None:
    now = args.response_at or current_local_timestamp()
    update_response_log(
        Path(args.log),
        checkin_id=args.checkin_id,
        response_received=args.response_received,
        response_received_at_local=now if args.response_received == "yes" else "",
        response_summary=args.summary,
        productive_progress=args.productive_progress,
        next_step=args.next_step,
        blocker=args.blocker,
        follow_up_owner=args.follow_up_owner,
        follow_up_due=args.follow_up_due,
        notes=args.notes,
    )
    print(f"updated check-in {args.checkin_id}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    suggest = subparsers.add_parser("suggest", help="Print today's adaptive prompt.")
    suggest.add_argument("--log", default=str(DEFAULT_LOG_PATH))
    suggest.set_defaults(func=command_suggest)

    send = subparsers.add_parser("send", help="Send and log today's Discord prompt.")
    send.add_argument("--log", default=str(DEFAULT_LOG_PATH))
    send.add_argument("--checkin-id", default="")
    send.add_argument("--dry-run", action="store_true")
    send.add_argument("--prompt", default="")
    send.add_argument(
        "--voice",
        choices=["gentle_coach", "direct_teammate", "game_challenge"],
        default="",
    )
    send.set_defaults(func=command_send)

    log_response = subparsers.add_parser(
        "log-response",
        help="Update a prompt row with a summarized response.",
    )
    log_response.add_argument("--log", default=str(DEFAULT_LOG_PATH))
    log_response.add_argument("--checkin-id", default="latest")
    log_response.add_argument("--response-received", choices=["yes", "no"], required=True)
    log_response.add_argument("--response-at", default="")
    log_response.add_argument("--summary", default="")
    log_response.add_argument(
        "--productive-progress",
        choices=["", "yes", "no", "partial"],
        default="",
    )
    log_response.add_argument("--next-step", default="")
    log_response.add_argument("--blocker", default="")
    log_response.add_argument("--follow-up-owner", default="")
    log_response.add_argument("--follow-up-due", default="")
    log_response.add_argument("--notes", default="")
    log_response.set_defaults(func=command_log_response)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
