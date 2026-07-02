---
type: brief
audience: IT specialist (new hire, no business context)
status: living document
tags:
  - crm
  - onboarding
---

# IT Onboarding Brief — The Customer Experience System

Welcome. This document explains, from zero, the business you're supporting, the
system we've built, what "finished" looks like, and where you take over. Read it
top to bottom once; afterwards it works as a reference.

---

## 1. The business in one paragraph

We sell to customers who usually start as **leads** (someone who might buy),
become **customers** (someone who did buy), and — when we've served them well —
become **referrers** (customers who bring us new leads). That last step matters
more than anything else: a referred lead is cheaper to win and more loyal than
any lead we can buy with advertising. So the entire system you're about to read
about exists to answer one question, continuously: **"Where is each person in
that journey, and what's the next thing we owe them?"**

## 2. The philosophy: files, not a SaaS CRM

We deliberately do **not** run this on Salesforce/HubSpot-style software. The
system is a folder of plain-text files:

- Every lead, customer, referral, and interaction is a **Markdown file** (`.md`)
  — a text file you can open in Notepad, grep, back up, and version-control.
- Structured data (status, dates, dollar values) lives in a small block of
  **YAML frontmatter** at the top of each file — machine-readable key: value pairs.
- Relationships ("this referral came from that customer") are **wikilinks** —
  `[[Globex]]` in one file points at the file named `Globex.md`.
- We view and edit these files in **[Obsidian](https://obsidian.md)** — a free
  desktop app that treats a folder ("vault") of Markdown files as a linked
  knowledge base and adds three superpowers we rely on:
  - **Bases** (`.base` files): live database views over the files — think
    "saved SQL queries rendered as tables," defined in YAML.
  - **Canvas** (`.canvas` files): visual whiteboards, stored as plain JSON.
  - **Backlinks**: open any customer file and see every file that links to it —
    the full relationship history with zero configuration.

**Why you should care as the IT person:** there is no database server, no
vendor lock-in, no API keys to babysit for the core system. The "database" is a
Git repository of text files. Everything you know about files, Git, and CI
applies directly.

## 3. The three-layer architecture

```
┌────────────────────────────────────────────────────────┐
│ Layer 3 · THE DATA (vault/CRM/)                        │
│ Lead, Customer, Referral, Touchpoint records + views   │  ← the business lives here
├────────────────────────────────────────────────────────┤
│ Layer 2 · THE AI SKILLS (skills/, .claude-plugin/)     │
│ Teach AI agents to read/write our file formats         │  ← leverage lives here
├────────────────────────────────────────────────────────┤
│ Layer 1 · THE PLUMBING (.github/workflows/)            │
│ Git repo, CI, weekly upstream sync, review bots        │  ← you own this
└────────────────────────────────────────────────────────┘
```

### Layer 1 — Plumbing (your home turf)

- **GitHub repo** `hfroget-305/obsidian-minimal` holds everything.
- **`sync-obsidian-skills.yml`**: a GitHub Action that runs every Monday,
  checks the upstream open-source skill definitions
  ([kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)), and
  opens a pull request when they change. It has a 10-minute timeout, doesn't
  persist credentials, and fails loudly if its rewrite step stops matching.
- **CodeRabbit** reviews every PR automatically. Nothing lands on `master`
  without passing review.

### Layer 2 — AI skills (the leverage)

`skills/` contains five instruction sets ("Agent Skills") that teach AI coding
agents (Claude Code and compatible tools) to work with our file formats
correctly: Obsidian Markdown, Bases syntax, JSON Canvas, the Obsidian CLI, and
a web-clipping tool (Defuddle). Because of these, an AI agent can create a
correctly-structured lead file, update a dashboard view, or redraw the journey
canvas on request — this whole CRM was built that way. Treat the skills as
vendored dependencies: the Monday sync keeps them current; you review the PR.

### Layer 3 — The data (the business)

`vault/CRM/` is the product. Four **record types**, each a template:

| Record | One file per… | Key fields | Lifecycle (`status`) |
|---|---|---|---|
| **Lead** | potential customer | `source`, `referrer`, `value`, `next_action`, `next_action_date` | new → contacted → qualified → proposal → won/lost |
| **Customer** | paying customer | `health` (green/yellow/red), `nps` (0–10), `last_contact`, `referrals_given` | onboarding → active ⇄ at-risk → churned |
| **Referral** | referral event | `referrer` → customer file, `referred` → lead file, `reward` | invited → contacted → converted/lost |
| **Touchpoint** | interaction | `about` → who, `channel`, `sentiment`, `follow_up` | — (append-only log) |

Plus two instruments over those records:

- **`Dashboards/CRM Dashboard.base`** — six live views: Lead Pipeline (grouped
  by stage, pipeline value summed), **Follow-ups Due** (anything overdue),
  Customers (NPS average), **At Risk** (red/yellow health *or* 30+ days of
  silence — our churn early-warning), Referrals, Recent Touchpoints.
- **`Customer Experience Flow.canvas`** — the visual journey map: Attract →
  Convert → Deliver → Delight & Refer, with the **referral flywheel** (promoters
  feed new leads) and a **continuous improvement loop** (detractor win-backs,
  lost-reason analysis, weekly review).

The operating rhythm is a **20-minute weekly review** documented in
`CRM Home.md`: clear overdue follow-ups → one action per at-risk customer →
chase referrals → pattern-match lost reasons → ship one small improvement.

## 4. The finished product — what "done" looks like

The end goal is a system where **humans only do the judgement work** (talking
to people, deciding health, choosing actions) and **everything mechanical is
automated**. Concretely, the finished product has five properties:

1. **Self-maintaining plumbing.** Dependencies update themselves via reviewed
   PRs (✅ already live: the Monday sync). Backups are automatic (Git history +
   an off-site copy). Nothing rots silently — every automated job fails loudly.

2. **Zero-touch record intake.** A new lead never gets typed in by hand:
   - Website form / inbound email → a correctly-formatted lead file appears in
     `CRM/Leads/` with `status: new` and today's date, via a small automation
     (GitHub Action, n8n flow, or a script watching a mailbox — your call).
   - Email/calendar interactions get logged as Touchpoint files the same way.

3. **The system nudges us, we never poll it.** Today the dashboard shows
   overdue follow-ups when we open it; finished means it **pushes**: a Monday
   digest (email or chat message) generated from the same data — overdue
   actions, at-risk customers, referral rewards owed. A scheduled job reads
   the frontmatter (it's just YAML — trivially parseable) and formats a summary.

4. **Experience metrics tracked over time, not just point-in-time.** A monthly
   snapshot job appends key numbers (pipeline value by source, NPS average,
   referral conversion rate, average days-to-first-contact) to a metrics note,
   so trends become visible. This is what "constantly improve the experience"
   means measurably: response times falling, NPS rising, flywheel spinning.

5. **AI-assisted operations.** Because of Layer 2, routine work is delegable
   in plain English: "log a touchpoint for today's Globex call, sentiment
   positive, follow-up next Tuesday" or "draft the weekly review." The skills
   guarantee the output lands in the right format, in the right folder.

## 5. Your first 90 days (proposed roadmap)

| Phase | Deliverable | Notes |
|---|---|---|
| **Week 1–2 · Learn & harden** | Run the weekly review once yourself; set up off-site backup of the repo; verify the Monday sync PR flow | You can't automate a process you haven't run by hand |
| **Week 3–6 · Intake automation** | Form/email → lead file pipeline; interaction → touchpoint pipeline | Highest-leverage single item; kills the most manual typing |
| **Week 7–10 · Push notifications** | Monday digest job (overdue / at-risk / rewards owed) | Read frontmatter, format, send — keep it boring and reliable |
| **Week 11–13 · Metrics history** | Monthly snapshot job + trends note | Enables the improvement loop to be judged by numbers |
| **Ongoing** | Review sync PRs; keep automations green; propose one process improvement per month | You're a participant in the improvement loop, not just its plumber |

## 6. Ground rules

- **Plain text is sacred.** Any automation you build reads/writes Markdown +
  YAML frontmatter in this repo. No shadow databases, no data that exists only
  inside a third-party tool.
- **Everything through PRs.** Automations commit to branches and open PRs, same
  as humans and the sync bot. Review is the safety net.
- **Fail loudly.** A silent broken automation is worse than no automation —
  follow the pattern in `sync-obsidian-skills.yml` (timeouts, explicit guards).
- **The customer never notices the system.** They just experience fast
  responses, remembered context, and thank-yous that arrive on time. That's
  the product.

## 7. Where everything lives

| What | Where |
|---|---|
| This brief | `vault/CRM/IT Onboarding Brief.md` |
| System hub + weekly ritual | `vault/CRM/CRM Home.md` |
| Visual journey map | `vault/CRM/Customer Experience Flow.canvas` |
| Live dashboard (6 views) | `vault/CRM/Dashboards/CRM Dashboard.base` |
| Record templates | `vault/CRM/Templates/` |
| Example records | `vault/CRM/{Leads,Customers,Referrals,Touchpoints}/` |
| AI skill definitions | `skills/` + `.claude-plugin/` |
| Weekly dependency sync | `.github/workflows/sync-obsidian-skills.yml` |
| Upstream skills source | https://github.com/kepano/obsidian-skills |

Questions this document didn't answer are bugs in this document — fix it via PR.
