#!/usr/bin/env python3
"""Create a CRM lead file from a GitHub event (issue form, dispatch, or manual run).

Reads the triggering event from GITHUB_EVENT_PATH / GITHUB_EVENT_NAME, so user
input never passes through shell interpolation. Writes the lead record to
vault/CRM/Leads/<Company>.md in the same shape as the Lead Template, and emits
step outputs (slug, lead_path, company, issue_number) via GITHUB_OUTPUT.

Fails loudly: any invalid or missing required input exits non-zero with a
message on stderr, which the workflow surfaces back onto the intake issue.
"""

import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LEADS_DIR = REPO_ROOT / "vault" / "CRM" / "Leads"

SOURCES = {"website", "referral", "ads", "event", "outreach", "other"}

# Issue-form headings (lowercased) -> canonical field names
HEADING_MAP = {
    "company": "company",
    "contact name": "contact",
    "email": "email",
    "phone": "phone",
    "source": "source",
    "referrer (existing customer)": "referrer",
    "estimated value (usd)": "value",
    "next action": "next_action",
    "next action date": "next_action_date",
    "notes": "notes",
}


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_issue_form(body: str) -> dict:
    """Parse GitHub issue-form markdown ('### Heading\\n\\nvalue') into fields."""
    fields = {}
    current = None
    buf: list[str] = []
    for line in (body or "").splitlines():
        m = re.match(r"^###\s+(.*)$", line)
        if m:
            if current:
                fields[current] = "\n".join(buf).strip()
            current = HEADING_MAP.get(m.group(1).strip().lower())
            buf = []
        elif current is not None:
            buf.append(line)
    if current:
        fields[current] = "\n".join(buf).strip()
    return {
        k: ("" if v.strip() in {"_No response_", "None"} else v.strip())
        for k, v in fields.items()
    }


def gather_fields() -> tuple[dict, str]:
    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")
    if not event_path or not os.path.exists(event_path):
        fail("GITHUB_EVENT_PATH is missing — this script runs inside Actions")
    with open(event_path) as f:
        event = json.load(f)

    if event_name == "workflow_dispatch":
        return dict(event.get("inputs") or {}), ""
    if event_name == "repository_dispatch":
        return dict(event.get("client_payload") or {}), ""
    if event_name == "issues":
        issue = event.get("issue") or {}
        return parse_issue_form(issue.get("body", "")), str(issue.get("number", ""))
    fail(f"unsupported event: {event_name}")
    raise AssertionError  # unreachable


def clean_line(value: str) -> str:
    """Single-line, trimmed, control characters removed."""
    return re.sub(r"[\x00-\x1f\x7f]", " ", str(value or "")).strip()


def yaml_str(value: str) -> str:
    """Quote a scalar safely for our frontmatter."""
    v = clean_line(value)
    if not v:
        return ""
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    fields, issue_number = gather_fields()

    def get(k: str) -> str:
        return clean_line(fields.get(k, ""))

    company = get("company")
    if not company:
        fail("'company' is required")

    # Filename: strict allowlist — letters, digits, space, and & ' - _ . , +
    # (defense-in-depth: no shell metacharacters even though values only ever
    # reach the workflow through env vars, never inline interpolation)
    slug_name = re.sub(r"[^A-Za-z0-9 &'\-_.,+]", "", company)
    slug_name = re.sub(r"\s+", " ", slug_name).strip().strip(".")
    if not slug_name:
        fail(f"company name {company!r} produces an empty filename")

    source = get("source").lower() or "other"
    if source not in SOURCES:
        source = "other"

    value = re.sub(r"[^0-9.]", "", get("value"))
    if value.count(".") > 1 or value == ".":
        value = ""

    nad = get("next_action_date")
    if nad:
        try:
            datetime.strptime(nad, "%Y-%m-%d")
        except ValueError:
            fail(f"next_action_date {nad!r} is not YYYY-MM-DD")

    referrer = get("referrer")
    if referrer and not referrer.startswith("[["):
        referrer = f"[[{referrer.strip('[]')}]]"

    notes = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", str(fields.get("notes") or "")).strip()
    today = date.today().isoformat()

    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    lead_path = LEADS_DIR / f"{slug_name}.md"
    if lead_path.exists():
        fail(
            f"a lead file named {lead_path.name!r} already exists — "
            "update that record instead of creating a duplicate"
        )

    fm = [
        "---",
        "type: lead",
        "status: new",
        f"source: {source}",
        f"referrer: {yaml_str(referrer)}",
        "owner:",
        f"email: {yaml_str(get('email'))}",
        f"phone: {yaml_str(get('phone'))}",
        f"value: {value}",
        f"created: {today}",
        f"last_contact: {today}",
        f"next_action: {yaml_str(get('next_action') or 'First response (24h target)')}",
        f"next_action_date: {nad or today}",
        "tags:",
        "  - crm",
        "  - lead",
        "---",
    ]

    body = f"""
# {company}

## Snapshot

- **Who:** {get('contact') or ''}
- **Problem they have:**
- **Why now:**

## Qualification

- [ ] Fit (right size / industry)
- [ ] Budget confirmed
- [ ] Decision maker identified
- [ ] Timeline agreed

## Notes

{notes if notes else '<!-- Log every interaction as a Touchpoint note and link it here -->'}

## Status values

`new` → `contacted` → `qualified` → `proposal` → `won` / `lost`

If `lost`, record the reason below — this feeds the weekly review:

**Lost reason:**
"""

    lead_path.write_text("\n".join(fm) + "\n" + body.lstrip("\n"), encoding="utf-8")
    print(f"created {lead_path.relative_to(REPO_ROOT)}")

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        branch_slug = re.sub(r"[^a-z0-9]+", "-", slug_name.lower()).strip("-")
        with open(out, "a") as f:
            f.write(f"company={slug_name}\n")
            f.write(f"slug={branch_slug}\n")
            f.write(f"lead_path={lead_path.relative_to(REPO_ROOT)}\n")
            f.write(f"issue_number={issue_number}\n")


if __name__ == "__main__":
    main()
