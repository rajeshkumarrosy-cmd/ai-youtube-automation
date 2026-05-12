import json
import os
from datetime import datetime

class ScriptGenerator:
    """
    Generates DIFFERENT scripts for short vs long videos
    Short: 45-60 seconds, 3 scenes
    Long: 5-8 minutes, 4 acts with subplots
    """
    
    def __init__(self):
        self.topics = self.load_topics()
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
        self.short_script_file = f"{self.output_dir}/short_script.json"
        self.long_script_file = f"{self.output_dir}/long_script.json"
    
    def load_topics(self):
        """Load topics from Step 1"""
        try:
            with open("output/scripts/trending_topics.json", 'r') as f:
                data = json.load(f)
                return data.get('topics', [])
        except FileNotFoundError:
            print("⚠️ No topics found!")
            return []
    
    # ============================================
    # SHORT SCRIPT: 45-60 seconds
    # ============================================
    def generate_short_script(self, topic):
        """
        SHORT VIDEO: 45-60 seconds
        - Hook instantly
        - Tell story fast
        - Leave audience wanting more
        - Perfect for Shorts
        """
        print(f"✍️ Generating SHORT script (45s)...")
        
        title = topic.get('title', 'Untitled')
        category = topic.get('category', 'Adventure')
        
        script = {
            'type': 'short',
            'format': 'vertical (9:16)',
            'duration': 45,
            'topic': title,
            'category': category,
            'created_at': datetime.now().isoformat(),
            
            'structure': 'Hook → Tension → Twist',
            
            'scenes': [
                {
                    'scene': 1,
                    'duration': 3,
                    'visual': f"INTENSE SHOCK IMAGE related to {title}",
                    'narration': f"Wait... what if {title.lower()} is actually real?",
                    'tone': 'shocked',
                    'music': 'suspenseful'
                },
                {
                    'scene': 2,
                    'duration': 25,
                    'visual': f"Evidence and story unfolds about {title}",
                    'narration': f"Experts discovered something about {title}. The truth is more shocking than anyone imagined. Scientists couldn't explain it for years.",
                    'tone': 'mysterious',
                    'music': 'building tension'
                },
                {
                    'scene': 3,
                    'duration': 17,
                    'visual': f"PLOT TWIST - Ultimate revelation about {title}",
                    'narration': f"But here's what NOBODY expected. The real story behind {title} will change how you see everything.",
                    'tone': 'shocking revelation',
                    'music': 'dramatic peak'
                }
            ],
            
            'hooks': [
                '0:00-0:03 = Immediate shock',
                '0:15 = "Wait..." moment',
                '0:30 = Plot twist hint',
                '0:42 = Cliffhanger ending'
            ]
        }
        
        return script
    
    # ============================================
    # LONG SCRIPT: 5-8 minutes
    # ============================================
    def generate_long_script(self, topic):
        """
        LONG VIDEO: 5-8 minutes
        - Deep storytelling
        - Character development
        - Multiple plot points
        - Emotional journey
        """
        print(f"📖 Generating LONG script (7 minutes)...")
        
        title = topic.get('title', 'Untitled')
        category = topic.get('category', 'Adventure')
        
        script = {
            'type': 'long',
            'format': 'horizontal (16:9)',
            'duration': '7 minutes',
            'total_seconds': 420,
            'topic': title,
            'category': category,
            'created_at': datetime.now().isoformat(),
            
            'structure': 'Introduction → Conflict → Climax → Resolution',
            
            'acts': {
                'act_1_opening': {
                    'name': 'THE QUESTION',
                    'timestamp': '0:00-1:30',
                    'duration': 90,
                    'purpose': 'Hook and establish mystery',
                    'scenes': [
                        {
                            'scene': 1,
                            'duration': 45,
                            'narration': f"Have you ever wondered what really happened with {title}? Most people don't know the REAL story.",
                            'visual': f"Intriguing visuals about {title}"
                        },
                        {
                            'scene': 2,
                            'duration': 45,
                            'narration': f"The official story says one thing. But the truth? The truth is much stranger than anyone imagined.",
                            'visual': f"News clips and evidence about {title}"
                        }
                    ]
                },
                
                'act_2_conflict': {
                    'name': 'THE INVESTIGATION',
                    'timestamp': '1:30-4:00',
                    'duration': 150,
                    'purpose': 'Build tension and reveal backstory',
                    'scenes': [
                        {
                            'scene': 3,
                            'duration': 50,
                            'narration': f"It started with a discovery. Scientists found something unexpected about {title}.",
                            'visual': f"Research and investigation scenes"
                        },
                        {
                            'scene': 4,
                            'duration': 50,
                            'narration': f"They kept digging deeper. What they found contradicted everything they believed about {title}.",
                            'visual': f"Mounting evidence and complications"
                        },
                        {
                            'scene': 5,
                            'duration': 50,
                            'narration': f"But their investigation caught the attention of powerful people. People who wanted to keep the truth about {title} hidden.",
                            'visual': f"Tension and conflict emerging"
                        }
                    ]
                },
                
                'act_3_climax': {
                    'name': 'THE REVELATION',
                    'timestamp': '4:00-6:00',
                    'duration': 120,
                    'purpose': 'Peak emotional moment, big reveal',
                    'scenes': [
                        {
                            'scene': 6,
                            'duration': 60,
                            'narration': f"They had to make a choice. Hide the truth about {title}, or risk everything to expose it.",
                            'visual': f"Critical decision moment"
                        },
                        {
                            'scene': 7,
                            'duration': 60,
                            'narration': f"They chose the truth. And what they revealed about {title} shocked the world. Everything changed after that.",
                            'visual': f"Shocking revelation and impact"
                        }
                    ]
                },
                
                'act_4_resolution': {
                    'name': 'THE TRUTH',
                    'timestamp': '6:00-7:00',
                    'duration': 60,
                    'purpose': 'Wrap up and life lesson',
                    'scenes': [
                        {
                            'scene': 8,
                            'duration': 30,
                            'narration': f"Today, the truth about {title} is finally known. But not everyone believes it.",
                            'visual': f"Aftermath and new normal"
                        },
                        {
                            'scene': 9,
                            'duration': 30,
                            'narration': f"What we learned from {title} is this: the truth always matters. Even when it's uncomfortable.",
                            'visual': f"Final reflection and conclusion"
                        }
                    ]
                }
            },
            
            'retention_points': [
                '0:30 - Hook question',
                '1:30 - Conflict introduced',
                '2:30 - Stakes raised',
                '3:30 - Major complication',
                '4:30 - Climax begins',
                '5:30 - Peak moment',
                '6:00 - Resolution starts',
                '6:30 - Final message'
            ]
        }
        
        return script
    
    # ============================================
    # SAVE SCRIPTS
    # ============================================
    def save_scripts(self, short_script, long_script):
        """Save both scripts"""
        with open(self.short_script_file, 'w') as f:
            json.dump(short_script, f, indent=2)
        print(f"✅ Short script saved")
        
        with open(self.long_script_file, 'w') as f:
            json.dump(long_script, f, indent=2)
        print(f"✅ Long script saved")
    
    # ============================================
    # MAIN RUN
    # ============================================
    def run(self):
        """Generate scripts"""
        print("\n" + "="*60)
        print("✍️ STEP 2: SCRIPT GENERATION")
        print("="*60 + "\n")
        
        if not self.topics:
            print("⚠️ No topics found! Using default...")
            self.topics = [{
                'title': 'The Most Incredible Discovery Ever',
                'category': 'Sci-Fi'
            }]
        
        topic = self.topics[0]
        print(f"🎯 Topic: {topic['title']}")
        print(f"📂 Category: {topic['category']}\n")
        
        # Generate different scripts
        short_script = self.generate_short_script(topic)
        long_script = self.generate_long_script(topic)
        
        # Save
        self.save_scripts(short_script, long_script)
        
        print(f"""
╔═══════════════════════════════════════════════════════╗
║         ✅ SCRIPT GENERATION COMPLETE                 ║
╚═══════════════════════════════════════════════════════╝

📊 SHORT SCRIPT (45 seconds):
   Scenes: 3
   Focus: Fast-paced, instant hook
   Structure: Hook → Tension → Twist

📊 LONG SCRIPT (7 minutes):
   Scenes: 9
   Focus: Deep storytelling
   Structure: Opening → Conflict → Climax → Resolution

✨ Both scripts are COMPLETELY DIFFERENT!
   - Short = Shorts/Reels
   - Long = YouTube Videos
        """)
        
        return {'short': short_script, 'long': long_script}

# ============================================
# RUN THE SCRIPT
# ============================================
if __name__ == "__main__":
    generator = ScriptGenerator()
    generator.run()
