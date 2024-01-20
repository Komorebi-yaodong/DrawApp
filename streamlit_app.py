from huggingface_hub import InferenceClient
import streamlit as st

if "draw_model" not in st.session_state:
    st.session_state.draw_model_list = {
        "现实-AbsoluteReality_v1.8.1":"https://api-inference.huggingface.co/models/digiplay/AbsoluteReality_v1.8.1",
        "现实-Absolute-Reality-1.81":"https://api-inference.huggingface.co/models/Lykon/absolute-reality-1.81",
        "动漫-AingDiffusion9.2":"https://api-inference.huggingface.co/models/digiplay/AingDiffusion9.2",
        "现实动漫-BluePencilRealistic_v01":"https://api-inference.huggingface.co/models/digiplay/bluePencilRealistic_v01",
        "动漫写实-Counterfeit-v2.5":"https://api-inference.huggingface.co/models/gsdf/Counterfeit-V2.5",
        "动漫写实-Counterfeit-v25-2.5d-tweak":"https://api-inference.huggingface.co/models/digiplay/counterfeitV2525d_tweak",
        "动漫可爱-Cuteyukimix":"https://api-inference.huggingface.co/models/stablediffusionapi/cuteyukimix",
        "动漫可爱-Cuteyukimixadorable":"https://api-inference.huggingface.co/models/stablediffusionapi/cuteyukimixadorable",
        "现实动漫-Dreamshaper-7":"https://api-inference.huggingface.co/models/Lykon/dreamshaper-7",
        "现实动漫-Dreamshaper_LCM_v7":"https://api-inference.huggingface.co/models/SimianLuo/LCM_Dreamshaper_v7",
        "动漫3D-DucHaitenDreamWorld":"https://api-inference.huggingface.co/models/DucHaiten/DucHaitenDreamWorld",
        "现实-EpiCRealism":"https://api-inference.huggingface.co/models/emilianJR/epiCRealism",
        "现实照片-EpiCPhotoGasm":"https://api-inference.huggingface.co/models/Yntec/epiCPhotoGasm",
        "动漫丰富-Ether-Blu-Mix-b5":"https://api-inference.huggingface.co/models/tensor-diffusion/Ether-Blu-Mix-V5",
        "动漫-Flat-2d-Animerge":"https://api-inference.huggingface.co/models/jinaai/flat-2d-animerge",
        "动漫风景-Genshin-Landscape-Diffusion":"https://api-inference.huggingface.co/models/Apocalypse-19/Genshin-Landscape-Diffusion",
        "现实照片-Juggernaut-XL-v7":"https://api-inference.huggingface.co/models/stablediffusionapi/juggernaut-xl-v7",
        "现实风景-Landscape_PhotoReal_v1":"https://api-inference.huggingface.co/models/digiplay/Landscape_PhotoReal_v1",
        "艺术水墨-MoXin":"https://api-inference.huggingface.co/models/zhyemmmm/MoXin",
        "现实写实-OnlyRealistic":"https://api-inference.huggingface.co/models/stablediffusionapi/onlyrealistic",
        "现实-Realistic-Vision-v51":"https://api-inference.huggingface.co/models/stablediffusionapi/realistic-vision-v51",
        "初始-StableDiffusion-2-1":"https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
        "初始-StableDiffusion-XL-0.9":"https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-0.9",
        "动漫-TMND-Mix":"https://api-inference.huggingface.co/models/stablediffusionapi/tmnd-mix",
        "animagine-XL-3.0":"https://api-inference.huggingface.co/models/cagliostrolab/animagine-xl-3.0",
        "艺术-Zavychromaxl-v3":"https://api-inference.huggingface.co/models/stablediffusionapi/zavychromaxlv3",
        "Dalle-v1.1":"https://api-inference.huggingface.co/models/dataautogpt3/OpenDalleV1.1",
        "Dalle-3-xl":"https://api-inference.huggingface.co/models/openskyml/dalle-3-xl",
        "playground-v2-美化":"https://api-inference.huggingface.co/models/playgroundai/playground-v2-1024px-aesthetic",
        "Dalle-proteus-v0.2":"https://api-inference.huggingface.co/models/dataautogpt3/ProteusV0.2",
    }
    st.session_state.draw_model = st.session_state.draw_model_list["Dalle-v1.1"]


show_app = st.container()

def change_paramater():
    st.session_state.draw_model = st.session_state.draw_model


def free_text_to_image(text):
    client = InferenceClient(model=st.session_state.draw_model_list[st.session_state.draw_model])
    image = client.text_to_image(text)
    return image


def main(prompt):
    show_app.write("**You:** " + prompt)
    image = free_text_to_image(prompt)
    show_app.image(image,use_column_width=True)


with st.sidebar:
    st.session_state.draw_model = st.selectbox('Draw Models', sorted(st.session_state.draw_model_list.keys(),key=lambda x:x.split("-")[0]),on_change=change_paramater)

prompt = st.chat_input("Send your prompt")
if prompt:
    main(prompt)