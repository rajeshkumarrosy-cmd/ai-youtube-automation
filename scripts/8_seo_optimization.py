import json
import os

print("\n🔍 STEP 8: SEO OPTIMIZATION")

try:
    with open("output/scripts/trending_topics.json") as f:
        topic = json.load(f)['selected_topic']['title']
except:
    topic = "Amazing Story"

seo = {
    'title': f"{topic} - You Won't Believe What Happened | Animated Story",
    'description': f"This incredible story about {topic} will change your perspective. Watch till the end for the shocking twist!",
    'tags': [
        f"#{topic.replace(' ', '')}",
        "#AnimatedStory",
        "#IncredibleStory",
        "#MustWatch",
        "#Trending"
    ]
}

with open("output/seo_package.json", 'w') as f:
    json.dump(seo, f, indent=2)

print(f"✅ Title: {seo['title'][:60]}...")
print(f"✅ Tags: {', '.join(seo['tags'][:3])}\n")
