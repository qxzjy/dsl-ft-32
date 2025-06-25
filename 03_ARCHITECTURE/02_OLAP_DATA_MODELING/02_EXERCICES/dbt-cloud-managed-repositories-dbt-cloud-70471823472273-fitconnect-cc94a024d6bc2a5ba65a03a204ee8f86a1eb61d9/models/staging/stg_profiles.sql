-- ===============================
-- dbt/models/staging/stg_profiles.sql
-- ===============================
select
    profileid,
    userid as user_id,
    firstname,
    lastname,
    birthdate,
    gender,
    height,
    currentweight,
    targetweight,
    fitnessgoal,
    activitylevel
from {{ source('fitconnect', 'profiles') }}
