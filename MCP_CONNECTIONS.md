# MCP Data Source Connections

Planning notes for Phase 2/3: instead of a hand-built CSV, signals and
personalization context should come from the tools we already use, all
searchable by the LLM through MCP in one place.

## Why

Right now `generate_sequence.py` only knows what's in `sample_leads.csv`.
Every field it personalizes with (`signal`, `topic`, `product_interest`)
has to be typed in by hand. The data actually lives across several
tools. Connecting them via MCP means the LLM can look a lead up once and
pull whatever context exists, instead of someone copying it in manually.

## Data sources

| Source | What it provides | Maps to |
|---|---|---|
| **Salesforce** | Accounts, contacts, opportunities, lead/account fields (industry, company size, owner) | `company`, `title`, account-level fit context; the CRM system of record for Phase 2 signal pulls |
| **Salesfinity** | Outbound call activity: call logs, dispositions, follow-ups, scored calls | Signal that a rep already engaged this lead by phone; disposition/notes can inform `topic` and timing (don't re-trigger a sequence mid-conversation) |
| **Fathom (CR)** | Call recordings: meeting summaries and transcripts | Richer `topic` / `product_interest` context straight from what the prospect actually said on a demo or discovery call |
| **Amplemarket** | Sequences, leads, accounts, contact enrichment | Phase 3 target — where the generated sequence actually gets created and the lead enrolled; also a source of existing sequence/lead state so we don't double-enroll |
| **OpenFunnel** | Account/contact research signals (intent, hiring, funding, tech stack, etc.) | Additional trigger `signal`s beyond the current four (`demo_request`, `website_visit`, `ebook_download`, `webinar_attendance`), and extra fodder for `product_interest` |

## How they fit together

1. **Signal detection** — a lead's `signal` (today typed manually into the
   CSV) should instead be derivable from Salesforce (form fill, pricing
   page visit tracked as an activity), OpenFunnel (intent/research
   signal), or Salesfinity (a call happened). `SIGNAL_TO_SEQUENCE` in
   `templates.py` already maps a signal name to a sequence — this just
   changes where the signal name comes from.
2. **Personalization context** — before rendering a sequence, look up the
   lead/company across Salesforce (firmographic + CRM fields), Fathom
   (recent call transcript/summary, if any), and OpenFunnel (research
   signals) to fill in `topic` and `product_interest` with real detail
   instead of the generic `DEFAULTS` fallback in `generate_sequence.py`.
3. **De-duplication / state** — check Salesfinity (recent call activity)
   and Amplemarket (already in an active sequence?) before generating and
   enrolling a new sequence, so a lead doesn't get a cold email while a
   rep is already on the phone with them.
4. **Delivery (Phase 3)** — once content is generated, create/enroll the
   lead in Amplemarket via its API/MCP tools instead of writing a `.txt`
   file to `output/`.

## Status

This is a planning doc only — no code here queries these sources yet.
`generate_sequence.py` still reads from a CSV. The next implementation
step (Phase 2) is to replace `load_leads()` with lookups against
Salesforce/OpenFunnel for signals, enriched with Fathom/Salesfinity
context, keeping `templates.py`'s placeholder fields as the interface.
