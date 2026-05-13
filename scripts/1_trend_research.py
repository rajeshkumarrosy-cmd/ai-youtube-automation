import json
import os
from datetime import datetime

class TrendResearcher:
    def __init__(self):
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_topics(self):
        topics = [
            {"title": "AI Becomes Conscious - What Happened Next", "category": "Sci-Fi"},
            {"title": "Time Traveler Found In 2024", "category": "Sci-Fi"},
            {"title": "Lost City of Gold Discovered", "category": "Mystery"},
            {"title": "The Disappearance That Shocked The World", "category": "Mystery"},
            {"title": "From Homeless to Billionaire", "category": "Motivational"},
        ]
        return topics
    
    def run(self):
        print("\n" + "="*60)
        print("📈 STEP 1: TREND RESEARCH")
        print("="*60)
        
        topics = self.get_topics()
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'topics': topics[:1],
        }
        
        output_file = f"{self.output_dir}/trending_topics.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✅ Selected Topic: {topics[0]['title']}")
        print(f"📁 Saved to: {output_file}\n")
        
        return data

if __name__ == "__main__":
    researcher = TrendResearcher()
    researcher.run()
