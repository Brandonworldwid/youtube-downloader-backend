from flask import Flask, request, jsonify
from pytube import YouTube
from flask_cors import CORS
import os  # ✅ Added for dynamic port binding on Render

app = Flask(__name__)
CORS(app)

@app.route("/video", methods=["POST"])
def get_video_info():
    data = request.json
    url = data.get("url")

    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        stream_list = [
            {
                "itag": stream.itag,
                "resolution": stream.resolution,
                "type": stream.mime_type
            }
            for stream in streams
        ]
        return jsonify({
            "title": yt.title,
            "thumbnail": yt.thumbnail_url,
            "streams": stream_list
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/download", methods=["POST"])
def download_video():
    data = request.json
    url = data.get("url")
    itag = data.get("itag")

    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)
        stream.download()
        return jsonify({"message": "Downloaded!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/")  # Optional test route
def home():
    return "YouTube Downloader backend is live!"

if __name__ == "__main__":
    # ✅ This is important for Render to detect and open the port
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
