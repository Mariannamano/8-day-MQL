# MQL Sequence Tool

Generates personalized outreach sequence content for marketing-qualified
leads (MQLs), based on which signal triggered them:

- **8-Day High-Intent Sequence** — triggered by a `demo_request` or a
  `website_visit` (e.g. viewing pricing). Five touches over 8 days.
- **20-Day Content Nurture Sequence** — triggered by an `ebook_download`
  or `webinar_attendance`. Six touches over 20 days.

## Status: Phase 1 (content generation only)

This version does **not** send anything or connect to any outside tool.
It takes a CSV of leads and writes out the personalized message text for
each step of the matching sequence, so you can review it, copy it into
your outreach tool (e.g. Amplemarket), or use it as the foundation for
later automation.

Planned next phases:
- **Phase 2**: pull signals automatically from wherever they actually
  live (website analytics, CRM, marketing automation) instead of a
  hand-built CSV.
- **Phase 3**: automatically create the lead and enroll them in the
  right sequence in Amplemarket via its API — no manual step at all.

See [MCP_CONNECTIONS.md](MCP_CONNECTIONS.md) for how the data sources
behind Phase 2/3 (Salesforce, Salesfinity, Fathom, Amplemarket,
OpenFunnel) are planned to connect via MCP so signals and
personalization context can be looked up in one place instead of typed
into a CSV by hand.

## Requirements

Python 3.8 or newer. No external libraries needed — everything used is
part of the Python standard library.

## Usage

```bash
python3 generate_sequence.py sample_leads.csv
```

This reads `sample_leads.csv` and writes one `.txt` file per lead into
the `output/` folder (created automatically), containing the full
personalized sequence for that lead.

To use it with your own leads, create your own CSV in the same format
(see `sample_leads.csv`) and run:

```bash
python3 generate_sequence.py your_leads.csv
```

## CSV format

| Column            | Required? | Notes                                                                 |
|-------------------|-----------|------------------------------------------------------------------------|
| `first_name`      | Yes       | |
| `company`         | Yes       | |
| `title`           | No        | Falls back to a generic phrase if left blank |
| `signal`          | Yes       | One of: `demo_request`, `website_visit`, `ebook_download`, `webinar_attendance` |
| `topic`           | No        | What specifically triggered them. Write it as a noun phrase — e.g. `our pricing page`, `our product`, `the Scaling Support Ops guide` — since it's dropped into sentences like "thanks for checking out {topic}". Avoid verb phrases like "requesting a demo". |
| `product_interest`| No        | What they seem interested in, e.g. `ticket automation` |

## Project structure

```
mql-sequence-tool/
  generate_sequence.py   - the script you run
  templates.py           - the actual message content for both sequences
  sample_leads.csv        - example input to test with
  output/                 - generated output lands here (git-ignored)
```

## Editing the message content

All the actual wording lives in `templates.py`, in the `SEQUENCES`
dictionary. Each step has a `day`, `subject`, and `body` — edit the text
directly and re-run the script to see your changes. The `{first_name}`,
`{company}`, `{title}`, `{topic}`, and `{product_interest}` placeholders
get filled in automatically from your CSV.
