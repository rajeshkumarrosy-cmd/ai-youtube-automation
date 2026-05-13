import json
import os
from datetime import datetime
import random

class TrendResearcher:
    def __init__(self):
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_topics(self):
        return [
            {
                "title": "AI Becomes Conscious",
                "category": "Sci-Fi",
                "short_hook": "What if AI suddenly woke up?",
                "long_hook": "The day artificial intelligence became conscious changed everything"
            },
            {
                "title": "Lost City of Gold Found",
                "category": "Mystery",
                "short_hook": "Scientists found something impossible",
                "long_hook": "After 500 years, the lost city was finally discovered"
            },
            {
                "title": "From Homeless to Billionaire",
                "category": "Motivational",
                "short_hook": "One decision changed everything",
                "long_hook": "Nobody believed he could do it. He proved them all wrong"
            },
            {
                "title": "Time Traveler Found in 2024",
                "category": "Sci-Fi",
                "short_hook": "He knew things nobody should know",
                "long_hook": "The stranger appeared from nowhere and knew the future"
            },
            {
                "title": "The Last Human on Earth",
                "category": "Sci-Fi",
                "short_hook": "Everyone was gone. Except one",
                "long_hook": "When the world ended, only one person survived"
            }
        ]
    
    def run(self):
        print("\n" + "="*60)
        print("📈 STEP 1: TREND RESEARCH")
        print("="*60)
        
        topics = self.get_topics()
        selected = random.choice(topics)
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'selected_topic': selected,
            'all_topics': topics
        }
        
        with open(f"{self.output_dir}/trending_topics.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ Selected Topic: {selected['title']}")
        print(f"   Category: {selected['category']}")
        print(f"   Short Hook: {selected['short_hook']}")
        print(f"   Long Hook: {selected['long_hook']}\n")
        
        return data

if __name__ == "__main__":
    TrendResearcher().run()
