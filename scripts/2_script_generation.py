import json
import os
from datetime import datetime

class ScriptGenerator:
    def __init__(self):
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
        self.topic = self.load_topic()
    
    def load_topic(self):
        try:
            with open("output/scripts/trending_topics.json", 'r') as f:
                return json.load(f)['selected_topic']
        except:
            return {
                "title": "Amazing Story",
                "short_hook": "What if this was real?",
                "long_hook": "The truth behind this story will shock you"
            }
    
    def generate_short_script(self):
        """
        SHORT VIDEO: 45 seconds
        Fast paced, shocking, viral
        """
        title = self.topic['title']
        hook = self.topic['short_hook']
        
        return {
            'type': 'short',
            'duration': 45,
            'title': title,
            'format': 'VERTICAL 9:16',
            'scenes': [
                {
                    'scene_number': 1,
                    'duration': 5,
                    'narration': f"{hook}!",
                    'visual_type': 'hook',
                    'background_color': '1a1a2e'
                },
                {
                    'scene_number': 2,
                    'duration': 20,
                    'narration': f"This is the story of {title}. Scientists and experts were completely shocked by what they found. Nobody expected this.",
                    'visual_type': 'story',
                    'background_color': '16213e'
                },
                {
                    'scene_number': 3,
                    'duration': 15,
                    'narration': f"The truth about {title} will change how you see everything. This is completely real.",
                    'visual_type': 'twist',
                    'background_color': '0f3460'
                },
                {
                    'scene_number': 4,
                    'duration': 5,
                    'narration': "Subscribe for more incredible stories every day!",
                    'visual_type': 'cta',
                    'background_color': 'e94560'
                }
            ]
        }
    
    def generate_long_script(self):
        """
        LONG VIDEO: 7 minutes
        COMPLETELY DIFFERENT from short
        Deep investigation style
        """
        title = self.topic['title']
        hook = self.topic['long_hook']
        
        return {
            'type': 'long',
            'duration': 420,
            'title': title,
            'format': 'HORIZONTAL 16:9',
            'scenes': [
                {
                    'scene_number': 1,
                    'duration': 45,
                    'narration': f"{hook}. Today we uncover the complete story that nobody has told before.",
                    'visual_type': 'opening',
                    'background_color': '0d0d0d'
                },
                {
                    'scene_number': 2,
                    'duration': 75,
                    'narration': f"The story of {title} began years ago. Most people have no idea what really happened. I spent months investigating this.",
                    'visual_type': 'backstory',
                    'background_color': '1a0a00'
                },
                {
                    'scene_number': 3,
                    'duration': 75,
                    'narration': f"When I started investigating {title}, I found documents that were never meant to be public. The evidence was overwhelming.",
                    'visual_type': 'investigation',
                    'background_color': '000a1a'
                },
                {
                    'scene_number': 4,
                    'duration': 60,
                    'narration': f"I interviewed people who witnessed {title} firsthand. Their accounts were impossible to believe. But they were telling the truth.",
                    'visual_type': 'testimony',
                    'background_color': '1a001a'
                },
                {
                    'scene_number': 5,
                    'duration': 60,
                    'narration': f"The deeper I went into {title}, the more dangerous it became. Powerful people did not want this story told.",
                    'visual_type': 'danger',
                    'background_color': '1a0000'
                },
                {
                    'scene_number': 6,
                    'duration': 60,
                    'narration': f"But then I found it. The proof. Everything about {title} was confirmed. This changes history.",
                    'visual_type': 'revelation',
                    'background_color': '001a00'
                },
                {
                    'scene_number': 7,
                    'duration': 30,
                    'narration': f"The truth about {title} is now out. Share this story. The world needs to know.",
                    'visual_type': 'closing',
                    'background_color': '0d0d0d'
                },
                {
                    'scene_number': 8,
                    'duration': 15,
                    'narration': "Subscribe for more incredible investigations. New story every single day.",
                    'visual_type': 'cta',
                    'background_color': '1a1a00'
                }
            ]
        }
    
    def run(self):
        print("\n" + "="*60)
        print("✍️ STEP 2: SCRIPT GENERATION")
        print("="*60)
        
        print(f"\n📝 Topic: {self.topic['title']}\n")
        
        short = self.generate_short_script()
        long = self.generate_long_script()
        
        with open(f"{self.output_dir}/short_script.json", 'w') as f:
            json.dump(short, f, indent=2)
        
        with open(f"{self.output_dir}/long_script.json", 'w') as f:
            json.dump(long, f, indent=2)
        
        print("✅ SHORT SCRIPT: 45 seconds, 4 scenes")
        print("   → Fast paced, viral style")
        print("\n✅ LONG SCRIPT: 7 minutes, 8 scenes")
        print("   → Deep investigation style")
        print("   → COMPLETELY DIFFERENT from short\n")
        
        return {'short': short, 'long': long}

if __name__ == "__main__":
    ScriptGenerator().run()
