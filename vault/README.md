# Vault starter content

Drop-in content for your Obsidian vault, built with the vendored Agent Skills
(`obsidian-markdown`, `obsidian-bases`, `json-canvas`).

## CRM — leads, customers & referrals

Copy the `CRM/` folder to the root of your vault. It contains:

| Path | What it is |
|------|------------|
| `CRM/CRM Home.md` | Hub note: journey map (Mermaid), data model, embedded dashboard views, weekly improvement ritual |
| `CRM/Customer Experience Flow.canvas` | Visual journey: Attract → Convert → Deliver → Delight & Refer, plus the continuous-improvement loop |
| `CRM/Dashboards/CRM Dashboard.base` | Six live views: Lead Pipeline, Follow-ups Due, Customers, At Risk, Referrals, Recent Touchpoints |
| `CRM/Templates/*.md` | Note templates for Lead, Customer, Referral, Touchpoint records |
| `CRM/Leads/`, `CRM/Customers/`, `CRM/Referrals/`, `CRM/Touchpoints/` | Example records so everything renders with data — replace with your own |

Requires Obsidian 1.9+ (the version that introduced Bases). Point Obsidian's core Templates plugin at
`CRM/Templates` to create records quickly.

The file node in the canvas references `CRM/CRM Home.md`, so keep the folder
named `CRM` at the vault root (or update that node's `file` path).

### Adding leads without typing (intake automation)

Three ways to create a lead record; each opens a pull request with a
correctly-formatted file in `CRM/Leads/` — nothing writes to `master` directly:

1. **Issue form** — open a "📥 New lead" issue (Issues → New issue). Works from
   a phone. The workflow builds the record, opens the PR, and closes the issue.
2. **Manual run** — Actions → "CRM lead intake" → Run workflow, fill the fields.
3. **API** — POST a `repository_dispatch` event (for a website form backend):

   ```bash
   curl -X POST \
     -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/repos/<owner>/<repo>/dispatches \
     -d '{"event_type":"new-lead","client_payload":{"company":"Acme Corp","email":"jane@acme.com","source":"website","value":"12000"}}'
   ```

Duplicate company names and malformed dates are rejected loudly (a comment on
the intake issue tells you why). See `.github/workflows/crm-lead-intake.yml`.
