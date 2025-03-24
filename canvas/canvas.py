import random
import streamlit as st

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
    return random.choice(['minecraft', 'pencil sketch', 'real photo', 'legoland'])


if st.session_state.stage == "welcome":
    st.session_state.selected = []

    title = '<p style="font-family:Ariel; color:Blue; font-size: 30px;">AI Crafting Canvas</p>'
    st.markdown(title, unsafe_allow_html=True)
    st.divider()

    col1, col2, center, col3, col4 = st.columns([1, 1, 1, 1, 1], vertical_alignment="center")
    with col2:
        st.markdown('<div style="text-align: right; vertical-align: center;">Pick</div>', unsafe_allow_html=True)
    with center:
        st.button('Icons', on_click=set_state, args=["images-pick-character"])

    title = '<p style="font-family:Ariel; color:Black; text-align: center;">OR          </p>'
    st.markdown(title, unsafe_allow_html=True)

    col1, col2, center, col3, col4 = st.columns([1, 1, 1, 1, 1], vertical_alignment="center")
    with col2:
        st.markdown('<div style="text-align: right; vertical-align: top;">Type Your</div>', unsafe_allow_html=True)
    with center:
        st.button('Prompt', on_click=set_state, args=["text"])


_ID_TO_PATH = {
    "mario": "mario.png",
    "sonic": "sonic.png",
    "hello kitty": "hellokitty.png",
    "pikachu": "pikachu.png",
    "cool car": "cool_car.png",
    "mickey mouse": "mickey_mouse.png",
    "transformer": "transformer.png",
    "peppa pig": "peppa_pig.png",
    "pink daisy duck": "daisy_duck.png",
    "city": "background-city.png",
    "sky": "background-sky.png",
    "forest": "background-trees.png",
    "undersea": "background-undersea.png",
    "theme park": "themepark.png",
    "living room": "living_room.png",
    "beach": "beach.png",
    "castle": "castle.png",
}

start_over_button = st.empty()
image_selections = st.empty()

if st.session_state.stage == "images-pick-character":
    with image_selections:
        characters_to_pick = ['mario', 'sonic', 'hello kitty', 'pikachu', 'cool car', 'mickey mouse', 'transformer', 'peppa pig']
        content = "<div><p>Pick one</p><p>"
        for character in characters_to_pick:
            content += f"<a href='#' id='{character}'><img width='20%' src='{_IMAGE_LOCATION}/{_ID_TO_PATH[character]}'></a>\n"
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

if st.session_state.stage == "images-pick-another":
    with image_selections:
        characters_to_pick = ['mario', 'sonic', 'hello kitty', 'pikachu', 'cool car', 'mickey mouse', 'transformer', 'peppa pig']
        content = "<div><p>Pick another</p><p>"
        for character in characters_to_pick:
            content += f"<a href='#' id='{character}'><img width='20%' src='{_IMAGE_LOCATION}/{_ID_TO_PATH[character]}'></a>\n"
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

if st.session_state.stage == "images-pick-background":
    image_selections.empty()
    with image_selections:
        content = f"""<p>Lastly, pick a background.</p>
            <a href='#' id='city'><img width='20%' src='{_IMAGE_LOCATION}/background-city.png'></a>
            <a href='#' id='sky'><img width='20%' src='{_IMAGE_LOCATION}/background-sky.png'></a>
            <a href='#' id='forest'><img width='20%' src='{_IMAGE_LOCATION}/background-trees.png'></a>
            <a href='#' id='undersea'><img width='20%' src='{_IMAGE_LOCATION}/background-undersea.png'></a>
            <a href='#' id='theme park'><img width='20%' src='{_IMAGE_LOCATION}/themepark.png'></a>
            <a href='#' id='living room'><img width='20%' src='{_IMAGE_LOCATION}/living_room.png'></a>
            <a href='#' id='beach'><img width='20%' src='{_IMAGE_LOCATION}/beach.png'></a>
            <a href='#' id='castle'><img width='20%' src='{_IMAGE_LOCATION}/castle.png'></a>
            """
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
    st.button('Draw!', on_click=set_state, args=["generate"])
    st.divider()

    # st.write("=== Last 10 prompts ===")
    # print("### success prompts ", st.session_state.success_prompts)
    # for last_prompt in reversed(st.session_state.success_prompts[-10:]):
    #     st.write(last_prompt)

if st.session_state.stage == "generate":
    from PIL import Image
    from io import BytesIO

    GCS_BUCKET="steam-night-2025-laurelwood"

    client = genai.Client(api_key=st.secrets['api_key'])

    if st.session_state.selected:
        selected = st.session_state.selected
        print(f"### SELCTED: {selected}")
        prompt = f"{selected[0]} and {selected[1]} in the {selected[2]} in the style of {get_random_style()}"
    else:
        prompt = st.session_state.prompt


    is_success = False
    with st.spinner("Please wait. AI is drawing an image..."):
        try:
            response = client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=f"{prompt}",
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio="4:3",
                        person_generation="ALLOW_ADULT",
                        include_rai_reason= True,
                    )
            )
            if response.generated_images and response.generated_images[0].image.image_bytes:
                is_success = True
                st.write(f"Generated an image of **{prompt}**!")
                st.session_state.success_prompts.append(prompt)
                generated_image = response.generated_images[0]
                # bucket = storage_client.bucket(GCS_BUCKET)
                # blob = bucket.blob(get_filename())
                # blob.upload_from_string(generated_image.image.image_bytes)
                st.image(Image.open(BytesIO(generated_image.image.image_bytes)))
            else:
                print(f"FAILED RESPONSE: {response}")
                is_success = False
        except genai.errors.ClientError as e:
            print(e)
            print("#### error")
            is_success = False

        except Exception as e:
            print(e)
            raise(e)

    if not is_success:
        st.write(f"Couldn't generate an image of **{prompt}** :(")
        st.write("Try a different prompt or images!")
    st.button('Start Over', on_click=set_state, args=["welcome"])