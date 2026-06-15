import csv
import importlib.util
import tempfile
import unittest
from unittest import mock
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "discord_accountability.py"
spec = importlib.util.spec_from_file_location("discord_accountability", MODULE_PATH)
discord_accountability = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discord_accountability)


class DiscordAccountabilityTest(unittest.TestCase):
    def test_choose_voice_softens_after_three_missed_responses(self):
        entries = [
            {"response_received": "no", "productive_progress": "no"},
            {"response_received": "no", "productive_progress": "no"},
            {"response_received": "no", "productive_progress": "no"},
        ]

        self.assertEqual(discord_accountability.choose_voice(entries), "gentle_coach")

    def test_choose_voice_uses_challenge_after_engaged_progress(self):
        entries = [
            {
                "response_received": "yes",
                "productive_progress": "yes",
                "response_summary": "Picked one print to test.",
            }
        ]

        self.assertEqual(discord_accountability.choose_voice(entries), "game_challenge")

    def test_choose_voice_defaults_to_direct_teammate_for_clear_next_action(self):
        entries = [
            {
                "response_received": "yes",
                "productive_progress": "partial",
                "next_step": "Photograph one finished piece.",
            }
        ]

        self.assertEqual(discord_accountability.choose_voice(entries), "direct_teammate")

    def test_recommended_send_hour_uses_most_common_response_hour(self):
        entries = [
            {"response_received_at_local": "2026-06-13T20:14:00"},
            {"response_received_at_local": "2026-06-14T19:40:00"},
            {"response_received_at_local": "2026-06-15T20:02:00"},
        ]

        self.assertEqual(discord_accountability.recommended_send_hour(entries), 20)

    def test_append_prompt_log_writes_summary_not_transcript(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            log_path = Path(tmp_dir) / "discord_accountability_log.csv"

            discord_accountability.append_prompt_log(
                log_path,
                checkin_id="2026-06-15-am",
                sent_at_local="2026-06-15T20:00:00",
                voice="direct_teammate",
                prompt="What is the smallest art-money step today?",
                recommended_send_hour=20,
            )

            with log_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(
            rows,
            [
                {
                    "checkin_id": "2026-06-15-am",
                    "sent_at_local": "2026-06-15T20:00:00",
                    "recommended_send_hour": "20",
                    "voice": "direct_teammate",
                    "prompt_text": "What is the smallest art-money step today?",
                    "discord_message_id": "",
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
            ],
        )

    def test_send_webhook_rejects_non_webhook_url_before_request(self):
        with mock.patch.object(discord_accountability.request, "urlopen") as urlopen:
            with self.assertRaises(SystemExit) as raised:
                discord_accountability.send_webhook(
                    "cd /Users/jjschultz/src/jack-art-business",
                    "hello",
                )

        self.assertIn("Discord webhook URL is invalid", str(raised.exception))
        urlopen.assert_not_called()

    def test_send_webhook_uses_discord_json_headers(self):
        captured = {}

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                return False

            def read(self):
                return b'{"id":"123"}'

        def fake_urlopen(webhook_request, timeout):
            captured["request"] = webhook_request
            captured["timeout"] = timeout
            return Response()

        with mock.patch.object(discord_accountability.request, "urlopen", fake_urlopen):
            message_id = discord_accountability.send_webhook(
                "https://discord.com/api/webhooks/123/token",
                "hello",
            )

        self.assertEqual(message_id, "123")
        self.assertEqual(captured["timeout"], 20)
        self.assertEqual(captured["request"].get_method(), "POST")
        self.assertEqual(captured["request"].headers["Content-type"], "application/json")
        self.assertIn("Jack Art Business", captured["request"].headers["User-agent"])
        self.assertEqual(
            captured["request"].full_url,
            "https://discord.com/api/webhooks/123/token?wait=true",
        )


if __name__ == "__main__":
    unittest.main()
