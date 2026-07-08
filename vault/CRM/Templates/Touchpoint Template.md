---
type: touchpoint
about:
date: "{{date:YYYY-MM-DD}}"
channel: call
sentiment: neutral
follow_up:
follow_up_date:
tags:
  - crm
  - touchpoint
---

# {{title}}

> Name this note `YYYY-MM-DD Who — What`, e.g. `2026-07-02 Globex — QBR`

## What happened

-

## How they felt

`sentiment`: `positive` / `neutral` / `negative` — if negative, consider setting the
customer's `health` to `yellow` or `red` and add a win-back action.

## Next step

Set `follow_up` (what) and `follow_up_date` (when). Mirror it onto the lead
note's `next_action` / `next_action_date`; for customers, update `next_review`.
The dashboard's Follow-ups Due view also catches the touchpoint itself.

## Channel values

`call` / `email` / `meeting` / `chat` / `event`
