select *
from {{ ref('fct_product_funnel') }}
where purchase_sessions > cart_sessions
   or cart_sessions > view_sessions
   or view_sessions > session_count
