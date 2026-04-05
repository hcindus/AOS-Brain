"""
AI Video Generation Pipeline Demo

This script demonstrates the complete pipeline for generating
marketing videos for AGI Company products.
"""

from video_generator import AIVideoGenerator, VideoConfig

def demo_humanpal():
    """Generate HumanPal marketing video"""
    
    print("=" * 70)
    print("HUMANPAL VIDEO GENERATION DEMO")
    print("=" * 70)
    
    generator = AIVideoGenerator(output_dir="./examples")
    
    config = VideoConfig(
        product_name="humanpal",
        duration=30,
        style="modern",
        resolution="1080p",
        voice_type="professional"
    )
    
    # Generate script
    script = generator._generate_script(config)
    
    print("\n📄 Generated Script:")
    print("-" * 70)
    
    for scene in script['scenes']:
        print(f"\n[{scene['type'].upper()}] ({scene['duration']}s)")
        print(f"Text: {scene['text']}")
        print(f"Visual: {scene['visual_prompt']}")
        
    print("\n" + "=" * 70)
    print("SCRIPT SAVED: ./examples/humanpal_script.json")
    print("=" * 70)
    
    return script


def demo_milkman():
    """Generate MilkMan marketing video"""
    
    print("\n" + "=" * 70)
    print("MILKMAN VIDEO GENERATION DEMO")
    print("=" * 70)
    
    generator = AIVideoGenerator(output_dir="./examples")
    
    config = VideoConfig(
        product_name="milkman",
        duration=30,
        style="professional",
        resolution="1080p",
        voice_type="energetic"
    )
    
    script = generator._generate_script(config)
    
    print("\n📄 Generated Script:")
    print("-" * 70)
    
    for scene in script['scenes']:
        print(f"\n[{scene['type'].upper()}] ({scene['duration']}s)")
        print(f"Text: {scene['text']}")
        
    print("\n" + "=" * 70)
    print("SCRIPT SAVED: ./examples/milkman_script.json")
    print("=" * 70)
    
    return script


if __name__ == "__main__":
    demo_humanpal()
    demo_milkman()
    
    print("\n" + "=" * 70)
    print("AI VIDEO PIPELINE DEMO COMPLETE")
    print("=" * 70)
    print("\nTo generate actual videos:")
    print("1. Set API keys: OPENAI_API_KEY, ELEVENLABS_API_KEY")
    print("2. Uncomment API calls in video_generator.py")
    print("3. Install MoviePy: pip install moviepy")
    print("4. Run: python demo.py")
