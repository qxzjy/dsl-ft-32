# Designing a Fitness App Database 🚴‍♂️

<img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmlkdXYzZG5iNW90bHpzemV3ZWlnemE3bnZhcjUzbG5vcXUyanM4YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/b4UEba8vntN2o/giphy.gif" width="400"/>

<Note type="tip" title="What will you learn in this exercise? 🧐🧐">

By the end of this exercise, based on the MERISE method, you will be able to:

- Put yourself in the shoes of a data engineer running domain analysis
- Analyze a real-world app and extract entities, relationships, and constraints  
- Apply logical modeling techniques to define a normalized schema  
- Translate that model into a physical, database-aware structure  
- Justify modeling decisions in terms of business logic, performance, and data integrity  

</Note>

This hands-on exercise will help solidify your understanding of the data modeling process by walking through the design of a real-world app—**FitConnect**, a fitness and social networking platform.

You'll go step-by-step from identifying key entities and relationships to implementing integrity constraints and exploring physical modeling decisions. The goal is not just to build a database—but to understand why your choices matter.

Let’s get started.

### The Business Context

FitConnect is a modern fitness application that combines several key features:

| | **Feature**              | **Description**                                                                 |
|----------|--------------------------|----------------------------------------------------------------------------------|
| 🏋️       | **Workout Tracking**     | Users log workout sessions, track sets, reps, duration, and monitor progress.   |
| 🥗       | **Nutrition Planning**   | Users set dietary goals, log meals, and receive nutrient feedback.              |
| 💬       | **Social Engagement**    | A social feed enables likes, comments, community challenges, and sharing.       |
| 🧑‍🏫       | **Personalized Coaching**| Users connect with trainers for tailored programs, feedback, and coaching.      |

## Domain Analysis

### Step 1: Domain Analysis - The Foundation of Everything

Domain analysis isn't just the first step in data modeling—it's arguably the most important. 

Let's walk you through how a professional data architect would approach this for our fitness application.

#### 1. Understanding Key Actors

For any system, we first need to understand *who* interacts with it. These aren't just tables in a database; they're real people and components with specific needs, behaviors, and relationships.

<Note type="unknown">

**TO DO:**

Identify all key actors interacting with our fitness app. If relevant try to break them down into categories depending on their specific needs, or usecases.

Try and think about your app both from an external user, and internal user standpoint, also note that not only humans will need to access data flowing through your app.
</Note>


##### Users/Members

Users are the primary actors in our fitness ecosystem. Let's break this down further:

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-Users.png?raw=true"/>

* **Fitness Enthusiasts** - Regular users tracking personal progress
* **Beginners** - Users new to fitness requiring more guidance
* **Athletes** - Advanced users with specialized training needs
* **Health-Focused Users** - People managing conditions or recovery

Each user type interacts with our system differently. A beginner might need simplified workout tracking, while an athlete might require detailed performance analytics.

When interviewing stakeholders, we might ask:
> How do users currently track their fitness progress?
> What frustrates them about existing fitness apps?
> What information do they need at different points in their fitness journey?

##### Trainers

Trainers have a dual role as both content creators and service providers:

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-Trainers.png?raw=true"/>

* **Content Creation** - Designing workout programs, exercise demonstrations
* **Client Management** - Tracking progress, adjusting plans, providing feedback
* **Expertise Sharing** - Publishing articles, tips, specialized knowledge

During our domain analysis, we'd shadow trainers to understand their workflow:
> How do you currently assign workouts to clients?
> What information do you need to assess client progress?
> How do you modify programs based on client feedback?

This helps us understand not just what data to store, but how it flows through the system from a trainer's perspective.

##### System Components

The "system" isn't a monolithic entity but a collection of automated services that:

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-System.png?raw=true"/>

* **Analyze** - Process raw data into actionable insights
* **Notify** - Alert users about goals, achievements, or necessary actions
* **Recommend** - Suggest workouts, meals, or adjustments based on progress
* **Authenticate** - Manage user identity and permissions
* **Integrate** - Connect with external services and devices

#### 2. Core Processes: The Lifeblood of Our System

Processes represent the dynamic activities that transform data and create value. Let's examine each one more deeply:

<Note type="unknown">

**TO DO:**

Here are the core processes we wish our app could help with:
1. Workout Completion
2. Meal Logging
3. Progress Tracking
4. Social Interaction
5. Challenge Participation

For each of these core processes, identify the various phases they could be composed of, and integrate the sepicific needs you heard about thanks to the user interview feedback.
</Note>

##### Workout Completion

<Note type="tip" title="Interview feedback">
During stakeholder interviews, we discovered that users often modify workouts mid-session:

> I might swap an exercise if equipment is unavailable.

> Sometimes I do extra sets if I'm feeling strong.
</Note>

This means our data model needs flexibility to handle real-time modifications while maintaining the integrity of the original plan.

This process has several distinct phases that our data model must support:

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-workout.png?raw=true"/>

1. **Planning** - Selecting or scheduling a workout
2. **Execution** - Performing exercises and recording results
3. **Reflection** - Rating difficulty, noting feedback
4. **Analysis** - Comparing to previous performance

##### Meal Logging

<Note type="tip" title="Interview feedback">
A key insight from user research:
> "I don't always log every ingredient. I need shortcuts for common meals."
</Note>

This suggests our model should support both detailed ingredient-level tracking and composite meal entries.

Nutrition tracking is complex and multi-dimensional:

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-Nutrition.png?raw=true"/>

1. **Food Entry** - Manual logging or barcode scanning
2. **Portion Estimation** - Converting real-world portions to nutritional values
3. **Pattern Recognition** - Identifying dietary habits and trends
4. **Goal Comparison** - Measuring intake against nutritional targets

##### Progress Tracking

Progress isn't just a single metric but a constellation of measurements:

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-fitness.png?raw=true"/>

* **Physical Metrics** - Weight, body measurements, body composition
* **Performance Metrics** - Strength, endurance, flexibility
* **Subjective Metrics** - Energy levels, motivation, sleep quality
* **Achievement Metrics** - Goals reached, habits maintained

The time dimension is critical here—progress happens over days, weeks, and months. Our data model must efficiently store and retrieve time-series data while supporting meaningful aggregation and visualization.

##### Social Interaction

<Note type="tip" title="Interview feedback">
Our model needs to balance privacy concerns with social features:
> I want to share my achievements, but not my weight.
> I want to see how I compare to peers, but anonymously.
</Note>

The social layer adds community dimension to individual fitness:

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-Social.png?raw=true"/>

* **Connection** - Following friends, trainers, and inspiration accounts
* **Sharing** - Publishing workouts, milestones, and achievements
* **Engagement** - Commenting, supporting, and motivating others
* **Competition** - Friendly contests and group challenges

##### Challenge Participation

Challenges add structured goals and community motivation:
<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-challenge.png?raw=true"/>

1. **Discovery** - Finding appropriate challenges
2. **Enrollment** - Joining and committing to participation
3. **Contribution** - Recording activities that count toward the challenge
4. **Ranking** - Comparing progress against other participants
5. **Completion** - Finishing and receiving recognition

#### 3. Information Flows: The Circulatory System

Information flows reveal how data moves between actors and processes, showing us where our database will need to support specific patterns of access and update.

<Note type="unknown">

**TO DO:**

Propose an information flow for the following usecases:

- User-Generated Workout Data: what happens when a user completes a workout through the app?
- Trainer-Guided Programming: what happens when a trainer prepares a workout and sends it for a user to complete?
- Wearable Device Integration: how is data recorded through wearable devices processed?

</Note>


##### User-Generated Workout Data

This flow begins when users complete workouts:

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-info_flow.png?raw=true"/>

A critical insight from studying this flow: Users need immediate feedback during workouts, which means some calculations must happen in real-time, not just in overnight batch processing.

##### Trainer-Guided Programming

This flow captures how professional guidance moves through the system:

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-info_flow2.png?raw=true"/>

The key modeling challenge here is balancing standardization (reusable workout templates) with personalization (individual adjustments).

##### Wearable Device Integration

This flow demonstrates how external data enters our ecosystem:

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-info_flow3.png?raw=true"/>

During stakeholder interviews, we discovered a critical constraint:

> Different devices track different metrics with varying accuracy and frequency.

Our data model must be flexible enough to accommodate inconsistent data sources while providing a unified view to users.

#### 4. Translating Analysis to Modeling Decisions

This domain analysis directly informs our modeling approach:

<Note type="unknown">

**TO DO:**

Based on the domain analysis we just completed, can you identify at least **5** key points we will have to keep in mind when modeling our database?
</Note>


1. The diverse user base suggests we need a flexible profile structure that can grow with user sophistication
2. The complex relationship between trainers and users requires careful modeling of permissions and visibility
3. The mid-workout modifications indicate we need separate entities for planned vs. actual workouts
4. The time-series nature of progress tracking suggests dedicated structures optimized for trend analysis
5. The social features indicate we need a robust permission system integrated with our data model

By thoroughly understanding the domain before drawing a single entity box, we ensure our data model serves real business needs rather than just theoretical correctness. This foundation will guide every subsequent modeling decision we make.

What would an entity-relationship diagram look like after this analysis? Let's move on to that next step.

## Conceptual Data Model - Main Frame

### Step 2: Entity Identification

Now, let's extract the core entities from our business requirements:

<Note type="unknown">

**TO DO:**

Based on the domain analysis, list out the entities we will represent in our database.

*hint: the solution lists 11 entities*

</Note>


1. **User** - The person using the application
2. **Profile** - Personal details, goals, and metrics
3. **Workout** - A collection of exercises performed in a session
4. **Exercise** - A specific physical activity with parameters
5. **WorkoutPlan** - A structured program of workouts over time
6. **Meal** - Food consumption with nutritional information
7. **Challenge** - Competitive events with goals and timeframes
8. **Achievement** - Recognition for meeting specific milestones
9. **Trainer** - Professional fitness instructor
10. **DeviceData** - Information synced from wearable technology
11. **Notification** - Personalized messages and reminders

### Step 3: Attribute Assignment

Let's take a few key entities and define their attributes:

<Note type="unknown">

**TO DO:**

For each entity you've listed, what attributes should you measure, make sure you indicate which of them are **primary keys**, or **foreign keys**.

Do this at least for the main four entities which are **user**, **profile**, **workout**, and **exercise**

*hint: you may have to go back and forth between entities as you realise some entities need to have some sort of relationship.*
</Note>

#### 1. **User**
- UserID (PK)
- Username
- Email
- Password (hashed)
- JoinDate
- LastLogin
- AccountStatus

#### 2. **Profile**
- ProfileID (PK)
- UserID (FK)
- FirstName
- LastName
- BirthDate
- Gender
- Height
- CurrentWeight
- TargetWeight
- FitnessGoal (enum: weight loss, muscle gain, endurance, etc.)
- ActivityLevel

#### 3.  **Workout**
- WorkoutID (PK)
- UserID (FK)
- WorkoutPlanID (FK, nullable)
- WorkoutDate
- Duration
- CaloriesBurned
- Notes
- Rating
- CompletionStatus

#### 4. **Exercise**
- ExerciseID (PK)
- Name
- Description
- Category (strength, cardio, flexibility, etc.)
- MuscleGroup
- DifficultyLevel
- DemoVideoURL

#### 5. **WorkoutPlan**
- WorkoutPlanID (PK)
- TrainerID (FK, nullable if user-generated)
- Name
- Description
- Goal (enum: strength, weight loss, endurance, flexibility, etc.)
- Level (beginner, intermediate, advanced)
- DurationWeeks
- CreationDate
- IsPublic (boolean, for shared plans)
- Tags (for searchability, like "HIIT", "Home Workouts", etc.)

#### 6. **Meal**
- MealID (PK)
- UserID (FK)
- MealDate
- MealType (enum: breakfast, lunch, dinner, snack)
- Name (optional, like "Chicken Salad" or "Meal Prep Box #3")
- Calories
- ProteinGrams
- CarbsGrams
- FatGrams
- Ingredients (JSON/text for optional ingredient-level detail)
- PortionSize (optional, grams/ml)
- Notes (user notes, like "ate half" or "very filling")

#### 7. **Challenge**
- ChallengeID (PK)
- CreatedBy (FK to TrainerID or UserID)
- Name
- Description
- StartDate
- EndDate
- GoalType (enum: distance, calories burned, number of workouts, weight lost, etc.)
- GoalTarget (numeric, e.g., "run 100 km" or "burn 10,000 calories")
- IsPublic (boolean)
- Reward (optional description, like badge, gift card, etc.)
- Rules (text or JSON for complex rules like "Only outdoor runs count")

#### 8. **Achievement**
- AchievementID (PK)
- Name
- Description
- CriteriaType (enum: workout completed, weight goal achieved, challenge won, consistency streak, etc.)
- CriteriaValue (numeric, if applicable, like "Complete 50 workouts")
- BadgeImageURL
- IsHiddenUntilEarned (boolean, for surprise achievements)
- CreatedDate

#### 9. **Trainer**
- TrainerID (PK)
- UserID (FK)  *(assuming Trainers have a User account too)*
- Certification (text)
- Specialties (list or JSON, like "strength training", "postpartum fitness")
- Biography
- WebsiteURL (optional)
- Availability (JSON or structured schedule fields)
- Rating (aggregate from user reviews, optional)

#### 10. **DeviceData**
- DeviceDataID (PK)
- UserID (FK)
- DeviceType (enum: Fitbit, Apple Watch, Garmin, etc.)
- DataType (enum: heart rate, steps, sleep, workout sync, calories, etc.)
- DataPayload (JSON, flexible to store time-series, etc.)
- SyncTimestamp
- SourceApp (optional, like "Apple Health" vs "Garmin Connect")

#### 11. **Notification**
- NotificationID (PK)
- UserID (FK)
- Type (enum: reminder, achievement unlocked, challenge update, trainer message, system alert)
- Title
- MessageBody
- CreatedAt
- IsRead (boolean)
- RelatedEntityID (nullable FK, if referencing ChallengeID, AchievementID, etc.)
- PriorityLevel (low, medium, high)

---

#### ✅ Quick Observations
- **Scalability:** Using JSON for flexible fields like `Ingredients` and `DeviceDataPayload` allows future expansion without schema overhauls.
- **User Personalization:** Lots of fields allow the system to tailor notifications, recommendations, etc.
- **Trainer-User Separation:** Clear distinction but also links between users and trainers.
- **Progress & Social Integration:** Achievements, Challenges, and Notifications are tightly aligned with your social and progress tracking goals.

### Step 4: Modeling Relationships

Now comes the critical part—defining how these entities relate to each other. Let's establish some key relationships:

<Note type="unknown">

**TO DO:**

Identify the relationships that may exist between your entities, the associated cardinality, and what additional characteristics may describe these relationships.

</Note>

Let's build a clean, professional **Entity-Relationship Diagram (ERD)** based on the entities and attributes we defined.

Here’s the structured **relationship mapping** first:

#### 🗂️ Entities and Key Relationships

| **Entity** | **Relationships** |
|------------|--------------------|
| **User** | - Has 1 Profile<br>- Has many Workouts</br><br>- Has many Meals</br><br>- Has many DeviceData records</br><br>- Has many Notifications</br><br>- Can join many Challenges</br><br>- Can earn many Achievements</br><br>- Can have zero or one Trainer</br><br>- A user can be followed by or follow many other users </br>(many-to-many)|
| **Profile** | - Belongs to 1 User |
| **Workout** | - Belongs to 1 User<br>- Can belong to 1 WorkoutPlan (nullable) </br><br>- Has many Exercises (via association) </br>|
| **Exercise** | - Can belong to many Workouts (many-to-many) |
| **WorkoutPlan** | - Created by 1 Trainer (optional)<br>- Has many Workouts</br><br>- Assigned to many Users (optional)</br> |
| **Meal** | - Belongs to 1 User |
| **Challenge** | - Created by 1 Trainer or User<br>- Has many Users (Participants) (many-to-many relationship) </br>|
| **Achievement** | - Can be earned by many Users (many-to-many) |
| **Trainer** | - Associated with many Users<br>- Creates many WorkoutPlans</br><br>- Creates many Challenges </br>|
| **DeviceData** | - Belongs to 1 User |
| **Notification** | - Belongs to 1 User |
| **UserChallengeParticipation** (Join Table) | - Tracks User participation in Challenges |
| **UserAchievement** (Join Table) | - Tracks Achievements earned by Users |
| **WorkoutExercise** (Join Table) | - Tracks Exercises within a Workout with details like sets, reps, etc. |

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-Entity_identification.png?raw=true"/>

### Step 5: Creating Junction Tables

For our many-to-many relationships, we need junction tables:

<Note type="unknown">

**TO DO:**

Many to many relationships cannot be solely be defined through the entity tables they describe, therefore identify the various many to many relationships, and design tables describing these relationships.

</Note>

Here's description of the junction tables we'll need to include many-to-many relationships in our data model.

#### WorkoutExercise
- WorkoutID (PK, FK)
- ExerciseID (PK, FK)
- SetCount
- RepCount
- Weight
- Duration
- Notes
- Order (position in workout)

#### UserChallenge
- UserID (PK, FK)
- ChallengeID (PK, FK)
- JoinDate
- CompletionStatus
- Progress
- Ranking

#### UserAchievement
- UserID
- AchievementID
- EarnedDate

#### UserFollows
- FollowerID (PK, FK to User)
- FollowingID (FK to User)
- FollowDate
- NotificationSettings

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-Entity_identification_Junction.png?raw=true"/>

### Step 5 b: Testing Our Model

Let's examine how our model would handle a real business question:

**Question:** "Show all workouts completed by User X in the last 30 days, including exercises, sets, and total volume lifted."

<Note type="unknown">

**TO DO:**

Write down the query logic that would lead to the result we asked for, you may use pseudo-code at this point.

</Note>

**Query Logic:**
1. Filter Workout table for UserID = X and WorkoutDate within last 30 days
2. Join to WorkoutExercise to get exercises performed
3. Join to Exercise to get exercise names
4. Join to WorkoutSet to get set details
5. Calculate volume (weight × reps × sets) for each exercise
6. Aggregate to get totals by workout and exercise

This demonstrates that our model can answer complex business questions that combine multiple entities and calculations.

## Logical Data Model - Main Frame

Understanding the domain and context for which you will build your data infrastructure is paramount. Now that we achieved that it is time to transalte this into a logical model that precisely describes tables, their attributes, their relationships, and cardinality in a technology agnostic fashion.

### Step 6: Logical data model

<Note type="unknown">

**TO DO:**

Use your prefered tool (we suggest [dbdiagram](https://dbdiagram.io/home)) to design the logical data model for your fitness app.

</Note>


Here's the dbml code that helps us generate the logical model:

```dbml
// FitConnect Logical Data Model

Table User {
  UserID int [pk, increment]
  Username varchar
  Email varchar
  Password varchar
  JoinDate datetime
  LastLogin datetime
  AccountStatus varchar
}

Table Profile {
  ProfileID int [pk, increment]
  UserID int [ref: - User.UserID] // User creates a Profile
  FirstName varchar
  LastName varchar
  BirthDate date
  Gender varchar
  Height float
  CurrentWeight float
  TargetWeight float
  FitnessGoal varchar
  ActivityLevel varchar
}

Table Workout {
  WorkoutID int [pk, increment]
  UserID int [ref: > User.UserID] // User starts a Workout
  WorkoutPlanID int [ref: > WorkoutPlan.WorkoutPlanID, null] // Workout is based on a WorkoutPlan
  WorkoutDate datetime
  Duration int
  CaloriesBurned float
  Notes text
  Rating int
  CompletionStatus varchar
}

Table Exercise {
  ExerciseID int [pk, increment]
  Name varchar
  Description text
  Category varchar
  MuscleGroup varchar
  DifficultyLevel varchar
  DemoVideoURL varchar
}

Table WorkoutPlan {
  WorkoutPlanID int [pk, increment]
  TrainerID int [ref: > Trainer.TrainerID, null] // Trainers create WorkoutPlans
  Name varchar
  Description text
  Goal varchar
  Level varchar
  DurationWeeks int
  CreationDate datetime
  IsPublic boolean
  Tags text
}

Table Meal {
  MealID int [pk, increment]
  UserID int [ref: > User.UserID] //
  MealDate datetime
  MealType varchar
  Name varchar
  Calories float
  ProteinGrams float
  CarbsGrams float
  FatGrams float
  Ingredients text
  PortionSize float
  Notes text
}

Table Challenge {
  ChallengeID int [pk, increment]
  CreatedBy int [ref : > User.UserID] // Users create Challenges
  Name varchar
  Description text
  StartDate datetime
  EndDate datetime
  GoalType varchar
  GoalTarget float
  IsPublic boolean
  Reward varchar
  Rules text
}

Table Achievement {
  AchievementID int [pk, increment]
  Name varchar
  Description text
  CriteriaType varchar
  CriteriaValue float
  BadgeImageURL varchar
  IsHiddenUntilEarned boolean
  CreatedDate datetime
}

Table Trainer {
  TrainerID int [pk, increment]
  UserID int [ref: > User.UserID] // Trainer trains Users
  Certification text
  Specialties text
  Biography text
  WebsiteURL varchar
  Availability text
  Rating float
}

Table DeviceData {
  DeviceDataID int [pk, increment]
  UserID int [ref: > User.UserID] // Device data belongs to User
  DeviceType varchar
  DataType varchar
  DataPayload text
  SyncTimestamp datetime
  SourceApp varchar
}

Table Notification {
  NotificationID int [pk, increment]
  UserID int [ref: > User.UserID] // Notification was sent to User
  Type varchar
  Title varchar
  MessageBody text
  CreatedAt datetime
  IsRead boolean
  RelatedEntityID int [null]
  PriorityLevel varchar
}

// Junction Tables

Table WorkoutExercise {
  WorkoutID int [pk, ref: > Workout.WorkoutID] // WorkoutExercise included in Workout
  ExerciseID int [pk, ref: > Exercise.ExerciseID] // WorkoutExercise is based on Exercise
  SetCount int
  RepCount int
  Weight float
  Duration int
  Notes text
  Order int
}

Table UserChallenge {
  UserID int [pk, ref: > User.UserID] // UserChallenge is a User
  ChallengeID int [pk, ref: > Challenge.ChallengeID] // UserChallenge take part in Challenge
  JoinDate datetime
  CompletionStatus varchar
  Progress float
  Ranking int
}

Table UserAchievement {
  UserID int [pk, ref: > User.UserID] // UserAchievement belongs to User
  AchievementID int [pk, ref: > Achievement.AchievementID] // UserAchievement achieves Achievement
  EarnedDate datetime
}

Table UserFollows {
  FollowerID int [pk, ref: > User.UserID] // FollowerID belongs to User
  FollowingID int [pk, ref: > User.UserID] // FollowingID belongs to User
  FollowDate datetime
  NotificationSettings text
}

```

## Physical Data Model - Main Frame

We now need to translate our logical model to a physical model using [dbdiagram.io](https://dbdiagram.io) for example. 

### Step 7: Physical modeling main frame

<Note type="unknown">

**TO DO:**

Translate your logical model into a physical model for postgresql. You are expected to provide the following elements :
- The sql code to create the database
- The sql code to help create access rules to the database that make sense for ensuring that:
  - administrator may have all rights on the database
  - each user may only access their personal data
  - data analysts may query the relevant data
- The sql code to produce the tables and their relationships
- OPTIONAL some tables in our schema have columns indicating the public or private nature of the data, how can you manage access to public vs private data in the app ?
</Note>

#### Creating the database

Here's the code you can use to create the postgresql database:

```sql
-- =====================================
-- Database: FitConnect
-- PostgreSQL Physical Data Model
-- =====================================

-- Create the database
CREATE DATABASE fitconnect;

-- Connect to the database (for script execution purposes)
\c fitconnect;

-- Create schema
CREATE SCHEMA fitconnect AUTHORIZATION postgres;
SET search_path TO fitconnect;
```

#### Access control

Below is a robust **access control implementation in SQL** as part of FitConnect’s **PostgreSQL physical data model**, following best practices for **role-based access control (RBAC)**.

- **Step 1: Create Database Roles**

We define **roles** (i.e., groups of permissions) rather than granting permissions directly to users. This promotes maintainability and security.

```sql
-- Base roles
CREATE ROLE fitconnect_user;
CREATE ROLE fitconnect_trainer;
CREATE ROLE fitconnect_admin;

-- Reader/writer roles for internal services (optional)
CREATE ROLE fitconnect_readonly;
CREATE ROLE fitconnect_writer;
```

- **Step 2: Create Application Users (Database Accounts)**

This is optional if you're managing users only at the application layer. But if you allow app-level DB login (e.g., analytics users or background jobs), create accounts and assign roles:

```sql
-- Sample user accounts
CREATE USER alice_user WITH PASSWORD 'secure_password';
GRANT fitconnect_user TO alice_user;

CREATE USER bob_trainer WITH PASSWORD 'secure_password';
GRANT fitconnect_trainer TO bob_trainer;

CREATE USER admin WITH PASSWORD 'super_secure_password';
GRANT fitconnect_admin TO admin;
```

- **Step 3: Grant Object-Level Access**

You’ll want to grant different levels of access to each role:

  - `fitconnect_user` (Basic user permissions)

```sql
-- Read/write access to own data
GRANT SELECT, INSERT, UPDATE ON 
  User, Profile, Workout, Meal, DeviceData, Notification 
TO fitconnect_user;

-- Read-only access to shared data
GRANT SELECT ON 
  WorkoutPlan, Challenge, Achievement, Exercise 
TO fitconnect_user;
```

  - `fitconnect_trainer` (More control)

```sql
-- All user rights
GRANT fitconnect_user TO fitconnect_trainer;

-- Additional access
GRANT INSERT, UPDATE, DELETE ON 
  WorkoutPlan, Challenge 
TO fitconnect_trainer;

-- Can assign achievements and view user progress
GRANT SELECT, UPDATE ON 
  UserChallenge, UserAchievement 
TO fitconnect_trainer;
```

  - `fitconnect_admin` (Full control)

```sql
-- Superuser-like role
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA fitconnect TO fitconnect_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA fitconnect TO fitconnect_admin;
```

- **Step 4: Row-Level Security (Optional but Powerful)**

PostgreSQL supports **Row-Level Security (RLS)** for multi-tenant safety.

Example: Only allow users to access **their own workouts**.

```sql
ALTER TABLE Workout ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_owns_workout ON Workout
  FOR ALL
  USING (UserID = current_setting('app.current_user_id')::int);
```

Then, before running queries from the app:

```sql
-- Set the current user ID at session start
SELECT set_config('app.current_user_id', '123', false);
```

You could use this mechanism for `Meal`, `DeviceData`, `Notification`, etc.

- **Step 5: Default Privileges (Future-Proofing)**

To ensure new tables follow the same access patterns:

```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA fitconnect
GRANT SELECT, INSERT, UPDATE ON TABLES TO fitconnect_user;
```

🔐 **Summary**

This setup provides:
- **RBAC (Role-Based Access Control)**
- **Least privilege** for users and trainers
- **Row-level isolation** for secure multi-tenancy
- **Clear privilege inheritance**
- **Maintainability** via grouped roles

#### Produce tables and relationships

Here's a code proposition for creating the tables and relationships in our fitconnect postgresql database:

```sql
CREATE TABLE "User" (
  "UserID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "Username" varchar,
  "Email" varchar,
  "Password" varchar,
  "JoinDate" datetime,
  "LastLogin" datetime,
  "AccountStatus" varchar
);

CREATE TABLE "Profile" (
  "ProfileID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "UserID" int,
  "FirstName" varchar,
  "LastName" varchar,
  "BirthDate" date,
  "Gender" varchar,
  "Height" float,
  "CurrentWeight" float,
  "TargetWeight" float,
  "FitnessGoal" varchar,
  "ActivityLevel" varchar
);

CREATE TABLE "Workout" (
  "WorkoutID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "UserID" int,
  "WorkoutPlanID" int,
  "WorkoutDate" datetime,
  "Duration" int,
  "CaloriesBurned" float,
  "Notes" text,
  "Rating" int,
  "CompletionStatus" varchar
);

CREATE TABLE "Exercise" (
  "ExerciseID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "Name" varchar,
  "Description" text,
  "Category" varchar,
  "MuscleGroup" varchar,
  "DifficultyLevel" varchar,
  "DemoVideoURL" varchar
);

CREATE TABLE "WorkoutPlan" (
  "WorkoutPlanID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "TrainerID" int,
  "Name" varchar,
  "Description" text,
  "Goal" varchar,
  "Level" varchar,
  "DurationWeeks" int,
  "CreationDate" datetime,
  "IsPublic" boolean,
  "Tags" text
);

CREATE TABLE "Meal" (
  "MealID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "UserID" int,
  "MealDate" datetime,
  "MealType" varchar,
  "Name" varchar,
  "Calories" float,
  "ProteinGrams" float,
  "CarbsGrams" float,
  "FatGrams" float,
  "Ingredients" text,
  "PortionSize" float,
  "Notes" text
);

CREATE TABLE "Challenge" (
  "ChallengeID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "CreatedBy" int,
  "Name" varchar,
  "Description" text,
  "StartDate" datetime,
  "EndDate" datetime,
  "GoalType" varchar,
  "GoalTarget" float,
  "IsPublic" boolean,
  "Reward" varchar,
  "Rules" text
);

CREATE TABLE "Achievement" (
  "AchievementID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "Name" varchar,
  "Description" text,
  "CriteriaType" varchar,
  "CriteriaValue" float,
  "BadgeImageURL" varchar,
  "IsHiddenUntilEarned" boolean,
  "CreatedDate" datetime
);

CREATE TABLE "Trainer" (
  "TrainerID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "UserID" int,
  "Certification" text,
  "Specialties" text,
  "Biography" text,
  "WebsiteURL" varchar,
  "Availability" text,
  "Rating" float
);

CREATE TABLE "DeviceData" (
  "DeviceDataID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "UserID" int,
  "DeviceType" varchar,
  "DataType" varchar,
  "DataPayload" text,
  "SyncTimestamp" datetime,
  "SourceApp" varchar
);

CREATE TABLE "Notification" (
  "NotificationID" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "UserID" int,
  "Type" varchar,
  "Title" varchar,
  "MessageBody" text,
  "CreatedAt" datetime,
  "IsRead" boolean,
  "RelatedEntityID" int,
  "PriorityLevel" varchar
);

CREATE TABLE "WorkoutExercise" (
  "WorkoutID" int,
  "ExerciseID" int,
  "SetCount" int,
  "RepCount" int,
  "Weight" float,
  "Duration" int,
  "Notes" text,
  "Order" int,
  PRIMARY KEY ("WorkoutID", "ExerciseID")
);

CREATE TABLE "UserChallenge" (
  "UserID" int,
  "ChallengeID" int,
  "JoinDate" datetime,
  "CompletionStatus" varchar,
  "Progress" float,
  "Ranking" int,
  PRIMARY KEY ("UserID", "ChallengeID")
);

CREATE TABLE "UserAchievement" (
  "UserID" int,
  "AchievementID" int,
  "EarnedDate" datetime,
  PRIMARY KEY ("UserID", "AchievementID")
);

CREATE TABLE "UserFollows" (
  "FollowerID" int,
  "FollowingID" int,
  "FollowDate" datetime,
  "NotificationSettings" text,
  PRIMARY KEY ("FollowerID", "FollowingID")
);

ALTER TABLE "Profile" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID");

ALTER TABLE "Workout" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID");

ALTER TABLE "Workout" ADD FOREIGN KEY ("WorkoutPlanID") REFERENCES "WorkoutPlan" ("WorkoutPlanID");

ALTER TABLE "WorkoutPlan" ADD FOREIGN KEY ("TrainerID") REFERENCES "Trainer" ("TrainerID");

ALTER TABLE "Meal" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID");

ALTER TABLE "Challenge" ADD FOREIGN KEY ("CreatedBy") REFERENCES "User" ("UserID");

ALTER TABLE "Trainer" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID");

ALTER TABLE "DeviceData" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID");

ALTER TABLE "Notification" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID");

ALTER TABLE "WorkoutExercise" ADD FOREIGN KEY ("WorkoutID") REFERENCES "Workout" ("WorkoutID");

ALTER TABLE "WorkoutExercise" ADD FOREIGN KEY ("ExerciseID") REFERENCES "Exercise" ("ExerciseID");

ALTER TABLE "UserChallenge" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID");

ALTER TABLE "UserChallenge" ADD FOREIGN KEY ("ChallengeID") REFERENCES "Challenge" ("ChallengeID");

ALTER TABLE "UserAchievement" ADD FOREIGN KEY ("UserID") REFERENCES "User" ("UserID");

ALTER TABLE "UserAchievement" ADD FOREIGN KEY ("AchievementID") REFERENCES "Achievement" ("AchievementID");

ALTER TABLE "UserFollows" ADD FOREIGN KEY ("FollowerID") REFERENCES "User" ("UserID");

ALTER TABLE "UserFollows" ADD FOREIGN KEY ("FollowingID") REFERENCES "User" ("UserID");

```

#### Public vs private data

Managing access to public data *alongside* private data (like user-specific workouts or plans) requires careful handling in PostgreSQL. Here's how you can ensure **public data is accessible to all users** without violating privacy of private records.

- **Option 1**: Use **Views** to Expose Public Data

Create SQL views that only expose rows where `IsPublic = TRUE`.

Example: Public Workout Plans

```sql
CREATE VIEW PublicWorkoutPlans AS
SELECT * FROM WorkoutPlan
WHERE IsPublic = TRUE;
```

You can then:
- Grant read access to the view only.
- Keep the base table fully protected.

```sql
GRANT SELECT ON PublicWorkoutPlans TO fitconnect_user, fitconnect_trainer;
```

This pattern is repeatable for other tables like `Challenge`, `MealTemplates`, etc.

- **Option 2**: Use **Row-Level Security (RLS)** With a Public Filter

If you're enforcing **Row-Level Security (RLS)** on a table, you can allow access to rows that are explicitly marked public.

Enable RLS on a table:
```sql
ALTER TABLE WorkoutPlan ENABLE ROW LEVEL SECURITY;
```

Create a security policy:
```sql
CREATE POLICY access_public_plans ON WorkoutPlan
FOR SELECT
USING (IsPublic = TRUE OR TrainerID = current_setting('app.current_trainer_id')::int);
```

Then in your app session:

```sql
SELECT set_config('app.current_trainer_id', '42', false);
```

This lets:
- Trainers access their own plans
- Anyone access public plans

You can do this for `Challenge`, `Meal`, `Workout`, etc.

- **Option 3**: Manage It in the Application Layer

Alternatively, if RLS is overkill or not supported in your stack:
- Always include `WHERE IsPublic = TRUE OR UserID = :current_user_id` in your queries.
- Centralize access logic in repository/service layers.

This is **easier to control and debug** in most ORMs and frameworks, but shifts the burden to the application.

🧠 Recommended Hybrid Strategy

| Layer            | Responsibility                                 |
|------------------|------------------------------------------------|
| **Database**     | Enforce RLS for critical personal data         |
| **Views**        | Safely expose public-only datasets             |
| **App Layer**    | Adds filtering and query-building flexibility  |

This gives you **secure defaults**, **developer flexibility**, and **least privilege** access.

## Cover specific usecases

Let's explore the exercise tracking portion of our model in more detail. This is crucial for the app's core functionality.

The challenge: We need to track not just which exercises users perform, but sets, reps, weights, and progress over time.

### A Three-Tier Structure

1. **Workout** (Session) - The overall fitness session
2. **WorkoutExercise** (Junction) - Which exercises were included
3. **WorkoutSet** (Details) - The specific sets performed

<Note type="unknown">

**TO DO:**

Design a WorkoutSet table that will track each specific set performed by the user.

Also produce the new logical model, you can focus only on the affected tables.

</Note>


<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-three-tier.png?raw=true"/>

#### WorkoutSet Table
- SetID (PK)
- WorkoutID (FK)
- ExerciseID (FK)
- SetNumber
- RepCount
- Weight
- Duration
- RestPeriod
- CompletionStatus
- Notes

This structure allows for:
- Tracking multiple sets with different weights/reps
- Comparing performance across workouts
- Analyzing progress over time for specific exercises

You may add the following code to your dbdiagram.io for completing the logical model:

```dbml
 Table WorkoutSet {
  SetID int [pk, increment]
  WorkoutID int [ref: > Workout.WorkoutID] // WorkoutSet is part of a Workout
  ExerciseID int [ref: > Exercise.ExerciseID] // WorkoutSet is for a specific Exercise
  SetNumber int
  RepCount int
  Weight float
  Duration int
  RestPeriod int
  CompletionStatus varchar
  Notes text
}
```

### Addressing the Design Challenge

Let's tackle our challenge question: How do we model the relationship between users, workout plans, and individual workouts?

#### The Complexity:
- Pre-defined plans that many users follow
- Custom plans created for specific users
- Users might modify a pre-defined plan

<Note type="unknown">

**TO DO:**

Design a solution for users to be able to customize their workouts based on templates.

</Note>

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-design-challenge.png?raw=true"/>

#### Our Solution:

1. **WorkoutPlanTemplate** table
   - TemplateID (PK)
   - Name
   - Description
   - DifficultyLevel
   - DurationWeeks
   - CreatorID (FK to Trainer or System)
   - IsPublic

2. **UserWorkoutPlan** table
   - PlanID (PK)
   - UserID (FK)
   - TemplateID (FK, nullable)
   - StartDate
   - CurrentWeek
   - CompletionStatus
   - IsModified

3. **PlannedWorkout** table
   - PlannedWorkoutID (PK)
   - PlanID (FK)
   - WorkoutTemplateID (FK)
   - ScheduledDay
   - ScheduledWeek
   - CompletionStatus

This approach allows users to:
- Follow standard plans without duplication in the database
- Personalize plans while maintaining the connection to the original
- Track progress through multi-week programs

You may add the following code to your dbml to complete the logical model:

```dbml

Table WorkoutPlanTemplate {
  TemplateID int [pk, increment]
  Name varchar
  Description text
  DifficultyLevel varchar
  DurationWeeks int
  CreatorID int [ref: > Trainer.TrainerID] // Created by Trainer or System
  IsPublic boolean
}

Table UserWorkoutPlan {
  PlanID int [pk, increment]
  UserID int [ref: > User.UserID] // Belongs to User
  TemplateID int [ref: > WorkoutPlanTemplate.TemplateID, null] // Optional source Template
  StartDate date
  CurrentWeek int
  CompletionStatus varchar
  IsModified boolean
}

Table PlannedWorkout {
  PlannedWorkoutID int [pk, increment]
  PlanID int [ref: > UserWorkoutPlan.PlanID] // Part of a User's plan
  WorkoutTemplateID int [ref: > WorkoutPlan.WorkoutPlanID] // Refers to a predefined workout (structure)
  ScheduledDay varchar // e.g., 'Monday'
  ScheduledWeek int
  CompletionStatus varchar
}

```

### Handling Time-Series Data

For our design decision about tracking user progress metrics over time:

**Question:** Should we store user metrics (weight, measurements) as fields in the User table that get updated, or as a series of records in a separate table?

**Analysis:**
- Storing in the User table:
   - Simple queries for current status
   - Loss of historical data
   - Limited analytical potential

- Using a separate ProgressMetrics table:
   - Preserves complete history
   - Enables trend analysis
   - Supports visualizations over time

<Note type="unknown">

**TO DO:**

Choose a solution for handling the time series data to let users track their metrics over time.

</Note>

<img src= "https://github.com/clmenyssa/images_dafs/blob/main/M01-D01-time-series.png?raw=true"/>

**Decision:** Create a dedicated **UserMetrics** table:
- MetricID (PK)
- UserID (FK)
- RecordDate
- Weight
- BodyFatPercentage
- ChestMeasurement
- WaistMeasurement
- HipMeasurement
- RestingHeartRate
- Other metrics as needed

This approach provides the foundation for powerful progress tracking and data-driven insights—a key value proposition for the app.

Here's the dbml code to add this table to the rest of our logical model:

```dbml
Table UserMetrics {
  MetricID int [pk, increment]
  UserID int [ref: > User.UserID] // Metrics belong to a User
  RecordDate date
  Weight float
  BodyFatPercentage float
  ChestMeasurement float
  WaistMeasurement float
  HipMeasurement float
  RestingHeartRate int
  Notes text [note: 'Optional field for additional context or custom metrics']
}

```

### Considering Future Expansion

A strong data model is not static — it grows with business needs. Below is how our architecture can gracefully evolve across key areas:

| **🌱 Area** | **📦 New Tables** | **🔗 Key Links** | **🧠 Things to Watch** |
|-------------|-------------------|-------------------|-------------------------|
| **🛒 E-commerce** | `Product`, `Order`, `OrderItem` | Products ↔ Exercises<br/>Orders ↔ Users | • Workout-based product suggestions<br/>• Inventory, payment & shipping |
| **👥 Group Training** | `TrainingGroup`, `GroupMembership`, `GroupSession`, `SessionAttendance` | Users ↔ Groups<br/>Sessions ↔ Trainers | • Permissions & roles<br/>• Session scheduling<br/>• Group analytics & messaging |
| **💳 Subscription Tiers** | `SubscriptionPlan`, `UserSubscription`, `PaymentHistory` | Users ↔ Plans<br/>Plans ↔ Payments | • Feature-based access<br/>• Trial periods<br/>• Plan changes & renewals |
| **🥗 Nutrition** | `MealPlan`, `PlannedMeal`, `MealFood`, `FoodItem` | Users ↔ MealPlans<br/>Meals ↔ Foods | • Calorie targets<br/>• Dietary restrictions<br/>• Grocery list generation |
| **🤖 AI Coaching** | `WorkoutRecommendation`, `UserPreference`, `FeedbackResponse`, `AIModel` | Recommendations ↔ History<br/>Feedback ↔ Models | • Personalization logic<br/>• Model versioning<br/>• A/B testing hooks |

Our model's modular design makes these expansions straightforward without requiring a complete restructure.

### Conclusion

Through this exercise, we've created a comprehensive data model for a complex fitness application. We've:

<Note type="tip" title="Learning Outcomes">

1. Analyzed the business domain to understand requirements
2. Identified key entities and their attributes
3. Established relationships between entities
4. Designed junction tables for many-to-many relationships
5. Created specialized structures for complex features
6. Tested the model against business questions
7. Considered future expansion needs

</Note>

Remember Elena from our lesson? Just like her healthcare system, **our fitness app isn't just tracking data—it's modeling an experience**.  

The database structure we've designed empowers users to transform their fitness journey from numbers into meaningful insights and progress.