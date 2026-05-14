#!/usr/bin/env python3
"""
Step 2: Script Generation
Generates short and long scripts using AI or templates
"""

import os
import json
import subprocess

print("\n" + "="*60)
print("✍️ STEP 2: SCRIPT GENERATION")
print("="*60)

# Create output folder
os.makedirs("output", exist_ok=True)

# Load the trending topic from Step 1
try:
    with open("output/trend.json", "r") as f:
        trend_data = json.load(f)
        topic = trend_data.get("topic", "An amazing discovery")
except:
    print("⚠️ No trend data found, using default topic")
    topic = "An amazing discovery changes everything"

print(f"\n📝 Topic: {topic}")

# ================================================================
# GENERATE SHORT SCRIPT (30-60 seconds)
# ================================================================

print("\n📱 Generating SHORT script...")

short_prompt = f"""
Create a 30-60 second viral YouTube SHORT script about: {topic}

Requirements:
- HOOK in first 5 seconds (grab attention!)
- 4 scenes with timings
- Shocking twist
- Call to action
- Make it PUNCHY and FAST

Format as JSON:
{{
    "title": "script title",
    "hook": "opening line",
    "scenes": [
        {{"number": 1, "duration": "5-10s", "description": "scene description"}},
        {{"number": 2, "duration": "5-10s", "description": "scene description"}},
        {{"number": 3, "duration": "5-10s", "description": "scene description"}},
        {{"number": 4, "duration": "5-10s", "description": "scene description"}}
    ],
    "ending": "call to action"
}}
"""

short_script = None

# Try to generate with AI
try:
    print("   🤖 Generating with AI...")
    result = subprocess.run(
        ["ollama", "run", "mistral", short_prompt],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    # Try to parse JSON from output
    import re
    json_match = re.search(r'\{.*\}', result.stdout, re.DOTALL)
    if json_match:
        short_script = json.loads(json_match.group())
        print("   ✅ AI generated short script")
except:
    print("   ⚠️ AI generation failed, using template")
    short_script = None

# Fallback to template
if not short_script:
    short_script = {
        "title": f"Shocking Discovery: {topic}",
        "hook": "Wait... you won't believe what just happened!",
        "scenes": [
            {
                "number": 1,
                "duration": "10s",
                "description": f"A mysterious discovery about {topic}"
            },
            {
                "number": 2,
                "duration": "10s",
                "description": "The situation becomes shocking"
            },
            {
                "number": 3,
                "duration": "10s",
                "description": "An unexpected twist revealed"
            },
            {
                "number": 4,
                "duration": "10s",
                "description": "The real truth emerges"
            }
        ],
        "ending": "Subscribe for more shocking discoveries!"
    }

print(f"   ✅ Short script: {len(short_script['scenes'])} scenes")

# ================================================================
# GENERATE LONG SCRIPT (5-8 minutes)
# ================================================================

print("\n📺 Generating LONG script...")

long_prompt = f"""
Create a 5-8 minute cinematic story script about: {topic}

Requirements:
- HOOK in first 30 seconds
- 8 scenes with detailed descriptions
- Rising action and climax
- Emotional beats
- Professional storytelling

Format as JSON:
{{
    "title": "story title",
    "description": "brief description",
    "scenes": [
        {{"number": 1, "duration": "60s", "description": "scene description"}},
        {{"number": 2, "duration": "60s", "description": "scene description"}},
        (... 6 more scenes ...)
    ],
    "ending": "conclusion message"
}}
"""

long_script = None

# Try to generate with AI
try:
    print("   🤖 Generating with AI...")
    result = subprocess.run(
        ["ollama", "run", "mistral", long_prompt],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    # Try to parse JSON from output
    import re
    json_match = re.search(r'\{.*\}', result.stdout, re.DOTALL)
    if json_match:
        long_script = json.loads(json_match.group())
        print("   ✅ AI generated long script")
except:
    print("   ⚠️ AI generation failed, using template")
    long_script = None

# Fallback to template
if not long_script:
    long_script = {
        "title": f"The Complete Story: {topic}",
        "description": f"A complete narrative journey about {topic}",
        "scenes": [
            {
                "number": 1,
                "duration": "60s",
                "description": "Introduction and setup"
            },
            {
                "number": 2,
                "duration": "60s",
                "description": "First revelation"
            },
            {
                "number": 3,
                "duration": "60s",
                "description": "Complication arrives"
            },
            {
                "number": 4,
                "duration": "60s",
                "description": "Tension builds"
            },
            {
                "number": 5,
                "duration": "60s",
                "description": "Major twist revealed"
            },
            {
                "number": 6,
                "duration": "60s",
                "description": "Consequences unfold"
            },
            {
                "number": 7,
                "duration": "60s",
                "description": "Climax moment"
            },
            {
                "number": 8,
                "duration": "60s",
                "description": "Resolution and ending"
            }
        ],
        "ending": "Remember to subscribe and like!"
    }

print(f"   ✅ Long script: {len(long_script['scenes'])} scenes")

# ================================================================
# SAVE SCRIPTS TO JSON
# ================================================================

print("\n💾 Saving scripts...")

scripts_data = {
    "topic": topic,
    "short": short_script,
    "long": long_script,
    "generated_at": str(os.popen("date").read().strip())
}

# Save main scripts file
with open("output/scripts.json", "w") as f:
    json.dump(scripts_data, f, indent=2)

print("   ✅ Saved: output/scripts.json")

# Also save individual script files for reference
with open("output/short_script.json", "w") as f:
    json.dump(short_script, f, indent=2)

print("   ✅ Saved: output/short_script.json")

with open("output/long_script.json", "w") as f:
    json.dump(long_script, f, indent=2)

print("   ✅ Saved: output/long_script.json")

# ================================================================
# SUMMARY
# ================================================================

print("\n" + "="*60)
print("✅ SCRIPT GENERATION COMPLETE")
print("="*60)

print(f"""
📝 Scripts Generated:

SHORT VIDEO:
   Title: {short_script['title']}
   Hook: {short_script['hook']}
   Scenes: {len(short_script['scenes'])}
   Duration: ~45 seconds

LONG VIDEO:
   Title: {long_script['title']}
   Description: {long_script['description']}
   Scenes: {len(long_script['scenes'])}
   Duration: ~8 minutes

📁 Files Saved:
   ✅ output/scripts.json (main file)
   ✅ output/short_script.json
   ✅ output/long_script.json
""")

print()
