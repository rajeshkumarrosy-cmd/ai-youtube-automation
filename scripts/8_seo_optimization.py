import json

class SEOOptimizer:
    def __init__(self):
        self.topic = self.load_topic()
    
    def load_topic(self):
        """Load topic"""
        try:
            with open("output/scripts/trending_topics.json", 'r') as f:
                data = json.load(f)
                return data['topics'][0]
        except:
            return {'title': 'Untitled'}
    
    def generate_titles(self):
        """Generate multiple viral titles"""
        topic = self.topic['title']
        
        titles = [
            f"{topic} - You Won't Believe What Happened Next",
            f"The {topic} Story That Shocked Millions",
            f"{topic}: The Hidden Truth Revealed",
            f"How {topic} Changed Everything | Incredible Story",
            f"{topic} - A Story Nobody Expected"
        ]
        
        return titles
    
    def generate_descriptions(self):
        """Generate SEO-optimized descriptions"""
        topic = self.topic['title']
        
        description = f"""
{topic} - An incredible story that will blow your mind! 🤯

In this video, we explore the fascinating world of {topic}. This amazing journey will teach you valuable lessons about life, emotions, and the unexpected.

🎬 What happens in this video:
✅ The incredible setup
✅ The shocking twist
✅ The powerful lesson

📌 Tags: {topic}, story, animation, life lesson, incredible, emotional

⏰ WATCH TILL THE END for an incredible surprise!

👍 Like, Comment, and Subscribe for more amazing stories every day!

#Animation #Story #IncredibleStory
        """
        
        return description.strip()
    
    def generate_hashtags(self):
        """Generate trending hashtags"""
        topic = self.topic['title']
        
        hashtags = [
            "#AnimationStory",
            "#MustWatch",
            "#IncredibleStory",
            "#EmotionalStory",
            "#AnimationChannel",
            "#StorytimeAnimation",
            "#ViralStory",
            f"#{topic.replace(' ', '')[:20]}",
            "#YouTubeShorts",
            "#Trending"
        ]
        
        return hashtags
    
    def generate_keywords(self):
        """Generate search keywords"""
        topic = self.topic['title']
        
        keywords = [
            topic,
            f"{topic} animation",
            f"{topic} story",
            "animated story",
            "emotional story animation",
            "incredible story",
            "life lessons",
            "animation channel",
            "storytelling",
            "short story animation"
        ]
        
        return keywords
    
    def generate_tags(self):
        """Generate YouTube tags"""
        return self.generate_keywords()
    
    def optimize_for_shorts(self):
        """Optimize for YouTube Shorts"""
        return {
            'duration': '15-60 seconds',
            'aspect_ratio': '9:16',
            'text_placement': 'center, high contrast',
            'music': 'trending, catchy, copyright-free',
            'retention': 'hook in first 2 seconds, avoid pauses'
        }
    
    def optimize_for_long_form(self):
        """Optimize for long-form videos"""
        return {
            'duration': '5-8 minutes',
            'aspect_ratio': '16:9',
            'retention': 'engagement hook every 15 seconds',
            'pacing': 'fast cuts, dynamic transitions',
            'storytelling': 'cinematic, emotional, climax-driven'
        }
    
    def generate_seo_package(self):
        """Generate complete SEO package"""
        seo_data = {
            'best_title': self.generate_titles()[0],
            'all_titles': self.generate_titles(),
            'description': self.generate_descriptions(),
            'hashtags': self.generate_hashtags(),
            'keywords': self.generate_keywords(),
            'tags': self.generate_tags(),
            'shorts_optimization': self.optimize_for_shorts(),
            'longform_optimization': self.optimize_for_long_form(),
            'upload_time': '2:00 PM UTC',  # Best engagement time
            'upload_days': ['Tuesday', 'Thursday', 'Saturday']
        }
        
        return seo_data
    
    def save_seo_data(self, seo_data):
        """Save SEO package"""
        with open("output/seo_package.json", 'w') as f:
            json.dump(seo_data, f, indent=2)
        
        return "output/seo_package.json"
    
    def run(self):
        """Generate SEO optimization"""
        print("🔍 STEP 8: SEO OPTIMIZATION STARTING...")
        
        seo_data = self.generate_seo_package()
        seo_file = self.save_seo_data(seo_data)
        
        print(f"""
        ╔════════════════════════════════════╗
        ║    SEO OPTIMIZATION COMPLETE        ║
        ╚════════════════════════════════════╝
        Title: {seo_data['best_title']}
        Keywords: {len(seo_data['keywords'])}
        Hashtags: {len(seo_data['hashtags'])}
        
        SEO Package: {seo_file}
        """)
        
        return seo_data

if __name__ == "__main__":
    optimizer = SEOOptimizer()
    optimizer.run()
