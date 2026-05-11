import json
import os
import subprocess
from datetime import datetime

class VoiceoverGenerator:
    def __init__(self):
        self.script = self.load_script()
        self.output_dir = "output/voiceovers"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_script(self):
        """Load script"""
        try:
            with open("output/scripts/short_script.json", 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def generate_voiceover_with_edge_tts(self, text, scene_num):
        """Use Edge TTS (Microsoft free service)"""
        output_file = f"{self.output_dir}/scene_{scene_num}.mp3"
        
        try:
            # Edge TTS command
            cmd = f'edge-tts --voice en-IN-NeerjaNeural --text "{text}" --write-media {output_file}'
            os.system(cmd)
            
            print(f"✅ Voiceover generated: {output_file}")
            return output_file
        except Exception as e:
            print(f"⚠️ Edge TTS error: {e}")
            return self.generate_with_pyttsx3(text, scene_num)
    
    def generate_with_pyttsx3(self, text, scene_num):
        """Fallback: Use pyttsx3"""
        import pyttsx3
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        # Set Indian accent if available
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'indian' in voice.name.lower() or 'hindi' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        output_file = f"{self.output_dir}/scene_{scene_num}.wav"
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        
        print(f"✅ Voiceover generated (pyttsx3): {output_file}")
        return output_file
    
    def extract_narration(self):
        """Extract narration from script"""
        narrations = []
        
        for scene in self.script.get('scenes', []):
            narrations.append({
                'scene': scene.get('scene'),
                'narration': scene.get('narration'),
                'duration': scene.get('duration')
            })
        
        return narrations
    
    def generate_all_voiceovers(self):
        """Generate voiceovers for all scenes"""
        narrations = self.extract_narration()
        voiceovers = []
        
        for narration in narrations:
            vo_file = self.generate_voiceover_with_edge_tts(
                narration['narration'],
                narration['scene']
            )
            
            voiceovers.append({
                'scene': narration['scene'],
                'narration': narration['narration'],
                'voiceover_file': vo_file,
                'duration': narration['duration']
            })
        
        return voiceovers
    
    def save_voiceover_data(self, voiceovers):
        """Save voiceover metadata"""
        data = {
            'generated_at': datetime.now().isoformat(),
            'voiceovers': voiceovers,
            'total_duration': sum([v['duration'] for v in voiceovers])
        }
        
        with open(f"{self.output_dir}/voiceover_data.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        return data
    
    def run(self):
        """Generate voiceovers"""
        print("🎙️ STEP 4: VOICEOVER GENERATION STARTING...")
        
        if not self.script:
            print("❌ No script found")
            return
        
        voiceovers = self.generate_all_voiceovers()
        vo_data = self.save_voiceover_data(voiceovers)
        
        print(f"""
        ╔════════════════════════════════════╗
        ║    VOICEOVERS GENERATED             ║
        ╚════════════════════════════════════╝
        Total Scenes: {len(voiceovers)}
        Total Duration: {vo_data['total_duration']}s
        """)
        
        return vo_data

if __name__ == "__main__":
    generator = VoiceoverGenerator()
    generator.run()
