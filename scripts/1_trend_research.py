import requests
import json
from datetime import datetime
import os
import random

class TrendResearcher:
    """
    Finds trending topics with comprehensive research
    """
    
    def __init__(self):
        self.output_dir = "output/scripts"
        os.makedirs(self.output_dir, exist_ok=True)
        self.output_file = f"{self.output_dir}/trending_topics.json"
    
    def get_animation_topics(self):
        """Get proven viral animation topics"""
        topics = {
            "Sci-Fi Animation": [
                "AI Becomes Conscious - What Happened Next",
                "First Contact With Aliens Discovered",
                "Time Traveler Found In 2024",
                "Parallel Universe Portal Opened",
                "Future Technology From Tomorrow",
                "The Last AI on Earth",
                "Robot Falls in Love",
                "Simulation Theory Proven True"
            ],
            "Mystery & Thriller": [
                "The Disappearance That Shocked the World",
                "Unsolved Mystery Finally Solved",
                "The Hidden Truth About Area 51",
                "Lost City of Gold Found",
                "The Man Who Lived 200 Years",
                "Cursed Artifact Discovered",
                "The Shadow Government Exposed",
                "Ancient Prophecy Came True"
            ],
            "Emotional Stories": [
                "The Last Letter He Never Read",
                "Love Story Across Time",
                "The Sacrifice Nobody Knew About",
                "Finding Family After 50 Years",
                "Second Chance at Life",
                "The Forgiveness That Changed Everything",
                "Mother Reunites With Lost Child",
                "True Love Against All Odds"
            ],
            "Motivational": [
                "From Homeless to Billionaire",
                "Never Give Up - Incredible True Story",
                "The Boy Nobody Believed In",
                "Against All Odds - True Survival",
                "Impossible Dream Achieved",
                "The Power of One Person",
                "Overcoming Disability to Success",
                "From Failure to Greatest Success"
            ],
            "Horror Animation": [
                "The Haunting of Blackwood Manor",
                "Midnight Terror in the City",
                "The Shadow Nobody Can Escape",
                "Cursed Video That Kills Watchers",
                "The Entity in the Walls",
                "Night of the Living Dead Returns",
                "The Possession Nobody Survived",
                "Evil in the Mirror"
            ],
            "Adventure & Action": [
                "Treasure Hunt Around the World",
                "The Greatest Heist Ever Planned",
                "Escape From Impossible Prison",
                "The Quest for Lost Atlantis",
                "Mountain Climber's Incredible Journey",
                "Explorer Finds Hidden Civilization",
                "The Adventure Nobody Survived",
                "Race Against Time"
            ]
        }
        return topics
    
    def calculate_viral_score(self, title):
        """Score topic for viral potential (0-100)"""
        score = 50  # Base score
        
        # Trigger words
        triggers = {
            'shocking': 15, 'unbelievable': 15, 'impossible': 12,
            'finally': 10, 'truth': 12, 'secret': 12, 'hidden': 12,
            'never': 10, 'incredible': 12, 'amazing': 10,
            'nobody': 8, 'mysterious': 10, 'haunted': 12,
            'discovered': 10, 'revealed': 10, 'exposed': 10
        }
        
        title_lower = title.lower()
        for trigger, points in triggers.items():
            if trigger in title_lower:
                score += points
        
        # Cap at 100
        return min(score, 100)
    
    def run(self):
        """Execute trend research"""
        print("\n" + "="*60)
        print("📈 STEP 1: TREND RESEARCH")
        print("="*60 + "\n")
        
        # Get topics
        all_topics_dict = self.get_animation_topics()
        
        # Score all topics
        all_topics = []
        for category, topic_list in all_topics_dict.items():
            for topic in topic_list:
                score = self.calculate_viral_score(topic)
                all_topics.append({
                    'title': topic,
                    'category': category,
                    'engagement_score': score,
                    'source': 'Viral Database'
                })
        
        # Sort by score
        all_topics.sort(key=lambda x: x['engagement_score'], reverse=True)
        
        # Select top 5
        selected = all_topics[:5]
        
        # Save
        data = {
            'generated_at': datetime.now().isoformat(),
            'topics': selected,
            'total_researched': len(all_topics)
        }
        
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print("✅ Top 5 Trending Topics Found:\n")
        for i, topic in enumerate(selected, 1):
            print(f"{i}. {topic['title']}")
            print(f"   Category: {topic['category']}")
            print(f"   Score: {topic['engagement_score']}/100\n")
        
        print(f"✅ Selected Topic: {selected[0]['title']}")
        print(f"📁 Saved to: {self.output_file}")
        
        return data

if __name__ == "__main__":
    researcher = TrendResearcher()
    researcher.run()
