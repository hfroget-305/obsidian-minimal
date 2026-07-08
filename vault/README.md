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
