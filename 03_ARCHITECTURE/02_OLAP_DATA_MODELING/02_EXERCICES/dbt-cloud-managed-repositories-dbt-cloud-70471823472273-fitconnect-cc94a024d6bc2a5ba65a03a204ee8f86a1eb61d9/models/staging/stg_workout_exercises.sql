-- ===============================
-- dbt/models/staging/stg_workout_exercises.sql
-- ===============================

select
    workoutid,
    exerciseid,
    setcount,
    repcount,
    weight,
    duration
from {{ source('fitconnect', 'workout_exercises') }}
