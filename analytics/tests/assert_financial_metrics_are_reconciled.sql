select *
from {{ ref('mart_financial_metrics') }}
where revenue <= 0
   or net_income is null
   or net_margin is null
