# import pickle
# import cv2
# import mediapipe as mp
# import numpy as np
# import pyttsx3  # For text to speech

# # Initialize TTS engine
# engine = pyttsx3.init()

# # Load the trained model
# model_dict = pickle.load(open('model3.p', 'rb'))
# model = model_dict['model3']

# # Initialize the webcam
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles

# # Allow dynamic detection of hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.3)

# # Label mapping (only using relevant ones)
# labels_dict = {
#     0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 
#     6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
#     12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R',
#     18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X',
#     24: 'Y', 25: 'space', 26: 'Hand'
# }

# allowed_labels = set(labels_dict.values())  # Only these will be detected/displayed

# # Keep track of last spoken character
# last_character = ""

# def normalize_landmarks(hand_landmarks, x_min, y_min):
#     data = []
#     for landmark in hand_landmarks:
#         data.append(landmark.x - x_min)
#         data.append(landmark.y - y_min)
#     return data

# # Text file for output
# output_file = open("output.txt", "a")  # 'a' to append text

# while True:
#     ret, frame = cap.read()
#     H, W, _ = frame.shape

#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = hands.process(frame_rgb)

#     # Display message
#     cv2.putText(frame, "Press 'W' for label matching", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             mp_drawing.draw_landmarks(
#                 frame, hand_landmarks,
#                 mp_hands.HAND_CONNECTIONS,
#                 mp_drawing_styles.get_default_hand_landmarks_style(),
#                 mp_drawing_styles.get_default_hand_connections_style())

#             x = [landmark.x for landmark in hand_landmarks.landmark]
#             y = [landmark.y for landmark in hand_landmarks.landmark]
#             data_aux = normalize_landmarks(hand_landmarks.landmark, min(x), min(y))

#             if len(data_aux) == 42:  # Ensure 21 landmarks (x, y)
#                 prediction = model.predict([np.asarray(data_aux)])
#                 predicted_character = labels_dict[int(prediction[0])]

#                 if predicted_character in allowed_labels:
#                     x1 = int(min(x) * W) - 10
#                     y1 = int(min(y) * H) - 10
#                     x2 = int(max(x) * W) + 10
#                     y2 = int(max(y) * H) + 10

#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
#                     cv2.putText(frame, predicted_character, (x1, y1 - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

#                     # Speak and write if new character detected
#                     if predicted_character != last_character:
#                         last_character = predicted_character
#                         engine.say(predicted_character)
#                         engine.runAndWait()
#                         output_file.write(predicted_character + '\n')

#                     # Print on 'w' press
#                     key = cv2.waitKey(1) & 0xFF
#                     if key == ord('w'):
#                         print(f"Key 'w' pressed. Matching label: {predicted_character}")

#     cv2.imshow('frame', frame)

#     # Break loop on ESC
#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
# output_file.close()
# cv2.destroyAllWindows()






import pickle
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
from collections import Counter

# Initialize TTS engine
engine = pyttsx3.init()

# Load all three trained models
model1_dict = pickle.load(open('model2.p', 'rb'))
model1 = model1_dict['model2']

model2_dict = pickle.load(open('model3.p', 'rb'))
model2 = model2_dict['model3']

model3_dict = pickle.load(open('model6.p', 'rb'))
model3 = model3_dict['model6']

models = [model1, model2, model3]  # List of all models

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Allow dynamic detection of hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.3)

# Label mapping (only using relevant ones)
labels_dict = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 
    6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
    12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R',
    18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X',
    24: 'Y', 25: 'space', 26: 'Hand'
}

allowed_labels = set(labels_dict.values())  # Only these will be detected/displayed

# Keep track of last spoken character
last_character = ""

def normalize_landmarks(hand_landmarks, x_min, y_min):
    data = []
    for landmark in hand_landmarks:
        data.append(landmark.x - x_min)
        data.append(landmark.y - y_min)
    return data

def get_majority_vote(predictions):
    # Count occurrences of each prediction
    vote_count = Counter(predictions)
    # Get the prediction with most votes
    majority_vote = vote_count.most_common(1)[0][0]
    return majority_vote

# Text file for output
output_file = open("output.txt", "a")  # 'a' to append text

while True:
    ret, frame = cap.read()
    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Display message
    cv2.putText(frame, "Press 'W' for label matching", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            x = [landmark.x for landmark in hand_landmarks.landmark]
            y = [landmark.y for landmark in hand_landmarks.landmark]
            data_aux = normalize_landmarks(hand_landmarks.landmark, min(x), min(y))

            if len(data_aux) == 42:  # Ensure 21 landmarks (x, y)
                # Get predictions from all models
                predictions = []
                for model in models:
                    prediction = model.predict([np.asarray(data_aux)])
                    predictions.append(int(prediction[0]))
                
                # Get majority vote
                majority_vote = get_majority_vote(predictions)
                predicted_character = labels_dict[majority_vote]

                if predicted_character in allowed_labels:
                    x1 = int(min(x) * W) - 10
                    y1 = int(min(y) * H) - 10
                    x2 = int(max(x) * W) + 10
                    y2 = int(max(y) * H) + 10

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

                    # Speak and write if new character detected
                    if predicted_character != last_character:
                        last_character = predicted_character
                        engine.say(predicted_character)
                        engine.runAndWait()
                        output_file.write(predicted_character + '\n')

                    # Print on 'w' press
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('w'):
                        print(f"Key 'w' pressed. Matching label: {predicted_character}")
                        print(f"Individual model predictions: {[labels_dict[p] for p in predictions]}")

    cv2.imshow('frame', frame)

    # Break loop on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
output_file.close()
cv2.destroyAllWindows()