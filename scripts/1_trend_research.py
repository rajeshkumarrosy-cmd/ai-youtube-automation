#!/usr/bin/env python3
"""
Step 1: Trend Research
Finds trending topics for video content
"""

import os
import json
import requests

print("\n" + "="*60)
print("📈 STEP 1: TREND RESEARCH")
print("="*60)

# Create output folder
os.makedirs("output", exist_ok=True)

# Default topics (fallback)
default_topics = [
    "AI Becomes Conscious",
    "Mysterious Discovery Changes Everything",
    "A Boy Finds Out His Best Friend Is An AI",
    "The Truth Nobody Knows About",
    "Shocking Secret Revealed",
    "The Impossible Happened",
    "Unbelievable Moment Caught On Camera"
]

topic = None

# Try to fetch from Reddit
print("\n🔍 Searching for trending topics...")

try:
    print("   Checking Reddit...")
    url = "https://www.reddit.com/r/Damnthatsinteresting/top.json?t=day"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers, timeout=10)
    posts = response.json()['data']['children']
    
    if posts:
        topic = posts[0]['data']['title']
        print(f"   ✅ Found trending topic: {topic}")
except Exception as e:
    print(f"   ⚠️ Reddit fetch failed: {e}")

# Fallback to default topic
if not topic:
    import random
    topic = random.choice(default_topics)
    print(f"   Using default topic: {topic}")

# ================================================================
# SAVE TREND DATA
# ================================================================

print("\n💾 Saving trend data...")

trend_data = {
    "topic": topic,
    "source": "reddit" if topic not in default_topics else "default",
    "timestamp": str(os.popen("date").read().strip())
}

with open("output/trend.json", "w") as f:
    json.dump(trend_data, f, indent=2)

print(f"   ✅ Saved: output/trend.json")

# ================================================================
# SUMMARY
# ================================================================

print("\n" + "="*60)
print("✅ TREND RESEARCH COMPLETE")
print("="*60)

print(f"""
📰 Today's Topic: {topic}

📁 Files Saved:
   ✅ output/trend.json
""")

print()
