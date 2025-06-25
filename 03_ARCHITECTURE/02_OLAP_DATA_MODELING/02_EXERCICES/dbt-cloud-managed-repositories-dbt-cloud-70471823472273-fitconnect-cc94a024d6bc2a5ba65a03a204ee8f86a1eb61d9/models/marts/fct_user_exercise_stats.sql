-- 🎯 This model calculates aggregated stats on exercises across a selected time grain

{% set grain = var('agg_grain', 'month') %}  -- Default to 'month' if no variable is passed

-- 1️⃣ Select completed workouts and truncate workoutdate to the selected grain
with workouts as (
    select
        workoutid,
        user_id,
        workoutdate,
        {{ truncate_date('workoutdate', grain) }} as period_start,  -- truncate to month/week
        rating
    from {{ ref('stg_workouts') }}
),

-- 2️⃣ Select all individual exercises performed
workout_exercises as (
    select *
    from {{ ref('stg_workout_exercises') }}
),

exercises as (
    select *
    from {{ ref('stg_exercises')}}
),

workout_exercises_muscle_group as (
    select
    we.workoutid,
    we.exerciseid,
    e.name as exercise_name,
    e.category,
    e.musclegroup,
    e.difficultylevel,
    we.setcount,
    we.repcount,
    we.weight,
    we.duration
    from workout_exercises we
    left join exercises e on we.exerciseid = e.exerciseid
),

-- 3️⃣ Join workouts and exercises
joined as (
    select
        w.user_id,
        w.workoutdate,
        w.period_start,
        w.rating,
        e.exerciseid,
        e.exercise_name,
        e.category,
        e.musclegroup,
        e.difficultylevel,
        e.setcount,
        e.repcount,
        e.weight,
        e.duration
    from workout_exercises_muscle_group e
    join workouts w on e.workoutid = w.workoutid
),

-- 4️⃣ Aggregate the joined data
agg as (
    select
        exerciseid,
        exercise_name,
        category,
        musclegroup,
        difficultylevel,
        period_start,
        count(*) as times_performed,  -- how many times this exercise was done
        avg(setcount) as avg_sets,
        avg(repcount) as avg_reps,
        avg(weight) as avg_weight,
        avg(duration) as avg_duration,
        avg(rating) as avg_rating
    from joined
    group by exerciseid, exercise_name, category, musclegroup, difficultylevel, period_start
)

-- ✅ Final output
select * from agg
