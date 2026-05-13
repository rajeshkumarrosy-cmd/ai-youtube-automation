import json
import os
from datetime import datetime

class ScriptGenerator:
    def __init__(self):
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
        self.load_topics()
    
    def load_topics(self):
        try:
            with open("output/scripts/trending_topics.json", 'r') as f:
                self.topics = json.load(f)['topics']
        except:
            self.topics = []
    
    def generate_short(self, topic):
        title = topic['title']
        
        script = {
            'type': 'short',
            'duration': 45,
            'topic': title,
            'scenes': [
                {
                    'scene': 1,
                    'duration': 5,
                    'text': f"What if {title.lower()} is actually real?"
                },
                {
                    'scene': 2,
                    'duration': 25,
                    'text': f"Experts discovered something shocking about {title}. The truth is more incredible than anyone imagined."
                },
                {
                    'scene': 3,
                    'duration': 15,
                    'text': f"Here's what nobody expected about {title}. This changes everything."
                }
            ]
        }
        return script
    
    def generate_long(self, topic):
        title = topic['title']
        
        script = {
            'type': 'long',
            'duration': 420,
            'topic': title,
            'scenes': [
                {
                    'scene': 1,
                    'duration': 60,
                    'text': f"Have you ever wondered about {title}? Today, I'm revealing the complete truth."
                },
                {
                    'scene': 2,
                    'duration': 120,
                    'text': f"My investigation into {title} took me around the world. I found documents nobody was supposed to see."
                },
                {
                    'scene': 3,
                    'duration': 120,
                    'text': f"Here's what I discovered about {title}. The evidence is overwhelming and undeniable."
                },
                {
                    'scene': 4,
                    'duration': 120,
                    'text': f"The implications of {title} are staggering. This could change how we understand everything."
                }
            ]
        }
        return script
    
    def run(self):
        print("\n" + "="*60)
        print("✍️ STEP 2: SCRIPT GENERATION")
        print("="*60)
        
        if not self.topics:
            print("❌ No topics found!")
            return None
        
        topic = self.topics[0]
        print(f"\n📝 Topic: {topic['title']}\n")
        
        short = self.generate_short(topic)
        long = self.generate_long(topic)
        
        with open(f"{self.output_dir}/short_script.json", 'w') as f:
            json.dump(short, f, indent=2)
        
        with open(f"{self.output_dir}/long_script.json", 'w') as f:
            json.dump(long, f, indent=2)
        
        print("✅ Short script: 45 seconds, 3 scenes")
        print("✅ Long script: 7 minutes, 4 scenes\n")
        
        return {'short': short, 'long': long}

if __name__ == "__main__":
    generator = ScriptGenerator()
    generator.run()
