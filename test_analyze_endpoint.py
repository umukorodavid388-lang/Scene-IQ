#!/usr/bin/env python
"""
Test script for the SceneIQ analysis endpoint.
Run this script to test the POST /api/analysis/analyze/ endpoint.
"""

import requests
import json
import time

def test_analyze_endpoint():
    """Test the analyze endpoint with sample scene text."""

    # Sample scene texts for testing
    test_scenes = [
        {
            "text": "The hero stands on the cliff edge, wind whipping through his hair. He screams in rage as the villain laughs maniacally. The camera zooms in on his tear-streaked face.",
            "scene_title": "Cliff Confrontation",
            "analysis_types": ["emotional", "visual", "audio", "pacing"]
        },
        {
            "text": "John and Mary sit quietly at the kitchen table. The clock ticks softly. 'I love you,' he whispers. She smiles peacefully.",
            "scene_title": "Quiet Moment",
            "analysis_types": ["emotional", "visual", "audio", "narrative"]
        },
        {
            "text": "The chase scene begins. Cars speed through the city streets, tires screeching. Gunshots echo as the hero dives behind a wall. The music swells dramatically.",
            "scene_title": "High-Speed Chase",
            "analysis_types": ["emotional", "visual", "audio", "pacing", "cinematography"]
        }
    ]

    base_url = "http://localhost:8000"

    print("🧪 Testing SceneIQ Analysis Endpoint")
    print("=" * 50)

    for i, scene_data in enumerate(test_scenes, 1):
        print(f"\n📋 Test {i}: {scene_data['scene_title']}")
        print("-" * 30)

        try:
            # Make the request
            start_time = time.time()
            response = requests.post(
                f"{base_url}/api/analysis/analyze/",
                json=scene_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            request_time = time.time() - start_time

            print(f"Status Code: {response.status_code}")
            print(".3f")

            if response.status_code == 200:
                result = response.json()

                print(f"Scene Title: {result['scene_title']}")
                print(f"Text Length: {result['text_length']} characters")
                print(f"Analysis Types: {len(result['analyses'])}")

                # Show analysis results
                for analysis in result['analyses']:
                    print(f"  • {analysis['analysis_type'].title()}: {analysis['score']:.1f}/10 "
                          f"(confidence: {analysis['confidence']:.2f})")
                    print(f"    {analysis['summary']}")

                print(f"Processing Time: {result['processing_time_seconds']:.3f}s")

            else:
                print(f"❌ Error: {response.text}")

        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the Django server is running on port 8000")
            print("   Run: python manage.py runserver")
            break
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")

    print("\n" + "=" * 50)
    print("✅ Testing complete!")

if __name__ == "__main__":
    test_analyze_endpoint()