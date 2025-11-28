"""
Muscle Heatmap Component for FitFlow AI
Generates interactive body diagram showing workout coverage
"""

from typing import Dict, List


def generate_muscle_heatmap_svg(muscle_status: Dict[str, Dict]) -> str:
    """
    Generate SVG body diagram with color-coded muscles
    muscle_status: Dict with muscle names and their status data
    """
    
    # Color mapping
    colors = {
        "red": "#FF6B35",      # Recently worked (0-2 days)
        "orange": "#F7931E",   # Recovering (3-4 days)
        "yellow": "#FFD93D",   # Ready (5-6 days)
        "blue": "#2EC4B6",     # Needs attention (7+ days)
        "gray": "#4A4A6A"      # Never worked
    }
    
    # Default color for muscles not in status
    default_color = colors["gray"]
    
    # Helper function to get muscle color
    def get_color(muscle_name: str) -> str:
        if muscle_name in muscle_status:
            return colors.get(muscle_status[muscle_name]["color"], default_color)
        return default_color
    
    svg = f"""
    <svg viewBox="0 0 1000 750" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%); border-radius: 16px; padding: 20px;">
        
        <!-- FRONT VIEW -->
        <g id="front-view">
            <text x="250" y="40" fill="#FFFFFF" font-size="20" font-weight="bold" text-anchor="middle">FRONT</text>
            
            <!-- Body outline -->
            <g opacity="0.2">
                <circle cx="250" cy="90" r="35" fill="#E0E0E0"/>
                <rect x="235" y="120" width="30" height="20" fill="#E0E0E0"/>
                <ellipse cx="250" cy="210" rx="70" ry="90" fill="#E0E0E0"/>
                <rect x="215" y="290" width="30" height="120" rx="15" fill="#E0E0E0"/>
                <rect x="255" y="290" width="30" height="120" rx="15" fill="#E0E0E0"/>
            </g>
            
            <!-- Shoulders -->
            <g class="muscle-group">
                <circle cx="185" cy="145" r="25" fill="{get_color('shoulders')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <circle cx="315" cy="145" r="25" fill="{get_color('shoulders')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <title>Shoulders - {muscle_status.get('shoulders', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Chest -->
            <g class="muscle-group">
                <ellipse cx="220" cy="180" rx="32" ry="40" fill="{get_color('chest')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <ellipse cx="280" cy="180" rx="32" ry="40" fill="{get_color('chest')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <title>Chest - {muscle_status.get('chest', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Biceps -->
            <g class="muscle-group">
                <ellipse cx="155" cy="190" rx="15" ry="35" fill="{get_color('arms')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <ellipse cx="345" cy="190" rx="15" ry="35" fill="{get_color('arms')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <title>Biceps - {muscle_status.get('arms', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Forearms -->
            <g class="muscle-group">
                <rect x="145" y="230" width="20" height="50" rx="10" fill="{get_color('arms')}" opacity="0.8" stroke="#FFF" stroke-width="1"/>
                <rect x="335" y="230" width="20" height="50" rx="10" fill="{get_color('arms')}" opacity="0.8" stroke="#FFF" stroke-width="1"/>
                <title>Forearms - {muscle_status.get('arms', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Core/Abs -->
            <g class="muscle-group">
                <rect x="210" y="225" width="80" height="70" rx="12" fill="{get_color('core')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <title>Core - {muscle_status.get('core', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Quads -->
            <g class="muscle-group">
                <rect x="215" y="300" width="30" height="105" rx="15" fill="{get_color('legs')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <rect x="255" y="300" width="30" height="105" rx="15" fill="{get_color('legs')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <title>Quads - {muscle_status.get('legs', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Label -->
            <text x="250" y="440" fill="#AAA" font-size="11" text-anchor="middle">Chest • Biceps • Forearms</text>
            <text x="250" y="455" fill="#AAA" font-size="11" text-anchor="middle">Quads • Core • Shoulders</text>
        </g>
        
        <!-- BACK VIEW -->
        <g id="back-view" transform="translate(500, 0)">
            <text x="250" y="40" fill="#FFFFFF" font-size="20" font-weight="bold" text-anchor="middle">BACK</text>
            
            <!-- Body outline -->
            <g opacity="0.2">
                <circle cx="250" cy="90" r="35" fill="#E0E0E0"/>
                <rect x="235" y="120" width="30" height="20" fill="#E0E0E0"/>
                <ellipse cx="250" cy="210" rx="70" ry="90" fill="#E0E0E0"/>
                <rect x="215" y="290" width="30" height="120" rx="15" fill="#E0E0E0"/>
                <rect x="255" y="290" width="30" height="120" rx="15" fill="#E0E0E0"/>
            </g>
            
            <!-- Rear Shoulders -->
            <g class="muscle-group">
                <circle cx="185" cy="145" r="25" fill="{get_color('shoulders')}" opacity="0.7" stroke="#FFF" stroke-width="1"/>
                <circle cx="315" cy="145" r="25" fill="{get_color('shoulders')}" opacity="0.7" stroke="#FFF" stroke-width="1"/>
                <title>Rear Shoulders - {muscle_status.get('shoulders', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Upper Back & Lats -->
            <g class="muscle-group">
                <path d="M 200 155 L 185 175 L 185 235 L 200 260 L 250 270 L 300 260 L 315 235 L 315 175 L 300 155 L 250 150 Z" 
                      fill="{get_color('back')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <title>Back - {muscle_status.get('back', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Lower Back -->
            <rect x="215" y="270" width="70" height="30" rx="10" fill="{get_color('back')}" opacity="0.8" stroke="#FFF" stroke-width="1"/>
            
            <!-- Triceps -->
            <g class="muscle-group">
                <ellipse cx="155" cy="190" rx="15" ry="35" fill="{get_color('arms')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <ellipse cx="345" cy="190" rx="15" ry="35" fill="{get_color('arms')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <title>Triceps - {muscle_status.get('arms', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Glutes -->
            <g class="muscle-group">
                <ellipse cx="230" cy="310" rx="25" ry="20" fill="{get_color('legs')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <ellipse cx="270" cy="310" rx="25" ry="20" fill="{get_color('legs')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <title>Glutes - {muscle_status.get('legs', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Hamstrings -->
            <g class="muscle-group">
                <rect x="215" y="335" width="30" height="60" rx="15" fill="{get_color('legs')}" opacity="0.8" stroke="#FFF" stroke-width="1"/>
                <rect x="255" y="335" width="30" height="60" rx="15" fill="{get_color('legs')}" opacity="0.8" stroke="#FFF" stroke-width="1"/>
                <title>Hamstrings - {muscle_status.get('legs', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Calves -->
            <g class="muscle-group">
                <ellipse cx="230" cy="410" rx="12" ry="25" fill="{get_color('legs')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <ellipse cx="270" cy="410" rx="12" ry="25" fill="{get_color('legs')}" opacity="0.9" stroke="#FFF" stroke-width="2"/>
                <title>Calves - {muscle_status.get('legs', {}).get('days_since_workout', 'Never')} days ago</title>
            </g>
            
            <!-- Label -->
            <text x="250" y="455" fill="#AAA" font-size="11" text-anchor="middle">Back • Triceps • Glutes • Calves</text>
        </g>
        
        <!-- Legend -->
        <g id="legend" transform="translate(150, 520)">
            <rect x="-20" y="-15" width="700" height="180" rx="12" fill="rgba(0,0,0,0.4)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
            
            <text x="330" y="10" fill="#FFFFFF" font-size="18" font-weight="bold" text-anchor="middle">Status Legend</text>
            
            <g transform="translate(50, 40)">
                <circle cx="10" cy="10" r="10" fill="{colors['red']}"/>
                <text x="30" y="16" fill="#FFF" font-size="14">Recently (0-2 days)</text>
            </g>
            
            <g transform="translate(280, 40)">
                <circle cx="10" cy="10" r="10" fill="{colors['orange']}"/>
                <text x="30" y="16" fill="#FFF" font-size="14">Recent (3-4 days)</text>
            </g>
            
            <g transform="translate(500, 40)">
                <circle cx="10" cy="10" r="10" fill="{colors['yellow']}"/>
                <text x="30" y="16" fill="#FFF" font-size="14">Ready (5-6 days)</text>
            </g>
            
            <g transform="translate(50, 80)">
                <circle cx="10" cy="10" r="10" fill="{colors['blue']}"/>
                <text x="30" y="16" fill="#FFF" font-size="14">Needs Work (7+ days)</text>
            </g>
            
            <g transform="translate(280, 80)">
                <circle cx="10" cy="10" r="10" fill="{colors['gray']}"/>
                <text x="30" y="16" fill="#FFF" font-size="14">Not Tracked</text>
            </g>
            
            <g transform="translate(50, 120)">
                <text x="0" y="0" fill="#FFD93D" font-size="13" font-style="italic">💡 Hover over muscles to see days since last workout</text>
            </g>
        </g>
        
        <style>
            .muscle-group {{
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            .muscle-group:hover {{
                opacity: 1 !important;
                filter: brightness(1.5) drop-shadow(0 0 12px rgba(255,255,255,0.6));
                transform: scale(1.08);
            }}
        </style>
    </svg>
    """
    
    return svg


def calculate_coverage_score(muscle_status: Dict[str, Dict]) -> int:
    """Calculate overall muscle coverage percentage"""
    total_muscles = 6  # chest, back, shoulders, arms, legs, core
    worked_muscles = len([m for m in muscle_status.values() if m['days_since_workout'] <= 6])
    
    return int((worked_muscles / total_muscles) * 100)
