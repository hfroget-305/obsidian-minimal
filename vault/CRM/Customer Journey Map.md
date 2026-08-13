---
type: journey-map
status: living document
owner: HF
created: 2026-08-13
tags:
  - crm
  - journey
---

# Customer Journey Map — Operational Edition

The complete, end-to-end customer journey: from need recognition through purchase,
onboarding, engagement, loyalty, advocacy, churn risk, and reactivation — with the
internal operational journey behind every stage. Companion to
[[Customer Experience Flow.canvas|Customer Experience Flow]] (the visual) and
[[CRM Home]] (the hub). Where that canvas shows *what* the journey is, this note
shows *where it breaks, where money leaks, what should trigger automatically, who
owns the next action, and how success is measured*.

> [!info] How to read this document
> Every claim is labeled:
> - **Known** — observable in this vault (records, templates, dashboard, workflows).
> - **Assumption** — inferred from the example records; verify before betting on it.
> - **Recommendation** — a proposed change, always tied to a measurable outcome.
> - ⚠️ **Data required to validate this** — the vault does not yet capture this number.

---

## 0. Business context

| Field | Value | Basis |
|---|---|---|
| Company / brand | Not recorded in the vault | ⚠️ Data required |
| Product / service | B2B operational-efficiency service sold as **Standard** and **Premium** plans, monthly or annual | Known ([[Globex]], [[Umbrella Co]]) |
| Primary customer | Ops leaders at small/mid-size firms (e.g. "Ops director, 40-person logistics firm") buying back staff time | Assumption (from [[Acme Corp]]) |
| Segments | Standard (monthly, ~$4.5–9k) vs Premium (annual, ~$12k+); referral-sourced vs cold-sourced | Assumption (from record values) |
| Average transaction value | ~$4.5k–$12k per deal | Known range from lead records; ⚠️ true average requires more data |
| Customer lifetime value | Examples: $9k (Standard) and $28k (Premium) | Known examples; ⚠️ portfolio CLV data required |
| Acquisition channels | Website, ads, events, outreach, **referrals** | Known (canvas + `source` field) |
| Lead volume / contact rate / conversion rate / churn rate | Not yet measured | ⚠️ Data required — the monthly metrics snapshot (IT brief §4.4) is the fix |
| Sales process | Founder-led (single `owner: HF`): first-contact call → qualification (fit/budget/authority/timeline) → proposal → close | Known (Lead Template) |
| Service process | Owner-led onboarding, QBRs, check-ins; health judgement per touchpoint | Known (Customer Template) |
| CRM | This vault: Markdown + YAML frontmatter, Obsidian Bases dashboard, Git/GitHub | Known |
| Phone system / messaging channels | Email known; touchpoint channels: call / email / meeting / chat / event. No phone system or SMS/WhatsApp recorded | Known (partial); ⚠️ data required |
| Major existing problems | Single-operator dependency; no speed-to-lead measurement; manual touchpoint logging; silent churn (the [[Umbrella Co]] pattern: champion left → 60% usage drop → 2 ignored emails before the system flagged it) | Known / Assumption |
| Primary objective | Spin the referral flywheel: serve well → NPS 9–10 → referral → cheaper, more loyal lead | Known (IT Onboarding Brief §1) |
| Compliance requirements | None recorded | ⚠️ Data required |

---

## 1. Stage — Trigger / Need recognition

*Before the customer knows we exist.*

- **The triggering event (Assumption):** an operational pain crosses a threshold — "manual dispatch is eating 10h/week" — usually forced by a deadline ("peak season starts in August"). The motivation is **functional** (time lost) with an **urgent** overlay (season, growth, a resignation).
- **Problem in the customer's words:** "we're drowning in manual work," "my team spends all week on X," "we can't scale for the busy season." They search for their *symptom*, not our category.
- **Alternatives considered first:** do nothing (busy-season adrenaline), hire another person, spreadsheet harder, generic software they already own.
- **Company is doing (Known):** nothing — this stage is invisible to the vault today.
- **Company should be doing (Recommendation):** content and ads keyed to the trigger language ("cut dispatch time," "survive peak season") rather than product language; ask every won customer "what happened the week before you contacted us?" and log it in the lead note's **Why now** field — the vault already has the field, it's just underused.
- **Data to capture:** `Why now` on every lead (already in Lead Template ✅ — enforce it at qualification).
- **KPI:** share of won leads with a recorded trigger event. ⚠️ Data required to validate trigger patterns.

## 2. Stage — Awareness

**Actions → Thoughts → Questions → Emotions → Objections → Next action**

| Channel (Known) | Likely first touch | The thought | The skepticism |
|---|---|---|---|
| Referral | A trusted peer says "talk to these people" | "Maria doesn't recommend things lightly" | Minimal — trust is borrowed |
| Website | Lands on pricing page ([[Initech]] came in this way) | "Can this actually fix my problem?" | "Looks small — will they still exist next year?" |
| Ads | Sees a promise ("10h/week back") | "Sounds nice, probably exaggerated" | High — claims need proof |
| Events | Meets the founder in person | "They know their stuff" | "Everyone sounds good at a booth" |
| Outreach | Cold email/call | "Who is this?" | Highest — unsolicited |

- **What captures attention:** a specific, quantified outcome in their vocabulary (Globex's "dispatch time under 2h" is the template — real numbers from real customers).
- **Credibility signals sought:** named customers, concrete numbers, a human who answers fast.
- **Immediate questions:** What does it cost? How long until it works? Who else like me uses it?
- **Company should be doing (Recommendation):** publish 2–3 one-paragraph outcome stories straight from customer notes' "Success looks like" + QBR results (with permission). Zero new infrastructure; the source material already exists in touchpoint notes.
- **Trust movement:** referral starts at high trust (+3 on the emotional scale); cold channels start at −1 and must *earn* the first point.
- **KPI:** leads by `source` (dashboard already groups this ✅); pipeline value by source (already summed ✅). ⚠️ Cost per channel data required for CAC.

## 3. Stage — Consideration

- **Compared against (Assumption):** hiring (a part-time hire ≈ our annual price — expect this math), bigger horizontal tools, "do nothing."
- **Information needed:** price, time-to-value, proof from a similar-size firm, what happens if it doesn't work.
- **Rational objections:** price vs. hire, integration effort, single-vendor risk (we're small).
- **Emotional objections:** "I'll look stupid if this fails," "I don't have time to onboard a tool while drowning" — the cruel irony of every busy-season buyer.
- **What increases perceived value:** speed and specificity of our answers. At this size, the *responsiveness of the sales process is the product demo* — a 2-hour reply says more than a case study.
- **What causes postponement:** vague pricing, slow replies, no deadline. The canvas rule "never leave a proposal hanging" (Known) exists precisely because of this.
- **Confidence-building content (Recommendation):** a one-page "first 30 days" plan attached to every proposal — it answers the *emotional* objection ("onboarding while drowning") which no price sheet touches.
- **Leak here:** leads that go quiet between `contacted` and `qualified` with no `next_action_date` set. The Follow-ups Due view only catches what has a date — **an empty `next_action_date` is invisible to the dashboard** (Known). See leak L2 in §15.

## 4. Stage — Lead capture / first contact

**Capture paths (Known):** website form / issue form / manual run / API dispatch → `crm-lead-intake.yml` → lead file PR. Duplicates and malformed dates rejected loudly ✅.

- **Capture immediately:** company, contact, email, source (+ referrer if referral), estimated value, next action + date. All fields exist in the intake workflow ✅.
- **Do NOT ask yet:** budget details, decision process, timeline — that's discovery-call material. Long forms kill inbound conversion.
- **Speed-to-lead targets (Recommendation — current canvas standard is "respond within 24h"; tighten it):**
  - **≤ 30 s (automated):** acknowledgment email — "got it, here's what happens next, here's a booking link."
  - **≤ 5 min (automated):** intake PR opened, owner notified (push, not pull).
  - **≤ 1 h (human, business hours):** personal reply or call for referral- and website-sourced leads — these are the hot ones.
  - **≤ 24 h (human, hard SLA):** first substantive contact for everything, `status: contacted`, first touchpoint logged.
- **Where leads currently leak (Known/Assumption):**
  1. The intake PR sits unmerged and unseen — nothing *pushes* a new-lead notification to the owner yet (the "system nudges us, we never poll" goal in the IT brief is not yet built for intake).
  2. No auto-acknowledgment to the lead — the ≤30 s window is currently silent.
  3. Channels without a capture path (phone, chat, DMs) rely on the owner remembering to type a record.
- **Automation to build first:** on lead-PR open → send acknowledgment + notify owner. Trigger→KPI spec in §14 (A1).
- **KPI:** time from lead `created` to first touchpoint (**speed-to-lead**) — computable today from frontmatter dates. ⚠️ Baseline data required.

## 5. Stage — Qualification / discovery

The Lead Template already encodes the four gates (Known): **Fit / Budget / Decision maker / Timeline.**

**Recommended question order** (rapport → intent → authority → urgency):
1. "Walk me through what happens today when ___" — rapport + surfaces the real workflow.
2. "What made you look for help *now*?" — intent + urgency; fills **Why now**.
3. "What have you already tried?" — uncovers the alternatives we're compared against.
4. "If this works, what does success look like in 90 days?" — becomes the customer note's **Success looks like** ✅ and, later, the QBR yardstick.
5. "Who else would need to be comfortable with this?" — authority, asked without challenging their status.
6. "Is there a date this needs to work by?" — urgency + natural close timeline.
7. Budget last, as a range check — after value is established, not before.

| Required | Useful | Friction — don't ask |
|---|---|---|
| Problem, Why now, decision maker, timeline, budget range | Team size, current tools, success metric | Org charts, procurement details, anything a form already captured |

- **Auto-populate (Known ✅):** source, referrer, created date, value via intake. **Agent-entered:** qualification checkboxes, Why now, snapshot. **AI-generated (Recommendation):** call-note → touchpoint file drafting via the vault's agent skills.
- **KPI:** qualification rate (`qualified` / `contacted`). ⚠️ Data required.

## 6. Stage — Decision / conversion

- **What makes them buy (Assumption):** a credible path from today's pain to a dated outcome, sold by someone who clearly understood their situation (§5 discovery is the sale).
- **Micro-moments before conversion:** re-reading the proposal, the price-vs-hire math, "what if it doesn't work?", checking us out one more time online, showing a colleague.
- **What almost stops them:** proposals without expiry dates or next steps; unanswered "small" questions; anything that feels like lock-in.
- **"I need to think about it" usually means (Assumption):** an unvoiced objection from §3 — price math, risk of looking bad, or a missing stakeholder. Answer: "Absolutely — what would you need to see to be confident either way?"
- **Risk reversal (Recommendation):** monthly Standard as an explicit low-risk on-ramp ([[Umbrella Co]] is a monthly Standard — the pattern exists ✅); a 30-day success checkpoint written into the proposal.
- **Urgency, honest version:** their own deadline ("peak season starts in August") — put *their* date in the proposal, never fake scarcity.
- **Company operational rule (Known ✅):** at `status: proposal`, `next_action_date` is mandatory. Add: proposals expire in 14 days, with a scheduled follow-up at day 3 and day 10 (Recommendation).
- **KPI:** proposal → won rate; average days in `proposal`. ⚠️ Data required.

## 7. Stage — Payment / transaction

⚠️ **Data required:** no payment provider, invoicing flow, or contract mechanism is recorded in the vault. The recovery journeys below are recommendations to adopt when payment tooling is documented.

| Failure mode | Recovery journey (Recommendation) |
|---|---|
| Payment declined | Auto-retry once → same-day personal email ("card hiccup, no rush — here's a fresh link") → mark lead/customer `next_action` for 48h follow-up |
| Payment abandoned (invoice sent, unpaid 7d) | Day 3 friendly nudge (auto) → day 7 personal call (human) → day 14 pause-and-park, log reason |
| Goes silent after verbal yes | Day 2 recap email restating *their* deadline → day 5 call → day 10 "should I close the file?" honesty email (often revives) |
| Contract unsigned | Daily reminder from e-sign tool (auto); after 3 business days, human call — the blocker is usually a question they didn't ask |
| Changes their mind | Human call, no script: capture the reason verbatim in **Lost reason** — this is the highest-grade product feedback we get |

- **Post-payment anxiety is real:** the moment money moves, the customer's emotion *drops* (see §11). The onboarding journey below is the antidote.
- **KPI:** payment success rate, invoice-to-paid days, contract completion rate. ⚠️ Data required.

---

## 8. First 7 days — onboarding journey

Goal chain: **reduce buyer's remorse → build trust → reach first value → prevent early cancellation → set the engagement rhythm.**
Highest-risk moments: **the silence right after payment** and **day 3–5** (if nothing has visibly happened yet, remorse peaks).

| When | Customer receives | Auto / Human | Why (anxiety it kills) |
|---|---|---|---|
| **Minute 0–10** | Receipt + personal-feeling welcome: what happens next, who to contact, kickoff booking link | Auto | "Did the payment go through? Was this real?" |
| **First hour** | Personal note from the owner: "Saw your order — kickoff options Tue/Wed. Here's your 30-day plan again." | Human | "Am I just a transaction now?" |
| **First 24 h** | Kickoff scheduled; customer note created from [[Customer Template]] (`status: onboarding`), lead history preserved (Known ✅); access/logins issued | Human + system | "Nothing is happening" |
| **Day 2** | Kickoff call: restate **Success looks like**, agree the first-value milestone and its date | Human | "Do they remember what I actually bought this for?" |
| **Day 3** | Setup progress note — even if partial: "X done, Y tomorrow" | Auto or human | Day-3 remorse peak: silence reads as regret |
| **Day 4** | First working piece delivered or demoed | Human | "When do I see anything?" |
| **Day 5** | Check-in: "What's confusing so far?" — invite the dumb questions explicitly | Human | Unasked questions become quiet resentment |
| **Day 6** | Short how-to for the one feature they'll use most | Auto | Overwhelm |
| **Day 7** | Week-1 review touchpoint (logged ✅): wins so far, next week's plan, first `sentiment` reading | Human | "Was this the right call?" — answered with evidence |

- **Proactively explain before they ask:** billing cadence and first invoice date; how support works; what's normal to feel slow in week 1; exactly when first value lands.
- **What causes early cancellation (Assumption):** silence, a missed kickoff, discovering an expectation mismatch that discovery should have caught.
- **Company internal (Recommendation):** an `onboarding_checklist` in the customer note; a Bases view "Onboarding" filtered to `status: onboarding` showing days-since-`since` — flag any customer still onboarding after 14 days.
- **KPIs:** welcome-contact-within-24h rate; kickoff-within-72h rate; day-7 sentiment; early (30-day) cancellation rate. ⚠️ Baselines required.

## 9. Activation

- **Primary activation event (Recommendation, needs validation):** *the customer's agreed success metric moves for the first time* — e.g. Globex seeing dispatch time drop at all. This is the moment the purchase stops being a bet. ⚠️ Data required to confirm correlation with retention.
- **Secondary events:** kickoff completed ≤72h; first unsolicited inbound question (they're invested); a second team member engaged; first positive-`sentiment` touchpoint.
- **Target (Recommendation):** activation inside 14 days; >80% of new customers.
- **What prevents it:** no agreed metric at kickoff (nothing to move), customer-side setup stalls, single-threaded contact going quiet.
- **Activation Score 0–100** (computable from vault fields today):

| Component | Points |
|---|---|
| Kickoff touchpoint logged ≤ 72h of `since` | 20 |
| Success metric agreed & written in note | 20 |
| First value delivered ≤ 7 days | 25 |
| ≥ 2 touchpoints in first 14 days | 15 |
| First positive `sentiment` recorded | 10 |
| Second contact person named in note | 10 |

Score < 50 at day 14 → treat as `health: yellow` regardless of vibes (Recommendation).

## 10. Engagement

- **What keeps customers engaged (Known pattern from [[Globex]]):** QBRs that show *their* numbers against *their* target ("dispatch time down to 1.8h — target hit 🎉"), a champion who feels seen, and follow-ups that arrive when promised (`follow_up` / `follow_up_date` discipline ✅).
- **What becomes annoying:** contact without content — check-ins that only serve *our* need for a `last_contact` refresh. Every message must carry value: a result, an insight, a delivered promise.
- **Milestones worth acknowledging:** target hit (celebrate in writing), anniversary of `since`, their busy-season survival, their referral converting (thank + reward ✅ per Referral Template).
- **Cadence (Recommendation, per customer):**
  - Monthly: short value note (email) — one number, one insight.
  - Quarterly: QBR (meeting) — results vs. target, NPS ask, roadmap.
  - Trigger-based: after any delivery, after any support issue resolution, at renewal minus 60 days.
  - Guardrail (Known ✅): the At Risk view flags 30+ days of silence — the cadence exists so that flag never fires for a healthy account.
- **Engagement signals to watch:** `days_since_contact` trend, sentiment mix, referrals given, inbound question frequency.
- **KPI:** % of active customers with `last_contact` ≤ 30 days (dashboard-computable today ✅); NPS average (already summarized ✅).

## 11. Service journey & recovery

⚠️ No support channel/tooling is recorded; the framework below is a Recommendation sized for a founder-led operation (email + call, no ticket system — touchpoint notes *are* the tickets, with `follow_up` as the SLA tracker).

| Scenario | Customer emotion | Respond within | Channel | Action | Escalate when |
|---|---|---|---|---|---|
| General question | Neutral | Same business day | Email | Answer + log touchpoint | — |
| Confused customer | −1 uncertain | Same day | Call > email | Walk through live; then send written recap | Same confusion twice → fix the docs, not the customer |
| Frustrated | −3 | ≤ 2 h | Call | Listen first, own it, give a dated fix plan | Any hint of "reconsidering" |
| Complaint | −3/−4 | ≤ 2 h | Call | Apologize specifically, fix, follow up in writing; `sentiment: negative` + `health` downgrade (Known rule ✅) | Always visible to owner (owner *is* the escalation today) |
| Billing concern | −2 | Same day | Email + call if unresolved | Fix first, explain second | Disputed charge |
| Service failure | −4 | ≤ 1 h acknowledgment | Call | Acknowledge → fix → post-mortem note → proactive make-good | Always |
| Cancellation / refund request | −5 | ≤ 2 h | Call, always | Understand reason before any counter; run win-back play only if the reason is fixable | Always |

**Service recovery framework:** Acknowledge fast → own it specifically → fix it visibly → follow up in writing → log touchpoint with honest `sentiment` → downgrade `health` if warranted → *make-good proportional to the failure*. A well-recovered failure creates more loyalty than no failure (the service-recovery paradox) — but only once per failure type; repeat failures burn trust permanently.

**CRM mechanics (all exist today ✅):** negative sentiment → health downgrade → At Risk view → weekly review picks it up ("one action each — never just watch").

## 12. Loyalty

- **Trust is generated by (Known pattern):** promises with dates that are kept (`follow_up_date` discipline), numbers over adjectives at QBRs, and remembering context ("the customer never notices the system. They just experience fast responses, remembered context, and thank-yous that arrive on time" — IT brief §6).
- **Emotional attachment:** the founder relationship — they buy from a person. Strength and risk at once (see single-operator leak, §15 L7).
- **Habitual usage:** our service embedded in their weekly operating rhythm; the QBR as a fixture in their calendar.
- **Memorable moments:** target-hit celebrations, busy-season saves, the unprompted "saw this and thought of your dispatch problem" note.
- **Measurable loyalty indicators:** NPS 9–10 sustained across surveys; `referrals_given` > 0 (the ultimate proof — Globex ✅); renewal without negotiation; expansion (Standard → Premium).

## 13. Advocacy & referrals

**The ask timing rule (Known ✅, canvas):** ask **while the win is fresh** — at emotional peaks, never randomly:

1. Immediately after a target-hit QBR (this is exactly how [[Globex → Acme Corp]] happened — Maria offered *at* the Q2 QBR).
2. Right after an NPS 9–10 response.
3. After a visible save/recovery handled well.
4. At renewal — they've just re-chosen us.

**Sequenced asks by moment (Recommendation):** review after first target hit → testimonial/case study after a QBR with numbers worth quoting → referral at NPS 9–10 → never more than one ask per moment.

**Automated referral journey (extends the Known follow-through checklist ✅):**
`nps: 9–10` recorded → next-day prompt to owner: "ask X for a referral" → referral note created (`invited`) → thank referrer ≤ 24h → contact referred lead ≤ 48h, `source: referral`, fast-track SLA → on `converted`: reward sent ≤ 48h (`reward: sent`) + tell the referrer what happened with their introduction — closing this loop is what produces *second* referrals.

**KPI (dashboard-ready today ✅):** referral conversion (`converted`/`invited`); `referrals_given` sum; % of NPS-9–10 customers actually asked. ⚠️ The last one needs an `asked` marker — add a checkbox to the Customer Template.

## 14. Churn & cancellation

**Classification (Assumption, pending lost/churn reason data):**

| Type | Example in vault | Preventable? |
|---|---|---|
| Trust/engagement churn | [[Umbrella Co]]: champion left → usage −60% → silence | **Yes** — with faster champion-change detection |
| Expectation churn | Discovery missed a mismatch | Yes — upstream, in §5 |
| Price churn | Price-vs-hire math flips | Sometimes — value evidence at QBRs |
| Operational churn | Their business changes/shrinks | No — part gracefully, stay referable |
| Competitor churn | Bigger tool bundles us away | Sometimes — switching cost is the relationship |

**Early-warning signals, ranked by weight — the Churn Risk Score 0–100 (computable from frontmatter today):**

| Signal | Points |
|---|---|
| `health: red` | +35 |
| `health: yellow` | +15 |
| Champion departed (note it as a flag) | +25 |
| `days_since_contact` > 30 (Known trigger ✅) | +20 |
| > 60 | +35 |
| Last two touchpoint `sentiment: negative` | +20 |
| `nps` ≤ 6 | +15 |
| Unanswered outreach ×2 | +15 |
| Payment failure | +15 |
| No activation by day 14 (§9) | +20 |

Cap at 100. **Umbrella Co today: red (35) + champion left (25) + 80+ days silence (35) + unanswered ×2 (15) = 100 — immediate save attempt.** The system's current binary At Risk flag said "at risk"; the score says "on fire." That difference is the point.

| Score | Tier | Automated action (Recommendation) |
|---|---|---|
| 0–25 | Normal | Nothing — don't create noise |
| 26–50 | Monitor | Surface in weekly review with the *reason* attached |
| 51–70 | Intervention | Auto-set `next_action`: value-focused check-in ≤ 7 days |
| 71–85 | High risk | Auto-set `health: red` if not already; owner call ≤ 48h |
| 86–100 | Save now | Same-day owner call; executive win-back play (Known ✅ — Umbrella's note already scripts it: onboarding for the replacement champion, then discount escalation) |

## 15. Win-back / reactivation

`churned` is a status, not an ending (Known — the lifecycle keeps the file).

**Journey:** Churn (exit interview, part gracefully) → **Cooling period** → re-engagement → recovery offer → reactivation → loyalty restoration.

- **Cooling period by churn type:** operational churn — 6 months, then "how did the season go?"; expectation churn — 3 months, only if the gap is now fixable; trust churn — 30 days, personal note, no offer attached.
- **Channel:** always personal email or call from the owner. Never automate the *message* — automate the **reminder** to send it (a `next_action_date` on the churned note keeps it in Follow-ups Due ✅ — zero new tooling).
- **Incentive:** lead with what changed ("we now do X, which was why you left"), not discounts. Discounts only for price churn, and only with a changed value story.
- **Do NOT contact when:** they churned angry and the cooling period hasn't passed; the churn reason still exists; they asked not to be.
- **KPI:** reactivation rate; reactivated-customer 12-month retention. ⚠️ Data required.

---

## 16. Emotional journey

```text
Trigger (−2 pain) → Awareness: referral (+3) / cold (−1)
→ Consideration (+1 hopeful) → Price math (−1) → Discovery call done well (+3)
→ Proposal wait (0) → Decision moment (−1 fear of being wrong) → Signed (+2 relief)
→ Post-payment silence risk (−2 ⚠️) → Welcome + kickoff ≤72h (+3)
→ Day 3–5 progress visible (+2) / invisible (−3 ⚠️) → First value (+4)
→ Activation: success metric moves (+5 ★) → Steady service (+3)
→ Service failure (−3) → Well-recovered (+4 paradox) / badly (−5 ⚠️)
→ QBR target hit (+5 ★ referral moment) → Renewal (+3)
→ Champion leaves (−2, silent ⚠️) → Ignored 30+ days (−4) → Churn (−5)
→ Win-back done right (+2) → Reactivation (+3)
```

- **Peaks (★):** activation and the target-hit QBR — *the only two moments to ask for referrals.*
- **Valleys (⚠️):** post-payment silence, invisible day 3–5, botched recovery, silent post-champion decay.
- **Moments of Truth** (disproportionate outcomes): first response speed · discovery call quality · post-payment first hour · first value delivery · first service failure · QBR · champion departure · renewal · cancellation conversation. (Expanded in §21.)

## 17. Touchpoint map

| Category | Touchpoints | Stage coverage | Fragmentation risk |
|---|---|---|---|
| Paid media | Ads, events | Awareness | ⚠️ Spend/results live outside the vault — no CAC by channel |
| Owned digital | Website + pricing page, intake form/API, acknowledgment email (to build) | Awareness → capture | Low — intake lands in `CRM/Leads/` ✅ |
| Human | Founder: calls, discovery, proposals, kickoff, QBRs, service, saves | Everything after capture | ⚠️ **Single point of failure — and the phone has no capture path**: an unlogged call never happened, as far as the system knows |
| Transactional | Proposals, contracts, invoices, receipts | Decision → payment | ⚠️ Entirely outside the vault today (§7) |
| Post-purchase | Welcome, kickoff, progress notes, QBRs, NPS asks, thank-yous, rewards, win-backs | Onboarding → advocacy | Low — touchpoint notes + backlinks give the full story ✅ |

**Rule (Recommendation):** every human touchpoint in any channel becomes a touchpoint note the same day — the vault is only as true as its logging discipline.

## 18. Customer journey database

The vault's four record types already cover most of the master list. Gaps → additions:

| Stage | Captured today (Known ✅) | Add (Recommendation) |
|---|---|---|
| Capture | `source`, `referrer`, `created`, `value`, contact info | `campaign` (which ad/event), auto-captured |
| Qualification | 4 checkboxes, Why now, snapshot | `lost_reason` as a frontmatter field (today it's body text — queryable is better) |
| Sales | `status`, `next_action(_date)`, `last_contact`, `owner` | `proposal_sent` date (enables days-in-proposal metric) |
| Onboarding | `since`, `status: onboarding` | `kickoff_date`, `first_value_date`, `activation_score` |
| Engagement | `health`, `nps`, `last_contact`, `next_review`, touchpoint `sentiment` | `champion` (named — so departure is detectable), `renewal_date` |
| Advocacy | `referrals_given`, referral records with `reward` | `referral_asked` flag |
| Churn | status | `churn_reason`, `churn_date`, `winback_date` |

**By entry mode:** auto-captured — intake fields, dates, computed scores; agent-entered — judgement fields (`health`, qualification, Why now, sentiment); AI-generated — touchpoint drafts from call notes, weekly-review digests, snapshot metrics (the Layer-2 skills exist for exactly this ✅).

## 19. AI & automation opportunities

Ordered by leverage; all follow the vault's ground rules (plain text, PRs, fail loudly).

**A1 — Speed-to-lead (build first)**
Trigger: lead PR opened by `crm-lead-intake.yml` → Condition: `status: new` → Action: acknowledgment email to lead + push notification to owner → Human: personal contact ≤ 1h (referral/website) / ≤ 24h (rest) → CRM: PR auto-labeled by source → KPI: median speed-to-lead.

**A2 — Follow-up enforcement**
Trigger: daily scheduled job → Condition: any lead in `proposal`/`qualified` with empty or past `next_action_date` → Action: Monday-digest line + *empty-date* alert (the dashboard's blind spot) → Human: owner sets/does the action → KPI: % pipeline records with a future `next_action_date`.

**A3 — Churn Risk Score (§14) as a Bases formula + digest**
Trigger: weekly → Condition: score ≥ 51 → Action: digest entry with reasons; ≥ 86 auto-sets `next_action: save call today` → Human: owner calls → KPI: at-risk→recovered rate.

**A4 — Referral moment detection**
Trigger: `nps` edited to 9–10, or QBR touchpoint with `sentiment: positive` → Action: prompt owner + pre-create referral note draft → Human: the actual ask (never automate the ask itself) → KPI: % peak moments converted to asks.

**A5 — Onboarding cadence**
Trigger: customer note created with `status: onboarding` → Action: schedule the §8 day-0/3/6 automated messages; flag if no kickoff touchpoint by day 3 → Human: kickoff, day-4 delivery, day-7 review → KPI: 14-day activation rate.

**A6 — Touchpoint capture assist**
Trigger: owner pastes raw call notes to the AI agent → Action: correctly-formatted touchpoint note + mirrored `next_action`/`follow_up` fields (skills already guarantee format ✅) → KPI: touchpoints logged per week (proxy for system truthfulness).

**A7 — Monthly metrics snapshot** (already roadmapped, IT brief §4.4)
Trigger: monthly cron → Action: append pipeline value by source, NPS avg, referral conversion, speed-to-lead, churn count to a `Metrics History` note → KPI: this *is* the KPI infrastructure — everything marked "⚠️ data required" in this document gets its baseline here.

**Human vs. machine boundary:** automation handles *remembering, formatting, computing, and nudging*; humans handle *every conversation that involves judgement, money, or emotion* — discovery, closes, kickoffs, QBRs, saves, win-backs, and the referral ask.

## 20. Friction & leak analysis

| # | Leak | Type | Problem → Cause → Impact | Detection | Fix | Rank |
|---|---|---|---|---|---|---|
| L1 | Silent intake | 📞 Lead | New-lead PR waits until owner polls GitHub → slow first contact → dead hot leads | Speed-to-lead metric | A1 | **CRITICAL** |
| L2 | Empty `next_action_date` | 💰 Revenue | Follow-ups Due can't show a date that isn't set → proposals rot invisibly | A2's empty-date scan | A2 + template default | **CRITICAL** |
| L3 | Unlogged interactions | 🧠 Information | Calls/chats outside email leave no touchpoint → `last_contact` lies → At Risk fires late (or never) | Touchpoints/week trend | A6 + same-day rule | **HIGH** |
| L4 | Champion departure undetected | 🔄 Retention | No `champion` field → the Umbrella pattern repeats | Churn score signal | §18 field + A3 | **HIGH** |
| L5 | No metrics history | 📊 Data | Point-in-time dashboard only → improvement loop can't be judged by numbers | — (it's absence) | A7 | **HIGH** |
| L6 | Referral loop half-closed | 💰 Revenue | Reward `pending` + referrer never told the outcome → no second referral (Globex's reward is pending now ✅ observable) | Referrals view | §13 loop + A4 | **MEDIUM** |
| L7 | Single operator | ⚙️ Operational | Everything human routes through one person → vacation = journey stops | — | Document playbooks (started ✅); A5/A1 reduce human load | **MEDIUM** |
| L8 | Transaction blind spot | 🤝 Trust | Payments/contracts un-tracked in vault → declined card or unsigned contract surfaces late | §7 journeys | Log transaction events as touchpoints | **MEDIUM** |

## 21. Moments of truth (top 10)

| # | Moment | Customer expects | Emotion | What goes wrong | Right response | Automation | KPI |
|---|---|---|---|---|---|---|---|
| 1 | First response after inquiry | Hours, not days | +1 hopeful | Silence → they call a competitor | ≤1h hot / ≤24h all (A1) | Ack ≤30s | Speed-to-lead |
| 2 | Discovery call | Being understood | +3 if real | Feature pitch instead of listening | §5 question order | Prep from note | Qualification rate |
| 3 | Proposal follow-through | A next step with a date | 0 waiting | Proposal hangs | 14-day expiry + d3/d10 touches | A2 | Days in proposal |
| 4 | First hour after payment | Reassurance | −2→+3 swing | Silence = instant remorse | §8 minute-0 + hour-1 | Welcome auto | Welcome ≤24h rate |
| 5 | First value delivery | Proof inside week 1 | +4 | "Still setting up" past day 5 | Day-4 delivery target | A5 flags | 14-day activation |
| 6 | First service failure | Fast, honest ownership | −4→+4 or −5 | Defensiveness, slowness | §11 recovery framework | Sentiment→health ✅ | Post-issue sentiment |
| 7 | QBR | Their numbers vs their target | +5 peak | Generic status meeting | Success-metric-anchored QBR | A4 catches the peak | NPS |
| 8 | Champion departs | We notice and re-onboard | −2 silent | Nobody notices (Umbrella ✅) | Re-onboard replacement ≤ 2 weeks | A3 signal | Save rate |
| 9 | Renewal | Re-earned, not assumed | +3 or −2 | Auto-renew surprise or lapse | Renewal-minus-60 value review | `renewal_date` trigger | Renewal rate |
| 10 | Cancellation conversation | Being heard | −5 | Retention script before listening | Reason first, then §14/§15 | Never automated | Save rate, exit NPS |

## 22. Top failures & delight opportunities

**Most likely failures (probability × revenue × experience):**
1. Hot lead contacted late (L1) — fix A1.
2. Proposal rots with no date (L2) — fix A2.
3. Post-payment silence remorse — fix §8 minute-0/hour-1.
4. Umbrella-pattern silent churn (L4) — fix champion field + A3.
5. Referral peak missed / loop unclosed (L6) — fix A4 + §13.
6. Discovery skipped under time pressure → expectation churn — fix: qualification gates are non-negotiable.
7. Unlogged interactions corrupt every downstream signal (L3).
8. Owner overload degrades everything at once (L7).
9. First failure handled defensively — fix §11.
10. Metrics never baselined, so none of this is ever judged (L5) — fix A7.

**Delight opportunities (high perceived value, low cost, referral potential):**
1. Reply to inquiries in minutes with something human.
2. Attach the 30-day plan to every proposal.
3. Personal owner note in the first hour after payment.
4. Celebrate the first metric movement the moment it happens — screenshot, one line, sent same day.
5. Tell referrers what their introduction turned into (close the story).
6. Send the reward *fast* (48h) — Globex's is pending right now.
7. "Saw this, thought of your dispatch problem" notes — 2 minutes, remembered for a year.
8. Anniversary thank-you with their year-in-numbers.
9. After a failure: a make-good they didn't ask for.
10. Pre-busy-season readiness check for every customer with a seasonal Why-now.

## 23. Prioritization & 48-hour experiments

**🔴 Fix immediately (0–48h)** — behavior changes, zero build:
proposal expiry + mandatory `next_action_date` (L2) · minute-0/hour-1 welcome as a manual checklist (§8) · send Globex's referral reward + close the loop (L6) · add `champion`/`renewal_date`/`lost_reason` fields to templates (§18).

**🟠 Build next (7–30d):** A1 speed-to-lead · A2 follow-up enforcement · Onboarding Bases view · A7 metrics snapshot (kills most ⚠️ flags).
**🟡 Optimize (30–90d):** A3 churn score · A4 referral detection · A5 onboarding cadence · §11 recovery playbook note.
**🟢 Strategic (90d+):** A6 AI touchpoint capture at scale · transaction-event integration (§7) · second-operator playbooks (L7).

**48-hour experiments** (each: hypothesis → change → metric → decision rule):

1. **1-hour response** on next 10 inbound leads → contact rate vs. memory-baseline → if ↑, build A1 now.
2. **Proposal expiry date** on next 5 proposals → days-in-proposal → keep if < current feel-baseline.
3. **Hour-1 personal welcome** for next 3 customers → day-7 sentiment → keep if all ≥ neutral.
4. **30-day plan attachment** on next 5 proposals → close rate + questions asked → keep if objections drop.
5. **Referral ask at next positive QBR** (scripted, in-moment) → ask→invite rate → formalize as A4 if ≥ 1 invite.
6. **Empty-`next_action_date` manual scan** Monday + Thursday → count found → if > 0 twice, A2 is justified.
7. **Same-day touchpoint logging** for one week → touchpoints/week vs. calendar reality → gap size justifies A6.
8. **Win-back message to Umbrella Co** per its own play (already scripted in the note ✅) → reply/no-reply → escalate to discount step per the note.
9. **"Why now?" asked on every new lead** this week → field fill rate → make it a qualification gate if insight quality is high.
10. **NPS ask at every touchpoint ≥ meeting-length** for two weeks → response rate → set the standing survey cadence from it.

## 24. Current state → future state

| Dimension | Current (Known) | Future |
|---|---|---|
| Intake | Automated to PR, then silent | Manual → **Automated**: ack ≤30s, owner pushed, contact ≤1h |
| Follow-up | Dashboard shows dated actions when opened | Reactive → **Proactive**: digests push; empty dates impossible |
| Churn | Binary At Risk flag, weekly glance | **Predictive**: scored, reasoned, tiered response |
| Referrals | Checklist after someone remembers | **Triggered** at detected emotional peaks |
| Metrics | Point-in-time views | **Measured**: monthly history, trend-judged improvement loop |
| Knowledge | Owner's head + growing playbooks | **Integrated**: every interaction a file, every playbook a note |
| Journey ownership | Department-of-one | **Customer-centric system** any operator (or AI agent) can run |

---

## Executive summary

**The 3 biggest problems**
1. **Speed-to-lead is unmanaged** — intake automation delivers a PR, then nothing pushes; hot leads cool in a queue nobody is watching (L1).
2. **The dashboard can't see what was never scheduled** — an empty `next_action_date` makes a rotting proposal invisible; the exact failure the system exists to prevent (L2).
3. **Churn detection fires too late and too bluntly** — Umbrella Co scored 100/100 on the churn model in §14 while the binary flag just said "at risk"; champion departure, the strongest signal, isn't even a field (L4).

**The 3 biggest opportunities**
1. **Close the referral loop completely** — thank fast, convert fast, reward fast, *report back* — the flywheel is the stated strategy and its motion is currently unmeasured.
2. **Own the first 7 days** — the §8 cadence turns the highest-remorse window into the highest-trust window, at near-zero cost.
3. **Baseline the numbers** (A7) — every "⚠️ data required" in this document resolves with one monthly snapshot job, and the improvement loop finally gets a scoreboard.

**The 3 automations to build first:** A1 speed-to-lead → A2 follow-up enforcement → A7 metrics snapshot.

**The 3 moments we must protect:** first response to a new lead · the first hour after payment · the target-hit QBR (the referral moment).

**The single most important KPI right now: median speed-to-lead** (lead `created` → first touchpoint). It is measurable today from existing frontmatter, it gates every downstream conversion, it is the strongest trust signal a small firm can send, and it is currently unknown. When it is consistently under one hour, move the spotlight to 14-day activation rate.

---

*Maintained like everything else here: notice friction → edit this note → PR. Questions this map doesn't answer are bugs in this map.*
