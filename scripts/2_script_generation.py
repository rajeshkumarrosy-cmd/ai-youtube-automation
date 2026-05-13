import json
import os
from datetime import datetime

class ScriptGenerator:
    def __init__(self):
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
        self.load_topic()
    
    def load_topic(self):
        try:
            with open("output/scripts/trending_topics.json", 'r') as f:
                data = json.load(f)
                self.topic = data.get('selected_topic', {})
        except:
            self.topic = {"title": "Amazing Story"}
    
    def generate_short_script(self):
        """SHORT: 45 seconds"""
        title = self.topic.get('title', 'Amazing Story')
        
        return {
            'type': 'short',
            'duration': 45,
            'title': title,
            'format': 'VERTICAL (9:16)',
            'pacing': 'FAST',
            'scenes': [
                {
                    'scene': 1,
                    'duration': 5,
                    'type': 'HOOK',
                    'narration': f"What if {title.lower()} actually happened?",
                    'visual_search': 'shocking revelation dramatic',
                    'emotion': 'SHOCK'
                },
                {
                    'scene': 2,
                    'duration': 20,
                    'type': 'BUILDUP',
                    'narration': f"Scientists discovered something incredible about {title}. The evidence is overwhelming.",
                    'visual_search': 'evidence investigation discovery',
                    'emotion': 'MYSTERY'
                },
                {
                    'scene': 3,
                    'duration': 15,
                    'type': 'TWIST',
                    'narration': f"But here's the truth about {title} that will shock you. This changes EVERYTHING.",
                    'visual_search': 'shocking truth revelation amazing',
                    'emotion': 'SHOCK'
                },
                {
                    'scene': 4,
                    'duration': 5,
                    'type': 'CTA',
                    'narration': "Subscribe for more incredible stories.",
                    'visual_search': 'subscribe button',
                    'emotion': 'ENGAGEMENT'
                }
            ]
        }
    
    def generate_long_script(self):
        """LONG: 7 minutes"""
        title = self.topic.get('title', 'Amazing Story')
        
        return {
            'type': 'long',
            'duration': 420,
            'title': title,
            'format': 'HORIZONTAL (16:9)',
            'pacing': 'CINEMATIC',
            'scenes': [
                {
                    'scene': 1,
                    'duration': 60,
                    'type': 'INTRODUCTION',
                    'narration': f"Have you ever wondered what really happened with {title}? Today, I'm revealing the complete untold story.",
                    'visual_search': 'cinematic introduction mysterious',
                    'emotion': 'CURIOSITY'
                },
                {
                    'scene': 2,
                    'duration': 90,
                    'type': 'INVESTIGATION BEGINS',
                    'narration': f"My journey investigating {title} started with a simple question. But the more I dug, the deeper the mystery became.",
                    'visual_search': 'investigation research discovery',
                    'emotion': 'INTRIGUE'
                },
                {
                    'scene': 3,
                    'duration': 90,
                    'type': 'EVIDENCE MOUNTING',
                    'narration': f"I found evidence about {title} that contradicted everything. The truth was hidden for years.",
                    'visual_search': 'evidence testimony investigation',
                    'emotion': 'TENSION'
                },
                {
                    'scene': 4,
                    'duration': 90,
                    'type': 'THE THREAT',
                    'narration': f"My investigation into {title} attracted unwanted attention. Powerful people wanted me to stop.",
                    'visual_search': 'danger threat conflict',
                    'emotion': 'DANGER'
                },
                {
                    'scene': 5,
                    'duration': 60,
                    'type': 'BREAKTHROUGH',
                    'narration': f"Then I found it. The smoking gun. Proof that {title} was completely different from what we believed.",
                    'visual_search': 'breakthrough discovery truth',
                    'emotion': 'REVELATION'
                },
                {
                    'scene': 6,
                    'duration': 60,
                    'type': 'FULL TRUTH',
                    'narration': f"Here's what really happened with {title}. The complete, unfiltered truth.",
                    'visual_search': 'amazing revelation truth',
                    'emotion': 'SHOCK'
                },
                {
                    'scene': 7,
                    'duration': 60,
                    'type': 'IMPLICATIONS',
                    'narration': f"The implications of {title} are staggering. We can never look at this the same way again.",
                    'visual_search': 'impact consequence change',
                    'emotion': 'AWESTRUK'
                },
                {
                    'scene': 8,
                    'duration': 30,
                    'type': 'CLOSING',
                    'narration': f"The truth of {title} is finally being told. Share this with everyone.",
                    'visual_search': 'conclusion resolution',
                    'emotion': 'EMPOWERMENT'
                }
            ]
        }
    
    def run(self):
        print("\n" + "="*70)
        print("✍️ STEP 2: SCRIPT GENERATION")
        print("="*70)
        
        if not self.topic.get('title'):
            print("❌ No topic found!")
            return None
        
        print(f"\n📝 Topic: {self.topic['title']}\n")
        
        short = self.generate_short_script()
        long = self.generate_long_script()
        
        with open(f"{self.output_dir}/short_script.json", 'w') as f:
            json.dump(short, f, indent=2)
        
        with open(f"{self.output_dir}/long_script.json", 'w') as f:
            json.dump(long, f, indent=2)
        
        print(f"✅ SHORT SCRIPT: 45 seconds, 4 scenes")
        print(f"✅ LONG SCRIPT: 7 minutes, 8 scenes\n")
        
        return {'short': short, 'long': long}

if __name__ == "__main__":
    generator = ScriptGenerator()
    generator.run()
