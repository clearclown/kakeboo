# backend/reciept.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import HumanMessagePromptTemplate
import base64
import os
from PIL import Image
import dotenv
import io

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#画像ファイルをbase64エンコードする
def encode_image(image_path):
    # Pillowを使って画像を開く
    img = Image.open(image_path)

    # 画像形式を判定し、適切なMIMEタイプを設定
    if img.format == 'JPEG':
        mime_type = 'image/jpeg'
    elif img.format == 'PNG':
        mime_type = 'image/png'
    else:
        raise ValueError(f"Unsupported image format: {img.format}")

    # 画像をメモリバッファに保存
    buffered = io.BytesIO()
    img.save(buffered, format=img.format)

    # バッファの内容をbase64エンコード
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str, mime_type

image_path = ""
base64_image, mime_type = encode_image(image_path)

#本当はImagePromptTemplateを使いたいが
image_template = {"image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}

chat = ChatOpenAI(temperature=0, model_name="gpt-4o-2024-08-06")

system = (
    ""
)

human_prompt = "{question}"
human_message_template = HumanMessagePromptTemplate.from_template([human_prompt, image_template])

prompt = ChatPromptTemplate.from_messages([("system", system), human_message_template])

chain = prompt | chat
result = chain.invoke({"question": ""})
print(result)
