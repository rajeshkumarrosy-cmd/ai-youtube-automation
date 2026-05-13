import os
import json

def check():
    print("\n" + "="*60)
    print("🔍 VIDEO DIAGNOSTIC")
    print("="*60 + "\n")
    
    # Check Step 1
    print("STEP 1: Trends")
    f = "output/scripts/trending_topics.json"
    if os.path.exists(f):
        with open(f) as file:
            d = json.load(file)
            print(f"   ✅ Topic: {d.get('selected_topic', {}).get('title')}")
    else:
        print("   ❌ Missing")
    
    # Check Step 2
    print("\nSTEP 2: Scripts")
    for t in ['short', 'long']:
        f = f"output/scripts/{t}_script.json"
        if os.path.exists(f):
            with open(f) as file:
                d = json.load(file)
                print(f"   ✅ {t}: {len(d.get('scenes', []))} scenes")
        else:
            print(f"   ❌ {t}: Missing")
    
    # Check Step 3
    print("\nSTEP 3: Visuals")
    f = "output/visuals/visual_data.json"
    if os.path.exists(f):
        with open(f) as file:
            d = json.load(file)
            short = d.get('short_scenes', [])
            long = d.get('long_scenes', [])
            print(f"   Short scenes: {len(short)}")
            print(f"   Long scenes: {len(long)}")
            
            for s in short:
                vf = s.get('file')
                exists = os.path.exists(vf) if vf else False
                size = os.path.getsize(vf)/(1024*1024) if exists else 0
                status = f"✅ {size:.2f}MB" if exists else "❌ MISSING"
                print(f"      Short Scene {s.get('scene')}: {status}")
            
            for s in long:
                vf = s.get('file')
                exists = os.path.exists(vf) if vf else False
                size = os.path.getsize(vf)/(1024*1024) if exists else 0
                status = f"✅ {size:.2f}MB" if exists else "❌ MISSING"
                print(f"      Long Scene {s.get('scene')}: {status}")
    else:
        print("   ❌ Visual data missing")
    
    # Check Step 4
    print("\nSTEP 4: Voiceovers")
    f = "output/voiceovers/voiceover_data.json"
    if os.path.exists(f):
        with open(f) as file:
            d = json.load(file)
            short = d.get('short_voiceovers', [])
            long = d.get('long_voiceovers', [])
            print(f"   Short voiceovers: {len(short)}")
            print(f"   Long voiceovers: {len(long)}")
            
            for s in short:
                af = s.get('file')
                exists = os.path.exists(af) if af else False
                size = os.path.getsize(af)/1024 if exists else 0
                status = f"✅ {size:.1f}KB" if exists else "❌ MISSING"
                print(f"      Short Voice {s.get('scene')}: {status}")
    else:
        print("   ❌ Voiceover data missing")
    
    # Check Step 6
    print("\nSTEP 6: Final Videos")
    for t in ['short', 'long']:
        f = f"output/videos/final_{t}.mp4"
        if os.path.exists(f):
            size = os.path.getsize(f)/(1024*1024)
            print(f"   ✅ {t}: {size:.2f} MB - READY!")
        else:
            print(f"   ❌ {t}: NOT FOUND")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    check()
