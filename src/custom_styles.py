# Modern Design System CSS for FitFlow AI
# Custom CSS with fitness-inspired color palette and premium components

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* ===== COLOR PALETTE ===== */
    :root {
        --primary-orange: #FF6B35;
        --secondary-blue: #004E89;
        --accent-gold: #F7931E;
        --success-teal: #2EC4B6;
        --dark: #1A1A2E;
        --light: #F8F9FA;
        --gray-100: #E9ECEF;
        --gray-200: #DEE2E6;
        --gray-300: #CED4DA;
        --gradient-primary: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        --gradient-secondary: linear-gradient(135deg, #004E89 0%, #2EC4B6 100%);
        --gradient-dark: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
    }
    
    /* ===== GLOBAL STYLES ===== */
    .stApp {
        background: var(--dark);
        color: var(--light);
        font-family: 'Inter', sans-serif;
    }
    
    /* ===== HEADERS ===== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        color: var(--light);
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* ===== CARDS ===== */
    .custom-card {
        background: linear-gradient(145deg, #242442 0%, #1A1A2E 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(255, 107, 53, 0.3);
    }
    
    .stat-card {
        background: var(--gradient-primary);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 16px rgba(255, 107, 53, 0.4);
    }
    
    .stat-card h3 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: white;
    }
    
    .stat-card p {
        font-size: 0.875rem;
        opacity: 0.9;
        margin: 0;
        color: white;
    }
    
    /* ===== ACHIEVEMENT CARD ===== */
    .achievement-card {
        background: linear-gradient(145deg, #2A2A4E 0%, #1F1F3A 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid var(--accent-gold);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .achievement-card.unlocked {
        border-left-color: var(--success-teal);
        background: linear-gradient(145deg, #2A4E4A 0%, #1F3A38 100%);
    }
    
    .achievement-icon {
        font-size: 2.5rem;
        filter: grayscale(100%);
    }
    
    .achievement-card.unlocked .achievement-icon {
        filter: grayscale(0%);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* ===== PROGRESS BARS ===== */
    .custom-progress {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        height: 24px;
        overflow: hidden;
        position: relative;
    }
    
    .custom-progress-bar {
        height: 100%;
        background: var(--gradient-primary);
        border-radius: 12px;
        position: relative;
        transition: width 0.5s ease;
    }
    
    .custom-progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* ===== MUSCLE HEATMAP ===== */
    .muscle-heatmap {
        background: linear-gradient(145deg, #242442 0%, #1A1A2E 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }
    
    .muscle-group {
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .muscle-group:hover {
        transform: scale(1.1);
        filter: brightness(1.2);
    }
    
    .muscle-legend {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.875rem;
    }
    
    .legend-color {
        width: 20px;
        height: 20px;
        border-radius: 4px;
    }
    
    /* ===== BADGES ===== */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-primary {
        background: var(--gradient-primary);
        color: white;
    }
    
    .badge-success {
        background: var(--success-teal);
        color: white;
    }
    
    .badge-warning {
        background: var(--accent-gold);
        color: var(--dark);
    }
    
    /* ===== BUTTONS ===== */
    .stButton button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
    }
    
    /* ===== SIDEBAR ===== */
    .css-1d391kg {
        background: var(--gradient-dark);
    }
    
    [data-testid="stSidebar"] {
        background: var(--gradient-dark);
    }
    
    /* ===== MOTIVATIONAL QUOTE ===== */
    .quote-card {
        background: var(--gradient-secondary);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        font-style: italic;
        font-size: 1.1rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 24px rgba(0, 78, 137, 0.4);
    }
    
    /* ===== EXERCISE LIBRARY ===== */
    .exercise-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
        padding: 1rem 0;
    }
    
    .exercise-card {
        background: linear-gradient(145deg, #242442 0%, #1A1A2E 100%);
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .exercise-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(255, 107, 53, 0.3);
        border-color: var(--primary-orange);
    }
    
    .exercise-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        background: linear-gradient(145deg, #2A2A4E 0%, #1F1F3A 100%);
    }
    
    .exercise-content {
        padding: 1rem;
    }
    
    /* ===== METRICS ===== */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-box {
        flex: 1;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-orange);
        font-family: 'Poppins', sans-serif;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--gray-300);
        margin-top: 0.25rem;
    }
    
    /* ===== CHAT MESSAGES ===== */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: var(--light);
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary);
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease;
    }
    
    /* ===== RECOVERY STATUS ===== */
    .recovery-indicator {
        width: 100%;
        height: 8px;
        background: var(--gray-200);
        border-radius: 4px;
        overflow: hidden;
    }
    
    .recovery-bar {
        height: 100%;
        transition: width 0.5s ease;
    }
    
    .recovery-bar.optimal {
        background: var(--success-teal);
    }
    
    .recovery-bar.warning {
        background: var(--accent-gold);
    }
    
    .recovery-bar.danger {
        background: var(--primary-orange);
    }
</style>
"""
