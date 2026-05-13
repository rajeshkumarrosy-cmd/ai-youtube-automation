import json
import os

print("\n📊 STEP 10: ANALYTICS")

videos = []
for t in ['short', 'long']:
    f = f"output/videos/final_{t}.mp4"
    if os.path.exists(f):
        videos.append(t)

print(f"\n✅ Videos created: {len(videos)}")
for v in videos:
    print(f"   ✅ {v.upper()} video ready")

with open("output/analytics_log.json", 'w') as f:
    json.dump({"videos_created": videos}, f)

print("\n✅ COMPLETE!\n")
