import os
import json

os.makedirs("output/music_sfx", exist_ok=True)

print("\n🎵 STEP 5: MUSIC (Skipped)")

with open("output/music_sfx/music_data.json", 'w') as f:
    json.dump({"status": "skipped"}, f)

print("✅ Done\n")
