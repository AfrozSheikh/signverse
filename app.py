from flask import Flask, render_template, Response, request, jsonify,send_from_directory
import os 
import cv2
import pickle
import numpy as np
import mediapipe as mp
import pyttsx3
import pyautogui
import time

app = Flask(__name__)

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Load the trained model (Random Forest)
model_dict = pickle.load(open('model/model6.p', 'rb'))
model = model_dict['model6']

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.6)

# Label dictionary for ASL (0: A, 1: B, ..., 25: Z)
labels_dict = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
    19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: ' '
}

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate

# Global variables for the app
word_buffer = ""
last_character = ""
output_text = ""
stop_signal = False
last_action_time = 0
cooldown = 3  # seconds cooldown between detections

def normalize_landmarks(hand_landmarks, x_min, y_min):
    return [coord for lm in hand_landmarks for coord in (lm.x - x_min, lm.y - y_min)]

def gen_frames():
    global word_buffer, last_character, output_text, stop_signal, last_action_time
    
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

        # Handle detection cooldown
        if current_time - last_action_time > cooldown:
            if predicted_character and predicted_character != "hand":
                # Add detected letter to buffer (allow repeats)
                word_buffer += predicted_character
                output_text = word_buffer  # Update the output text for the web interface
                last_action_time = current_time

            # If hand detected, press space and speak full buffer, then clear buffer
            elif hand_detected:
                pyautogui.press('space')
                
                if word_buffer.strip() != "":
                    engine.say(word_buffer)
                    engine.runAndWait()
                    word_buffer = ""
                    output_text = ""  # Clear the output text
                last_action_time = current_time

        # Show instructions and current buffer on screen
        # cv2.putText(frame, "ASL Characters A-Z", (10, 40),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        # cv2.putText(frame, f"Buffer: {word_buffer}", (10, 80),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

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
    global word_buffer, output_text, last_character
    word_buffer = ""
    output_text = ""
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
    return jsonify(text=output_text)

@app.route('/speak', methods=['POST'])
def speak():
    engine.say(output_text)
    engine.runAndWait()
    return jsonify(success=True)


# Route for sign language keyboard page
@app.route('/signkeyb')
def signkeyb():
    """Route for the ASL fingerspelling visualizer"""
    return render_template('signkeyb.html')

# Route to serve static images
@app.route('/images/asl/<filename>')
def serve_asl_image(filename):
    """Serve ASL letter images from static directory"""
    return send_from_directory(os.path.join(app.root_path, 'static', 'images', 'asl'), filename)

@app.route('/team')
def team():
    return render_template('team.html')

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,debug=True)

# from flask import Flask, render_template, Response, request, jsonify
# import cv2
# import pickle
# import numpy as np
# import mediapipe as mp
# import pyttsx3
# import time

# app = Flask(__name__)

# from flask_cors import CORS
# app = Flask(__name__)
# CORS(app)


# # Load the trained model (Random Forest)
# model_dict = pickle.load(open('model/model6.p', 'rb'))
# model = model_dict['model6']

# # Mediapipe setup
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.6)

# # TTS engine
# engine = pyttsx3.init()

# # Label dictionary for ASL (0: A, 1: B, ..., 25: Z, 25: 'hand')
# labels_dict = {
#     0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 
#     6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 
#     12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 
#     18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 
#     23: 'X', 24: 'Y', 25: 'hand'
# }

# allowed_labels = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 
#                  'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 
#                  'X', 'Y', 'hand'}

# # Store output
# output_text = ""
# stop_signal = False
# last_character = ""

# def normalize_landmarks(hand_landmarks, x_min, y_min):
#     """
#     Normalize the hand landmarks to fit in a fixed range.
#     """
#     return [coord for lm in hand_landmarks for coord in (lm.x - x_min, lm.y - y_min)]


# def gen_frames():
#     global output_text, stop_signal, last_character
#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#     # Add these variables for timing control
#     last_detection_time = 0
#     detection_delay = 4.0  # 1 second delay between detections
#     current_character = ""
#     character_persist_time = 0

#     while not stop_signal:
#         success, frame = cap.read()
#         if not success:
#             break

#         current_time = time.time()
#         H, W, _ = frame.shape
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = hands.process(frame_rgb)

#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 # Draw landmarks on the frame
#                 mp_drawing.draw_landmarks(
#                     frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
#                     mp_drawing_styles.get_default_hand_landmarks_style(),
#                     mp_drawing_styles.get_default_hand_connections_style())

#                 # Only process detection if enough time has passed
#                 if current_time - last_detection_time >= detection_delay:
#                     # Extract x and y coordinates of landmarks
#                     x = [lm.x for lm in hand_landmarks.landmark]
#                     y = [lm.y for lm in hand_landmarks.landmark]

#                     # Normalize the hand landmarks
#                     data_aux = normalize_landmarks(hand_landmarks.landmark, min(x), min(y))

#                     if len(data_aux) == 42:
#                         # Make prediction using the trained Random Forest model
#                         prediction = model.predict([np.asarray(data_aux)])

#                         # Get predicted character from the labels dictionary
#                         predicted_character = labels_dict.get(int(prediction[0]), "")

#                         if predicted_character in allowed_labels:
#                             # Update current character and detection time
#                             current_character = predicted_character
#                             last_detection_time = current_time
#                             character_persist_time = current_time

#                             # Add to output text only if it's different from last character
#                             if predicted_character != last_character:
#                                 last_character = predicted_character
#                                 output_text += predicted_character

#                 # Always show the last detected character (even if we're not processing new ones)
#                 if current_character:
#                     x = [lm.x for lm in hand_landmarks.landmark]
#                     y = [lm.y for lm in hand_landmarks.landmark]
#                     x1, y1 = int(min(x) * W) - 10, int(min(y) * H) - 10
#                     x2, y2 = int(max(x) * W) + 10, int(max(y) * H) + 10
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
#                     cv2.putText(frame, current_character, (x1, y1 - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3)

#         # Display the frame with instructions
#         cv2.putText(frame, "ASL Characters A-Z", (10, 40),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     cap.release()
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/clear', methods=['POST'])
# def clear():
#     global output_text, last_character
#     output_text = ""
#     last_character = ""
#     return jsonify(success=True)

# @app.route('/video_feed')
# def video_feed():
#     global stop_signal
#     stop_signal = False
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/how-it-works')
# def how_it_works():
#     return render_template('how-it-works.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# @app.route('/stop', methods=['POST'])
# def stop():
#     global stop_signal
#     stop_signal = True
#     return jsonify(success=True)

# @app.route('/get_output', methods=['GET'])
# def get_output():
#     return jsonify(text=output_text)

# @app.route('/speak', methods=['POST'])
# def speak():
#     engine.say(output_text)
#     engine.runAndWait()
#     return jsonify(success=True)


# @app.route('/team')
# def team():
#     return render_template('team.html')


# app.jinja_env.auto_reload = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True


# if __name__ == '__main__':
#     app.run(debug=True)

