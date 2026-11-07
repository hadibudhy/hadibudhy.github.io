# CFPB complaint monitoring

This project uses aggregate facets from the CFPB's public Consumer Complaint Database API to monitor issue mix and company-coded responses for one company and product. It stores no complaint rows or narratives.

## Reproduce

From the repository root, install `requests` and `matplotlib` if needed, then run:

```powershell
python projects/growth-analytics/06-cfpb-complaint-monitoring/src/analyze.py
```

The script requests one monthly filtered aggregate at a time for TransUnion's `Credit reporting or other personal consumer reports` complaints, January 2025 through September 2026. It writes metrics and charts under `public/`. The live API changes over time; the checked-in aggregate snapshot records the API update timestamp and its own canonical snapshot hash.

## Source and limits

- Source: [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)
- API documentation: [CFPB Open Tech](https://cfpb.github.io/api/ccdb/)
- The CFPB says published complaint data are freely available for anyone to use, analyze, and build on.
- The CFPB says complaint records are not a statistical sample of consumers' marketplace experiences. Complaint counts are not rates without customer or market-share denominators.
- The source is generally updated daily. Complaints are published after a company responds, confirms a commercial relationship, or after 15 days, whichever comes first.
- The cutoff ends September 2026, before the October 29, 2026 form-taxonomy update. Company response codes and the timely-response field do not measure satisfaction or resolution quality.
- The analysis uses aggregate API facets only and does not save complaint records, narratives, or ZIP codes.
