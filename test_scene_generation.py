#!/usr/bin/env python
"""
Test script for the SceneIQ scene generation and analysis endpoints.
Run this script to test generating scenes for movies and analyzing them.
"""

import requests
import json
import time

def test_scene_generation():
    """Test the scene generation and analysis endpoints."""

    base_url = "http://localhost:8000"

    print("🎬 Testing SceneIQ Scene Generation & Analysis")
    print("📝 Note: Both GET and POST methods are supported for all endpoints")
    print("=" * 60)

    # First, let's get a list of movies to work with
    try:
        response = requests.get(f"{base_url}/api/movies/", timeout=10)
        if response.status_code == 200:
            movies_data = response.json()
            if movies_data['results']:
                movie = movies_data['results'][0]  # Take the first movie
                movie_id = movie['id']
                movie_title = movie['title']
                print(f"📽️  Using movie: {movie_title} (ID: {movie_id})")
            else:
                print("❌ No movies found in database. Please add some movies first.")
                return
        else:
            print(f"❌ Failed to get movies: {response.status_code}")
            return

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running on port 8000")
        print("   Run: python manage.py runserver")
        return
    except Exception as e:
        print(f"❌ Error getting movies: {e}")
        return

    # Test 1: Generate scenes for the movie (using GET request)
    print(f"\n🛠️  Test 1: Generating scenes for '{movie_title}' (GET request)")
    print("-" * 40)

    try:
        # Using GET request with query parameters
        params = {
            "movie_id": movie_id,
            "num_scenes": 3,
            "analyze_scenes": "false"
        }

        start_time = time.time()
        response = requests.get(
            f"{base_url}/api/analysis/generate-scenes/",
            params=params,
            timeout=15
        )
        request_time = time.time() - start_time

        print(f"Status Code: {response.status_code}")
        print(".3f")

        if response.status_code == 201:
            result = response.json()
            print(f"✅ Scenes created: {result['scenes_created']}")
            print(f"🎭 Scenes generated:")
            for scene in result['scenes']:
                print(f"   • {scene['title']} ({scene['scene_type']}) - Emotional intensity: {scene['emotional_intensity']}/10")

        elif response.status_code == 400 and "already has" in response.text:
            print("ℹ️  Movie already has scenes. Skipping generation, proceeding to analysis.")
        else:
            print(f"❌ Generation failed: {response.text}")
            return

    except Exception as e:
        print(f"❌ Generation error: {e}")
        return

    # Test 2: Analyze the movie scenes (using GET request)
    print(f"\n🔍 Test 2: Analyzing scenes for '{movie_title}' (GET request)")
    print("-" * 40)

    try:
        # Using GET request with query parameters
        params = {
            "movie_id": movie_id,
            "analysis_types": "emotional,visual,audio,pacing"
        }

        start_time = time.time()
        response = requests.get(
            f"{base_url}/api/analysis/analyze-movie-scenes/",
            params=params,
            timeout=20
        )
        request_time = time.time() - start_time

        print(f"Status Code: {response.status_code}")
        print(".3f")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Scenes analyzed: {result['scenes_analyzed']}/{result['total_scenes']}")

            if result['analyses']:
                print("📊 Analysis Results:")
                for analysis_item in result['analyses'][:2]:  # Show first 2
                    scene_title = analysis_item['scene_title']
                    analysis = analysis_item['analysis']
                    print(f"   • {scene_title}:")
                    for analysis_detail in analysis['analyses']:
                        score = analysis_detail['score']
                        analysis_type = analysis_detail['analysis_type']
                        print(f"     - {analysis_type.title()}: {score:.1f}/10")
            else:
                print("ℹ️  All scenes were already analyzed.")

        else:
            print(f"❌ Analysis failed: {response.text}")

    except Exception as e:
        print(f"❌ Analysis error: {e}")

    # Test 3: Get scenes for the movie
    print(f"\n📋 Test 3: Retrieving scenes for '{movie_title}'")
    print("-" * 40)

    try:
        response = requests.get(
            f"{base_url}/api/scenes/by_movie/?movie_id={movie_id}",
            timeout=10
        )

        if response.status_code == 200:
            scenes = response.json()
            print(f"✅ Found {len(scenes)} scenes:")
            for scene in scenes:
                print(f"   • {scene['title']} ({scene['scene_type']}) - {scene['duration_seconds']}s")
        else:
            print(f"❌ Failed to get scenes: {response.status_code}")

    except Exception as e:
        print(f"❌ Error retrieving scenes: {e}")

    print("\n" + "=" * 60)
    print("✅ Testing complete!")

if __name__ == "__main__":
    test_scene_generation()