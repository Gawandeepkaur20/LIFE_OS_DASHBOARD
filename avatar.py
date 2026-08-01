from urllib.parse import quote
import random

STYLE = """
masterpiece,
best quality,
ultra detailed,
photorealistic,
8k,
professional concept art,
cinematic lighting,
dramatic shadows,
realistic,
sharp focus,
single character,
centered composition,
high quality,
"""

def generate_avatar(score):

    lighting = random.choice([
        "golden hour lighting",
        "blue neon lighting",
        "soft studio lighting",
        "warm sunlight",
        "volumetric lighting",
        "dramatic cinematic lighting"
    ])

    camera = random.choice([
        "front portrait",
        "eye level portrait",
        "close-up portrait",
        "waist-up portrait"
    ])

    if score >= 80:

        scenes = [

            "young software engineering student coding confidently in a modern workspace, books, coffee mug, phone kept face down",

            "college student happily studying with laptop and books, organized desk, productivity and discipline",

            "young programmer taking a break and reading a book beside laptop, peaceful study room",

            "software engineer completing tasks while sunlight enters through the window, healthy digital lifestyle",

            "focused university student balancing coding, exercise bottle and books on desk"

        ]

    elif score >= 60:

        scenes = [

            "college student trying to balance studies and smartphone use, books beside laptop",

            "software engineering student looking at laptop while phone vibrates nearby, resisting distractions",

            "student keeping phone away while concentrating on assignments",

            "young programmer organizing daily schedule with laptop and smartphone on desk",

            "student choosing books over social media, calm modern study room"

        ]

    elif score >= 40:

        scenes = [

            "college student distracted by Instagram notifications while studying, unfinished homework on desk",

            "young programmer repeatedly checking smartphone instead of coding, messy workspace",

            "student scrolling social media while laptop displays unfinished project",

            "college student overwhelmed by endless notifications floating around study desk",

            "young adult unable to focus because of glowing smartphone"

        ]

    else:

        scenes = [

            "digital zombie staring at glowing smartphone, hundreds of Instagram TikTok and YouTube notifications floating around",

            "college student trapped inside giant smartphone, social media consuming all attention",

            "student chained by charging cables while endlessly scrolling phone in dark room",

            "young adult drowning in floating mobile phones and social media icons, exhausted expression",

            "digital prisoner surrounded by glowing smartphone screens, dark cinematic room, addiction concept"

        ]

    scene = random.choice(scenes)

    prompt = f"""
{STYLE}

{scene}

{lighting}

{camera}

portrait orientation

no anime

no cartoon

no landscape

no forest

no mountains

no lake

focus on one human character

highly detailed face

professional photography
"""

    seed = random.randint(1,999999)

    url = (
        "https://image.pollinations.ai/prompt/"
        f"{quote(prompt)}"
        f"?seed={seed}"
        "&width=768"
        "&height=1024"
        "&model=flux"
        "&nologo=true"
    )

    return url