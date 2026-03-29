# AI Video Generation Pipeline
**Based on:** AI-Video-Generation-Automation  
**Purpose:** Automated marketing video creation for AGI Company products

## Overview

Complete pipeline that generates marketing videos from product descriptions:
1. **Script Generation** (GPT/MiniMax) - Creates compelling marketing copy
2. **Visual Generation** (DALL-E/MiniMax Image) - Creates product imagery  
3. **Voice Generation** (Eleven Labs) - Professional voiceover
4. **Video Assembly** (MoviePy) - Combines everything into final MP4

## Products Supported

- HumanPal - AI avatar generation
- MilkMan - Delivery optimization
- ReggieStarr - POS system
- Dark Factory - Manufacturing

## Usage

```python
from ai_video_pipeline import VideoGenerator

generator = VideoGenerator()
generator.create_product_video(
    product="humanpal",
    script_style="modern",
    duration=30,
    output="humanpal_ad.mp4"
)
```

## Requirements

- Python 3.8+
- MoviePy
- OpenAI API (or MiniMax for scripts)
- DALL-E API (or MiniMax for images)
- Eleven Labs API (for voice)

## Files

- `video_generator.py` - Main pipeline
- `script_templates/` - Marketing script templates
- `output/` - Generated videos
- `assets/` - Stock footage and music
