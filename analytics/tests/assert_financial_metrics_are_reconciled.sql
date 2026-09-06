with actual as (
    select fiscal_year, revenue, net_income, source_accession
    from {{ ref('mart_financial_metrics') }}
), expected as (
    select fiscal_year, revenue, net_income, source_accession
    from {{ ref('expected_financial_metrics') }}
)
select
    coalesce(actual.fiscal_year, expected.fiscal_year) as fiscal_year,
    actual.revenue as actual_revenue,
    expected.revenue as expected_revenue,
    actual.net_income as actual_net_income,
    expected.net_income as expected_net_income,
    actual.source_accession as actual_accession,
    expected.source_accession as expected_accession
from expected
left join actual using (fiscal_year)
where actual.fiscal_year is null
   or abs(actual.revenue - expected.revenue) > 1
   or abs(actual.net_income - expected.net_income) > 1
   or actual.source_accession <> expected.source_accession
