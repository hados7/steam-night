import logging
import random
import streamlit as st
import streamlit.components.v1 as components
import sys

from google import genai
from google.cloud import storage
from google.genai import types
from st_click_detector import click_detector

storage_client = storage.Client()

_IMAGE_LOCATION = "https://storage.googleapis.com/lw-steam-night-input-images"

if 'stage' not in st.session_state:
    st.session_state.stage = "welcome"

if 'selected' not in st.session_state:
    st.session_state.selected = []

if 'prompt' not in st.session_state:
    st.session_state.prompt = ""

if 'success_prompts' not in st.session_state:
    st.session_state.success_prompts = []


def get_filename():
  from datetime import datetime
  import pytz

  # Get the current date and time with local timezone information
  now_local = datetime.now(pytz.timezone('America/Los_Angeles'))

  # Format the datetime object as a string
  formatted_time = now_local.strftime("%Y-%m%d-%H%M%S")
  name = f"{formatted_time}.jpg"
  # print(name)
  return name

def set_state(name):
    st.session_state.stage = name

def get_random_style():
    return random.choice([
        # 'minecraft',
        'pencil sketch',
        'animation',
        'legoland',
        'pastel sketch',
        'studio ghibli'])


if st.session_state.stage == "welcome":
    st.session_state.selected = []

    title = """
        <div>
        <p style="font-family:Ariel; color:Blue; font-size: 30px;">
        <img src="https://storage.googleapis.com/lw-steam-night-input-images/robot_image.png" height="100"></img>
        AI Crafting Canvas
        </p>
        </div>
    """
    st.markdown(title, unsafe_allow_html=True)
    st.divider()

    col1, col2, center, col3, col4 = st.columns([1, 1, 1, 1, 1], vertical_alignment="center")
    with col2:
        st.markdown('<div style="text-align: right; vertical-align: center;">Pick</div>', unsafe_allow_html=True)
    with center:
        st.button('Icons', on_click=set_state, args=["images-pick-character"])

    col1, col2, col3 = st.columns([1, 2, 2])
    with col2:
        title = '<p style="font-family:Ariel; color:Black; text-align: center;">OR</p>'
        st.markdown(title, unsafe_allow_html=True)

    col1, col2, center, col3, col4 = st.columns([1, 1, 1, 1, 1], vertical_alignment="center")
    with col2:
        st.markdown('<div style="text-align: right; vertical-align: top;">Type Your</div>', unsafe_allow_html=True)
    with center:
        st.button('Prompt', on_click=set_state, args=["text"])


_ID_TO_PATH = {
    "mario": "mario.png",
    "minion": "minion.png",
    "dragon": "dragon.png",
    "sonic": "sonic.png",
    "elsa": "elsa.png",
    "hello kitty": "hellokitty.png",
    "pikachu": "pikachu.png",
    "cool car": "cool_car.png",
    "mickey mouse": "mickey_mouse.png",
    "transformer": "transformer.png",
    "peppa pig": "peppa_pig.png",
    "pink daisy duck": "daisy_duck.png",
    "spiderman": "spiderman.png",
}

_BACKGROUND_MAP = {
    "city": "background-city.png",
    "sky": "background-sky.png",
    "forest": "background-trees.png",
    "undersea": "background-undersea.png",
    "great ocean": "background-ocean.png",
    "theme park": "themepark.png",
    "living room": "living_room.png",
    "beach": "beach.png",
    "castle": "castle.png",
    "universe": "universe.png",
    "spaceship cockpit": "spaceship_cockpit.png",
}

start_over_button = st.empty()
image_selections = st.empty()

if 'first_icons' not in st.session_state:
    st.session_state.first_icons = random.sample(list(_ID_TO_PATH.keys()), 8)

if st.session_state.stage == "images-pick-character":
    with image_selections:
        #characters_to_pick = random.sample(['mario', 'sonic', 'hello kitty', 'pikachu', 'cool car', 'mickey mouse', 'transformer', 'peppa pig'], 8)
        content = "<div><p>Pick the first icon.</p><p>"
        for icon in st.session_state.first_icons:
            content += f"<a href='#' id='{icon}'><img width='20%' src='{_IMAGE_LOCATION}/{_ID_TO_PATH[icon]}'></a>\n"
        content += "</p></div>"
        clicked = click_detector(content)

    if clicked:
        st.session_state.selected.append(clicked)
        print(f"### {clicked} clicked!")
        st.session_state.stage = "images-pick-another"

    with start_over_button:
        col1, col2 = st.columns([5, 1])
        with col2:
            st.button('Start Over', on_click=set_state, key="start_over1", args=["welcome"])

if 'second_icons' not in st.session_state:
    st.session_state.second_icons = random.sample(list(_ID_TO_PATH.keys()), 8)

if st.session_state.stage == "images-pick-another":
    with image_selections:
        content = "<div><p>How about pick another?</p><p>"
        for icon in st.session_state.second_icons:
            content += f"<a href='#' id='{icon}'><img width='20%' src='{_IMAGE_LOCATION}/{_ID_TO_PATH[icon]}'></a>\n"
        content += "</p></div>"
        clicked = click_detector(content)

        if clicked:
            st.session_state.selected.append(clicked)
            print(f"### {clicked} clicked!")
            st.session_state.stage = "images-pick-background"

    start_over_button.empty()
    with start_over_button:
        col1, col2 = st.columns([5, 1])
        with col2:
            st.button('Start Over', on_click=set_state, key="start_over2", args=["welcome"])

if 'backgrounds' not in st.session_state:
    st.session_state.backgrounds = random.sample(list(_BACKGROUND_MAP.keys()), 8)
if st.session_state.stage == "images-pick-background":
    image_selections.empty()
    with image_selections:
        content = f"<p>Lastly, pick a background!</p>"
        for icon in st.session_state.backgrounds:
            content += f"<a href='#' id='{icon}'><img width='20%' src='{_IMAGE_LOCATION}/{_BACKGROUND_MAP[icon]}'></a>\n"
        clicked = click_detector(content)

        if clicked:
            st.session_state.selected.append(clicked)
            print(f"### {clicked} clicked!")
            st.session_state.stage = "generate"

    start_over_button.empty()
    with start_over_button:
        col1, col2 = st.columns([5, 1])
        with col2:
            st.button('Start Over', on_click=set_state, key="start_over3", args=["welcome"])


if st.session_state.stage == "text":
    col1, col2 = st.columns([5, 1])
    with col2:
        st.button('Start Over', on_click=set_state, args=["welcome"])
    st.divider()

    prompt = st.text_input('What do you want AI to draw?', key="prompt")
    st.button('Go!', on_click=set_state, args=["generate"])
    st.divider()

    # st.write("=== Last 10 prompts ===")
    # print("### success prompts ", st.session_state.success_prompts)
    # for last_prompt in reversed(st.session_state.success_prompts[-10:]):
    #     st.write(last_prompt)

if st.session_state.stage == "generate":
    from PIL import Image
    from io import BytesIO

    start_over_button.empty()
    with start_over_button:
        col1, col2 = st.columns([5, 1])
        with col2:
            st.button('Start Over', on_click=set_state, key="start_over4", args=["welcome"])


    GCS_BUCKET="lw-steam-night-images"

    client = genai.Client(vertexai=True, project="lw-steam-night", location="us-west1")

    if st.session_state.selected:
        selected = st.session_state.selected
        print(f"### SELECTED: {selected}")
        prompt = f"{selected[0]} and {selected[1]} in the {selected[2]}"
    else:
        prompt = st.session_state.prompt

    html_code = f"""
        <script id="{random.randint(1000, 9999)}">
        var e = document.getElementById("result_text");
        if (e) {{
            e.scrollIntoView({{behavior: "smooth"}});
            e.remove();
        }}
        </script>
    """


    is_success = False
    with st.spinner("Please wait. AI is creating an image..."):
        try:
            final_prompt = f"{prompt} in the style of {get_random_style()}"
            print(f"### final_prompt = {final_prompt}")
            logging.info(f"### final_prompt = {final_prompt}")
            response = client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=final_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="4:3",
                    person_generation="ALLOW_ADULT",
                    include_rai_reason= True,
                )
            )
            if response.generated_images and response.generated_images[0].image.image_bytes:
                is_success = True
                st.html(f"""
                        <div id="result_text" style="height: 100px;">
                        See the other screen for the created image, <b>{prompt}</b>!
                        </div>
                        """)
                components.html(html_code)
                generated_image = response.generated_images[0]
                filename = get_filename()
                bucket = storage_client.bucket(GCS_BUCKET)
                blob = bucket.blob(filename)
                blob.upload_from_string(generated_image.image.image_bytes)
                blob = bucket.blob(filename.split('.')[0] + '.txt')
                blob.upload_from_string(prompt)
                # Use the below code when you want to show the image in the canvas app.
                # st.image(Image.open(BytesIO(generated_image.image.image_bytes)))
                # st.html(f"<p style='text-align: center;'><b>{prompt}</b></p>")
            else:
                print(f"FAILED RESPONSE: {response}")
                is_success = False
        except genai.errors.ClientError as e:
            if e.code == 429:
                st.write(f"Quota exceeded!")
            print(f"#### genai.errors.ClientError: {e}")
            is_success = False

        except Exception as e:
            print(f"#### Exception: {e}")
            is_success = False

    sys.stdout.flush()
    if not is_success:
        st.html(f"<p>Couldn't generate an image of <b>{prompt}</b> &#x1F625;</p>")
        st.write("Try a different prompt or images!")
    st.button('Start Over', on_click=set_state, args=["welcome"])