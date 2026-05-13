import os
import json

print("\n📤 STEP 9: YOUTUBE UPLOAD")

videos = []
for t in ['short', 'long']:
    f = f"output/videos/final_{t}.mp4"
    if os.path.exists(f):
        size = os.path.getsize(f) / (1024 * 1024)
        videos.append({'type': t, 'file': f, 'size_mb': round(size, 2)})
        print(f"✅ {t.upper()} video ready: {size:.2f} MB")

try:
    with open("output/seo_package.json") as f:
        seo = json.load(f)
    print(f"\n📋 Title: {seo['title'][:60]}...")
except:
    pass

record = {
    "status": "ready_for_upload",
    "videos": videos
}

with open("output/upload_record.json", 'w') as f:
    json.dump(record, f, indent=2)

print(f"""
📝 UPLOAD STEPS:
   1. Download video from output/videos/
   2. Go to youtube.com/studio
   3. Upload video
   4. Add title from seo_package.json
   5. Publish!
""")
