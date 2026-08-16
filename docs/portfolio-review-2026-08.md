# Portfolio screening review

Review date: 2026-08-16

This review treats the portfolio as a candidate submission for a senior Data Analyst / Analytics Engineer role, with applied AI as a supporting capability. The review separates credible evidence from claims that would need a real employer context or a larger validation sample.

## Before the improvement pass

### Recruiter score: 6.2 / 10

The identity was visible, but the homepage promoted seven projects with similar visual weight. The strongest evidence was mixed with older and narrower work, so a 30–60 second scan required too much sorting. The value proposition was clear but generic, and the three impact numbers did not explain their source or business context. Navigation worked, but the portfolio did not make the intended shortlist narrative obvious.

I would have continued to a deeper review, but I would not have given an immediate strong shortlist recommendation for a competitive senior pool. The candidate looked capable; the presentation did not yet prove prioritization and senior judgment quickly enough.

### Data/Analytics Manager score: 6.4 / 10

The retail, taxi, restaurant, fake-job, and AI projects provided real evidence of cleaning, modeling, evaluation, and communication. However, the seven newer dataset projects were often decision frameworks rather than full analyses. Several had strong limitations but limited driver analysis: airfare was a national benchmark, JOLTS was aggregate labor-market context, Airbnb had no bookings, and clickstream had no confirmed orders. That honesty helped credibility, but it also limited the demonstrated senior depth.

## Project challenge

| Project | So what? / decision | Evidence strength | Main weakness | Portfolio role |
| --- | --- | --- | --- | --- |
| ComplaintFlow AI triage | Should support operations route a complaint automatically, retrieve a playbook, or escalate? | Strong architecture, reliability contract, tests, and evaluation harness | Evaluation fixture is small and synthetic; hosted-model results are not measured | Featured AI engineering project |
| Online Retail | Where should retention and market-expansion effort go? | Strong cleaning, concentration, repeat-revenue evidence, and scenario math | No margin, shipping, or campaign-outcome data | Featured customer-growth case |
| NYC Taxi | Where should capacity be concentrated? | Strong scale, time, geography, and trip-economics evidence | One month; no vehicle-hours or supply data | Featured operations case |
| Restaurant Inspections | Where should quality follow-up focus? | Strong inspection-level rollup and data-quality discipline | Missing grades and inspection-mix bias limit causal interpretation | Featured risk/quality case |
| Fake Job Detection | How should a platform balance missed scams and review workload? | Strong threshold trade-off, precision/recall, cross-validation, and model comparison | Historical dataset; no live drift or reviewer-cost evidence | Featured applied ML case |
| MDS Customer Value | Can the business trust and reuse its customer-value metric? | Clear pipeline, testing, and ownership story | No measured downstream decision or saved business time | Supporting data-engineering proof |
| Netflix Content Strategy | Should content freshness be judged with one target? | Good mix analysis and clear business interpretation | No viewership, retention, or content-cost outcome | Supporting strategy case |
| World Happiness | What changed over time and which factors are associated? | Strong balanced-panel and correlation limitations | Weak direct business decision; policy conclusions remain broad | Supporting analytical breadth |
| Clickstream Funnel | Which journey transition deserves the next product experiment? | Clear measurement-gap diagnosis and funnel evidence | No confirmed order link; no root cause beyond instrumentation | Supporting product analytics case |
| Bank Marketing | Which contacts deserve more campaign attention? | Good segmentation and explicit response-vs-profit warning | No incremental test, cost, or deposit-value evidence | Supporting marketing case |
| Airfare Pricing | Can the commercial team interpret fare movement safely? | Good benchmark and mix/elasticity framing | National series is context, not a route pricing analysis | Supporting pricing context |
| SEC Company Performance | Is growth also improving reported profitability? | Clear revenue/net-income/margin comparison and filing caveats | One company; no segment or cash-flow driver analysis | Supporting financial case |
| Airbnb Marketplace | Is listing supply healthy and resilient? | Good supply mix and host concentration evidence | No bookings, occupancy, revenue, or demand-side data | Supporting marketplace case |
| BLS Workforce | Is pressure coming from hiring demand or exits? | Correct separation of openings, hires, quits, and separations | Aggregate context cannot explain company/team root causes | Supporting workforce context |
| Credit Default Risk | Which accounts deserve earlier support or review? | Good exposure/risk/governance framing | Historical dataset; no current fairness or intervention result | Supporting risk case |

## Priority findings

### P0 — Hurts interview chances

No justified P0 remains after this pass. The previous P0 risks were project overload, weak homepage prioritization, unsupported headline metrics, and unclear senior positioning. The homepage now features five projects, metrics are tied to validated portfolio evidence, and the profile explicitly covers analytics engineering and applied AI.

### P1 — Important improvements remaining

1. The seven newer dataset projects still need deeper row-level analysis or should remain clearly labeled as scoped decision studies. They should not be presented as equivalent to the strongest retail, taxi, fake-job, and ComplaintFlow work.
2. The portfolio has no resume or detailed employment evidence. The site should not fabricate one, but a real resume and role history would materially improve screening confidence.
3. ComplaintFlow’s evaluation is an engineering contract, not proof of production model quality. A privacy-reviewed real complaint sample, reviewer labels, hosted-model comparison, and cost/latency measurements are the next credible upgrade.
4. Several case studies recommend experiments but do not show completed experiments. The writing correctly labels these as proposals; they should not be presented as measured business impact.

### P2 — Polish

- Add consistent “Decision / Evidence / Recommendation” labels to older case studies.
- Add public repository links for the newer analytical projects if the underlying notebooks or scripts are ready.
- Add a short portfolio index by capability for hiring managers who want to scan SQL, Python, experimentation, operations, and AI engineering separately.

## After the improvement pass

### Recruiter score: 7.6 / 10

The first screen now communicates the profile faster: senior analyst / analytics engineer, applied AI, and business decisions across growth, operations, and risk. Five featured projects create a credible scan path, and the full library is clearly secondary. The candidate is now interview-worthy for a senior analyst or analytics-engineering screen.

### Data/Analytics Manager score: 7.5 / 10

The portfolio now shows stronger judgment through explicit limitations, KPI framing, scenario math, escalation rules, evaluation contracts, and measurement plans. The strongest work demonstrates senior analytical thinking. The score remains below an unequivocal 8 because several public datasets cannot support the full root-cause and business-impact chain, and the AI project still uses a small synthetic evaluation fixture.

## Final recommendation

**Recommend an interview for a senior Data Analyst / Analytics Engineer role, with a focused discussion of the retail, taxi, fake-job, and ComplaintFlow projects.**

I would not yet treat the portfolio alone as proof of approximately ten years of production ownership. I would use the interview to test real stakeholder experience, shipped systems, SQL depth, trade-off decisions, and how the candidate moved from analysis to measured business change.
