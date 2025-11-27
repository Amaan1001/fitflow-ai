import streamlit as st
import random
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from src.user_profile import UserProfile, WorkoutLog
from src.rag_engine import RAGEngine
from src.llm_handler import LLMHandler
from src.workout_generator import WorkoutGenerator
from src.gamification import GamificationEngine
from src.recovery_analyzer import RecoveryAnalyzer
from src.muscle_heatmap import generate_muscle_heatmap_svg, calculate_coverage_score
from src.custom_styles import CUSTOM_CSS
from config import (
    APP_TITLE, APP_ICON, SESSION_USER_PROFILE, SESSION_CHAT_HISTORY, 
    SESSION_WORKOUT_PLAN, SESSION_CURRENT_DAY, SESSION_WORKOUT_LOGS,
    USER_PROFILES_FILE, WORKOUT_LOGS_FILE, MOTIVATIONAL_QUOTES, STORAGE_DIR
)
import uuid

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

if SESSION_USER_PROFILE not in st.session_state:
    st.session_state[SESSION_USER_PROFILE] = None
if SESSION_CHAT_HISTORY not in st.session_state:
    st.session_state[SESSION_CHAT_HISTORY] = []
if SESSION_WORKOUT_PLAN not in st.session_state:
    st.session_state[SESSION_WORKOUT_PLAN] = None
if SESSION_CURRENT_DAY not in st.session_state:
    st.session_state[SESSION_CURRENT_DAY] = 1
if SESSION_WORKOUT_LOGS not in st.session_state:
    st.session_state[SESSION_WORKOUT_LOGS] = []
if 'completed_exercises_today' not in st.session_state:
    st.session_state.completed_exercises_today = set()

@st.cache_resource
def initialize_system():
    rag_engine = RAGEngine()
    rag_engine.initialize_database()
    llm_handler = LLMHandler()
    workout_gen = WorkoutGenerator(rag_engine, llm_handler)
    gamification = GamificationEngine(STORAGE_DIR)
    recovery = RecoveryAnalyzer(STORAGE_DIR)
    return rag_engine, llm_handler, workout_gen, gamification, recovery

rag_engine, llm_handler, workout_gen, gamification, recovery = initialize_system()

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def create_demo_users():
    demo_users = [
        {
            "user_id": "demo_user_001",
            "name": "Alex Johnson",
            "fitness_goal": "muscle_gain",
            "experience_level": "beginner",
            "days_per_week": 3,
            "session_duration": 60,
            "injuries_limitations": "",
            "total_workouts": 12,
            "current_streak": 4
        },
        {
            "user_id": "demo_user_002",
            "name": "Sarah Williams",
            "fitness_goal": "weight_loss",
            "experience_level": "intermediate",
            "days_per_week": 4,
            "session_duration": 45,
            "injuries_limitations": "Knee sensitivity",
            "total_workouts": 24,
            "current_streak": 7
        },
        {
            "user_id": "demo_user_003",
            "name": "Mike Chen",
            "fitness_goal": "strength",
            "experience_level": "advanced",
            "days_per_week": 5,
            "session_duration": 75,
            "injuries_limitations": "",
            "total_workouts": 58,
            "current_streak": 12
        }
    ]
    return demo_users

def load_demo_user(demo_user_data):
    profile = UserProfile(
        user_id=demo_user_data['user_id'],
        name=demo_user_data['name'],
        fitness_goal=demo_user_data['fitness_goal'],
        experience_level=demo_user_data['experience_level'],
        days_per_week=demo_user_data['days_per_week'],
        session_duration=demo_user_data['session_duration'],
        injuries_limitations=demo_user_data['injuries_limitations'],
        total_workouts=demo_user_data['total_workouts'],
        current_streak=demo_user_data['current_streak']
    )
    return profile

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .exercise-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: white;
    }
    .success-badge {
        background: #48bb78;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
    }
    .motivational-quote {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-style: italic;
        font-size: 1.1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### {APP_ICON} FitFlow AI")
    st.markdown("---")
    
    if st.session_state[SESSION_USER_PROFILE] is None:
        st.info("🎯 Get Started!")
        
        demo_users = create_demo_users()
        
        with st.expander("🚀 Quick Start: Load Demo User", expanded=True):
            demo_names = [f"{u['name']} ({u['fitness_goal'].replace('_', ' ').title()})" for u in demo_users]
            selected_demo = st.selectbox("Choose a demo profile:", demo_names)
            
            if st.button("Load Demo Profile", type="primary"):
                demo_idx = demo_names.index(selected_demo)
                profile = load_demo_user(demo_users[demo_idx])
                st.session_state[SESSION_USER_PROFILE] = profile
                
                with st.spinner("Generating workout plan..."):
                    workout_plan = workout_gen.generate_workout_plan(profile)
                    st.session_state[SESSION_WORKOUT_PLAN] = workout_plan
                
                st.success(f"Welcome back, {profile.name}! 🎉")
                st.rerun()
        
        st.markdown("---")
        st.markdown("**Or Create New Profile:**")
        
        with st.form("profile_form"):
            name = st.text_input("Name*", placeholder="John Doe")
            
            fitness_goal = st.selectbox(
                "Fitness Goal*",
                options=["muscle_gain", "weight_loss", "strength", "general_fitness"],
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            experience_level = st.selectbox(
                "Experience Level*",
                options=["beginner", "intermediate", "advanced"],
                format_func=lambda x: x.title()
            )
            
            days_per_week = st.slider("Days per Week", min_value=3, max_value=5, value=3)
            
            session_duration = st.slider("Session Duration (minutes)", min_value=30, max_value=90, value=60, step=15)
            
            injuries = st.text_area("Injuries or Limitations", placeholder="e.g., Lower back pain, knee injury...")
            
            submitted = st.form_submit_button("Create Profile", type="primary")
            
            if submitted:
                if not name:
                    st.error("Please enter your name")
                else:
                    profile = UserProfile(
                        user_id=str(uuid.uuid4()),
                        name=name,
                        fitness_goal=fitness_goal,
                        experience_level=experience_level,
                        days_per_week=days_per_week,
                        session_duration=session_duration,
                        injuries_limitations=injuries
                    )
                    
                    profile.save_to_file(USER_PROFILES_FILE)
                    st.session_state[SESSION_USER_PROFILE] = profile
                    
                    with st.spinner("Generating your personalized workout plan..."):
                        workout_plan = workout_gen.generate_workout_plan(profile)
                        st.session_state[SESSION_WORKOUT_PLAN] = workout_plan
                    
                    st.success("Profile created! 🎉")
                    st.rerun()
    
    else:
        profile = st.session_state[SESSION_USER_PROFILE]
        
        st.markdown("### 👤 Your Profile")
        st.write(f"**{profile.name}**")
        st.write(f"🎯 {profile.fitness_goal.replace('_', ' ').title()}")
        st.write(f"📊 {profile.experience_level.title()}")
        st.write(f"📅 {profile.days_per_week} days/week")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Workouts", profile.total_workouts)
        with col2:
            st.metric("Current Streak", f"{profile.current_streak} 🔥")
        
        st.markdown("---")
        
        if st.session_state[SESSION_WORKOUT_PLAN]:
            st.markdown("### 📋 Your Plan")
            plan = st.session_state[SESSION_WORKOUT_PLAN]
            
            for day in plan['weekly_plan']:
                muscle_groups = ", ".join([mg.title() for mg in day['muscle_groups']])
                is_current = day['day'] == st.session_state[SESSION_CURRENT_DAY]
                prefix = "👉 " if is_current else "    "
                st.write(f"{prefix}**Day {day['day']}:** {muscle_groups}")
            
            st.markdown("---")
            
            if st.button("🔄 Regenerate Plan"):
                with st.spinner("Generating new plan..."):
                    new_plan = workout_gen.generate_workout_plan(profile)
                    st.session_state[SESSION_WORKOUT_PLAN] = new_plan
                st.success("New plan generated!")
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", type="secondary"):
            st.session_state[SESSION_USER_PROFILE] = None
            st.session_state[SESSION_WORKOUT_PLAN] = None
            st.session_state[SESSION_CHAT_HISTORY] = []
            st.session_state[SESSION_WORKOUT_LOGS] = []
            st.session_state.completed_exercises_today = set()
            llm_handler.clear_memory()
            st.rerun()

if st.session_state[SESSION_USER_PROFILE] is None:
    
    st.markdown('<p class="main-header">Welcome to FitFlow AI! 🏋️‍♂️</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h2>Your Personal AI Gym Concierge</h2>
            <p style='font-size: 1.2rem; color: #666;'>
                Get personalized workout plans, expert guidance, and stay motivated—all powered by AI
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: rgb(118, 75, 162); border-radius: 10px;'>
            <h3>🎯 Personalized Plans</h3>
            <p>AI-generated workouts tailored to your goals, experience, and available equipment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: rgb(118, 75, 162); border-radius: 10px;'>
            <h3>💬 24/7 AI Trainer</h3>
            <p>Ask questions about form, technique, and get instant expert guidance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: rgb(118, 75, 162); border-radius: 10px;'>
            <h3>📈 Track Progress</h3>
            <p>Monitor your workouts, streaks, and improvements over time</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center;'>
        <h2>🚀 Ready to Transform Your Fitness Journey?</h2>
        <p style='font-size: 1.1rem;'>Get started in the sidebar → Create your profile or try a demo!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("### ✨ Why FitFlow AI?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **For Gym Members:**
        - ✅ Personal trainer guidance without the cost
        - ✅ Workouts that match your gym's equipment
        - ✅ Never feel lost or confused in the gym
        - ✅ Stay accountable with tracking
        """)
    
    with col2:
        st.markdown("""
        **For Gym Owners:**
        - 💰 Reduce member churn by 15-25%
        - 💰 Increase supplement sales through recommendations
        - 💰 Deliver premium experience without hiring trainers
        - 💰 Data insights on member behavior
        """)

else:
    
    profile = st.session_state[SESSION_USER_PROFILE]
    
    st.markdown(f'<p class="main-header">{APP_ICON} Welcome back, {profile.name}!</p>', unsafe_allow_html=True)
    
    quote = random.choice(MOTIVATIONAL_QUOTES)
    st.markdown(f'<div class="motivational-quote">💪 {quote}</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "💬 AI Chat", 
        "📅 Today's Workout", 
        "🗺️ Muscle Heatmap",
        "📚 Exercise Library",
        "🏆 Achievements",
        "📊 Progress", 
        "💊 Supplements"
    ])
    
    with tab1:
        st.header("Chat with Your AI Trainer")
        
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state[SESSION_CHAT_HISTORY]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        user_input = st.chat_input("Ask me anything about your workout...")
        
        if user_input:
            st.session_state[SESSION_CHAT_HISTORY].append({
                "role": "user",
                "content": user_input
            })
            
            with st.chat_message("user"):
                st.markdown(user_input)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    
                    workout_plan = st.session_state[SESSION_WORKOUT_PLAN]
                    
                    query_lower = user_input.lower()
                    
                    if any(word in query_lower for word in ["supplement", "protein", "creatine", "nutrition"]):
                        supplements = rag_engine.get_supplements_for_goal(profile.fitness_goal)
                        
                        supp_context = "\n".join([
                            f"- {s['name']}: {s['description']} (${s['price']})"
                            for s in supplements
                        ])
                        
                        response = llm_handler.recommend_supplements(
                            fitness_goal=profile.fitness_goal.replace('_', ' ').title(),
                            available_supplements=supp_context
                        )
                    
                    elif any(word in query_lower for word in ["how", "form", "technique", "do i", "visual", "example", "show me"]):
                        # Check if user is asking for multiple examples or just one
                        num_results = 3 if any(word in query_lower for word in ["visual", "example", "show", "alternatives"]) else 1
                        
                        # Extract muscle groups from query
                        muscle_group_keywords = {
                            "back": "back",
                            "chest": "chest",
                            "legs": "legs",
                            "leg": "legs",
                            "shoulders": "shoulders",
                            "shoulder": "shoulders",
                            "arms": "arms",
                            "arm": "arms",
                            "biceps": "arms",
                            "triceps": "arms",
                            "core": "core",
                            "abs": "core",
                            "cardio": "cardio"
                        }
                        
                        detected_muscle_groups = []
                        for keyword, muscle_group in muscle_group_keywords.items():
                            if keyword in query_lower:
                                if muscle_group not in detected_muscle_groups:
                                    detected_muscle_groups.append(muscle_group)
                        
                        exercises = rag_engine.search_exercises(
                            query=user_input,
                            gym_id=profile.gym_id,
                            muscle_groups=detected_muscle_groups if detected_muscle_groups else None,
                            n_results=num_results
                        )
                        
                        if exercises:
                            # Build context from retrieved exercises
                            if len(exercises) == 1:
                                ex = exercises[0]
                                context = f"**{ex['name']}**\n\nInstructions: {ex['instructions']}\nVideo: {ex['video_url']}"
                            else:
                                # Multiple exercises
                                context = "Here are relevant exercises:\n\n"
                                for idx, ex in enumerate(exercises, 1):
                                    context += f"{idx}. **{ex['name']}**\n"
                                    context += f"   - Instructions: {ex['instructions']}\n"
                                    context += f"   - Video: {ex['video_url']}\n\n"
                            
                            response = llm_handler.answer_with_exercise_context(
                                user_question=user_input,
                                context=context
                            )
                            
                            st.markdown(response)
                            
                            # Display visual examples
                            st.markdown("---")
                            st.markdown("### 📹 Visual Examples")
                            
                            for ex in exercises:
                                st.markdown(f"**{ex['name']}**")
                                
                                col1, col2 = st.columns([1, 1])
                                with col1:
                                    if ex.get('gif_url'):
                                        st.image(ex['gif_url'], caption=f"{ex['name']} demonstration", use_container_width=True)
                                    else:
                                        st.info("GIF not available")
                                
                                with col2:
                                    st.markdown(f"**Equipment:** {', '.join(ex['equipment'])}")
                                    st.markdown(f"**Difficulty:** {ex['difficulty'].title()}")
                                    st.markdown(f"**Muscle Group:** {ex['muscle_group'].title()}")
                                    st.markdown(f"[📹 Watch Video Tutorial]({ex['video_url']})")
                                
                                st.markdown("---")
                        else:
                            response = llm_handler.chat_with_context(
                                user_message=user_input,
                                system_context=profile.get_profile_summary()
                            )
                            st.markdown(response)
                    
                    elif "today" in query_lower or "workout" in query_lower:
                        current_workout = workout_plan['weekly_plan'][st.session_state[SESSION_CURRENT_DAY] - 1]
                        
                        exercises_list = "\n".join([
                            f"{i+1}. {ex['name']} - {ex['sets']} sets × {ex['reps']} reps"
                            for i, ex in enumerate(current_workout['exercises'])
                        ])
                        
                        context = f"""
Today's Workout (Day {current_workout['day']}):
Target: {', '.join([mg.title() for mg in current_workout['muscle_groups']])}

Exercises:
{exercises_list}

Estimated Duration: {current_workout['estimated_duration']} minutes
Estimated Calories: {current_workout['estimated_calories']} kcal
"""
                        
                        response = llm_handler.chat_with_context(
                            user_message=user_input,
                            system_context=f"{profile.get_profile_summary()}\n{context}"
                        )
                        st.markdown(response)
                    
                    else:
                        response = llm_handler.chat_with_context(
                            user_message=user_input,
                            system_context=profile.get_profile_summary()
                        )
                        st.markdown(response)
                    
                    st.session_state[SESSION_CHAT_HISTORY].append({
                        "role": "assistant",
                        "content": response
                    })
        
        st.markdown("---")
        st.subheader("💡 Quick Questions")
        col1, col2, col3 = st.columns(3)
        
        quick_questions = [
            "What's my workout today?",
            "How do I improve my bench press form?",
            "What supplements should I take for muscle gain?"
        ]
        
        for idx, (col, question) in enumerate(zip([col1, col2, col3], quick_questions)):
            with col:
                if st.button(question, key=f"quick_q_{idx}"):
                    st.session_state[SESSION_CHAT_HISTORY].append({
                        "role": "user",
                        "content": question
                    })
                    st.rerun()
    
    with tab2:
        st.header("Today's Workout")
        
        if st.session_state[SESSION_WORKOUT_PLAN]:
            plan = st.session_state[SESSION_WORKOUT_PLAN]
            current_day = st.session_state[SESSION_CURRENT_DAY]
            
            # Day selector
            selected_day = st.selectbox(
                "Select Day",
                options=list(range(1, plan['total_days'] + 1)),
                index=current_day - 1,
                format_func=lambda x: f"Day {x}",
                key="day_selector"
            )
            st.session_state[SESSION_CURRENT_DAY] = selected_day
            
            workout = plan['weekly_plan'][selected_day - 1]
            
            st.markdown(f"### Day {workout['day']}: {', '.join([mg.title() for mg in workout['muscle_groups']])}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Exercises", len(workout['exercises']))
            with col2:
                st.metric("Est. Duration", f"{workout['estimated_duration']} min")
            with col3:
                st.metric("Est. Calories", f"{workout['estimated_calories']} kcal")
            
            st.markdown("---")
            
            # Mark Day Complete button
            if st.button("✅ Mark Day Complete", type="primary", use_container_width=True):
                # Create workout log
                log = WorkoutLog(
                    log_id=str(uuid.uuid4()),
                    user_id=profile.user_id,
                    date=datetime.now(),
                    day_number=selected_day,
                    exercises_completed=list(st.session_state.completed_exercises_today),
                    total_exercises=len(workout['exercises']),
                    duration_minutes=workout['estimated_duration'],
                    calories_burned=workout['estimated_calories']
                )
                log.save_to_file(WORKOUT_LOGS_FILE)
                
                # Update profile
                profile.total_workouts += 1
                profile.current_streak += 1
                profile.last_workout_date = datetime.now().isoformat()
                profile.save_to_file(USER_PROFILES_FILE)
                st.session_state[SESSION_USER_PROFILE] = profile
                
                # Update gamification
                total_sets = sum(ex.get('sets', 3) for ex in workout['exercises'])
                total_reps = sum(ex.get('sets', 3) * ex.get('reps', 10) for ex in workout['exercises'])
                
                gamification_result = gamification.update_workout_completion(
                    user_id=profile.user_id,
                    exercises_completed=len(workout['exercises']),
                    total_sets=total_sets,
                    total_reps=total_reps
                )
                
                # Save workout intensity for recovery tracking
                workout_data = {
                    'total_sets': total_sets,
                    'total_reps': total_reps,
                    'muscle_groups': workout['muscle_groups']
                }
                intensity = recovery.calculate_intensity(workout_data, profile.experience_level)
                recovery.save_workout_intensity(profile.user_id, intensity)
                
                # Show success message
                st.success("🎉 Workout completed! Great job!")
                
                # Show XP gained
                xp_result = gamification_result['xp_result']
                if xp_result['leveled_up']:
                    st.balloons()
                    st.success(f"🎊 LEVEL UP! You're now Level {xp_result['new_level']}!")
                
                st.info(f"💫 +{xp_result['xp_gained']} XP earned!")
                
                # Show newly unlocked achievements
                if gamification_result['newly_unlocked']:
                    st.markdown("### 🏆 New Achievements Unlocked!")
                    for ach in gamification_result['newly_unlocked']:
                        st.markdown(f"**{ach.icon} {ach.name}** - {ach.description}")
                
                st.session_state.completed_exercises_today = set()
                st.rerun()
            
            st.markdown("---")
            
            completed_count = len(st.session_state.completed_exercises_today)
            total_count = len(workout['exercises'])
            progress = completed_count / total_count if total_count > 0 else 0
            
            st.progress(progress)
            st.write(f"**Progress:** {completed_count}/{total_count} exercises completed")
            
            st.markdown("---")
            
            for idx, exercise in enumerate(workout['exercises'], 1):
                exercise_id = exercise['id']
                is_completed = exercise_id in st.session_state.completed_exercises_today
                
                with st.expander(
                    f"{'✅' if is_completed else '⬜'} Exercise {idx}: {exercise['name']}" + 
                    f" ({exercise['difficulty'].title()})",
                    expanded=not is_completed
                ):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**💪 Muscle Group:** {exercise['muscle_group'].title()}")
                        st.markdown(f"**🏋️ Equipment:** {', '.join(exercise['equipment'])}")
                        st.markdown(f"**📊 Sets × Reps:** {exercise['sets']} × {exercise['reps']}")
                        
                        if exercise.get('gif_url'):
                            st.image(exercise['gif_url'], width=300)
                        
                        st.markdown("**📝 Instructions:**")
                        st.write(exercise['instructions'])
                        
                        st.markdown(f"**📹 [Watch Video Tutorial]({exercise['video_url']})**")
                        
                        if exercise.get('alternatives'):
                            with st.expander("🔄 Alternative Exercises"):
                                for alt_id in exercise['alternatives']:
                                    alt_ex = rag_engine.get_exercise_by_id(alt_id)
                                    if alt_ex:
                                        if st.button(f"Switch to: {alt_ex['name']}", key=f"alt_{exercise_id}_{alt_id}"):
                                            st.info(f"Switched to {alt_ex['name']}")
                    
                    with col2:
                        st.markdown("### Track Sets")
                        
                        for set_num in range(1, exercise['sets'] + 1):
                            set_key = f"set_{exercise_id}_{set_num}"
                            st.checkbox(f"Set {set_num}", key=set_key)
                        
                        st.markdown("---")
                        
                        if st.button(f"✓ Complete Exercise", key=f"complete_{exercise_id}", type="secondary"):
                            st.session_state.completed_exercises_today.add(exercise_id)
                            st.rerun()
                        
                        if is_completed:
                            st.markdown('<span class="success-badge">✓ Completed</span>', unsafe_allow_html=True)
        
        else:
            st.warning("No workout plan generated yet!")
    
    with tab3:
        st.header("🗺️ Your Muscle Coverage")
        
        # Get recovery status for each muscle group
        muscle_status = recovery.get_muscle_recovery_status(profile.user_id)
        
        # Calculate coverage score
        coverage = calculate_coverage_score(muscle_status)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display heatmap
            svg = generate_muscle_heatmap_svg(muscle_status)
            import streamlit.components.v1 as components
            components.html(svg, height=650, scrolling=False)
        
        with col2:
            # Coverage score
            st.markdown(f'''
            <div class="stat-card">
                <p>Weekly Coverage</p>
                <h3>{coverage}%</h3>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown("### Muscle Groups Status")
            
            for muscle, status in muscle_status.items():
                days = status['days_since_workout']
                color_map = {
                    "red": "Recently worked",
                    "orange": "Recovering",
                    "yellow": "Ready to train",
                    "blue": "Needs attention"
                }
                
                badge_class = "primary" if status['color'] == "red" else "warning" if status['color'] in ["orange", "yellow"] else "success"
                
                st.markdown(f'''
                <div class="custom-card">
                    <strong>{muscle.title()}</strong><br/>
                    <span class="badge badge-{badge_class}">{color_map.get(status['color'], 'Unknown')}</span><br/>
                    <small>{days} days since last workout</small>
                </div>
                ''', unsafe_allow_html=True)
            
            # AI recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Recommendations")
            
            # Find neglected muscles
            neglected = [m for m, s in muscle_status.items() if s['days_since_workout'] > 6]
            
            if neglected:
                st.info(f"💡 Focus on: {', '.join([m.title() for m in neglected])}")
                
                if st.button("Get Workout Plan for Neglected Muscles"):
                    # Generate workout for neglected muscles
                    with st.spinner("Creating personalized workout..."):
                        exercises = rag_engine.search_exercises(
                            query=f"{' '.join(neglected)} workout",
                            gym_id=profile.gym_id,
                            muscle_groups=neglected,
                            n_results=5
                        )
                        
                        st.success("**Recommended Exercises:**")
                        for ex in exercises[:3]:
                            st.markdown(f"- **{ex['name']}** ({ex['muscle_group']})")
            else:
                st.success("✅ Great balance! All muscle groups trained recently.")
    
    with tab4:
        st.header("📚 Exercise Library")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_muscle = st.multiselect(
                "Muscle Groups",
                ["chest", "back", "shoulders", "arms", "legs", "core", "cardio"],
                default=[]
            )
        
        with col2:
            filter_difficulty = st.selectbox(
                "Difficulty",
                ["All", "beginner", "intermediate", "advanced"]
            )
        
        with col3:
            search_query = st.text_input("🔍 Search exercises", placeholder="e.g., bench press")
        
        # Get exercises
        all_exercises = rag_engine.exercises_data
        
        # Apply filters
        filtered = all_exercises
        
        if filter_muscle:
            filtered = [ex for ex in filtered if ex['muscle_group'] in filter_muscle]
        
        if filter_difficulty != "All":
            filtered = [ex for ex in filtered if ex['difficulty'] == filter_difficulty]
        
        if search_query:
            filtered = [ex for ex in filtered if search_query.lower() in ex['name'].lower()]
        
        st.markdown(f"**Found {len(filtered)} exercises**")
        
        # Display exercises in grid
        cols_per_row = 3
        for i in range(0, len(filtered), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(filtered):
                    ex = filtered[i + j]
                    with col:
                        with st.expander(f"**{ex['name']}**", expanded=False):
                            if ex.get('gif_url'):
                                st.image(ex['gif_url'], use_container_width=True)
                            
                            st.markdown(f"**Muscle:** {ex['muscle_group'].title()}")
                            st.markdown(f"**Difficulty:** {ex['difficulty'].title()}")
                            st.markdown(f"**Equipment:** {', '.join(ex['equipment'])}")
                            st.markdown(f"**Instructions:**")
                            st.write(ex['instructions'])
                            st.markdown(f"[📹 Watch Tutorial]({ex['video_url']})")
    
    with tab5:
        st.header("🏆 Achievements & Progress")
        
        # Get user stats
        stats = gamification.get_user_stats(profile.user_id)
        level_progress = gamification.get_level_progress(stats)
        
        # Top stats row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="stat-card">
                <p>Level</p>
                <h3>{stats.level}</h3>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="stat-card">
                <p>Total XP</p>
                <h3>{stats.xp}</h3>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="stat-card">
                <p>Streak</p>
                <h3>{stats.current_streak} 🔥</h3>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="stat-card">
                <p>Achievements</p>
                <h3>{stats.achievements_unlocked}</h3>
            </div>
            ''', unsafe_allow_html=True)
        
        # Level progress
        st.markdown("### Level Progress")
        progress_pct = level_progress['progress_percentage']
        st.markdown(f'''
        <div class="custom-progress">
            <div class="custom-progress-bar" style="width: {progress_pct}%"></div>
        </div>
        <p style="text-align: center; margin-top: 0.5rem;">
            {level_progress['xp_in_level']} / {level_progress['xp_for_next_level']} XP to Level {stats.level + 1}
        </p>
        ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Achievements
        st.markdown("### 🏅 Your Achievements")
        
        achievements = gamification.get_achievements(profile.user_id)
        
        # Group by category
        categories = {}
        for ach in achievements:
            if ach.category not in categories:
                categories[ach.category] = []
            categories[ach.category].append(ach)
        
        for category, achs in categories.items():
            st.markdown(f"#### {category.title()} Achievements")
            
            for ach in achs:
                unlocked_class = "unlocked" if ach.unlocked else ""
                
                # Determine progress display
                if ach.category == "workout":
                    progress_val = stats.total_workouts
                elif ach.category == "streak":
                    progress_val = stats.current_streak
                elif "sets" in ach.id:
                    progress_val = stats.total_sets
                elif "reps" in ach.id:
                    progress_val = stats.total_reps
                else:
                    progress_val = 0
                
                unlock_text = f"Unlocked {ach.unlocked_date[:10]}" if ach.unlocked else f"Progress: {progress_val}/{ach.requirement}"
                
                st.markdown(f'''
                <div class="achievement-card {unlocked_class}">
                    <div class="achievement-icon">{ach.icon}</div>
                    <div style="flex: 1;">
                        <strong>{ach.name}</strong><br/>
                        <small>{ach.description}</small><br/>
                        <small style="opacity: 0.7;">{unlock_text}</small>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    with tab6:
        st.header("Your Progress")
        
        logs = WorkoutLog.load_user_logs(WORKOUT_LOGS_FILE, profile.user_id)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Workouts",
                value=profile.total_workouts,
                delta=f"+{len(logs)} logged"
            )
        
        with col2:
            st.metric(
                label="Current Streak",
                value=f"{profile.current_streak} days",
                delta="🔥 Keep it up!"
            )
        
        with col3:
            total_calories = sum([log.calories_burned for log in logs])
            st.metric(
                label="Total Calories",
                value=f"{total_calories} kcal",
                delta="Burned"
            )
        
        with col4:
            completion_rate = (len(logs) / (profile.total_workouts or 1)) * 100
            st.metric(
                label="Completion Rate",
                value=f"{completion_rate:.0f}%",
                delta="This month"
            )
        
        st.markdown("---")
        
        if logs:
            st.subheader("📈 Workout Frequency")
            
            dates = [log.date.strftime("%Y-%m-%d") for log in logs[-30:]]
            workout_counts = {}
            for date in dates:
                workout_counts[date] = workout_counts.get(date, 0) + 1
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(workout_counts.keys()),
                    y=list(workout_counts.values()),
                    marker_color='rgb(102, 126, 234)'
                )
            ])
            
            fig.update_layout(
                title="Workouts Per Day (Last 30 Days)",
                xaxis_title="Date",
                yaxis_title="Workouts",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            st.subheader("📅 Recent Workouts")
            
            for log in logs[:10]:
                with st.expander(f"Day {log.day_number} - {log.date.strftime('%B %d, %Y')}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Duration:** {log.duration_minutes} min")
                    with col2:
                        st.write(f"**Exercises:** {log.exercises_completed}/{log.total_exercises}")
                    with col3:
                        st.write(f"**Calories:** {log.calories_burned} kcal")
                    
                    if log.notes:
                        st.write(f"**Notes:** {log.notes}")
        
        else:
            st.info("📊 No workout history yet. Complete your first workout to see progress!")
            
            st.markdown("""
            <div style='text-align: center; padding: 3rem; background: #f7fafc; border-radius: 10px;'>
                <h3>🚀 Start Your Fitness Journey Today!</h3>
                <p>Track your workouts to see amazing visualizations of your progress</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab7:
        st.header("Recommended Supplements")
        
        supplements = rag_engine.get_supplements_for_goal(profile.fitness_goal)
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
            <h3>🎯 Supplements for Your Goal: {profile.fitness_goal.replace('_', ' ').title()}</h3>
            <p>Based on your fitness goal, here are our AI-recommended supplements</p>
        </div>
        """, unsafe_allow_html=True)
        
        if supplements:
            cols = st.columns(2)
            
            for idx, supp in enumerate(supplements):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div style='border: 2px solid #e0e0e0; border-radius: 10px; padding: 1.5rem; margin-bottom: 1rem; background: white;'>
                        <h3>{supp['name']}</h3>
                        <p style='color: #666;'>{supp['description']}</p>
                        <p style='font-size: 1.5rem; color: #667eea; font-weight: bold;'>${supp['price']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("**Benefits:**")
                    for benefit in supp['benefits']:
                        st.write(f"✓ {benefit}")
                    
                    if st.button(f"Learn More About {supp['name']}", key=f"supp_{supp['id']}"):
                        with st.spinner("Getting AI recommendation..."):
                            response = llm_handler.recommend_supplements(
                                fitness_goal=profile.fitness_goal.replace('_', ' ').title(),
                                available_supplements=f"{supp['name']}: {supp['description']}"
                            )
                            st.info(response)
                    
                    st.markdown("---")
        
        else:
            st.info("No specific supplement recommendations for your goal right now.")
        
        st.markdown("---")
        
        st.subheader("💬 Ask About Supplements")
        supp_question = st.text_input("Have a question about supplements?", placeholder="e.g., When should I take protein?")
        
        if st.button("Ask AI", key="ask_supp"):
            if supp_question:
                with st.spinner("Getting answer..."):
                    all_supps = "\n".join([f"- {s['name']}: {s['description']}" for s in rag_engine.supplements_data])
                    response = llm_handler.recommend_supplements(
                        fitness_goal=profile.fitness_goal.replace('_', ' ').title(),
                        available_supplements=all_supps
                    )
                    st.success("AI Response:")
                    st.write(response)
        
        st.markdown("---")
        
        st.markdown("""
        <div style='background: #fff3cd; padding: 1rem; border-radius: 10px; border-left: 4px solid #ffc107;'>
            <strong>⚠️ Disclaimer:</strong> Supplement recommendations are for informational purposes only. 
            Consult with a healthcare professional before starting any supplement regimen.
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p><strong>FitFlow AI</strong> - Your Personal Gym Concierge 🏋️</p>
        <p><small>Built with LangChain, Ollama & RAG Technology</small></p>
        <p><small>© 2024 FitFlow AI. Empowering fitness journeys with AI.</small></p>
    </div>
    """, unsafe_allow_html=True)