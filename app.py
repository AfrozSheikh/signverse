from flask import Flask, render_template, Response, request, jsonify
import cv2
import pickle
import numpy as np
import mediapipe as mp
import pyttsx3
import time

from collections import Counter

app = Flask(__name__)

# Load only model2
model2_dict = pickle.load(open('model/model3.p', 'rb'))
model2 = model2_dict['model3']

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.4)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# TTS engine
engine = pyttsx3.init()

# Label mapping
labels_dict = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',
    6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
    12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R',
    18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X',
    24: 'Y', 25: 'space'
}
allowed_labels = set(labels_dict.values())

# Store output
output_text = ""
stop_signal = False

def normalize_landmarks(hand_landmarks, x_min, y_min):
    data = []
    for landmark in hand_landmarks:
        data.append(landmark.x - x_min)
        data.append(landmark.y - y_min)
    return data

def gen_frames():
    global output_text, stop_signal
    cap = cv2.VideoCapture(0)
    last_character = ""

    while not stop_signal:
        success, frame = cap.read()
        if not success:
            break

        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                x = [landmark.x for landmark in hand_landmarks.landmark]
                y = [landmark.y for landmark in hand_landmarks.landmark]
                data_aux = normalize_landmarks(hand_landmarks.landmark, min(x), min(y))

                if len(data_aux) == 42:
                    pred = model2.predict([np.asarray(data_aux)])
                    predicted_character = labels_dict[int(pred[0])]

                    if predicted_character in allowed_labels and predicted_character != last_character:
                        output_text += " " if predicted_character == 'space' else predicted_character
                        last_character = predicted_character
                        time.sleep(5)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clear', methods=['POST'])
def clear():
    global output_text
    output_text = ""
    return jsonify(success=True)

@app.route('/video_feed')
def video_feed():
    global stop_signal
    stop_signal = False
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop', methods=['POST'])
def stop():
    global stop_signal
    stop_signal = True
    return jsonify(success=True)

@app.route('/get_output', methods=['GET'])
def get_output():
    return jsonify(text=output_text)

@app.route('/speak', methods=['POST'])
def speak():
    engine.say(output_text)
    engine.runAndWait()
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
