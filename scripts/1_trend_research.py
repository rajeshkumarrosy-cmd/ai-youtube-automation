import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import random

class TrendResearcher:
    def __init__(self):
        self.trends = []
        self.output_file = "output/scripts/trending_topics.json"
    
    def get_youtube_trends(self):
        """Scrape YouTube trending page"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # YouTube Trends (using RSS feed)
            url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCkRfArvrzheW2E7b6SVV8UQ"
            response = requests.get("https://trends.google.com/trending/rss?geo=IN", headers=headers, timeout=10)
            
            print("✅ YouTube trends fetched")
            return response.text
        except Exception as e:
            print(f"⚠️ YouTube trends error: {e}")
            return None
    
    def get_reddit_trends(self):
        """Scrape Reddit trending topics"""
        try:
            subreddits = [
                "r/AnimationStudios",
                "r/storytelling",
                "r/horror",
                "r/Damnthatsinteresting",
                "r/MadeMeSmile",
                "r/KidsStories"
            ]
            
            reddit_trends = []
            for sub in subreddits:
                url = f"https://www.reddit.com/{sub}/hot.json"
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    for post in data['data']['children'][:3]:
                        reddit_trends.append({
                            'title': post['data']['title'],
                            'score': post['data']['score'],
                            'source': 'Reddit'
                        })
            
            print(f"✅ Reddit trends fetched: {len(reddit_trends)} topics")
            return reddit_trends
        except Exception as e:
            print(f"⚠️ Reddit error: {e}")
            return []
    
    def get_google_trends(self):
        """Get Google Trends data"""
        try:
            # Manual trending topics (since API requires setup)
            google_trends = [
                "AI animation stories",
                "Motivational stories",
                "Mystery stories",
                "Mythology explained",
                "Emotional storytelling",
                "Fantasy adventures",
                "Horror animations",
                "Funny animal videos",
                "Life lessons",
                "Sci-fi concepts"
            ]
            print("✅ Google Trends loaded (manual)")
            return google_trends
        except Exception as e:
            print(f"⚠️ Google Trends error: {e}")
            return []
    
    def get_animation_niche_topics(self):
        """Get viral animation niche topics"""
        topics = {
            "Kids Stories": [
                "The Little Girl Who Saved Her Village",
                "Magic Forest Adventure",
                "Friendship Forever",
                "Dream Come True",
                "Hidden Treasure Quest"
            ],
            "Horror Animation": [
                "The Haunted House Mystery",
                "Midnight Terror",
                "The Shadow Man",
                "Cursed Artifact",
                "Ghost in the Machine"
            ],
            "Motivational": [
                "From Zero to Hero",
                "Never Give Up Story",
                "Overcoming Impossible Odds",
                "The Power of Kindness",
                "Success Against All Odds"
            ],
            "Mystery": [
                "The Missing Scientist",
                "Unsolved Disappearance",
                "Secret Underground City",
                "The Time Traveler",
                "Ancient Prophecy"
            ],
            "Sci-Fi": [
                "AI Becomes Conscious",
                "First Contact with Aliens",
                "Time Loop Mystery",
                "Parallel Universe",
                "Future World Discovery"
            ],
            "Mythology": [
                "Greek Gods Today",
                "Hindu Mythology Explained",
                "Norse Gods Adventure",
                "Egyptian Legends",
                "Lost Civilizations"
            ]
        }
        return topics
    
    def analyze_engagement_potential(self, topic):
        """Score topic for viral potential"""
        score = 0
        viral_keywords = [
            'mystery', 'hidden', 'secret', 'shocking', 'twist',
            'emotional', 'heartwarming', 'incredible', 'impossible',
            'haunted', 'supernatural', 'magic', 'adventure'
        ]
        
        topic_lower = topic.lower()
        for keyword in viral_keywords:
            if keyword in topic_lower:
                score += 15
        
        return min(score, 100)
    
    def select_daily_topic(self):
        """Select best topic for today"""
        all_topics = []
        
        # Combine all sources
        reddit = self.get_reddit_trends()
        google = self.get_google_trends()
        niche = self.get_animation_niche_topics()
        
        # Flatten and score
        for category, topics in niche.items():
            for topic in topics:
                all_topics.append({
                    'title': topic,
                    'category': category,
                    'engagement_score': self.analyze_engagement_potential(topic),
                    'source': 'Niche Database'
                })
        
        # Sort by engagement score
        all_topics.sort(key=lambda x: x['engagement_score'], reverse=True)
        
        # Select top 3 for variety
        selected = all_topics[:3]
        
        return selected
    
    def save_trends(self, topics):
        """Save trends to file"""
        data = {
            'date': datetime.now().isoformat(),
            'topics': topics,
            'total_researched': len(topics)
        }
        
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Trends saved to {self.output_file}")
        return data
    
    def run(self):
        """Execute trend research"""
        print("🔍 STEP 1: TREND RESEARCH STARTING...")
        
        selected_topics = self.select_daily_topic()
        saved_data = self.save_trends(selected_topics)
        
        print(f"""
        ╔════════════════════════════════════╗
        ║    TRENDING TOPICS SELECTED        ║
        ╚════════════════════════════════════╝
        """)
        
        for i, topic in enumerate(selected_topics, 1):
            print(f"\n{i}. {topic['title']}")
            print(f"   Category: {topic['category']}")
            print(f"   Engagement Score: {topic['engagement_score']}/100")
        
        return saved_data

if __name__ == "__main__":
    researcher = TrendResearcher()
    researcher.run()
