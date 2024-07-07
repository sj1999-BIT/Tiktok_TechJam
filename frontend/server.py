
import json

from flask import Flask, render_template, url_for, request, send_file, jsonify
from backend.main import run





app = Flask(__name__)


# def serve_pil_image(pil_img):
#     """
#     Serves a PIL (Pillow) image over HTTP.
#
#     :param: pil_img: A PIL image (Pillow image).
#     :return: An HTTP response containing the image data.
#     """
#     img_io = BytesIO()
#     pil_img.save(img_io, 'JPEG', quality=70)
#     img_io.seek(0)
#     return send_file(img_io, mimetype='image/jpeg',download_name='my_image.jpg')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_seg_img():
    user_prompt = request.form.get('widthDiv')
    video_path = "../backend/input_video/uploaded_video.mp4"

    print(f"user prompt is {user_prompt}")

    video_file = request.files['video']
    video_file.save('../backend/input_video/uploaded_video.mp4')

    filepath = run(video_path,  user_prompt)

    return send_file(filepath, mimetype='audio/mpeg')



if __name__ == "__main__":
    app.config["EXPLAIN_TEMPLATE_LOADING"] = True
    app.run(host='localhost', port=5000, debug=True)