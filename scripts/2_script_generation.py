import json
import os
from datetime import datetime

class ScriptGenerator:
    """
    Generates COMPLETELY DIFFERENT scripts for SHORT vs LONG
    """
    
    def __init__(self):
        self.topics = self.load_topics()
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_topics(self):
        """Load topics"""
        try:
            with open("output/scripts/trending_topics.json", 'r') as f:
                return json.load(f).get('topics', [])
        except:
            return []
    
    def generate_short_script(self, topic):
        """
        SHORT: 45-60 seconds
        Hook fast, tell story quick, leave them wanting more
        """
        title = topic['title']
        category = topic['category']
        
        print("✍️ Generating SHORT video script (45 seconds)...")
        
        script = {
            'type': 'short',
            'duration': 45,
            'topic': title,
            'category': category,
            
            'structure': 'HOOK → TENSION → TWIST → END',
            
            'scenes': [
                {
                    'scene': 1,
                    'duration': 5,
                    'type': 'hook',
                    'visual': 'Shocking dramatic scene',
                    'narration': f"What if everything you knew about {title} was wrong?",
                    'emotion': 'Shock',
                    'pacing': 'Fast'
                },
                {
                    'scene': 2,
                    'duration': 20,
                    'type': 'buildup',
                    'visual': 'Evidence and tension',
                    'narration': f"Scientists discovered something impossible about {title}. Governments tried to hide it. But the truth was too big.",
                    'emotion': 'Mystery',
                    'pacing': 'Medium'
                },
                {
                    'scene': 3,
                    'duration': 15,
                    'type': 'twist',
                    'visual': 'Shocking revelation',
                    'narration': f"Here's what nobody expected about {title}. This changes EVERYTHING.",
                    'emotion': 'Shock',
                    'pacing': 'Fast'
                },
                {
                    'scene': 4,
                    'duration': 5,
                    'type': 'cta',
                    'visual': 'Subscribe reminder',
                    'narration': "Subscribe for more shocking discoveries.",
                    'emotion': 'Engaging',
                    'pacing': 'Normal'
                }
            ],
            
            'key_moments': [
                '0:00-0:05: Shock hook',
                '0:15: "What if..." question',
                '0:25: Mystery deepens',
                '0:35: Plot twist hint',
                '0:40: Final revelation',
                '0:45: Subscribe call'
            ]
        }
        
        return script
    
    def generate_long_script(self, topic):
        """
        LONG: 6-8 minutes
        Deep story, character arc, emotional journey
        COMPLETELY DIFFERENT from short
        """
        title = topic['title']
        category = topic['category']
        
        print("📖 Generating LONG video script (7 minutes)...")
        
        script = {
            'type': 'long',
            'duration': 420,  # 7 minutes
            'topic': title,
            'category': category,
            
            'structure': 'ACT 1: THE QUESTION → ACT 2: THE INVESTIGATION → ACT 3: THE TRUTH → ACT 4: THE IMPACT',
            
            'acts': {
                'act_1': {
                    'name': 'THE QUESTION',
                    'duration': 60,
                    'scenes': [
                        {
                            'duration': 30,
                            'narration': f"Have you ever wondered what really happened with {title}? Most people don't know the REAL story.",
                            'visual': 'Intriguing introduction'
                        },
                        {
                            'duration': 30,
                            'narration': "The official story is one thing. But I've uncovered something that changes everything.",
                            'visual': 'Building intrigue'
                        }
                    ]
                },
                'act_2': {
                    'name': 'THE INVESTIGATION',
                    'duration': 180,
                    'scenes': [
                        {
                            'duration': 60,
                            'narration': f"It started with a simple discovery about {title}. But the more I investigated, the deeper the mystery became.",
                            'visual': 'Investigation begins'
                        },
                        {
                            'duration': 60,
                            'narration': "I found documents nobody was supposed to see. Interviews with people who were silenced. Evidence that contradicted everything.",
                            'visual': 'Evidence mounting'
                        },
                        {
                            'duration': 60,
                            'narration': "But my investigation attracted attention. Powerful people wanted me to stop. They had everything to lose if the truth came out.",
                            'visual': 'Tension rising'
                        }
                    ]
                },
                'act_3': {
                    'name': 'THE TRUTH',
                    'duration': 120,
                    'scenes': [
                        {
                            'duration': 60,
                            'narration': f"Here's what I found about {title}. It's more incredible than any fiction. And it's completely real.",
                            'visual': 'Major revelation'
                        },
                        {
                            'duration': 60,
                            'narration': "The implications are staggering. This could change how we understand everything about this topic.",
                            'visual': 'Full truth revealed'
                        }
                    ]
                },
                'act_4': {
                    'name': 'THE IMPACT',
                    'duration': 60,
                    'scenes': [
                        {
                            'duration': 30,
                            'narration': f"Today, {title} is no longer hidden. The world knows the truth.",
                            'visual': 'Aftermath'
                        },
                        {
                            'duration': 30,
                            'narration': "What we learned is this: The truth always matters. Even when it's uncomfortable, even when powerful people want to hide it.",
                            'visual': 'Final thought'
                        }
                    ]
                }
            },
            
            'retention_hooks': [
                '0:30 - Opening question',
                '1:30 - Conflict introduced',
                '2:30 - Stakes raised',
                '3:30 - Major revelation hint',
                '4:30 - Climax begins',
                '5:30 - Truth revealed',
                '6:30 - Resolution'
            ]
        }
        
        return script
    
    def run(self):
        """Generate scripts"""
        print("\n" + "="*60)
        print("✍️ STEP 2: SCRIPT GENERATION")
        print("="*60 + "\n")
        
        if not self.topics:
            print("❌ No topics found!")
            return None
        
        topic = self.topics[0]
        print(f"📝 Topic: {topic['title']}\n")
        
        # Generate scripts
        short = self.generate_short_script(topic)
        long = self.generate_long_script(topic)
        
        # Save
        with open(f"{self.output_dir}/short_script.json", 'w') as f:
            json.dump(short, f, indent=2)
        
        with open(f"{self.output_dir}/long_script.json", 'w') as f:
            json.dump(long, f, indent=2)
        
        print(f"""
✅ SCRIPTS GENERATED!

📱 SHORT VIDEO: 45 seconds
   - 4 scenes
   - Hook → Buildup → Twist → CTA
   - Fast paced

📺 LONG VIDEO: 7 minutes  
   - 4 acts with subplots
   - Question → Investigation → Truth → Impact
   - Deep storytelling

✨ Both are COMPLETELY DIFFERENT!
        """)
        
        return {'short': short, 'long': long}

if __name__ == "__main__":
    generator = ScriptGenerator()
    generator.run()
