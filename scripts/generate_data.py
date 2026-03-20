#!/usr/bin/env python3
"""Synthetic data generator for the RAG-RBAC chatbot. stdlib only."""
from __future__ import annotations
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
random.seed(SEED)

BASE = Path(__file__).parent.parent / "data" / "raw"

FIRST = ["Alex","Jordan","Taylor","Morgan","Casey","Riley","Drew","Avery","Quinn","Blake",
         "Reese","Logan","Parker","Hayden","Cameron","Skyler","Dakota","Rowan","Emery","Sage"]
LAST  = ["Chen","Rodriguez","Kim","Patel","Thompson","Williams","Johnson","Garcia","Martinez",
         "Davis","Wilson","Anderson","Taylor","Thomas","Jackson","White","Harris","Martin","Lewis","Clark"]

def name(): return f"{random.choice(FIRST)} {random.choice(LAST)}"
def isodate(days_ago_min=30, days_ago_max=1200):
    return (date.today() - timedelta(days=random.randint(days_ago_min, days_ago_max))).isoformat()
def frontmatter(doc_id, title, dept, access_roles, classification, doc_type):
    roles_str = ", ".join(f'"{r}"' for r in access_roles)
    return f"""---
doc_id: "{doc_id}"
title: "{title}"
department: "{dept}"
access_roles: [{roles_str}]
classification: "{classification}"
doc_type: "{doc_type}"
created_date: "{isodate(1, 90)}"
---

"""

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  [ok] {path.relative_to(BASE.parent.parent)}")

# ── FINANCE ────────────────────────────────────────────────────────────────────

def fin_q1_report():
    rev = 4.2; exp = 3.1; net = round(rev - exp, 1)
    prev_rev = round(rev * 0.88, 1); prev_net = round(prev_rev - 2.9, 1)
    content = frontmatter("fin_001","Q1 2024 Financial Report","finance",["finance","clevel"],"confidential","report")
    content += f"""# Q1 2024 Financial Report

## Executive Summary

Total revenue for Q1 2024 reached **${rev}M**, representing a **{round((rev-prev_rev)/prev_rev*100,1)}% increase** year-over-year (Q1 2023: ${prev_rev}M). Net income of **${net}M** reflects disciplined cost management despite increased headcount and infrastructure investments.

## Revenue Breakdown

| Revenue Stream | Q1 2024 | Q1 2023 | YoY Change |
|---|---|---|---|
| Subscription (SaaS) | $2.8M | $2.3M | +21.7% |
| Professional Services | $0.9M | $0.7M | +28.6% |
| Licensing | $0.5M | $0.4M | +25.0% |
| **Total** | **${rev}M** | **${prev_rev}M** | **+{round((rev-prev_rev)/prev_rev*100,1)}%** |

## Operating Expenses

| Category | Q1 2024 | % of Revenue |
|---|---|---|
| Salaries & Benefits | $1.8M | 42.9% |
| Marketing & Sales | $0.6M | 14.3% |
| Infrastructure & Cloud | $0.4M | 9.5% |
| G&A | $0.3M | 7.1% |
| **Total OpEx** | **${exp}M** | **73.8%** |

## EBITDA

- **Gross Profit**: $3.6M (85.7% margin)
- **EBITDA**: $1.3M (31.0% margin)
- **Net Income**: ${net}M (26.2% margin)
- vs Q1 2023 Net Income: ${prev_net}M — improvement of ${round(net-prev_net,1)}M

## Departmental Cost Allocation

| Department | Budget | Actual | Variance |
|---|---|---|---|
| Engineering | $820K | $798K | +$22K |
| Marketing | $610K | $627K | -$17K |
| HR & Operations | $340K | $328K | +$12K |
| Finance & Legal | $230K | $241K | -$11K |

## Key Financial Metrics

- **Cash Position**: $8.4M (up from $7.2M Q4 2023)
- **Accounts Receivable**: $1.1M (DSO: 32 days)
- **Monthly Burn Rate**: $1.03M
- **Runway**: 18+ months at current burn

## Q2 2024 Outlook

Revenue guidance of $4.5M–$4.8M based on current pipeline. Marketing expansion planned for Q2 may increase OpEx by 8–10%.
"""
    write(BASE / "finance" / "q1_financial_report_2024.md", content)

def fin_marketing_expenses():
    content = frontmatter("fin_002","Marketing Expense Breakdown Q1 2024","finance",["finance","clevel"],"confidential","report")
    content += """# Marketing Expense Breakdown — Q1 2024

## Total Marketing Spend: $627,000

### Paid Digital Advertising

| Channel | Budget | Actual Spend | Impressions | CPC | Conversions |
|---|---|---|---|---|---|
| Google Ads (Search) | $120,000 | $118,400 | 1,240,000 | $2.14 | 890 |
| LinkedIn Ads | $45,000 | $47,200 | 380,000 | $8.60 | 142 |
| Meta (Facebook/Instagram) | $35,000 | $33,800 | 920,000 | $1.22 | 310 |
| Programmatic Display | $20,000 | $19,100 | 5,400,000 | $0.23 | 48 |
| **Subtotal Digital** | **$220,000** | **$218,500** | **7,940,000** | — | **1,390** |

### Events & Sponsorships

| Event | Cost | Leads Generated | Cost per Lead |
|---|---|---|---|
| TechCrunch Disrupt Sponsorship | $45,000 | 87 | $517 |
| SaaStr Annual Booth | $28,000 | 63 | $444 |
| Webinar Series (6 sessions) | $12,000 | 214 | $56 |
| Industry Roundtables | $8,000 | 41 | $195 |
| **Subtotal Events** | **$93,000** | **405** | **$230** |

### Content & Creative

| Item | Spend |
|---|---|
| Content production (blog, whitepapers) | $42,000 |
| Video production (3 case studies) | $38,000 |
| Design & brand assets | $18,000 |
| SEO & technical content | $15,000 |
| **Subtotal Content** | **$113,000** |

### Tools & Technology

| Tool | Annual Cost | Q1 Allocation |
|---|---|---|
| HubSpot Marketing Hub | $48,000/yr | $12,000 |
| Salesforce CRM | $36,000/yr | $9,000 |
| Semrush | $14,400/yr | $3,600 |
| Other MarTech | $22,000/yr | $5,500 |
| **Subtotal Tools** | — | **$30,100** |

### Headcount (Marketing Team — 7 FTEs)

- Total fully loaded cost: $172,400 (Q1)
- Includes 2 new hires onboarded February 1

## ROI Summary

- Total pipeline generated from marketing: $3.2M
- Marketing-sourced closed revenue Q1: $840K
- **Marketing ROI: 134%** (revenue / spend)
- Blended Customer Acquisition Cost: $451
"""
    write(BASE / "finance" / "marketing_expense_breakdown.md", content)

def fin_capex():
    content = frontmatter("fin_003","Equipment CapEx Schedule 2024","finance",["finance","clevel"],"confidential","report")
    content += """# Equipment Capital Expenditure Schedule — 2024

## Approved CapEx Budget: $485,000

### IT Infrastructure

| Asset | Qty | Unit Cost | Total | Useful Life | Annual Depreciation |
|---|---|---|---|---|---|
| Dell PowerEdge R750 Servers | 4 | $18,500 | $74,000 | 5 years | $14,800 |
| NetApp Storage Array (200TB) | 1 | $62,000 | $62,000 | 7 years | $8,857 |
| Cisco Network Switches | 6 | $4,200 | $25,200 | 7 years | $3,600 |
| UPS Battery Backup Systems | 2 | $8,400 | $16,800 | 5 years | $3,360 |
| **Subtotal Infrastructure** | — | — | **$178,000** | — | **$30,617** |

### End-User Computing

| Asset | Qty | Unit Cost | Total | Useful Life | Annual Depreciation |
|---|---|---|---|---|---|
| MacBook Pro 14" (M3 Pro) | 35 | $2,400 | $84,000 | 3 years | $28,000 |
| Dell XPS 15 Laptops | 12 | $1,800 | $21,600 | 3 years | $7,200 |
| External Monitors (27") | 50 | $420 | $21,000 | 5 years | $4,200 |
| Peripherals & Accessories | — | — | $14,000 | 3 years | $4,667 |
| **Subtotal End-User** | — | — | **$140,600** | — | **$44,067** |

### Office Furniture & Fit-Out

| Item | Cost | Useful Life |
|---|---|---|
| Ergonomic workstations (20 units) | $48,000 | 7 years |
| Conference room AV (2 rooms) | $32,000 | 5 years |
| Reception & common area | $22,000 | 7 years |
| Signage & branding | $8,400 | 10 years |
| **Subtotal Office** | **$110,400** | — |

### Q1 2024 Actual Spend vs Budget

| Category | Budget | Q1 Actual | Remaining |
|---|---|---|---|
| IT Infrastructure | $178,000 | $162,000 | $16,000 |
| End-User Computing | $140,600 | $98,400 | $42,200 |
| Office Fit-Out | $110,400 | $110,400 | $0 |
| **Total** | **$429,000** | **$370,800** | **$58,200** |

*Remaining $56,000 of approved budget reserved for H2 planned purchases.*

## Depreciation Schedule Summary

- **Total 2024 Annual Depreciation**: $128,450
- **Net Book Value of All Assets (end Q1)**: $892,300
- Depreciation method: Straight-line
"""
    write(BASE / "finance" / "equipment_capex_schedule.md", content)

def fin_reimbursement():
    content = frontmatter("fin_004","Employee Reimbursement Policy","finance",["finance","clevel","hr","general"],"internal","policy")
    content += """# Employee Reimbursement Policy

**Effective Date:** January 1, 2024 | **Owner:** Finance Department

## Overview

This policy governs reimbursement of business expenses incurred by employees. All expenses must be (1) business-related, (2) reasonable, and (3) submitted within 30 days of incurring them.

## Expense Categories & Limits

### Travel

| Expense | Limit | Notes |
|---|---|---|
| Domestic flights | Actual (economy) | Book 14+ days in advance |
| International flights | Actual (economy) | Requires VP approval |
| Hotel | $250/night domestic | $350/night international |
| Rental car | $75/day | Mid-size or smaller |
| Ride-share/taxi | Actual | Receipt required >$25 |
| Personal vehicle mileage | $0.67/mile (IRS rate) | Log required |
| Parking | $40/day | Airport long-term only |

### Meals & Entertainment

| Situation | Limit | Approval Required |
|---|---|---|
| Individual meal (travel) | $75/day | No |
| Team lunch (≤5 people) | $30/person | Manager approval |
| Client entertainment | $150/person | Director approval |
| Team dinner/celebration | $60/person | VP approval |

### Equipment & Supplies

- Home office equipment (one-time): up to $500 — requires IT approval
- Professional books/subscriptions: up to $200/year — no approval needed
- Training materials: up to $500 — manager approval required

### Professional Development

- Conferences & seminars: up to $2,000/year — manager + HR approval
- Online courses/certifications: up to $1,500/year — manager approval
- Professional memberships: up to $400/year — manager approval

## Approval Thresholds

| Amount | Approver |
|---|---|
| Up to $200 | Direct manager |
| $201 – $1,000 | Department director |
| $1,001 – $5,000 | VP of Finance |
| Over $5,000 | CFO |

## Submission Process

1. Submit via Expensify within 30 days of expense
2. Attach receipt for any item over $25
3. Include business purpose in description field
4. Select correct cost centre/project code
5. Expenses approved within 5 business days
6. Reimbursed in next payroll cycle

## Non-Reimbursable Items

- Alcohol (except pre-approved client entertainment)
- Personal travel extensions
- Traffic fines or parking tickets
- Personal care items
- Lost or stolen items

Questions: finance-team@company.com
"""
    write(BASE / "finance" / "reimbursement_policy.md", content)

# ── MARKETING ─────────────────────────────────────────────────────────────────

def mkt_campaign():
    content = frontmatter("mkt_001","Q1 2024 Campaign Performance Report","marketing",["marketing","clevel"],"internal","report")
    content += """# Q1 2024 Campaign Performance Report

## Summary

Q1 2024 saw strong performance across paid and organic channels. Total marketing-qualified leads (MQLs): **1,847**. Pipeline generated: **$3.2M**.

## Campaign Results

### Campaign 1: "Scale Without Limits" (SaaS Brand Awareness)

| Metric | Value |
|---|---|
| Platform | Google Display + YouTube |
| Budget | $48,000 |
| Impressions | 2,340,000 |
| Click-through Rate | 2.8% |
| Clicks | 65,520 |
| Landing Page Conversions | 4.2% |
| MQLs Generated | 312 |
| Cost per MQL | $154 |
| Pipeline Attributed | $620,000 |

### Campaign 2: "Enterprise Security Spotlight" (ABM)

| Metric | Value |
|---|---|
| Platform | LinkedIn + Direct Outreach |
| Target Accounts | 85 |
| Budget | $62,000 |
| Account Reach | 78/85 (91.8%) |
| MQLs Generated | 94 |
| Cost per MQL | $660 |
| Pipeline Attributed | $890,000 |
| Avg Deal Size | $94,700 |

### Campaign 3: "ROI Calculator" (Mid-Funnel)

| Metric | Value |
|---|---|
| Platform | Google Search + Retargeting |
| Budget | $35,000 |
| Impressions | 480,000 |
| CTR | 6.2% |
| Conversions (tool usage) | 1,840 |
| MQLs from tool | 267 |
| Cost per MQL | $131 |

### Campaign 4: "Customer Stories" (Case Study Series)

| Metric | Value |
|---|---|
| Channels | Email, LinkedIn, Blog |
| Budget | $28,000 |
| Email Open Rate | 34.2% |
| Click Rate | 8.7% |
| MQLs Generated | 189 |

### Campaign 5: Webinar Series — "AI in the Enterprise" (6 sessions)

| Metric | Value |
|---|---|
| Total Registrants | 3,840 |
| Avg Attendance Rate | 48% |
| Live Attendees (total) | 1,843 |
| MQLs Generated | 441 |
| Cost per MQL | $27 |

### Campaign 6: SaaStr Annual Conference

| Metric | Value |
|---|---|
| Budget | $73,000 |
| Booth Visitors | 420 |
| Business Cards / Badge Scans | 387 |
| MQLs Generated | 63 |
| Cost per MQL | $1,159 |
| Pipeline Attributed | $410,000 |

## Aggregate Q1 Metrics

| Metric | Q1 2024 | Q1 2023 | Change |
|---|---|---|---|
| Total MQLs | 1,847 | 1,340 | +37.8% |
| Blended CPL | $451 | $520 | -13.3% |
| Pipeline Generated | $3.2M | $2.4M | +33.3% |
| MQL → SQL Rate | 38% | 31% | +7pp |
| SQL → Close Rate | 34% | 29% | +5pp |

## Top Performing Channels by MQL Volume

1. Webinars: 441 MQLs (24%)
2. Brand Awareness (Google/YT): 312 MQLs (17%)
3. ROI Calculator: 267 MQLs (14%)
4. Customer Stories: 189 MQLs (10%)
5. ABM: 94 MQLs (5%)
"""
    write(BASE / "marketing" / "q1_campaign_performance.md", content)

def mkt_feedback():
    content = frontmatter("mkt_002","Customer Feedback Analysis Q1 2024","marketing",["marketing","clevel"],"internal","report")
    content += """# Customer Feedback Analysis — Q1 2024

## NPS Score: 72 (Excellent)

Surveyed 840 customers (response rate: 34%). NPS improved from 67 in Q4 2023.

| Category | % of Respondents |
|---|---|
| Promoters (9–10) | 78% |
| Passives (7–8) | 16% |
| Detractors (0–6) | 6% |

## Sentiment Analysis by Theme

| Theme | Positive | Neutral | Negative | Net Sentiment |
|---|---|---|---|---|
| Product reliability | 84% | 12% | 4% | +80% |
| Customer support | 71% | 18% | 11% | +60% |
| Onboarding experience | 68% | 20% | 12% | +56% |
| Pricing & value | 61% | 24% | 15% | +46% |
| Feature completeness | 58% | 28% | 14% | +44% |
| Documentation | 52% | 30% | 18% | +34% |

## Top Praise Themes

1. **Reliability & Uptime** (mentioned by 67% of promoters) — "Has never gone down during a critical period"
2. **Integration ecosystem** (54%) — "Connects seamlessly with our existing stack"
3. **Support responsiveness** (48%) — "Support team responds within the hour, always helpful"
4. **ROI clarity** (41%) — "We can directly attribute $2M in cost savings to the platform"

## Top Pain Points

1. **Reporting limitations** (mentioned by 43% of detractors) — "Dashboards are not customisable enough"
2. **Mobile app** (38%) — "Mobile experience feels like an afterthought"
3. **Onboarding duration** (35%) — "Took 6 weeks to fully onboard our team, expected 2"
4. **API rate limits** (28%) — "Rate limits constrain our automation workflows"

## Verbatim Quotes by Segment

### Enterprise (>500 seats)
> "The platform has transformed how our operations team handles cross-departmental workflows. The RBAC features are particularly valuable — each department only sees what they need." — VP Operations, Manufacturing Co.

### Mid-Market (50–500 seats)
> "Support is phenomenal. Every ticket gets a same-day response and the team actually understands our technical environment." — CTO, FinTech Startup

### SMB (<50 seats)
> "Pricing feels high for our team size, but the ROI justifies it. We cut our reporting time by 70%." — Operations Manager, E-commerce

## Customer Health Scores (Gainsight)

| Segment | Avg Health | At-Risk Accounts | Champion Accounts |
|---|---|---|---|
| Enterprise | 84/100 | 3 | 22 |
| Mid-Market | 76/100 | 12 | 48 |
| SMB | 68/100 | 31 | 89 |

## Action Items for Q2

- [ ] Launch custom reporting beta (addresses #1 pain point)
- [ ] Release mobile app v2.0 redesign (Q2 target)
- [ ] Reduce onboarding time to 3 weeks with new success playbook
- [ ] API rate limit increase for enterprise tier
"""
    write(BASE / "marketing" / "customer_feedback_analysis.md", content)

def mkt_sales():
    content = frontmatter("mkt_003","Sales Metrics Dashboard Q1 2024","marketing",["marketing","clevel"],"confidential","report")
    content += """# Sales Metrics Dashboard — Q1 2024

## Key Metrics at a Glance

| Metric | Q1 2024 | Q1 2023 | Target | Status |
|---|---|---|---|---|
| ARR | $16.8M | $13.4M | $17.0M | 🟡 Near |
| MRR | $1.4M | $1.12M | $1.42M | 🟡 Near |
| New ARR | $2.1M | $1.6M | $2.0M | 🟢 Beat |
| Churned ARR | $280K | $240K | <$300K | 🟢 On Track |
| Net Revenue Retention | 118% | 112% | 115% | 🟢 Beat |
| Churn Rate | 2.1% | 2.2% | <2.5% | 🟢 On Track |
| Win Rate | 34% | 29% | 32% | 🟢 Beat |

## Pipeline by Stage

| Stage | # Deals | Pipeline Value | Avg Deal Size | Avg Age |
|---|---|---|---|---|
| Prospecting | 184 | $4.2M | $22,800 | 8 days |
| Discovery | 96 | $5.8M | $60,400 | 18 days |
| Demo Completed | 54 | $6.1M | $113,000 | 31 days |
| Proposal Sent | 28 | $4.8M | $171,400 | 47 days |
| Negotiation | 12 | $3.2M | $266,700 | 68 days |
| **Total Active** | **374** | **$24.1M** | **$64,400** | — |

## Closed Deals Q1 2024

- **Closed-Won**: 47 deals — $2.1M new ARR
- **Closed-Lost**: 92 deals — $3.8M lost pipeline
- **Win Rate**: 34% (by count), 36% (by value)

## Top 5 Deals Closed Q1

| Account | ARR | Segment | Primary Use Case |
|---|---|---|---|
| Meridian Financial Group | $420K | Enterprise | Compliance automation |
| NovaTech Industries | $280K | Enterprise | Ops workflow |
| Cascade Health Systems | $195K | Mid-Market | Data governance |
| Brightwater Logistics | $168K | Mid-Market | Supply chain analytics |
| Apex Consulting | $112K | Mid-Market | Client reporting |

## Sales Velocity

- **Average Sales Cycle**: 67 days (down from 82 days Q1 2023)
- **Average Contract Value**: $44,700
- **Lead Response Time**: 4.2 hours (target: <6 hours)
- **Quota Attainment**: 94% of reps at or above 80% quota

## Expansion Revenue

- Upsell revenue Q1: $840K
- Cross-sell revenue Q1: $320K
- **Net Expansion ARR**: $1.16M (55% of new ARR)

## Churn Analysis

| Reason | # Accounts | ARR Lost |
|---|---|---|
| Went with competitor | 4 | $128K |
| Budget cut / bankruptcy | 3 | $82K |
| Product gaps | 2 | $48K |
| Acquisition (merged) | 1 | $22K |
| **Total** | **10** | **$280K** |
"""
    write(BASE / "marketing" / "sales_metrics_dashboard.md", content)

# ── HR ─────────────────────────────────────────────────────────────────────────

def hr_directory():
    depts = ["Engineering","Marketing","Finance","HR","Operations","Product"]
    titles = {
        "Engineering": ["Software Engineer","Senior Software Engineer","Staff Engineer","Engineering Manager"],
        "Marketing": ["Marketing Analyst","Senior Marketing Manager","Content Strategist","Growth Manager"],
        "Finance": ["Financial Analyst","Senior Accountant","Finance Manager","Controller"],
        "HR": ["HR Coordinator","HR Business Partner","Recruiter","HR Manager"],
        "Operations": ["Operations Analyst","Operations Manager","Project Manager","COO"],
        "Product": ["Product Manager","Senior Product Manager","UX Designer","VP Product"],
    }
    bands = ["L3","L3","L4","L4","L5","L5","L6"]
    random.seed(SEED)
    employees = []
    managers = {}
    for i in range(1, 31):
        dept = random.choice(depts)
        title = random.choice(titles[dept])
        band = random.choice(bands)
        emp = {
            "id": f"EMP-{i:04d}",
            "name": name(),
            "dept": dept,
            "title": title,
            "band": band,
            "start": isodate(90, 1500),
        }
        employees.append(emp)
        if "Manager" in title or "Director" in title or title.startswith("VP") or title.startswith("COO"):
            managers[dept] = emp["id"]

    rows = "\n".join(
        f"| {e['id']} | {e['name']} | {e['dept']} | {e['title']} | {e['band']} | {e['start']} | {managers.get(e['dept'], 'EMP-0005')} |"
        for e in employees
    )
    content = frontmatter("hr_001","Employee Directory","hr",["hr","clevel"],"restricted","directory")
    content += f"""# Employee Directory — As of {date.today().isoformat()}

**Total Headcount:** 30 active employees across 6 departments

## All Employees

| Emp ID | Name | Department | Title | Band | Start Date | Manager ID |
|---|---|---|---|---|---|---|
{rows}

## Department Headcount Summary

| Department | Headcount | Avg Tenure (months) |
|---|---|---|
| Engineering | 10 | 18.4 |
| Marketing | 5 | 14.2 |
| Finance | 4 | 22.1 |
| HR | 3 | 16.8 |
| Operations | 4 | 24.3 |
| Product | 4 | 11.7 |

## Band Distribution

| Band | Count | Salary Range |
|---|---|---|
| L3 | 12 | $75,000 – $95,000 |
| L4 | 10 | $95,000 – $125,000 |
| L5 | 6 | $125,000 – $165,000 |
| L6 | 2 | $165,000 – $220,000 |

*Salary ranges are base compensation only. Does not include equity or bonuses.*
"""
    write(BASE / "hr" / "employee_directory.md", content)

def hr_attendance():
    content = frontmatter("hr_002","Attendance Report Q1 2024","hr",["hr","clevel"],"confidential","report")
    content += """# Attendance Report — Q1 2024

## Overall Attendance Rate: 94.2%

Working days in Q1 2024: 63 | Total employee-days: 1,890 | Days absent: 110

## Attendance by Department

| Department | Headcount | Expected Days | Days Present | Attendance Rate |
|---|---|---|---|---|
| Engineering | 10 | 630 | 601 | 95.4% |
| Marketing | 5 | 315 | 298 | 94.6% |
| Finance | 4 | 252 | 239 | 94.8% |
| HR | 3 | 189 | 176 | 93.1% |
| Operations | 4 | 252 | 234 | 92.9% |
| Product | 4 | 252 | 242 | 96.0% |

## Leave Type Breakdown

| Leave Type | Days Taken | % of Absences |
|---|---|---|
| Planned PTO | 68 | 61.8% |
| Sick Leave | 28 | 25.5% |
| Bereavement | 4 | 3.6% |
| Personal Leave | 10 | 9.1% |

## PTO Utilization

- Total PTO balance (all employees): 842 days accrued
- PTO taken Q1: 68 days
- **Utilization rate: 8.1%** (annualised target: 75%)
- Employees with >20 days banked: 8 (flagged for mandatory use)

## Trends

- Highest absence week: Week of Feb 12 (flu season) — 6.8% daily absence rate
- Lowest absence week: Week of Jan 8 — 1.2% daily absence rate
- Monday and Friday have 2.3× higher absence rate than midweek

## Action Items

- HR to remind 8 employees with high PTO balances to schedule leave
- Operations team absence rate (92.9%) below company target of 93.5% — investigate root cause
- Consider wellness initiatives to reduce sick leave in Q3/Q4
"""
    write(BASE / "hr" / "attendance_report_q1.md", content)

def hr_payroll():
    content = frontmatter("hr_003","Payroll Summary Q1 2024","hr",["hr","clevel"],"restricted","report")
    content += """# Payroll Summary — Q1 2024

**CONFIDENTIAL — HR & Finance Eyes Only**

## Total Payroll: $2,847,000

### Base Salary by Department

| Department | Headcount | Total Base (Q1) | Avg Base Salary | Benefits (18%) |
|---|---|---|---|---|
| Engineering | 10 | $892,500 | $357,000/yr | $160,650 |
| Marketing | 5 | $368,750 | $295,000/yr | $66,375 |
| Finance | 4 | $312,000 | $312,000/yr | $56,160 |
| HR | 3 | $196,500 | $262,000/yr | $35,370 |
| Operations | 4 | $278,000 | $278,000/yr | $50,040 |
| Product | 4 | $420,000 | $420,000/yr | $75,600 |
| **Total** | **30** | **$2,467,750** | **$329,000/yr** | **$444,195** |

*Total cost including benefits: $2,911,945*

### Salary Bands

| Band | Count | Salary Range | Midpoint |
|---|---|---|---|
| L3 | 12 | $75,000 – $95,000 | $85,000 |
| L4 | 10 | $95,000 – $125,000 | $110,000 |
| L5 | 6 | $125,000 – $165,000 | $145,000 |
| L6 | 2 | $165,000 – $220,000 | $192,500 |

### Benefits Breakdown

| Benefit | Employer Cost (Q1) |
|---|---|
| Health Insurance (Medical/Dental/Vision) | $284,400 |
| 401(k) Match (4% of base) | $98,710 |
| Life & Disability Insurance | $28,400 |
| HSA Contribution | $32,685 |
| **Total Benefits** | **$444,195** |

### Bonus & Variable Compensation

- Q1 performance bonuses paid: $224,000 (tied to Q4 2023 performance)
- Sales commissions: $148,000
- Referral bonuses: $12,000

### Payroll Cycle

- Pay frequency: Bi-weekly (26 pay periods/year)
- Direct deposit: 100% of employees
- Payroll processor: ADP
- Next payroll run: April 5, 2024

### Headcount Changes Q1

| Event | Count | Impact |
|---|---|---|
| New hires | 3 | +$87,500/qtr |
| Departures | 1 | -$28,750/qtr |
| Promotions (band change) | 2 | +$9,000/qtr |
| Merit increases (effective Mar 1) | 12 | +$34,500/qtr |
"""
    write(BASE / "hr" / "payroll_summary.md", content)

def hr_performance():
    promotees = [name() for _ in range(3)]
    pip_person = name()
    content = frontmatter("hr_004","Performance Reviews Q1 2024","hr",["hr","clevel"],"restricted","report")
    content += f"""# Performance Reviews — Q1 2024

**Review Cycle:** Q1 2024 (covers Jan–Mar 2024)
**Participation Rate:** 100% (30/30 employees reviewed)

## Rating Distribution

Performance is rated on a 5-point scale:
- **5 — Exceptional**: Consistently exceeds all expectations, significant impact
- **4 — Exceeds Expectations**: Regularly goes beyond role requirements
- **3 — Meets Expectations**: Fully competent, delivers on all commitments
- **2 — Needs Improvement**: Some gaps in performance, improvement plan required
- **1 — Unsatisfactory**: Significant performance issues, immediate action required

| Rating | Count | % of Team |
|---|---|---|
| 5 — Exceptional | 3 | 10% |
| 4 — Exceeds Expectations | 8 | 26.7% |
| 3 — Meets Expectations | 16 | 53.3% |
| 2 — Needs Improvement | 2 | 6.7% |
| 1 — Unsatisfactory | 1 | 3.3% |

## Department Performance Summary

| Department | Avg Rating | Top Performer | Notes |
|---|---|---|---|
| Engineering | 3.8 | See details | Strong delivery on platform v3 |
| Marketing | 3.6 | See details | Exceeded MQL targets by 38% |
| Finance | 3.4 | See details | Accurate close, minimal adjustments |
| HR | 3.5 | See details | Successful onboarding of 3 new hires |
| Operations | 3.2 | See details | Process improvements in Q1 |
| Product | 3.9 | See details | Highest avg rating this quarter |

## Promotion Recommendations

The following employees are recommended for promotion effective Q2 2024:

1. **{promotees[0]}** — Engineering → L4 to L5
   - Rationale: Led platform migration, mentored 2 junior engineers, delivered 3 major features on time

2. **{promotees[1]}** — Product → L3 to L4
   - Rationale: Shipped 4 high-impact features, exceptional stakeholder management, strong data-driven approach

3. **{promotees[2]}** — Marketing → L4 to L5
   - Rationale: Campaign ROI 134%, built entire ABM programme from scratch, exceeding targets by 28%

*Promotions pending final approval from respective VPs and CFO sign-off on compensation adjustment.*

## Performance Improvement Plan (PIP)

**Employee:** {pip_person} | Department: Operations | Band: L3

- PIP initiated: February 14, 2024
- Duration: 90 days (ends May 14, 2024)
- Issues: Repeated missed deadlines (4 instances Q4 2023), communication gaps with cross-functional teams
- Goals set: 100% on-time delivery for 8 weeks, weekly 1:1 with manager, complete project management training
- Current status: Showing improvement — 6/6 deliverables on time since PIP start

## Calibration Notes

- Overall team rating average: 3.41 (target: 3.2–3.6 — on track)
- No significant rating inflation observed
- Manager consistency review completed: 2 managers flagged for calibration coaching
"""
    write(BASE / "hr" / "performance_reviews_q1.md", content)

# ── ENGINEERING ───────────────────────────────────────────────────────────────

def eng_architecture():
    content = frontmatter("eng_001","System Architecture Overview","engineering",["engineering","clevel"],"internal","technical")
    content += """# System Architecture Overview

**Last Updated:** March 2024 | **Owner:** Engineering Team

## Architecture Overview

Our platform follows a microservices architecture deployed on AWS. All services communicate via REST APIs and an event bus (AWS EventBridge). Data is stored in a combination of PostgreSQL (relational), DynamoDB (key-value), and S3 (object storage).

## Microservices

### 1. auth-service
- **Language:** Python 3.11 / FastAPI
- **Responsibility:** JWT issuance, OAuth2, RBAC enforcement, session management
- **Database:** PostgreSQL (users, roles, permissions)
- **SLA:** 99.99% uptime | P50 <20ms | P99 <80ms
- **Instances:** 3 (min) — 10 (max) via Auto Scaling

### 2. api-gateway
- **Language:** Node.js 20 / Express
- **Responsibility:** Rate limiting, request routing, API versioning, request/response logging
- **Upstream:** All microservices
- **SLA:** 99.99% uptime | P50 <10ms overhead | P99 <50ms overhead
- **Rate Limits:** 1,000 req/min per API key (enterprise: 10,000)

### 3. data-pipeline
- **Language:** Python 3.11 / Celery + Redis
- **Responsibility:** ETL orchestration, data ingestion from 12 source systems, transformation, quality checks
- **Database:** PostgreSQL (pipeline state), S3 (raw + processed data)
- **SLA:** 99.9% uptime | Data freshness: <15 min for streaming, <4 hrs for batch
- **Schedule:** Batch runs at 02:00, 06:00, 12:00, 18:00 UTC

### 4. ml-inference
- **Language:** Python 3.11 / FastAPI + Ray Serve
- **Responsibility:** Real-time ML model serving, A/B testing, model versioning
- **Infrastructure:** GPU instances (g4dn.xlarge) in auto-scaling group
- **SLA:** 99.9% uptime | P50 <200ms | P99 <800ms
- **Models in Production:** 4 (anomaly detection, churn prediction, NLP classifier, recommendation)

### 5. notification-service
- **Language:** Go 1.22
- **Responsibility:** Email, Slack, in-app, and webhook notifications
- **Queue:** AWS SQS
- **SLA:** 99.9% uptime | Delivery <30 seconds for high-priority

## Data Flow

```
External Sources → api-gateway → auth-service (validate)
                                       ↓
                             data-pipeline (ingest/transform)
                                       ↓
                              PostgreSQL / S3 / DynamoDB
                                       ↓
                              ml-inference (score/predict)
                                       ↓
                            notification-service (alert)
```

## Infrastructure

| Component | Service | Region |
|---|---|---|
| Compute | AWS ECS (Fargate) | us-east-1 (primary), eu-west-1 (DR) |
| Database | AWS RDS PostgreSQL 15 | Multi-AZ |
| Cache | AWS ElastiCache (Redis 7) | Cluster mode |
| Object Store | AWS S3 | us-east-1 + replication |
| CDN | CloudFront | Global |
| Secrets | AWS Secrets Manager | — |
| Monitoring | DataDog + CloudWatch | — |

## Security

- All inter-service communication via mTLS
- Secrets rotated every 30 days via Secrets Manager
- VPC with private subnets for all data stores
- WAF in front of api-gateway
- PII encrypted at rest (AES-256) and in transit (TLS 1.3)
"""
    write(BASE / "engineering" / "system_architecture.md", content)

def eng_devprocess():
    content = frontmatter("eng_002","Development Process & Standards","engineering",["engineering","clevel"],"internal","process")
    content += """# Development Process & Standards

**Owner:** Engineering | **Version:** 2.1 | **Last Updated:** January 2024

## Sprint Cadence

- **Sprint Length:** 2 weeks
- **Sprint Planning:** Monday 10:00 AM (Day 1)
- **Daily Standup:** 9:30 AM Mon–Fri (15 min max, async Slack update if remote)
- **Sprint Review:** Friday 3:00 PM (Day 10) — demo to stakeholders
- **Retrospective:** Friday 4:00 PM (Day 10) — engineering team only

## Git Branching Strategy (GitFlow)

```
main          ← production-ready, tagged releases only
  └── develop ← integration branch, always deployable
        ├── feature/JIRA-123-description ← feature work
        ├── bugfix/JIRA-456-description  ← bug fixes
        └── hotfix/JIRA-789-description  ← prod hotfixes (branch from main)
```

**Branch naming:** `<type>/JIRA-<ticket>-<short-description>` (kebab-case)

## Pull Request Policy

**All PRs require:**
1. Passing CI pipeline (lint + test + build)
2. Minimum 1 approving review (2 for changes to auth-service or data models)
3. No unresolved comments
4. PR description using template (problem, solution, test plan, screenshots if UI)

**PR Size Guidelines:**
- Target: <400 lines changed
- >800 lines: requires engineering manager pre-approval
- Split large features into stacked PRs

## Testing Standards

| Layer | Tool | Required Coverage |
|---|---|---|
| Unit | pytest / Jest | >80% line coverage |
| Integration | pytest + testcontainers | Key user journeys |
| E2E | Playwright | Critical paths only |
| Load | Locust | Before major releases |
| Security | Bandit + Snyk | Every PR |

## Deployment Pipeline

```
PR Merged to develop
  → GitHub Actions CI (lint, test, build Docker image)
  → Push to ECR (dev tag)
  → Deploy to staging (ECS, auto)
  → Integration tests run against staging
  → Manual approval gate (engineering manager)
  → Deploy to production (ECS, blue/green)
  → Smoke tests
  → Notify #deployments Slack channel
```

**Deploy Frequency:** 2–4 times per week to production

## Code Review Standards

- Review within 1 business day of PR creation
- Comments must be actionable (suggest specific change, not just "fix this")
- Use Conventional Comments labels: `nit:`, `suggestion:`, `blocker:`, `question:`
- Authors respond to all comments before merging

## Definition of Done

- [ ] Code complete and reviewed
- [ ] Unit + integration tests passing
- [ ] Documentation updated (API docs, runbook if infra change)
- [ ] Feature flag configured if gradual rollout
- [ ] Monitoring alert configured if new metric
- [ ] JIRA ticket updated to Done
"""
    write(BASE / "engineering" / "development_process.md", content)

def eng_runbook():
    oncall = [name() for _ in range(4)]
    content = frontmatter("eng_003","Operational Runbook","engineering",["engineering","clevel"],"internal","runbook")
    content += f"""# Operational Runbook

**Owner:** Engineering | **Last Updated:** February 2024

## On-Call Rotation

Weekly rotation. Current schedule:

| Week | Primary | Secondary |
|---|---|---|
| Mar 18–24 | {oncall[0]} | {oncall[1]} |
| Mar 25–31 | {oncall[1]} | {oncall[2]} |
| Apr 1–7 | {oncall[2]} | {oncall[3]} |
| Apr 8–14 | {oncall[3]} | {oncall[0]} |

**On-call hours:** 24/7. Pager via PagerDuty. Target response: <15 min for P1, <1 hr for P2.

## Incident Severity Levels

| Severity | Definition | Response Time | Incident Commander |
|---|---|---|---|
| P1 — Critical | Full outage, data loss risk, security breach | 15 minutes | On-call engineer + Engineering Manager |
| P2 — High | Major feature down, >25% of users impacted | 1 hour | On-call engineer |
| P3 — Medium | Degraded performance, workaround exists | 4 hours | On-call engineer |
| P4 — Low | Minor issue, cosmetic, no user impact | Next business day | Assigned in JIRA |

## Incident Response Process

### P1/P2 Response Steps

1. **Acknowledge** PagerDuty alert within SLA
2. **Join** #incident-YYYY-MM-DD Slack channel (auto-created by PagerDuty)
3. **Assess** — check DataDog dashboards, CloudWatch logs, status page
4. **Communicate** — post initial update to #incidents within 10 min:
   > "P[1/2] incident in progress. Impacted: [service]. Investigating. ETA: [X]"
5. **Mitigate** — apply temporary fix if available (rollback, feature flag disable, scale up)
6. **Resolve** — deploy permanent fix
7. **Update** status page at status.company.com
8. **Post-mortem** — required for all P1/P2 within 48 hours

## Escalation Path

```
On-call Engineer
  → Engineering Manager ({oncall[0]} primary backup)
    → VP Engineering
      → CTO
        → CEO (P1 only, if customer data at risk)
```

## Monitoring & Alerting Thresholds

| Metric | Warning | Critical | Action |
|---|---|---|---|
| API error rate | >1% | >5% | Page on-call |
| API P99 latency | >500ms | >2,000ms | Page on-call |
| CPU utilisation | >70% | >90% | Auto-scale + page |
| Memory utilisation | >80% | >95% | Page on-call |
| DB connections | >80% of max | >95% of max | Page on-call |
| Queue depth (SQS) | >1,000 msgs | >10,000 msgs | Page on-call |
| Disk usage | >75% | >90% | Page on-call |

## Common Runbooks

### High API Latency
1. Check DataDog APM → identify slow traces
2. Check RDS slow query log → look for missing indexes
3. Check ElastiCache hit rate → if <85%, investigate cache invalidation
4. Scale ECS tasks if CPU-bound

### Database Connection Exhaustion
1. `SELECT count(*) FROM pg_stat_activity;` — identify idle connections
2. Terminate idle connections: `SELECT pg_terminate_backend(pid) WHERE state='idle' AND ...`
3. Check connection pool settings in each service
4. Scale RDS instance if persistent

### Deployment Rollback
```bash
# List recent task definitions
aws ecs list-task-definitions --family-prefix <service-name> --sort DESC

# Roll back to previous
aws ecs update-service --cluster prod --service <service> --task-definition <prev-task-def>
```

## Maintenance Windows

- **Scheduled maintenance:** Sundays 02:00–04:00 UTC
- **Database backups:** Daily at 01:00 UTC (retained 30 days)
- **Certificates renewal:** Auto-renewed via ACM (alert 30 days before expiry)
"""
    write(BASE / "engineering" / "operational_runbook.md", content)

# ── CLEVEL ────────────────────────────────────────────────────────────────────

def clevel_board():
    content = frontmatter("cl_001","Board Deck Q1 2024","clevel",["clevel"],"restricted","presentation")
    content += """# Board Deck — Q1 2024

**BOARD CONFIDENTIAL — Do Not Distribute**

## Q1 2024 Scorecard

| KPI | Target | Actual | Status |
|---|---|---|---|
| ARR | $17.0M | $16.8M | 🟡 |
| New ARR | $2.0M | $2.1M | 🟢 |
| Gross Margin | 82% | 85.7% | 🟢 |
| Net Revenue Retention | 115% | 118% | 🟢 |
| Churn Rate | <2.5% | 2.1% | 🟢 |
| Headcount | 32 | 30 | 🟡 |
| Cash Balance | >$7.5M | $8.4M | 🟢 |
| Burn Multiple | <1.5x | 1.2x | 🟢 |

## Strategic Highlights

### What Went Well
- Exceeded new ARR target by 5% — driven by enterprise segment
- Net Revenue Retention hit all-time high of 118%
- Gross margin improvement of 3pp from infrastructure optimisation
- Launched 2 of 4 planned Q1 features on time

### Challenges
- 2 engineering hires delayed to Q2 (competitive market)
- Mobile app NPS lagging at 58 — redesign in progress
- APAC expansion delayed due to compliance review

## M&A Pipeline

| Target | Status | ARR | Strategic Fit | Est. Valuation |
|---|---|---|---|---|
| DataBridge Analytics | LOI Signed | $3.2M | Data pipeline complement | $28M |
| Nexus Workflow Tools | Due Diligence | $1.8M | Process automation | $16M |
| Synapse AI | Initial Talks | $4.1M | ML capabilities | $45M |

*DataBridge acquisition expected to close Q2 2024. Board approval required.*

## Financial Position

- **Cash:** $8.4M
- **Monthly Burn:** $1.03M
- **Runway:** 18+ months
- **Series B Close:** $22M raised (January 2024)
- **Next Fundraise:** Series C planned Q4 2025 at $45M target

## Key Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Enterprise deal slippage | Medium | High | 3× pipeline coverage maintained |
| Engineering hiring lag | High | Medium | Contractor programme initiated |
| Competitive pricing pressure | Medium | Medium | Value-based selling training |
| Regulatory (data privacy) | Low | High | Legal review ongoing, DPA updates |

## Q2 2024 Priorities

1. Close DataBridge acquisition
2. Ship mobile app v2.0
3. Complete 2 engineering hires
4. Launch APAC pilot (2 customers)
5. Raise Series C lead investor process
"""
    write(BASE / "clevel" / "board_deck_q1.md", content)

def clevel_strategic():
    content = frontmatter("cl_002","Strategic Plan 2024","clevel",["clevel"],"restricted","strategy")
    content += """# Strategic Plan 2024–2025

**STRICTLY CONFIDENTIAL**

## Vision

Become the leading enterprise workflow intelligence platform for mid-market and enterprise companies by end of 2025, with $40M ARR and operations across North America, Europe, and APAC.

## Strategic Objectives (OKRs)

### OKR 1: Accelerate Enterprise Growth
- KR1: Grow ARR from $16.8M to $28M by Dec 2024
- KR2: Increase enterprise (>500 seat) accounts from 22 to 45
- KR3: Achieve NRR of 125%+ by Q4 2024

### OKR 2: Product Leadership
- KR1: Ship 12 major features (3 per quarter)
- KR2: Achieve mobile NPS >75 by Q3 2024
- KR3: Launch AI-native analytics module by Q3 2024

### OKR 3: International Expansion
- KR1: Sign 5 APAC customers by Q4 2024
- KR2: Hire APAC Country Manager by Q2 2024
- KR3: Achieve SOC2 Type II + ISO27001 by Q3 2024

### OKR 4: Operational Excellence
- KR1: Reduce customer onboarding from 6 weeks to 3 weeks
- KR2: Achieve 99.99% uptime for core platform
- KR3: Reduce support ticket volume by 30% via self-serve

### OKR 5: Team & Culture
- KR1: Grow headcount from 30 to 42 by Dec 2024
- KR2: Maintain eNPS >50
- KR3: Complete leadership training for all L5+ managers

## 18-Month Roadmap

| Quarter | Product | Go-to-Market | Infrastructure |
|---|---|---|---|
| Q2 2024 | Mobile v2, AI analytics beta | APAC pilot launch | SOC2 Type II audit |
| Q3 2024 | AI analytics GA, API v3 | APAC Country Manager hire | ISO27001 certification |
| Q4 2024 | Workflow automation module | Series C process begins | EU data residency |
| Q1 2025 | Platform v4 architecture | Series C close | APAC data centre |
| Q2 2025 | DataBridge integration GA | EMEA expansion | Multi-region active-active |

## Headcount Plan

| Department | Current | Q2 Hire | Q3 Hire | Q4 Hire | End 2024 |
|---|---|---|---|---|---|
| Engineering | 10 | 3 | 2 | 1 | 16 |
| Sales | 5 | 2 | 1 | 1 | 9 |
| Marketing | 5 | 1 | 0 | 1 | 7 |
| Customer Success | 3 | 1 | 1 | 0 | 5 |
| HR & Ops | 7 | 1 | 0 | 0 | 8 |
| **Total** | **30** | **8** | **4** | **3** | **45** |

## Funding Plan

- **Current:** Series B ($22M, closed Jan 2024)
- **Milestone for Series C:** $28M ARR, APAC live, AI module launched
- **Target raise:** $45M Series C — Q4 2025
- **Lead investor outreach:** Begin Q3 2025
- **Use of funds:** 60% go-to-market, 30% product/engineering, 10% ops
"""
    write(BASE / "clevel" / "strategic_plan_2024.md", content)

# ── GENERAL ───────────────────────────────────────────────────────────────────

def gen_policies():
    content = frontmatter("gen_001","Company Policies","general",["finance","marketing","hr","engineering","clevel","employee"],"internal","policy")
    content += """# Company Policies

**Effective:** January 1, 2024 | **Owner:** HR Department

## Code of Conduct

All employees are expected to:
- Act with integrity, honesty, and respect in all interactions
- Treat colleagues, customers, and partners with dignity regardless of background
- Protect confidential company and customer information
- Report unethical behaviour to HR or via the anonymous ethics hotline: 1-800-555-0199
- Avoid conflicts of interest; disclose any potential conflicts to your manager immediately

Violations of the Code of Conduct may result in disciplinary action up to and including termination.

## Remote Work Policy

**Hybrid Model:** 3 days in-office, 2 days remote (Tuesday/Wednesday required in-office)

- Remote work days: Monday, Thursday, Friday (or as agreed with manager)
- Home office setup: Company provides $500 equipment allowance (laptop, monitor, peripherals)
- Working hours: Core hours 10 AM–3 PM local time; flexible outside that window
- Internet: Employees are responsible for reliable internet connection; VPN required for all work
- Video on during team meetings (unless bandwidth constrained — use virtual background)

**Fully Remote Roles:** Designated roles only (listed in job description). Manager approval required for ad hoc full-remote weeks.

## Information Security Policy

- All devices must have full-disk encryption enabled
- Use company-provided password manager (1Password) — no reusing passwords
- MFA required on all work accounts (Google Workspace, GitHub, AWS, Slack)
- Report phishing emails to security@company.com — do not click links
- Do not store company data on personal devices or unapproved cloud services
- Data classification: Public / Internal / Confidential / Restricted — handle accordingly
- Security incidents must be reported within 1 hour of discovery

## Leave Policy

| Leave Type | Entitlement | Notes |
|---|---|---|
| Annual Leave (PTO) | 20 days/year | Accrues from start date, max 30 days rollover |
| Sick Leave | 10 days/year | No carry-over, doctor's note for >3 consecutive days |
| Parental Leave | 16 weeks (primary) / 8 weeks (secondary) | Fully paid |
| Bereavement | 5 days (immediate family), 2 days (extended) | — |
| Public Holidays | 11 days | Per office location calendar |
| Mental Health Days | 2 days/year | No explanation required |

Leaves must be requested and approved in Workday at least 5 business days in advance (except sick leave and emergencies).

## Expense & Reimbursement

See the full Reimbursement Policy for limits. Key points:
- Submit via Expensify within 30 days
- Receipts required for all items over $25
- Personal credit card or company card (issued to L5+)

## Anti-Harassment Policy

The company maintains a zero-tolerance policy for harassment, discrimination, or bullying of any kind. This includes:
- Unwelcome physical contact
- Verbal or written harassment
- Discrimination based on gender, race, religion, disability, sexual orientation, age, or any protected characteristic

To report: HR directly, or anonymous hotline 1-800-555-0199. All reports investigated within 5 business days.
"""
    write(BASE / "general" / "company_policies.md", content)

def gen_events():
    content = frontmatter("gen_002","Upcoming Company Events","general",["finance","marketing","hr","engineering","clevel","employee"],"public","notice")
    content += f"""# Upcoming Company Events & Calendar

**Last Updated:** {date.today().isoformat()}

## Q2 2024 Company Events

### All-Hands Meeting — March 28, 2024
- **Time:** 2:00 PM – 4:00 PM EST (virtual + in-person)
- **Location:** HQ Main Auditorium + Zoom
- **Agenda:** Q1 results, Q2 strategy, product roadmap preview, team awards
- **Host:** CEO & Leadership Team
- Add to calendar: calendar.company.com/all-hands-q1-2024

### Q2 2024 Kickoff — April 5, 2024
- **Time:** 10:00 AM – 12:00 PM EST
- **Location:** Virtual (Zoom)
- **Agenda:** Department OKRs, cross-team dependencies, sprint planning preview
- All department heads presenting 15-min updates

### Engineering Demo Day — April 12, 2024
- **Time:** 3:00 PM – 5:00 PM EST
- Engineering team showcases Q1 technical work + upcoming features
- Open to all employees

### Company Lunch & Learn Series

| Date | Topic | Speaker | Location |
|---|---|---|---|
| April 9 | AI in Enterprise: Practical Applications | External Speaker | HQ + Virtual |
| April 23 | Building Your Personal Brand | HR Team | Virtual |
| May 7 | Financial Wellness 101 | Finance Partner | HQ + Virtual |
| May 21 | Mental Health at Work | Employee Assistance Program | Virtual |

### Team Social Events

| Date | Event | Details |
|---|---|---|
| April 19 | Engineering Game Night | Board games + pizza, HQ |
| April 26 | Marketing Team Offsite | Full day, venue TBD |
| May 10 | Company Volunteer Day | Habitat for Humanity build |
| May 24 | Summer Kickoff BBQ | HQ rooftop, 4 PM onwards |

## Public Holidays (US Office) — 2024

| Date | Holiday |
|---|---|
| Jan 15 | Martin Luther King Jr. Day ✓ |
| Feb 19 | Presidents' Day ✓ |
| May 27 | Memorial Day |
| Jun 19 | Juneteenth |
| Jul 4 | Independence Day |
| Sep 2 | Labor Day |
| Nov 28 | Thanksgiving Day |
| Nov 29 | Day after Thanksgiving |
| Dec 25 | Christmas Day |
| Dec 26 | Company Holiday |

## Training & Development

| Programme | Format | Frequency | Enroll |
|---|---|---|---|
| Manager Essentials | 4-week virtual cohort | Quarterly | HR portal |
| Technical Writing Workshop | 1-day in-person | Bi-annual | HR portal |
| Security Awareness Training | Online (1 hr) | Annual (required) | Workday |
| Diversity & Inclusion | Online (2 hr) | Annual (required) | Workday |

Questions: events@company.com
"""
    write(BASE / "general" / "upcoming_events.md", content)

def gen_faq():
    content = frontmatter("gen_003","Employee FAQ","general",["finance","marketing","hr","engineering","clevel","employee"],"public","faq")
    content += """# Employee FAQ

## Benefits & Compensation

**Q: When does benefits enrollment open?**
A: Open enrollment runs October 1–15 each year for the following calendar year. New hires have 30 days from start date to enroll. Log into Workday → Benefits → Enrollment.

**Q: What health insurance plans are available?**
A: Three plans through Aetna: (1) HMO Basic — $0 premium employee, (2) PPO Plus — $45/month employee, (3) High-Deductible HSA — $0 premium + $800 company HSA contribution. Dental and vision through MetLife.

**Q: How does the 401(k) work?**
A: Company matches 4% of base salary. Vesting: 25% after year 1, 50% year 2, 75% year 3, 100% year 4. Log into Fidelity NetBenefits to manage contributions.

**Q: How do I view my pay stubs?**
A: Workday → Pay → Pay Stubs. Pay stubs available 2 business days before each pay date.

**Q: What is the equity / stock options situation?**
A: All full-time employees receive options as part of their offer. 4-year vesting with 1-year cliff. Contact finance@company.com for your current grant details or to understand exercise windows.

## IT & Equipment

**Q: How do I get IT support?**
A: Submit a ticket at help.company.com or Slack #it-help. Response time: 2 hours for P1 (system down), 4 hours P2, next business day P3. Emergency: ext. 4357 (HELP).

**Q: My laptop is broken / stolen — what do I do?**
A: Report immediately to IT (help.company.com) and HR. For theft, also file a police report and send report number to HR. Replacement typically issued within 2 business days.

**Q: Can I install software on my work laptop?**
A: Approved software list at it.company.com/approved-software. For anything not listed, submit a software request via IT portal. Unlicensed or unapproved software is not permitted.

**Q: How do I set up VPN?**
A: Download Tailscale from the IT portal. Authentication is via your company Google account + MFA. Instructions at it.company.com/vpn-setup.

## Onboarding

**Q: What does my first week look like?**
A: Day 1: IT setup, HR paperwork, office tour. Day 2: Department intro meetings. Days 3–5: Role-specific onboarding sessions. Full onboarding plan sent by HR before start date.

**Q: Where do I find company documentation and processes?**
A: Notion (notion.company.com) is our company wiki. Access via your Google SSO login.

**Q: Who should I contact for different questions?**
A:
- Pay/benefits → HR: hr@company.com or Workday
- IT issues → IT: help.company.com
- Expense reimbursement → Finance: finance-team@company.com
- Legal/contracts → Legal: legal@company.com
- Ethics/concerns → ethics@company.com or 1-800-555-0199

## Policies

**Q: How do I request time off?**
A: Submit in Workday → Time Off → Request. At least 5 business days notice required (except emergencies). Approval from direct manager within 2 business days.

**Q: Can I work from a different country / state temporarily?**
A: Up to 2 weeks per year without additional approval. Longer periods require HR and legal review (tax implications). Contact hr@company.com before making plans.

**Q: How do I submit an expense report?**
A: Use Expensify (expensify.com, login with company email). Submit within 30 days. For amounts >$200, manager approval required before submission. See Reimbursement Policy for limits.
"""
    write(BASE / "general" / "faq.md", content)

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Generating synthetic data -> {BASE}\n")
    fin_q1_report()
    fin_marketing_expenses()
    fin_capex()
    fin_reimbursement()
    mkt_campaign()
    mkt_feedback()
    mkt_sales()
    hr_directory()
    hr_attendance()
    hr_payroll()
    hr_performance()
    eng_architecture()
    eng_devprocess()
    eng_runbook()
    clevel_board()
    clevel_strategic()
    gen_policies()
    gen_events()
    gen_faq()

    files = list(BASE.rglob("*.md"))
    words = sum(len(f.read_text(encoding="utf-8").split()) for f in files)
    print(f"\nDone — {len(files)} files, ~{words:,} words generated.")

if __name__ == "__main__":
    main()
