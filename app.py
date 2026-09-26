"""Local demonstration API for Agri-Vyakaroti.

This service validates crop images; it does not diagnose diseases. No model is
downloaded, no random medical/agricultural advice is produced, and uploads are
processed in memory rather than saved under user-controlled filenames.
"""
import io
import os
import warnings

from flask import Flask, jsonify, request
from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge

MAX_IMAGE_BYTES = 8 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 25_000_000


def create_app():
    app = Flask(__name__)
    # Allow multipart overhead while enforcing the exact file limit below.
    app.config['MAX_CONTENT_LENGTH'] = MAX_IMAGE_BYTES + 64 * 1024

    @app.errorhandler(RequestEntityTooLarge)
    def too_large(_error):
        return jsonify(error='Choose an image smaller than 8 MB.'), 413

    @app.get('/')
    @app.get('/api/health')
    def health():
        return jsonify(status='online', service='Agri-Vyakaroti API', mode='demo', model_available=False)

    @app.post('/api/crop-scan')
    def scan_crop():
        file = request.files.get('image')
        if file is None or not file.filename:
            return jsonify(error='Choose a crop image first.'), 400
        raw = file.stream.read(MAX_IMAGE_BYTES + 1)
        if len(raw) > MAX_IMAGE_BYTES:
            return jsonify(error='Choose an image smaller than 8 MB.'), 413
        if not raw:
            return jsonify(error='The image is empty.'), 400
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error', Image.DecompressionBombWarning)
                with Image.open(io.BytesIO(raw)) as image:
                    if image.format not in {'JPEG', 'PNG', 'WEBP'}:
                        return jsonify(error='Use a JPG, PNG, or WebP image.'), 415
                    width, height = image.size
                    if width * height > Image.MAX_IMAGE_PIXELS:
                        return jsonify(error='Choose an image with at most 25 million pixels.'), 400
                    image.verify()
                # Decode as well as verify to catch truncated image data.
                with Image.open(io.BytesIO(raw)) as image:
                    image.load()
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
            return jsonify(error='This file is not a readable crop image.'), 400
        return jsonify(
            disease_name='Image recorded for review', confidence=None,
            treatment='This demonstration validates your image only. An agronomist must review the crop before any treatment decision.',
            status='pending_review', mode='demo', image={'width': width, 'height': height},
        )

    @app.get('/api/weather-risk')
    def weather_risk():
        return jsonify(
            mode='demo', location='Jalgaon District', current_temp=28,
            humidity=88, rainfall_probability=0.80,
            risk_assessment='Illustrative wet conditions. Confirm weather locally before field work.',
            forecast=[
                {'day': 'Today', 'temp': 28, 'rain': '80%', 'humidity': '88%'},
                {'day': 'Tomorrow', 'temp': 27, 'rain': '90%', 'humidity': '92%'},
                {'day': 'Day 3', 'temp': 29, 'rain': '30%', 'humidity': '75%'},
            ],
        )

    @app.get('/api/iot-traps')
    def iot_traps():
        return jsonify(mode='demo', cluster_id='Jalgaon District', active_traps=5, alerts=[
            {'trap_id': 'TRP-001', 'pest_detected': 'Spodoptera moth', 'count': 45, 'status': 'high', 'coordinates': [21.0, 75.5]},
            {'trap_id': 'TRP-002', 'pest_detected': 'Locust swarm', 'count': 120, 'status': 'high', 'coordinates': [20.9, 75.6]},
            {'trap_id': 'TRP-045', 'pest_detected': 'Whitefly', 'count': 85, 'status': 'moderate', 'coordinates': [21.1, 75.4]},
            {'trap_id': 'TRP-018', 'pest_detected': 'Fall armyworm', 'count': 62, 'status': 'moderate', 'coordinates': [20.95, 75.45]},
            {'trap_id': 'TRP-022', 'pest_detected': 'Aphid', 'count': 210, 'status': 'high', 'coordinates': [21.05, 75.65]},
        ])

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(error='This endpoint does not exist.'), 404

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host=os.environ.get('HOST', '127.0.0.1'), port=int(os.environ.get('PORT', '10000')), debug=False)
