---
type: referral
referrer:
referred:
date: 2026-01-01
status: invited
reward: pending
tags:
  - crm
  - referral
---

# {{title}}

> Name this note `Referrer → Referred`, e.g. `Globex → Acme Corp`

## Details

- **Referrer** (existing customer): link them in `referrer`, e.g. `"[[Globex]]"`
- **Referred** (new lead): link the lead note in `referred` once created, with `source: referral` and `referrer` set on the lead

## Follow-through

- [ ] Thank the referrer within 24h
- [ ] Contact the referred lead within 48h
- [ ] Update `status` as it moves
- [ ] Send reward when converted, set `reward: sent`

## Status values

`invited` → `contacted` → `converted` / `lost`

## Reward values

`pending` → `sent` (or `n/a`)
