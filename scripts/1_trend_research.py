import json
import os
from datetime import datetime
import random

class TrendResearcher:
    def __init__(self):
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_viral_topics(self):
        """Topics that GUARANTEE views"""
        topics = {
            "Sci-Fi": [
                {
                    "title": "AI Becomes Conscious - What Happened Next",
                    "keywords": ["artificial intelligence", "consciousness", "robot"],
                    "duration_short": 45,
                    "duration_long": 420
                },
                {
                    "title": "Time Traveler Discovered in 2024",
                    "keywords": ["time travel", "future", "paradox"],
                    "duration_short": 45,
                    "duration_long": 420
                },
                {
                    "title": "Parallel Universe Portal Opened",
                    "keywords": ["portal", "universe", "dimensions"],
                    "duration_short": 45,
                    "duration_long": 420
                }
            ],
            "Mystery": [
                {
                    "title": "The Disappearance That Shocked The World",
                    "keywords": ["missing", "mystery", "investigation"],
                    "duration_short": 45,
                    "duration_long": 420
                },
                {
                    "title": "Lost City of Gold Finally Found",
                    "keywords": ["treasure", "ancient", "discovery"],
                    "duration_short": 45,
                    "duration_long": 420
                }
            ],
            "Motivational": [
                {
                    "title": "From Homeless to Billionaire - True Story",
                    "keywords": ["success", "inspiration", "transformation"],
                    "duration_short": 45,
                    "duration_long": 420
                },
                {
                    "title": "Never Give Up - Incredible True Story",
                    "keywords": ["motivation", "persistence", "achievement"],
                    "duration_short": 45,
                    "duration_long": 420
                }
            ]
        }
        return topics
    
    def run(self):
        print("\n" + "="*70)
        print("📈 STEP 1: TREND RESEARCH")
        print("="*70)
        
        topics_dict = self.get_viral_topics()
        
        # Select one random topic
        category = random.choice(list(topics_dict.keys()))
        topic = random.choice(topics_dict[category])
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'selected_topic': topic,
            'category': category
        }
        
        output_file = f"{self.output_dir}/trending_topics.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ SELECTED TOPIC:")
        print(f"   Title: {topic['title']}")
        print(f"   Category: {category}")
        print(f"   Saved: {output_file}\n")
        
        return data

if __name__ == "__main__":
    researcher = TrendResearcher()
    researcher.run()
