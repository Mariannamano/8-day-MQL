"""
Message templates for the two MQL sequences.

Each sequence is a list of steps. Each step has:
- day: how many days after the trigger signal this message goes out
- subject: subject line template
- body: message body template

Templates use Python's str.format() placeholders. Available fields for
any lead (see generate_sequence.py / sample_leads.csv):
    {first_name}   - lead's first name
    {company}      - lead's company name
    {title}        - lead's job title
    {topic}        - the specific thing that triggered them (page visited,
                      ebook title, webinar name) - optional, falls back to
                      a generic phrase if not provided
    {product_interest} - optional, what they seem interested in

SIGNAL_TO_SEQUENCE maps a raw signal name to which sequence it triggers.
"""

SIGNAL_TO_SEQUENCE = {
    "demo_request": "high_intent_8day",
    "website_visit": "high_intent_8day",
    "ebook_download": "nurture_20day",
    "webinar_attendance": "nurture_20day",
}

SEQUENCES = {
    "high_intent_8day": {
        "label": "8-Day High-Intent Sequence",
        "trigger_signals": ["demo_request", "website_visit"],
        "steps": [
            {
                "day": 0,
                "subject": "Following up on your interest, {first_name}",
                "body": (
                    "Hi {first_name},\n\n"
                    "Thanks for checking out {topic} — I wanted to reach out personally "
                    "since it looks like {company} might be exploring options in this space.\n\n"
                    "Happy to walk you through how teams like yours are using us, whenever's "
                    "convenient. Do you have 15 minutes this week?\n\n"
                    "Best,\n"
                ),
            },
            {
                "day": 1,
                "subject": "Quick question, {first_name}",
                "body": (
                    "Hi {first_name},\n\n"
                    "Following up on my note yesterday — no pressure at all, just curious "
                    "what prompted you to look into {topic}. Is there a specific problem "
                    "you're trying to solve at {company} right now?\n\n"
                    "Happy to point you in the right direction even if it's not us.\n\n"
                    "Best,\n"
                ),
            },
            {
                "day": 3,
                "subject": "How teams like {company} are solving this",
                "body": (
                    "Hi {first_name},\n\n"
                    "Thought this might be useful — we've worked with other {title} peers "
                    "facing similar challenges around {product_interest}. Happy to share "
                    "a quick example of how they approached it if that's helpful.\n\n"
                    "Still open to grabbing 15 minutes if it's useful timing.\n\n"
                    "Best,\n"
                ),
            },
            {
                "day": 5,
                "subject": "Still exploring options?",
                "body": (
                    "Hi {first_name},\n\n"
                    "Wanted to check back in — a lot of folks in your position tell us "
                    "timing and budget are the biggest question marks early on. Happy to "
                    "tailor a conversation around whatever's most useful for {company} "
                    "right now, no generic pitch.\n\n"
                    "Worth a quick call?\n\n"
                    "Best,\n"
                ),
            },
            {
                "day": 8,
                "subject": "Should I close your file, {first_name}?",
                "body": (
                    "Hi {first_name},\n\n"
                    "I don't want to keep cluttering your inbox — if now isn't the right "
                    "time for {company}, totally understand. Just let me know and I'll "
                    "check back in down the line instead.\n\n"
                    "If you'd still like to connect, I'm around.\n\n"
                    "Best,\n"
                ),
            },
        ],
    },
    "nurture_20day": {
        "label": "20-Day Content Nurture Sequence",
        "trigger_signals": ["ebook_download", "webinar_attendance"],
        "steps": [
            {
                "day": 0,
                "subject": "Here's your copy of {topic}",
                "body": (
                    "Hi {first_name},\n\n"
                    "Thanks for grabbing {topic} — hope it's useful for {company}. "
                    "I'll follow up over the next few weeks with a few extra resources "
                    "in case they're helpful, no strings attached.\n\n"
                    "Let me know if you have any questions in the meantime.\n\n"
                    "Best,\n"
                ),
            },
            {
                "day": 3,
                "subject": "One idea worth trying from {topic}",
                "body": (
                    "Hi {first_name},\n\n"
                    "Wanted to flag one thing from {topic} that tends to make the biggest "
                    "difference for teams like {company}: getting the basics right on "
                    "{product_interest} before anything else. Curious if that resonates "
                    "with where you are today.\n\n"
                    "Best,\n"
                ),
            },
            {
                "day": 7,
                "subject": "How another {title} approached this",
                "body": (
                    "Hi {first_name},\n\n"
                    "Sharing a quick story: a {title} at a company similar to {company} "
                    "used the same ideas from {topic} and saw a real shift within a "
                    "quarter. Happy to share more detail if useful.\n\n"
                    "Best,\n"
                ),
            },
            {
                "day": 11,
                "subject": "A trend worth watching",
                "body": (
                    "Hi {first_name},\n\n"
                    "Following up with something a bit broader — we're seeing more teams "
                    "rethink their approach to {product_interest} this year. Happy to "
                    "send over what we're seeing work, if that'd be useful for {company}.\n\n"
                    "Best,\n"
                ),
            },
            {
                "day": 15,
                "subject": "Any questions on {topic}?",
                "body": (
                    "Hi {first_name},\n\n"
                    "Just checking in — did {topic} raise any questions for you or the "
                    "team at {company}? Happy to jump on a quick call if it'd help to "
                    "talk through anything.\n\n"
                    "Best,\n"
                ),
            },
            {
                "day": 20,
                "subject": "Want to see this in action, {first_name}?",
                "body": (
                    "Hi {first_name},\n\n"
                    "It's been a few weeks since {topic} — if it's still relevant for "
                    "{company}, I'd love to show you how this looks in practice. Worth "
                    "15 minutes?\n\n"
                    "Best,\n"
                ),
            },
        ],
    },
}
