-- ===============================
-- dbt/models/staging/stg_workouts.sql
-- ===============================
select
    workoutid,
    userid as user_id,
    workoutplanid,
    workoutdate,
    duration,
    caloriesburned,
    rating,
    completionstatus
from {{ source('fitconnect', 'workouts') }}
