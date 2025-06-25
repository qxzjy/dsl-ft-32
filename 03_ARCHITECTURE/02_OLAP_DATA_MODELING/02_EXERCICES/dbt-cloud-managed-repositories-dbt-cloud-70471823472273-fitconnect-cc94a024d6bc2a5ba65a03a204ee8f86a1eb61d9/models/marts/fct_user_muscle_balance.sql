-- Use a variable for aggregation grain: week or month
{% set grain = var('agg_grain', 'week') %}

-- Stage 1: Get workouts
with workouts as (
    select
        workoutid,
        user_id,
        workoutdate,
        duration,
        caloriesburned
    from {{ ref('stg_workouts') }}
),

-- Stage 2: Get exercises with muscle group info
workout_exercises as (
    select
        workoutid,
        exerciseid,
        duration as exercise_duration
    from {{ ref('stg_workout_exercises') }}
),

exercises as (
    select
        exerciseid,
        musclegroup
    from {{ ref('stg_exercises')}}
),

workout_exercises_muscle_group as (
    select
    we.workoutid,
    we.exerciseid,
    we.exercise_duration,
    e.musclegroup
    from workout_exercises we
    left join exercises e on we.exerciseid = e.exerciseid
),

-- Stage 3: Attach period (week/month) to workouts
workout_periods as (
    select
        w.workoutid,
        w.user_id,
        w.duration as workout_duration,
        w.caloriesburned,
        {{ truncate_date('w.workoutdate', grain) }} as period_start
    from workouts w
),

-- Stage 4: Combine workouts with exercises, calculate calories per minute
combined as (
    select
        wp.user_id,
        wp.period_start,
        e.musclegroup,
        e.exercise_duration,
        wp.caloriesburned
    from workout_periods wp
    join workout_exercises_muscle_group e on wp.workoutid = e.workoutid
),

-- Stage 5: Aggregate metrics at muscle group level
muscle_group_stats as (
    select
        user_id,
        period_start,
        musclegroup,
        count(*) as exercise_count,
        sum(exercise_duration) as total_duration,
        sum(caloriesburned) as total_calories
    from combined
    group by user_id, period_start, musclegroup
),

-- Stage 6: Compute totals per user/period for percentages
total_counts as (
    select
        user_id,
        period_start,
        sum(exercise_count) as total_exercises,
        sum(total_duration) as total_time,
        sum(total_calories) as total_cals
    from muscle_group_stats
    group by user_id, period_start
),

-- Stage 7: Join everything and compute percentages
final as (
    select
        m.user_id,
        m.period_start,
        m.musclegroup,
        m.exercise_count,
        m.total_duration,
        m.total_calories,
        t.total_exercises,
        t.total_time,
        t.total_cals,
        -- Percentage of total exercises done on this muscle group
        round(m.exercise_count * 100.0 / t.total_exercises, 2) as pct_exercises,
        -- Percentage of time spent on this group
        round(m.total_duration * 100.0 / t.total_time, 2) as pct_duration,
        -- Percentage of calories burned on this group
        round(m.total_calories * 100.0 / t.total_cals, 2) as pct_calories
    from muscle_group_stats m
    join total_counts t
      on m.user_id = t.user_id and m.period_start = t.period_start
)

-- Final result
select * from final