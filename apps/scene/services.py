import random
from typing import List, Dict, Any
from django.utils import timezone
from .models import Scene
from apps.movies.models import Movie


class SceneGenerator:
    """Service for generating scenes from movie data."""

    # Scene templates by genre
    SCENE_TEMPLATES = {
        'action': [
            {
                'title': 'Opening Action Sequence',
                'description': 'High-octane opening with intense action and fast-paced movement.',
                'scene_type': 'action',
                'emotional_intensity': 8,
                'key_moments': True,
                'transcript': 'The hero bursts through the door, guns blazing. "This ends now!" he shouts as bullets fly everywhere.'
            },
            {
                'title': 'Climactic Battle',
                'description': 'The final confrontation between hero and villain in an epic showdown.',
                'scene_type': 'climax',
                'emotional_intensity': 9,
                'key_moments': True,
                'transcript': 'They circle each other, weapons drawn. "You\'ve taken everything from me," the hero growls. The villain laughs. "And I\'ll take more."'
            },
            {
                'title': 'Chase Sequence',
                'description': 'Heart-pounding pursuit through city streets with high-speed action.',
                'scene_type': 'action',
                'emotional_intensity': 7,
                'key_moments': False,
                'transcript': 'Tires screech as the car swerves through traffic. Horns blare, pedestrians dive for cover. The hero floors the accelerator.'
            }
        ],
        'drama': [
            {
                'title': 'Emotional Revelation',
                'description': 'A powerful moment of emotional breakthrough and character development.',
                'scene_type': 'dialogue',
                'emotional_intensity': 8,
                'key_moments': True,
                'transcript': '"I never told you the truth," she whispers, tears streaming down her face. "I was afraid you\'d hate me."'
            },
            {
                'title': 'Family Dinner',
                'description': 'Tense family interaction revealing underlying conflicts and relationships.',
                'scene_type': 'dialogue',
                'emotional_intensity': 6,
                'key_moments': False,
                'transcript': 'The family sits around the table in uncomfortable silence. Father clears his throat. "So, how was everyone\'s day?"'
            },
            {
                'title': 'Quiet Reflection',
                'description': 'Character alone with their thoughts, contemplating life choices.',
                'scene_type': 'exposition',
                'emotional_intensity': 5,
                'key_moments': False,
                'transcript': 'He stares out the window at the rain, lost in memories. The weight of years presses down on him.'
            }
        ],
        'horror': [
            {
                'title': 'The Discovery',
                'description': 'Terrifying moment when characters discover something horrifying.',
                'scene_type': 'climax',
                'emotional_intensity': 10,
                'key_moments': True,
                'transcript': 'The door creaks open. What they see makes them scream. "Oh God, what is that thing?" someone whispers in horror.'
            },
            {
                'title': 'Building Tension',
                'description': 'Suspenseful scene building dread and anticipation of terror.',
                'scene_type': 'exposition',
                'emotional_intensity': 7,
                'key_moments': False,
                'transcript': 'Every shadow seems to move. Footsteps echo in the empty hallway. They know something is watching them.'
            },
            {
                'title': 'Jump Scare Moment',
                'description': 'Sudden fright that shocks the characters and audience.',
                'scene_type': 'action',
                'emotional_intensity': 9,
                'key_moments': False,
                'transcript': 'A hand bursts from the darkness, grabbing her ankle. She screams as she\'s dragged into the shadows.'
            }
        ],
        'comedy': [
            {
                'title': 'Misunderstanding',
                'description': 'Humorous situation caused by a comedic misunderstanding.',
                'scene_type': 'dialogue',
                'emotional_intensity': 6,
                'key_moments': False,
                'transcript': '"Wait, you thought I said marry? I said bury! As in, bury the treasure!" He laughs uncontrollably.'
            },
            {
                'title': 'Physical Comedy',
                'description': 'Slapstick humor with physical comedy and timing.',
                'scene_type': 'action',
                'emotional_intensity': 7,
                'key_moments': False,
                'transcript': 'He slips on the banana peel, arms flailing wildly. The pie hits him square in the face. Everyone bursts out laughing.'
            },
            {
                'title': 'Romantic Mix-up',
                'description': 'Comedic romantic confusion and awkward situations.',
                'scene_type': 'dialogue',
                'emotional_intensity': 5,
                'key_moments': False,
                'transcript': '"You\'re dating my sister? But I thought... wait, which sister?" The confusion mounts as more relatives appear.'
            }
        ],
        'sci-fi': [
            {
                'title': 'First Contact',
                'description': 'Moment of first encounter with alien life or advanced technology.',
                'scene_type': 'climax',
                'emotional_intensity': 8,
                'key_moments': True,
                'transcript': 'The alien ship hovers silently. A beam of light descends. "We come in peace," echoes in their minds.'
            },
            {
                'title': 'Technological Marvel',
                'description': 'Awe-inspiring display of futuristic technology and science.',
                'scene_type': 'exposition',
                'emotional_intensity': 6,
                'key_moments': False,
                'transcript': 'The machine hums to life, lights dancing across its surface. "This will change everything," the scientist murmurs.'
            },
            {
                'title': 'Time Paradox',
                'description': 'Confusing and mind-bending temporal anomaly or paradox.',
                'scene_type': 'dialogue',
                'emotional_intensity': 7,
                'key_moments': False,
                'transcript': '"If I go back and change the past, will I still exist to make this choice?" The paradox gives him a headache.'
            }
        ]
    }

    # Default scenes for other genres
    DEFAULT_SCENES = [
        {
            'title': 'Opening Scene',
            'description': 'Introduction to the main characters and setting.',
            'scene_type': 'exposition',
            'emotional_intensity': 4,
            'key_moments': False,
            'transcript': 'The camera pans across the landscape, introducing us to the world of the story.'
        },
        {
            'title': 'Key Moment',
            'description': 'Important turning point in the narrative.',
            'scene_type': 'climax',
            'emotional_intensity': 7,
            'key_moments': True,
            'transcript': 'Everything changes in this pivotal moment. The character makes a life-altering decision.'
        },
        {
            'title': 'Resolution',
            'description': 'Conclusion and wrapping up of the main plot points.',
            'scene_type': 'dialogue',
            'emotional_intensity': 5,
            'key_moments': False,
            'transcript': 'As the story comes to a close, characters reflect on their journey and what they\'ve learned.'
        }
    ]

    @staticmethod
    def generate_scenes_for_movie(movie: Movie, num_scenes: int = 3) -> List[Scene]:
        """
        Generate realistic scenes for a movie based on its genre and metadata.

        Args:
            movie: The movie instance to generate scenes for
            num_scenes: Number of scenes to generate (default: 3)

        Returns:
            List of created Scene objects
        """
        genre = movie.genre.lower() if movie.genre else 'other'
        templates = SceneGenerator.SCENE_TEMPLATES.get(genre, SceneGenerator.DEFAULT_SCENES)

        # Ensure we don't exceed available templates
        num_scenes = min(num_scenes, len(templates))

        # Randomly select scenes from templates
        selected_templates = random.sample(templates, num_scenes)

        created_scenes = []
        scene_number = 1

        # Calculate total movie duration in seconds
        movie_duration_seconds = (movie.duration_minutes or 120) * 60

        for template in selected_templates:
            # Distribute scenes across the movie timeline
            start_time = (scene_number - 1) * (movie_duration_seconds // num_scenes)
            duration = random.randint(60, 300)  # 1-5 minutes per scene
            end_time = min(start_time + duration, movie_duration_seconds)

            # Customize scene based on movie data
            scene_title = template['title']
            scene_description = template['description']

            # Add movie-specific elements
            if movie.cast:
                cast_list = [name.strip() for name in movie.cast.split(',')[:3]]
                if cast_list:
                    scene_description += f" Featuring {', '.join(cast_list)}."

            # Create location based on genre or random
            locations = {
                'action': ['City Street', 'Warehouse', 'Mountain Peak', 'Underground Bunker'],
                'drama': ['Living Room', 'Restaurant', 'Office', 'Park Bench'],
                'horror': ['Abandoned House', 'Dark Forest', 'Basement', 'Attic'],
                'comedy': ['Coffee Shop', 'Party', 'Office', 'Restaurant'],
                'sci-fi': ['Spaceship', 'Laboratory', 'Alien Planet', 'Future City']
            }
            location_options = locations.get(genre, ['Unknown Location', 'Various Locations'])
            location = random.choice(location_options)

            # Generate characters from cast
            characters = ""
            if movie.cast:
                cast_members = [name.strip() for name in movie.cast.split(',')]
                scene_characters = random.sample(cast_members, min(3, len(cast_members)))
                characters = ', '.join(scene_characters)

            # Create the scene
            scene = Scene.objects.create(
                movie=movie,
                title=scene_title,
                description=scene_description,
                scene_type=template['scene_type'],
                start_time_seconds=start_time,
                end_time_seconds=end_time,
                location=location,
                characters=characters,
                transcript=template['transcript'],
                scene_number=scene_number,
                emotional_intensity=template['emotional_intensity'],
                key_moments=template['key_moments'],
                tags=f"{genre}, {template['scene_type']}"
            )

            created_scenes.append(scene)
            scene_number += 1

        return created_scenes

    @staticmethod
    def get_scenes_for_analysis(movie: Movie) -> List[Dict[str, Any]]:
        """
        Get scenes from a movie formatted for analysis.

        Args:
            movie: The movie to get scenes from

        Returns:
            List of scene data dictionaries ready for analysis
        """
        scenes = Scene.objects.filter(movie=movie).order_by('scene_number')

        scene_data = []
        for scene in scenes:
            scene_data.append({
                'id': scene.id,
                'title': scene.title,
                'description': scene.description,
                'transcript': scene.transcript or scene.description,
                'scene_type': scene.scene_type,
                'emotional_intensity': scene.emotional_intensity,
                'start_time': scene.start_time_seconds,
                'duration': scene.duration_seconds,
                'location': scene.location,
                'characters': scene.characters
            })

        return scene_data