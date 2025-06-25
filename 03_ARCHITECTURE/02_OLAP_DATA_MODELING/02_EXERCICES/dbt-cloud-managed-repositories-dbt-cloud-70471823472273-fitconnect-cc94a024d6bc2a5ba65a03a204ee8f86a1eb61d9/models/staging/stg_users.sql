-- ===============================
-- dbt/models/staging/stg_users.sql
-- ===============================
select
    userid as user_id,
    username,
    email,
    joindate,
    lastlogin,
    accountstatus
from {{ source('fitconnect', 'users') }}
