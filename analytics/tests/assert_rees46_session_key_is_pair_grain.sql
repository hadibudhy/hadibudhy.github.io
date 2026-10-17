select user_session_key
from {{ ref('stg_rees46_events') }}
where user_session_key is not null
group by user_session_key
having count(distinct user_id) <> 1
    or count(distinct user_session) <> 1
