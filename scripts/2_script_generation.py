import json
import os
from datetime import datetime

class ScriptGenerator:
    """
    Generates complete video scripts from trending topics
    Uses template-based generation (no API required)
    """
    
    def __init__(self):
        self.topics = self.load_topics()
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
        self.short_script_file = f"{self.output_dir}/short_script.json"
        self.long_script_file = f"{self.output_dir}/long_script.json"
    
    # ============================================
    # METHOD 1: Load Topics from Previous Step
    # ============================================
    def load_topics(self):
        """
        Loads the trending topics from Step 1
        """
        try:
            with open("output/scripts/trending_topics.json", 'r') as f:
                data = json.load(f)
                return data.get('topics', [])
        except FileNotFoundError:
            print("⚠️ No trending topics found!")
            return []
    
    # ============================================
    # METHOD 2: Generate Short Script (45-60 sec)
    # ============================================
    def generate_short_script(self, topic):
        """
        Creates a complete short-form video script
        Duration: 45-60 seconds
        Format: 3 scenes with narration
        """
        print(f"✍️ Generating short script for: {topic}")
        
        # Get topic info
        title = topic.get('title', 'Untitled')
        category = topic.get('category', 'Story')
        
        # Create scene narrations based on category
        narrations = self.create_narrations_by_category(title, category)
        
        # Create script structure
        script = {
            'type': 'short',
            'format': 'vertical',  # 9:16 for shorts
            'duration': 45,
            'topic': title,
            'category': category,
            'created_at': datetime.now().isoformat(),
            
            'scenes': [
                {
                    'scene': 1,
                    'duration': 3,
                    'timing': '0:00-0:03',
                    
                    # VISUAL INSTRUCTIONS FOR ANIMATOR
                    'visual': {
                        'description': f"Shocking moment related to: {title}",
                        'style': 'Pixar 3D cinematic',
                        'emotion': 'shock',
                        'colors': ['bright_red', 'gold', 'black'],
                        'lighting': 'dramatic spotlight',
                        'camera_movement': 'zoom_in',
                        'camera_speed': 'fast'
                    },
                    
                    # NARRATION FOR VOICEOVER
                    'narration': narrations['hook'],
                    
                    # AUDIO SETTINGS
                    'audio': {
                        'mood': 'suspenseful',
                        'music_intensity': 'building'
                    },
                    
                    # EFFECTS
                    'effects': {
                        'transition_in': 'quick_zoom',
                        'transition_out': 'fade',
                        'text_overlay': 'None'
                    }
                },
                
                {
                    'scene': 2,
                    'duration': 25,
                    'timing': '0:03-0:28',
                    
                    'visual': {
                        'description': f"The incredible story unfolds: {title}",
                        'style': 'Pixar 3D cinematic',
                        'emotion': 'mystery',
                        'colors': ['blue', 'purple', 'cyan'],
                        'lighting': 'atmospheric',
                        'camera_movement': 'smooth_pan',
                        'camera_speed': 'slow'
                    },
                    
                    'narration': narrations['middle'],
                    
                    'audio': {
                        'mood': 'dramatic',
                        'music_intensity': 'building'
                    },
                    
                    'effects': {
                        'transition_in': 'fade',
                        'transition_out': 'fade',
                        'text_overlay': 'Title text'
                    }
                },
                
                {
                    'scene': 3,
                    'duration': 17,
                    'timing': '0:28-0:45',
                    
                    'visual': {
                        'description': f"Plot twist! {title}",
                        'style': 'Pixar 3D cinematic',
                        'emotion': 'shocking',
                        'colors': ['red', 'white', 'yellow'],
                        'lighting': 'intense',
                        'camera_movement': 'quick_zoom',
                        'camera_speed': 'fast'
                    },
                    
                    'narration': narrations['twist'],
                    
                    'audio': {
                        'mood': 'intense',
                        'music_intensity': 'peak'
                    },
                    
                    'effects': {
                        'transition_in': 'shock_cut',
                        'transition_out': 'black_fade',
                        'text_overlay': 'Subscribe button reminder'
                    }
                }
            ],
            
            # RETENTION HOOKS - Keep viewers watching
            'retention_hooks': [
                {'time': '0:00-0:03', 'hook': 'Shocking visual hook'},
                {'time': '0:15', 'hook': 'Question asked - curiosity gap'},
                {'time': '0:25', 'hook': 'Hint at revelation'},
                {'time': '0:40', 'hook': 'Unexpected twist'}
            ],
            
            # EMOTIONAL JOURNEY
            'emotional_arc': {
                'start': 'curious',
                'middle': 'intrigued',
                'climax': 'shocked',
                'end': 'satisfied'
            }
        }
        
        return script
    
    # ============================================
    # METHOD 3: Generate Long Script (5-8 min)
    # ============================================
    def generate_long_script(self, topic):
        """
        Creates a complete long-form video script
        Duration: 5-8 minutes
        Format: Full cinematic storytelling
        """
        print(f"📖 Generating long script for: {topic}")
        
        title = topic.get('title', 'Untitled')
        category = topic.get('category', 'Story')
        
        # Get narrations for long form
        long_narrations = self.create_long_narrations(title, category)
        
        script = {
            'type': 'long',
            'format': 'horizontal',  # 16:9
            'duration': '7 minutes',
            'total_seconds': 420,
            'topic': title,
            'category': category,
            'created_at': datetime.now().isoformat(),
            
            # COMPLETE STORY STRUCTURE
            'structure': {
                
                # ACT 1: OPENING (0:00-1:00)
                'opening': {
                    'act': 1,
                    'duration': 60,
                    'timestamp': '0:00-1:00',
                    'purpose': 'Hook + Context',
                    'key_emotion': 'curiosity',
                    
                    'scenes': [
                        {
                            'scene': 1,
                            'duration': 30,
                            'narration': long_narrations['opening_hook'],
                            'visual': f"Shocking visual of {title}",
                            'music': 'suspenseful_buildup',
                            'camera': 'zoom_in'
                        },
                        {
                            'scene': 2,
                            'duration': 30,
                            'narration': long_narrations['opening_context'],
                            'visual': f"News headlines about {title}",
                            'music': 'dramatic_strings',
                            'camera': 'fast_pan'
                        }
                    ]
                },
                
                # ACT 2: CONFLICT (1:00-4:00)
                'conflict': {
                    'act': 2,
                    'duration': 180,
                    'timestamp': '1:00-4:00',
                    'purpose': 'Build tension + Backstory',
                    'key_emotion': 'mystery',
                    
                    'scenes': [
                        {
                            'scene': 3,
                            'duration': 45,
                            'narration': long_narrations['backstory_1'],
                            'visual': f"Character introduction related to {title}",
                            'music': 'mysterious_ambient',
                            'camera': 'slow_pan'
                        },
                        {
                            'scene': 4,
                            'duration': 45,
                            'narration': long_narrations['backstory_2'],
                            'visual': f"Montage of research and investigation",
                            'music': 'building_orchestral',
                            'camera': 'montage_cuts'
                        },
                        {
                            'scene': 5,
                            'duration': 45,
                            'narration': long_narrations['discovery'],
                            'visual': f"The breakthrough moment",
                            'music': 'climactic_strings',
                            'camera': 'dramatic_zoom'
                        },
                        {
                            'scene': 6,
                            'duration': 45,
                            'narration': long_narrations['conflict_rise'],
                            'visual': f"Mysterious figures in shadows",
                            'music': 'ominous_warning',
                            'camera': 'glitch_effect'
                        }
                    ]
                },
                
                # ACT 3: CLIMAX (4:00-6:30)
                'climax': {
                    'act': 3,
                    'duration': 150,
                    'timestamp': '4:00-6:30',
                    'purpose': 'Peak emotional moment',
                    'key_emotion': 'shock',
                    
                    'scenes': [
                        {
                            'scene': 7,
                            'duration': 50,
                            'narration': long_narrations['climax_1'],
                            'visual': f"Conflict/confrontation scene",
                            'music': 'intense_action',
                            'camera': 'shaky_danger'
                        },
                        {
                            'scene': 8,
                            'duration': 50,
                            'narration': long_narrations['climax_2'],
                            'visual': f"Character making critical decision",
                            'music': 'emotional_orchestral',
                            'camera': 'close_up_emotion'
                        },
                        {
                            'scene': 9,
                            'duration': 50,
                            'narration': long_narrations['climax_3'],
                            'visual': f"The twist revelation",
                            'music': 'powerful_swell',
                            'camera': 'dramatic_zoom'
                        }
                    ]
                },
                
                # ACT 4: ENDING (6:30-7:00)
                'ending': {
                    'act': 4,
                    'duration': 30,
                    
