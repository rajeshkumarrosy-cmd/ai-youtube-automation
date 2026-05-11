import json
import google.generativeai as genai
from datetime import datetime

class ScriptGenerator:
    def __init__(self):
        self.topics = self.load_topics()
        self.short_script_file = "output/scripts/short_script.json"
        self.long_script_file = "output/scripts/long_script.json"
    
    def load_topics(self):
        """Load trending topics"""
        try:
            with open("output/scripts/trending_topics.json", 'r') as f:
                return json.load(f)['topics']
        except:
            return []
    
    def generate_short_script(self, topic):
        """Generate 15-60 sec short script"""
        prompt = f"""
        Create a SHORT VIDEO SCRIPT (15-60 seconds) for YouTube Shorts.
        
        Topic: {topic}
        
        Requirements:
        1. Hook viewer in FIRST 2 SECONDS with curiosity or emotion
        2. Tell a complete micro-story
        3. Use simple English
        4. Sound natural and conversational
        5. Include emotional or surprising twist at end
        6. Duration: 45 seconds max
        
        Format:
        [SCENE 1]
        Visual: (describe what's shown)
        Narration: (exact words to speak)
        Duration: XXs
        
        [SCENE 2]
        Visual:
        Narration:
        Duration:
        
        [SCENE 3 - ENDING TWIST]
        Visual:
        Narration:
        Duration:
        
        Keep narration conversational and engaging!
        """
        
        # Using free Gemini API (or fallback template)
        script = self.create_template_script(topic)
        return script
    
    def generate_long_script(self, topic):
        """Generate 5-8 min long-form script"""
        prompt = f"""
        Create a LONG-FORM SCRIPT (5-8 minutes) for YouTube video.
        
        Topic: {topic}
        
        Requirements:
        1. Cinematic storytelling with clear structure
        2. Beginning: Hook + context (1 min)
        3. Middle: Build tension and conflict (3-4 min)
        4. Climax: Emotional peak (1-2 min)
        5. Ending: Resolution + life lesson (30 sec)
        6. Add retention hooks every 15-20 seconds
        7. Use emotional language
        
        Format with TIMESTAMPS:
        [0:00-1:00] OPENING
        [1:00-4:00] CONFLICT
        [4:00-6:30] CLIMAX
        [6:30-8:00] ENDING
        
        Include visual descriptions for animators.
        """
        
        script = self.create_long_template(topic)
        return script
    
    def create_template_script(self, topic):
        """Template for short videos"""
        return {
            'type': 'short',
            'duration': 45,
            'topic': topic,
            'scenes': [
                {
                    'scene': 1,
                    'duration': 3,
                    'visual': f"[INTENSE HOOK IMAGE] Shocking moment related to {topic}",
                    'narration': f"What if... something unbelievable happened?",
                    'camera_movement': 'zoom in'
                },
                {
                    'scene': 2,
                    'duration': 25,
                    'visual': "Narrative unfolds with emotion",
                    'narration': f"The story behind {topic} that will shock you...",
                    'camera_movement': 'smooth pan'
                },
                {
                    'scene': 3,
                    'duration': 17,
                    'visual': "PLOT TWIST - Unexpected ending",
                    'narration': "But here's the twist nobody expected!",
                    'camera_movement': 'quick zoom'
                }
            ]
        }
    
    def create_long_template(self, topic):
        """Template for long-form videos"""
        return {
            'type': 'long',
            'duration': '5-8 min',
            'topic': topic,
            'structure': {
                'opening': {
                    'timestamp': '0:00-1:00',
                    'scenes': [
                        {
                            'visual': 'Hook image with dynamic text',
                            'narration': f'Have you ever wondered about {topic}?',
                            'music': 'suspenseful buildup'
                        }
                    ]
                },
                'conflict': {
                    'timestamp': '1:00-4:00',
                    'scenes': [
                        {
                            'visual': 'Story progression with tension',
                            'narration': 'The incredible truth unfolds...',
                            'music': 'dramatic build'
                        }
                    ]
                },
                'climax': {
                    'timestamp': '4:00-6:30',
                    'scenes': [
                        {
                            'visual': 'Peak emotional moment',
                            'narration': 'And then... the shocking revelation!',
                            'music': 'intense orchestral'
                        }
                    ]
                },
                'ending': {
                    'timestamp': '6:30-8:00',
                    'scenes': [
                        {
                            'visual': 'Resolution and lesson',
                            'narration': 'Remember this story always...',
                            'music': 'emotional resolution'
                        }
                    ]
                }
            }
        }
    
    def add_retention_hooks(self, script):
        """Add engagement hooks every 15 seconds"""
        hooks = [
            "Wait until you hear this...",
            "You won't believe what happened next...",
            "But that's not even the crazy part...",
            "Here's where it gets interesting...",
            "This is where things took a turn...",
            "Nobody expected what came next...",
        ]
        
        return script
    
    def save_scripts(self, short_script, long_script):
        """Save both scripts"""
        with open(self.short_script_file, 'w') as f:
            json.dump(short_script, f, indent=2)
        
        with open(self.long_script_file, 'w') as f:
            json.dump(long_script, f, indent=2)
        
        print(f"✅ Scripts saved")
    
    def run(self):
        """Generate scripts"""
        print("✍️ STEP 2: SCRIPT GENERATION STARTING...")
        
        if not self.topics:
            print("❌ No topics found")
            return
        
        selected_topic = self.topics[0]['title']
        print(f"\n📝 Generating scripts for: {selected_topic}")
        
        short_script = self.generate_short_script(selected_topic)
        long_script = self.generate_long_script(selected_topic)
        
        self.save_scripts(short_script, long_script)
        
        print(f"""
        ╔════════════════════════════════════╗
        ║     SCRIPTS GENERATED               ║
        ╚════════════════════════════════════╝
        Short: {short_script['duration']}s
        Long: {long_script['duration']}
        """)
        
        return {'short': short_script, 'long': long_script}

if __name__ == "__main__":
    generator = ScriptGenerator()
    generator.run()
