#!/usr/bin/env python3
"""
MQL Sequence Generator - Phase 1

Takes leads (from a CSV file) and, based on which signal fired for each
lead, generates the personalized message content for every step of the
matching sequence (8-day high-intent, or 20-day nurture).

This phase does NOT send anything or talk to any external system - it
just produces the personalized text so you can review it, copy it into
your outreach tool, or use it as the input for a later automated phase.

USAGE:
    python3 generate_sequence.py sample_leads.csv

    This reads sample_leads.csv and writes one text file per lead into
    the output/ folder, e.g. output/jane_doe_acme_corp.txt

CSV COLUMNS EXPECTED (see sample_leads.csv for an example):
    first_name        - required
    company            - required
    title              - optional
    signal             - required. One of: demo_request, website_visit,
                         ebook_download, webinar_attendance
    topic              - optional. What specifically triggered them.
                         Write it as a noun phrase, since it gets dropped
                         into sentences like "thanks for checking out
                         {topic}" - e.g. "our pricing page", "our product",
                         "the Scaling Support Ops guide", "our Q3 webinar".
                         Avoid verb phrases like "requesting a demo".
    product_interest   - optional. What they seem interested in
"""

import csv
import sys
import os
from pathlib import Path

from templates import SIGNAL_TO_SEQUENCE, SEQUENCES

# Sensible fallback values so a missing optional field doesn't break
# personalization - it just reads a bit more generically instead of
# crashing.
DEFAULTS = {
    "title": "there",
    "topic": "what you looked at",
    "product_interest": "this area",
}

REQUIRED_FIELDS = ["first_name", "company", "signal"]


def load_leads(csv_path):
    leads = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):  # row 1 is the header
            missing = [field for field in REQUIRED_FIELDS if not row.get(field)]
            if missing:
                print(
                    f"Skipping row {row_num}: missing required field(s) {missing}"
                )
                continue
            leads.append(row)
    return leads


def build_sequence_for_lead(lead):
    signal = lead["signal"].strip()
    sequence_key = SIGNAL_TO_SEQUENCE.get(signal)
    if sequence_key is None:
        known = ", ".join(sorted(SIGNAL_TO_SEQUENCE.keys()))
        raise ValueError(
            f"Unknown signal '{signal}' for {lead.get('first_name')}. "
            f"Expected one of: {known}"
        )

    sequence = SEQUENCES[sequence_key]

    # Fill in defaults for any optional fields that weren't provided.
    fields = {**DEFAULTS, **{k: v for k, v in lead.items() if v}}

    messages = []
    for step in sequence["steps"]:
        messages.append(
            {
                "day": step["day"],
                "subject": step["subject"].format(**fields),
                "body": step["body"].format(**fields),
            }
        )

    return sequence_key, sequence["label"], messages


def render_lead_output(lead, sequence_key, sequence_label, messages):
    lines = [
        f"Lead: {lead['first_name']} — {lead['company']} ({lead.get('title', 'n/a')})",
        f"Signal: {lead['signal']}",
        f"Sequence: {sequence_label} ({sequence_key})",
        "=" * 60,
        "",
    ]
    for msg in messages:
        lines.append(f"--- Day {msg['day']} ---")
        lines.append(f"Subject: {msg['subject']}")
        lines.append("")
        lines.append(msg["body"])
        lines.append("")
    return "\n".join(lines)


def safe_filename(lead):
    raw = f"{lead['first_name']}_{lead['company']}"
    cleaned = "".join(c if c.isalnum() or c in (" ", "_") else "" for c in raw)
    return cleaned.strip().replace(" ", "_").lower() + ".txt"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generate_sequence.py <leads.csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        sys.exit(1)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    leads = load_leads(csv_path)
    if not leads:
        print("No valid leads found in the CSV.")
        sys.exit(1)

    for lead in leads:
        try:
            sequence_key, sequence_label, messages = build_sequence_for_lead(lead)
        except ValueError as e:
            print(f"Skipping {lead.get('first_name', '?')}: {e}")
            continue

        output_text = render_lead_output(lead, sequence_key, sequence_label, messages)
        out_path = output_dir / safe_filename(lead)
        out_path.write_text(output_text, encoding="utf-8")
        print(f"Wrote {out_path} ({sequence_label}, {len(messages)} messages)")

    print(f"\nDone. {len(leads)} lead(s) processed. See the output/ folder.")


if __name__ == "__main__":
    main()
