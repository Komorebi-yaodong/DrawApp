from datetime import datetime
import concurrent.futures
import streamlit as st
import requests
import json
import time


st.write("<h2> Draw-T2I""</h2>",unsafe_allow_html=True)

resolution_list = {
    "1:1":"1:1",
    "16:9":"16:9",
    "4:3":"4:3",
    "3:4":"3:4",
    "9:16":"9:16",
}


if "img_num" not in st.session_state:
    st.session_state.img_num = 1
if "resolution" not in st.session_state:
    st.session_state.resolution = list(resolution_list.keys())[0]


show_input = st.container()
show_app = st.container()


def generate_image(prompt,resolution):

    def queue_prompt(prompt):
        p = {
            "model": "dall-e-3",
            "prompt": prompt + f" ---{resolution}",
            "n": 1,
            "size": "1024x1024"
        }
        data = json.dumps(p).encode('utf-8')
        response =  requests.post("https://fluximgcom.komorebi-zyd.workers.dev/", data=data)
        if response.status_code != 200:
            st.error(f"Failed to send prompt to server, {response.status_code}")
        return response.json()

    def get_image(queue_res):
            url = queue_res["data"][0]["url"]
            resp = requests.get(url)
            if resp.status_code != 200:
                st.error(f"Failed to get image from server, {resp.status_code}")
            return resp.content
    
    queue_res = queue_prompt(prompt)
    name = datetime.fromtimestamp(datetime.now().timestamp()).strftime('%Y-%m-%d %H-%M-%S')
    return name,get_image(queue_res)


@st.cache_data
def show_images(prompt,images,time_delta):
    with show_app:
        with st.container(border=True):
            with st.expander(prompt):
                st.image(images)
                # st.write(f"**Prompt**: {prompt}")
                st.write(f"**Time**: {time_delta} seconds")


# def t2i_input(prompt,number=st.session_state.img_num,resolution=st.session_state.resolution):
#     start = time.time()
#     images = []
#     names = []
#     for i in range(number):
#         name,image = generate_image(prompt,resolution)
#         if image is None: 
#             st.error(name)
#         names.append(name)
#         images.append(image)

#     end = time.time()
#     show_images(prompt,images,end-start)


def t2i_input(prompt, number=st.session_state.img_num, resolution=st.session_state.resolution):
    start = time.time()
    images = []
    names = []

    # 定义生成图像的任务
    def generate_image_task(i):
        return generate_image(prompt, resolution)

    # 使用 ThreadPoolExecutor 并行执行任务
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交所有任务
        future_to_index = {executor.submit(generate_image_task, i): i for i in range(number)}
        
        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            try:
                name, image = future.result()
                if image is None:
                    st.error(name)
                names.append(name)
                images.append(image)
            except Exception as exc:
                st.error(f'生成图像失败: {exc}')
    
    # 计算总用时
    end = time.time()
    show_images(prompt,images,end-start)


with st.sidebar:
    st.session_state.resolution = st.selectbox("**Resolution**",options=resolution_list)
    st.session_state.img_num = st.slider(label="**Image Number**",min_value=1,max_value=4,step=1)

prompt = st.chat_input("Send your prompt")
if prompt:
    t2i_input(prompt,st.session_state.img_num,st.session_state.resolution)