import json
import os
from datetime import datetime

class ScriptGenerator:
    """
    Generates complete video scripts from trending topics
    NO EXTERNAL API NEEDED - Uses templates and rules
    """
    
    def __init__(self):
        self.topics = self.load_topics()
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
        self.short_script_file = f"{self.output_dir}/short_script.json"
        self.long_script_file = f"{self.output_dir}/long_script.json"
    
    # ============================================
    # METHOD 1: Load Topics from Step 1
    # ============================================
    def load_topics(self):
        """
        Loads trending topics from Step 1
        """
        try:
            with open("output/scripts/trending_topics.json", 'r') as f:
                data = json.load(f)
                return data.get('topics', [])
        except FileNotFoundError:
            print("⚠️ No trending topics found!")
            return []
    
    # ============================================
    # METHOD 2: Generate Narration Based on Category
    # ============================================
    def get_narration_templates(self, category, title):
        """
        Gets narration templates based on story category
        NO API CALL NEEDED
        """
        
        templates = {
            'Sci-Fi': {
                'scene1': f"What if {title.lower()} suddenly became a reality?",
                'scene2': f"In 2024, scientists made a discovery about {title.lower()}. Something extraordinary.",
                'scene3': f"But here's the twist nobody expected about {title.lower()}."
            },
            'Horror': {
                'scene1': f"The terrifying truth about {title.lower()} is finally revealed.",
                'scene2': f"Witnesses reported something shocking related to {title.lower()}. Something unexplainable.",
                'scene3': f"And then, something even more horrifying about {title.lower()} happened."
            },
            'Motivational': {
                'scene1': f"How did someone achieve {title.lower()}? The answer might surprise you.",
                'scene2': f"Against all odds, they pursued their dream of {title.lower()}. Here's how they did it.",
                'scene3': f"The lessons from {title.lower()} will change how you see success."
            },
            'Mystery': {
                'scene1': f"The mystery of {title.lower()} has stumped experts for years.",
                'scene2': f"Investigators finally uncovered the truth about {title.lower()}.",
                'scene3': f"The shocking revelation about {title.lower()} will blow your mind."
            },
            'Kids Stories': {
                'scene1': f"Once upon a time, {title.lower()} began an incredible adventure.",
                'scene2': f"On their journey, they discovered something magical about {title.lower()}.",
                'scene3': f"And that's how {title.lower()} changed everything forever."
            },
            'Emotional': {
                'scene1': f"The story of {title.lower()} is one of heartbreak and hope.",
                'scene2': f"Through tears and struggles, someone overcame {title.lower()}.",
                'scene3': f"The lesson from {title.lower()} will touch your heart forever."
            },
            'Adventure': {
                'scene1': f"The adventure of {title.lower()} begins with a single decision.",
                'scene2': f"Facing unimaginable challenges, they pursued {title.lower()}.",
                'scene3': f"The incredible ending of {title.lower()} will amaze you."
            }
        }
        
        # Return template for category, or default
        return templates.get(category, templates['Adventure'])
    
    # ============================================
    # METHOD 3: Generate Short Script (45-60 sec)
    # ============================================
    def generate_short_script(self, topic):
        """
        Creates a complete short-form video script
        Duration: 45-60 seconds
        """
        print(f"✍️ Generating short script for: {topic['title']}")
        
        title = topic.get('title', 'Untitled')
        category = topic.get('category', 'Adventure')
        
        # Get narration for this category
        narrations = self.get_narration_templates(category, title)
        
        script = {
            'type': 'short',
            'format': 'vertical',
            'duration': 45,
            'topic': title,
            'category': category,
            'created_at': datetime.now().isoformat(),
            
            'scenes': [
                {
                    'scene': 1,
                    'duration': 3,
                    'timing': '0:00-0:03',
                    'visual': {
                        'description': f"Shocking moment related to: {title}",
                        'style': 'Pixar 3D cinematic',
                        'emotion': 'shock',
                        'colors': ['bright_red', 'gold', 'black'],
                        'lighting': 'dramatic spotlight',
                        'camera_movement': 'zoom_in',
                        'camera_speed': 'fast'
                    },
                    'narration': narrations['scene1'],
                    'audio': {
                        'mood': 'suspenseful',
                        'music_intensity': 'building'
                    },
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
                    'narration': narrations['scene2'],
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
                    'narration': narrations['scene3'],
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
            
            'retention_hooks': [
                {'time': '0:00-0:03', 'hook': 'Shocking visual hook'},
                {'time': '0:15', 'hook': 'Question asked - curiosity gap'},
                {'time': '0:25', 'hook': 'Hint at revelation'},
                {'time': '0:40', 'hook': 'Unexpected twist'}
            ],
            
            'emotional_arc': {
                'start': 'curious',
                'middle': 'intrigued',
                'climax': 'shocked',
                'end': 'satisfied'
            }
        }
        
        return script
    
    # ============================================
    # METHOD 4: Generate Long Script (5-8 min)
    # ============================================
    def generate_long_script(self, topic):
        """
        Creates a complete long-form video script
        Duration: 5-8 minutes
        """
        print(f"📖 Generating long script for: {topic['title']}")
        
        title = topic.get('title', 'Untitled')
        category = topic.get('category', 'Adventure')
        
        # Get narrations
        narrations = self.get_narration_templates(category, title)
        
        script = {
            'type': 'long',
            'format': 'horizontal',
            'duration': '7 minutes',
            'total_seconds': 420,
            'topic': title,
            'category': category,
            'created_at': datetime.now().isoformat(),
            
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
                            'narration': f"Have you ever wondered about {title}?",
                            'visual': f"Shocking visual of {title}",
                            'music': 'suspenseful_buildup',
                            'camera': 'zoom_in'
                        },
                        {
                            'scene': 2,
                            'duration': 30,
                            'narration': f"This is the story nobody is talking about. A story that could change everything.",
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
                            'narration': f"For years, nobody knew the truth about {title}.",
                            'visual': f"Character introduction related to {title}",
                            'music': 'mysterious_ambient',
                            'camera': 'slow_pan'
                        },
                        {
                            'scene': 4,
                            'duration': 45,
                            'narration': f"They spent years searching for answers about {title}. Everyone said they were crazy.",
                            'visual': f"Montage of research and investigation",
                            'music': 'building_orchestral',
                            'camera': 'montage_cuts'
                        },
                        {
                            'scene': 5,
                            'duration': 45,
                            'narration': f"And then, they found something incredible related to {title}.",
                            'visual': f"The breakthrough moment",
                            'music': 'climactic_strings',
                            'camera': 'dramatic_zoom'
                        },
                        {
                            'scene': 6,
                            'duration': 45,
                            'narration': f"But what they didn't know was that someone else had been watching.",
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
                            'narration': f"The stakes had never been higher. Everything changed.",
                            'visual': f"Conflict/confrontation scene",
                            'music': 'intense_action',
                            'camera': 'shaky_danger'
                        },
                        {
                            'scene': 8,
                            'duration': 50,
                            'narration': f"A critical choice had to be made. There was no going back.",
                            'visual': f"Character making critical decision",
                            'music': 'emotional_orchestral',
                            'camera': 'close_up_emotion'
                        },
                        {
                            'scene': 9,
                            'duration': 50,
                            'narration': f"And then, something nobody expected happened.",
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
                    'timestamp': '6:30-7:00',
                    'purpose': 'Resolution + Lesson',
                    'key_emotion': 'reflection',
                    'scenes': [
                        {
                            'scene': 10,
                            'duration': 20,
                            'narration': f"To this day, people still wonder about {title}.",
                            'visual': f"Resolution scene",
                            'music': 'emotional_resolution',
                            'camera': 'slow_fade'
                        },
                        {
                            'scene': 11,
                            'duration': 10,
                            'narration': f"What do you think about {title}? Let us know in the comments!",
                            'visual': f"Final message",
                            'music': 'quiet_strings',
                            'camera': 'black_fade'
                        }
                    ]
                }
            },
            
            'retention_hooks': [
                {'time': '0:00-0:30', 'hook': 'Opening question hook'},
                {'time': '0:45', 'hook': 'Curiosity gap'},
                {'time': '1:30', 'hook': 'Plot twist hint'},
                {'time': '2:30', 'hook': 'Major revelation'},
                {'time': '3:30', 'hook': 'Conflict introduced'},
                {'time': '4:00', 'hook': 'Stakes raised'},
                {'time': '4:30', 'hook': 'Climax buildup'},
                {'time': '5:30', 'hook': 'Peak moment'},
                {'time': '6:00', 'hook': 'Plot twist revealed'},
                {'time': '6:30', 'hook': 'Resolution'}
            ],
            
            'emotional_arc': {
                'opening': 'curious',
                'buildup': 'tense',
                'climax': 'shocked',
                'ending': 'thoughtful'
            },
            
            'target_audience': '18-45 years old',
            'estimated_views': '5000-15000',
            'estimated_watch_time_minutes': 4.5
        }
        
        return script
    
    # ============================================
    # METHOD 5: Save Scripts
    # ============================================
    def save_scripts(self, short_script, long_script):
        """
        Saves both scripts to JSON files
        """
        # Save short script
        with open(self.short_script_file, 'w') as f:
            json.dump(short_script, f, indent=2)
        print(f"✅ Short script saved: {self.short_script_file}")
        
        # Save long script
        with open(self.long_script_file, 'w') as f:
            json.dump(long_script, f, indent=2)
        print(f"✅ Long script saved: {self.long_script_file}")
    
    # ============================================
    # METHOD 6: Print Results
    # ============================================
    def print_script_info(self, short_script, long_script):
        """
        Prints script information
        """
        print(f"""
╔═══════════════════════════════════════════════════════╗
║            📝 SCRIPTS GENERATED SUCCESSFULLY           ║
╚═══════════════════════════════════════════════════════╝

📊 SHORT SCRIPT:
   Duration: {short_script['duration']} seconds
   Scenes: {len(short_script['scenes'])}
   Format: {short_script['format']}
   Topic: {short_script['topic']}
   Category: {short_script['category']}
   File: {self.short_script_file}

📊 LONG SCRIPT:
   Duration: {long_script['duration']}
   Acts: {len(long_script['structure'])}
   Format: {long_script['format']}
   Topic: {long_script['topic']}
   File: {self.long_script_file}

✨ Features:
   ✓ Retention hooks included
   ✓ Emotional arc designed
   ✓ Camera movements detailed
   ✓ Music mood specified
   ✓ Narration written
   ✓ NO API calls needed
        """)
    
    # ============================================
    # MAIN RUN METHOD
    # ============================================
    def run(self):
        """
        Execute script generation
        """
        print("\n" + "="*60)
        print("✍️ STEP 2: SCRIPT GENERATION STARTING...")
        print("="*60 + "\n")
        
        # Check if topics exist
        if not self.topics:
            print("⚠️ No topics found! Using default topic...")
            self.topics = [{
                'title': 'The Most Incredible AI Story Ever Told',
                'category': 'Sci-Fi'
            }]
        
        # Select best topic
        selected_topic = self.topics[0]
        print(f"\n🎯 Selected Topic: {selected_topic['title']}")
        print(f"📂 Category: {selected_topic['category']}\n")
        
        # Generate scripts
        short_script = self.generate_short_script(selected_topic)
        long_script = self.generate_long_script(selected_topic)
        
        # Save to files
        self.save_scripts(short_script, long_script)
        
        # Print results
        self.print_script_info(short_script, long_script)
        
        print(f"""
╔═══════════════════════════════════════════════════════╗
║           ✅ SCRIPT GENERATION COMPLETE               ║
╚═══════════════════════════════════════════════════════╝

🎬 Next Step: Visual Generation
        """)
        
        return {
            'short': short_script,
            'long': long_script
        }

# ============================================
# RUN THE SCRIPT
# ============================================
if __name__ == "__main__":
    generator = ScriptGenerator()
    generator.run()
