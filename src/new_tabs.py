# New Tab Implementations for FitFlow AI
# This file contains the code for the new tabs: Muscle Heatmap, Exercise Library, and Achievements

# TAB 3: MUSCLE HEATMAP
muscle_heatmap_tab = """
    with tab3:
        st.header("🗺️ Your Muscle Coverage")
        
        #Get recovery status for each muscle group
        muscle_status = recovery.get_muscle_recovery_status(profile.user_id)
        
        # Calculate coverage score
        coverage = calculate_coverage_score(muscle_status)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display heatmap
            svg = generate_muscle_heatmap_svg(muscle_status)
            st.markdown(f'<div class="muscle-heatmap">{svg}</div>', unsafe_allow_html=True)
        
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
                
                st.markdown(f'''
                <div class="custom-card">
                    <strong>{muscle.title()}</strong><br/>
                    <span class="badge badge-{status['status']}">{color_map.get(status['color'], 'Unknown')}</span><br/>
                    <small>{days} days since last workout</small>
                </div>
                ''', unsafe_allow_html=True)
            
            # AI recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Recommendations")
            
            # Find neglected muscles
            neglected = [m for m, s in muscle_status.items() if s['days_since_workout'] > 6]
            
            if neglected:
                st.info(f"💡 Focus on: {', '.join(neglected).title()}")
                
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
"""

# TAB 4: EXERCISE LIBRARY
exercise_library_tab = """
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
"""

# TAB 5: ACHIEVEMENTS
achievements_tab = """
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
                unlock_text = f"Unlocked {ach.unlocked_date[:10]}" if ach.unlocked else f"Progress: {stats.total_workouts}/{ach.requirement}"
                
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
"""

# Print for reference
print("New tab implementations created")
