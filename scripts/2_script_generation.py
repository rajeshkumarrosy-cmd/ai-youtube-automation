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
                self.topic = data['selected_topic']
        except:
            self.topic = {"title": "Default Story"}
    
    def generate_short_script(self):
        """SHORT: 45 seconds - FAST PACED"""
        title = self.topic['title']
        
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
                    'narration': f"Scientists made an incredible discovery. Nobody expected this about {title}. The evidence is overwhelming.",
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
            ],
            'total_narration': "What if it actually happened? Scientists made an incredible discovery. Nobody expected this. The evidence is overwhelming. But here's the truth that will shock you. This changes everything. Subscribe for more incredible stories."
        }
    
    def generate_long_script(self):
        """LONG: 7 minutes - DEEP STORYTELLING (COMPLETELY DIFFERENT)"""
        title = self.topic['title']
        
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
                    'narration': f"Have you ever wondered what really happened with {title}? Today, I'm revealing the complete untold story. The truth has been hidden for years, but I finally uncovered it.",
                    'visual_search': 'cinematic introduction mysterious',
                    'emotion': 'CURIOSITY'
                },
                {
                    'scene': 2,
                    'duration': 90,
                    'type': 'INVESTIGATION BEGINS',
                    'narration': f"My journey investigating {title} started with a simple question. But the more I dug, the deeper the mystery became. I found documents nobody was supposed to see.",
                    'visual_search': 'investigation research discovery',
                    'emotion': 'INTRIGUE'
                },
                {
                    'scene': 3,
                    'duration': 90,
                    'type': 'EVIDENCE MOUNTING',
                    'narration': f"I interviewed witnesses who risked everything to tell the truth about {title}. Their stories contradicted everything the government said. The evidence was undeniable.",
                    'visual_search': 'interview testimony evidence',
                    'emotion': 'TENSION'
                },
                {
                    'scene': 4,
                    'duration': 90,
                    'type': 'THE THREAT',
                    'narration': f"But my investigation attracted unwanted attention. Powerful people wanted me to stop. They had everything to lose if the truth about {title} came out.",
                    'visual_search': 'danger threat conflict',
                    'emotion': 'DANGER'
                },
                {
                    'scene': 5,
                    'duration': 60,
                    'type': 'BREAKTHROUGH',
                    'narration': f"Then I found it. The smoking gun. The proof that everything about {title} was a lie. This could change history.",
                    'visual_search': 'breakthrough discovery truth',
                    'emotion': 'REVELATION'
                },
                {
                    'scene': 6,
                    'duration': 60,
                    'type': 'FULL TRUTH',
                    'narration': f"Here's what really happened with {title}. The complete, unfiltered truth. This is bigger than anyone imagined.",
                    'visual_search': 'amazing revelation truth',
                    'emotion': 'SHOCK'
                },
                {
                    'scene': 7,
                    'duration': 60,
                    'type': 'IMPLICATIONS',
                    'narration': f"The implications of {title} are staggering. This could reshape how we understand everything. We can never look at this the same way again.",
                    'visual_search': 'impact consequence change',
                    'emotion': 'AWESTRUK'
                },
                {
                    'scene': 8,
                    'duration': 30,
                    'type': 'CLOSING',
                    'narration': f"The story of {title} is finally being told. Share this with everyone. The truth cannot be hidden anymore.",
                    'visual_search': 'conclusion resolution',
                    'emotion': 'EMPOWERMENT'
                }
            ],
            'total_narration': "Have you ever wondered what really happened? Today I'm revealing the complete untold story. The truth has been hidden for years. My journey started with a simple question. The deeper I dug, the deeper the mystery became. I found documents nobody was supposed to see. I interviewed witnesses who risked everything. Their stories contradicted everything the government said. My investigation attracted unwanted attention. Powerful people wanted me to stop. Then I found it. The smoking gun. The proof that everything was a lie. Here's what really happened. The complete, unfiltered truth. This is bigger than anyone imagined. The implications are staggering. We can never look at this the same way again. The story is finally being told. Share this with everyone. The truth cannot be hidden anymore."
        }
    
    def run(self):
        print("\n" + "="*70)
        print("✍️ STEP 2: SCRIPT GENERATION (COMPLETELY DIFFERENT)")
        print("="*70)
        
        short = self.generate_short_script()
        long = self.generate_long_script()
        
        with open(f"{self.output_dir}/short_script.json", 'w') as f:
            json.dump(short, f, indent=2)
        
        with open(f"{self.output_dir}/long_script.json", 'w') as f:
            json.dump(long, f, indent=2)
        
        print(f"\n✅ SHORT SCRIPT: 45 seconds")
        print(f"   - 4 scenes")
        print(f"   - FAST paced")
        print(f"   - Hook → Buildup → Twist → CTA")
        
        print(f"\n✅ LONG SCRIPT: 7 minutes (COMPLETELY DIFFERENT)")
        print(f"   - 8 scenes")
        print(f"   - CINEMATIC pacing")
        print(f"   - Full story arc with investigation + breakthrough\n")
        
        return {'short': short, 'long': long}

if __name__ == "__main__":
    generator = ScriptGenerator()
    generator.run()
