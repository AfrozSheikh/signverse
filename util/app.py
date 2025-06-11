from flask import Flask, render_template, Response, request, jsonify
import cv2
import pickle
import numpy as np
import mediapipe as mp
import pyttsx3
import time
import pyautogui

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model (Random Forest)
model_dict = pickle.load(open(r'C:\Users\asus\OneDrive\Desktop\opencv-python\SignVerseFinal\model\model6.p', 'rb'))
model = model_dict['model6']

# Mediapipe setup for multi-hand detection (max 3 hands)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=3, min_detection_confidence=0.6)

# TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate

# Label dictionary for ASL (0: A, 1: B, ..., 25: Z, 25: 'hand')
labels_dict = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 
    6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 
    12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 
    18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 
    23: 'X', 24: 'Y', 25: 'hand'
}

allowed_labels = set(labels_dict.values())

# Global variables
output_text = ""
stop_signal = False

# Buffer and cooldown variables
word_buffer = ""
last_character = ""
cooldown = 3  # seconds cooldown between detections
last_action_time = 0

def normalize_landmarks(hand_landmarks, x_min, y_min):
    """
    Normalize the hand landmarks to fit in a fixed range.
    """
    return [coord for lm in hand_landmarks for coord in (lm.x - x_min, lm.y - y_min)]

def gen_frames():
    global output_text, stop_signal, word_buffer, last_character, last_action_time
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while not stop_signal:
        ret, frame = cap.read()
        if not ret:
            break

        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        current_time = time.time()
        hand_detected = False
        predicted_character = ""

        if results.multi_hand_landmarks:
            hand_detected = True
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                x = [lm.x for lm in hand_landmarks.landmark]
                y = [lm.y for lm in hand_landmarks.landmark]

                data_aux = normalize_landmarks(hand_landmarks.landmark, min(x), min(y))

                if len(data_aux) == 42:
                    prediction = model.predict([np.asarray(data_aux)])
                    predicted_character = labels_dict.get(int(prediction[0]), "")

                    # Draw bounding box and character
                    x1, y1 = int(min(x) * W) - 10, int(min(y) * H) - 10
                    x2, y2 = int(max(x) * W) + 10, int(max(y) * H) + 10
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3)

        # Handle detection cooldown and buffer update
        if current_time - last_action_time > cooldown:
            if predicted_character and predicted_character != "hand":
                # Add detected letter to buffer (allow repeats)
                word_buffer += predicted_character
                print(f"Added letter: {predicted_character}")
                print(f"Current buffer: {word_buffer}")
                last_action_time = current_time

            # If hand detected (without recognized letter), treat as space press and speak
            elif hand_detected:
                pyautogui.press('space')
                print("Typed space key")

                if word_buffer.strip() != "":
                    print(f"Speaking word: {word_buffer}")
                    engine.say(word_buffer)
                    engine.runAndWait()
                    word_buffer = ""
                last_action_time = current_time

        # Display instructions and buffer on screen
        cv2.putText(frame, "ESC to exit | ASL Characters A-Z", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        cv2.putText(frame, f"Buffer: {word_buffer}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clear', methods=['POST'])
def clear():
    global word_buffer, last_character
    word_buffer = ""
    last_character = ""
    return jsonify(success=True)

@app.route('/video_feed')
def video_feed():
    global stop_signal
    stop_signal = False
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how-it-works.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/stop', methods=['POST'])
def stop():
    global stop_signal
    stop_signal = True
    return jsonify(success=True)

@app.route('/get_output', methods=['GET'])
def get_output():
    global word_buffer
    return jsonify(text=word_buffer)

@app.route('/speak', methods=['POST'])
def speak():
    global word_buffer
    if word_buffer.strip():
        engine.say(word_buffer)
        engine.runAndWait()
    return jsonify(success=True)

@app.route('/team')
def team():
    return render_template('team.html')

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(debug=True)
