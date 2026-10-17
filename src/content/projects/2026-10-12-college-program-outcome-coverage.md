---
title: "College Program Outcomes: Check Coverage Before Comparing Earnings"
date: 2026-10-12
categories: [business analytics, education]
tags: [college-scorecard, data-quality, student-outcomes, portfolio-review]
excerpt: "A coverage audit of federal program outcomes finds that reportable earnings vary sharply by credential and institution type, making unqualified program rankings unsafe."
problem: "Education leaders may use public program earnings to guide portfolio reviews, but privacy suppression and repeated branch records can distort comparisons."
result: "After deduplicating branch records, 37.6% of domestic bachelor's program rows reported a four-year earnings median. Coverage was 54.2% for public programs and 24.8% for private nonprofits."
featured: false
published: true
caseId: college-program-outcome-coverage
kind: completed
primaryTrack: analytics-engineering
displayOrder: 110
evidenceManifest: /data/evidence/college-program-outcome-coverage.json
evidenceVisuals:
  - /images/college-scorecard-earnings-coverage-credential.png
  - /images/college-scorecard-earnings-coverage-control.png
  - /images/college-scorecard-branch-deduplication.png
header:
  teaser: /images/college-scorecard-earnings-coverage-credential.png
---

## Project brief

- **Project:** Audit coverage of College Scorecard program earnings.
- **Question:** Are public earnings complete enough to guide program reviews?
- **Built:** A branch-deduplicated program table and coverage comparisons by credential and institution control.
- **Result:** 37.6% of domestic bachelor's program records reported a four-year earnings median. Coverage was 54.2% for public programs and 24.8% for private nonprofits.

## Business question

College leaders may compare majors or institutions using public earnings figures. If some programs have no reportable value, a ranking can describe only the visible part of the portfolio and make the coverage gap hard to see.

The business question is: **is the College Scorecard field-of-study file complete and comparable enough to guide a program review, and what should leaders check before acting on it?**

## Data and preparation

The source is the U.S. Department of Education's College Scorecard **Most Recent Cohorts: Field of Study** file, released on June 10, 2026. It contains 227,980 rows with earnings, debt, institution, field-of-study, and credential data. The unit for these outcome measures is the institution system, four-digit Classification of Instructional Programs field, and credential level.

The Department calculates some outcome measures at the six-digit OPEID institution-system level and repeats them across branch campuses. I verified that repeated earnings and debt values matched, then kept one row per OPEID6, field, and credential. For the comparison below, I excluded foreign institutions and non-credential coursework. I treat a numeric median as reportable and keep the source's `PS` privacy-suppression value separate. In the domestic bachelor's rows, every nonnumeric earnings cell is marked `PS`.

## Stakeholder questions

- **How many domestic bachelor's records have reportable earnings?** 25,283 of 67,212 distinct program records, or 37.6%.
- **Does coverage differ by institution control?** Yes. Coverage was 54.2% for public, 24.8% for private nonprofit, and 44.5% for for-profit programs.
- **Can a missing value be treated as zero?** No. Every nonnumeric domestic bachelor's earnings cell is marked `PS` for privacy suppression.

## Findings

### Earnings coverage changes by credential

Only **37.6%** of the distinct domestic bachelor's program records report a four-year earnings median. Coverage also varies across credential levels, so each comparison needs its own coverage count.

![Share of College Scorecard program records with a reportable four-year earnings median by credential level](/images/college-scorecard-earnings-coverage-credential.png)

This means the absence of an earnings value cannot be read as a low outcome or a zero. It is a coverage condition that must stay visible in a decision dashboard.

### Public programs are more visible than private nonprofit programs

Among domestic bachelor's program records, **54.2%** of public programs had a reportable median, compared with **24.8%** of private nonprofit programs and **44.5%** of private for-profit programs. This describes reporting coverage in the file. It does not show that one institution type has better student outcomes.

![Reported versus privacy-suppressed PS four-year earnings values in domestic bachelor's program records by institution control](/images/college-scorecard-earnings-coverage-control.png)

Because coverage differs by institution type, a comparison of visible medians could over-represent groups with more reportable cells. The source does not provide the value for each suppressed cell.

### Branch rows need to be collapsed before counting programs

The raw file contains **70,557** U.S. bachelor's rows for the three domestic control groups. After collapsing repeated branch-campus outcomes to distinct institution-system, field, and credential records, **67,212** program records remain. That removes **3,345 repeated rows** from this bachelor's comparison.

![Raw U.S. bachelor's rows and distinct College Scorecard program records after branch-campus deduplication](/images/college-scorecard-branch-deduplication.png)

The deduplication changes the count, not the reported outcome values. It prevents the same institution-system result from appearing as multiple independent programs just because the institution has multiple campuses.

## Built

The analysis verifies the source snapshot, checks repeated branch values, deduplicates to institution-system, field, and credential, and measures reportable-value coverage. It does not impute suppressed values.

## Result

The coverage and branch-record hypotheses were supported. Most domestic bachelor's program records did not have a reportable four-year earnings median, and coverage varied by institution control. The dataset can support a first-pass review, but it cannot support an unqualified league table across institutions.

- Show reportable and privacy-suppressed counts next to outcome summaries.
- Compare the same field and credential, and keep institution-system records deduplicated.
- Use internal completion, enrollment, debt, cost, and employment data to investigate programs with weak or missing public outcomes.
- Do not treat missing data as zero, infer program quality from coverage, or use these aggregate values as a forecast for an individual student.

## Technical notes

The analysis covers the June 10, 2026 field-of-study snapshot. Earnings describe federally aided completers who were working and not enrolled during the measurement year. The values are institution-system, field, and credential medians; they do not include every graduate or provide a causal return on tuition. Privacy-suppressed cells are not imputed. Download instructions, hashes, and regeneration details are in [`docs/new-public-data-case-notes.md`](https://github.com/hadibudhy/hadibudhy.github.io/blob/master/docs/new-public-data-case-notes.md).

Sources: the [College Scorecard data download](https://collegescorecard.ed.gov/data/) and the [Field of Study technical documentation](https://collegescorecard.ed.gov/assets/FieldOfStudyDataDocumentation.pdf). The data does not establish that a particular institution, major, or policy caused a graduate's earnings.
