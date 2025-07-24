from flask import Flask, request, send_file, jsonify
from moviepy.editor import ImageClip
import tempfile
import os

app = Flask(__name__)


@app.route('/v1/image/convert/video', methods=['POST'])
def image_to_video():
    data = request.get_json()
    url = data['image_url']
    length = float(data['length'])
    fps = int(data.get('frame_rate', 25))
    zoom_speed = float(data.get('zoom_speed', 1.0))
    uid = data.get('id', 'out')

    # Converte imagem em clip de vídeo com zoom contínuo
    clip = ImageClip(url).set_duration(length).set_fps(fps)
    clip = clip.resize(lambda t: 1 + zoom_speed * t / length)

    # Salva em arquivo temporário
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    clip.write_videofile(tmp.name, codec='libx264', audio=False, verbose=False, logger=None)

    # Retorna o vídeo criado
    response = send_file(tmp.name, mimetype='video/mp4', as_attachment=True,
                         download_name=f'{uid}.mp4')

    # Remove o arquivo após envio
    @response.call_on_close
    def cleanup():
        os.unlink(tmp.name)
    return response


@app.route('/health', methods=['GET'])
def health():
    return jsonify(status='ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
