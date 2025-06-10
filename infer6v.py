import pickle
import cv2
import mediapipe as mp
import numpy as np
# Load the trained model (Random Forest)
model_dict = pickle.load(open('./model6.p', 'rb'))
model = model_dict['model6']

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.6)

# Label dictionary for ASL (0: A, 1: B, ..., 25: Z)
labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 
               12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 
               23: 'X', 24: 'Y', 25: 'hand'}

allowed_labels = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
                  'U', 'V', 'W', 'X', 'Y', 'hand'}

# Word buffer
word_buffer = ""
last_character = ""

# Optional output file
output_file = open("output.txt", "a")

def normalize_landmarks(hand_landmarks, x_min, y_min):
    """
    Normalize the hand landmarks to fit in a fixed range.
    """
    return [coord for lm in hand_landmarks for coord in (lm.x - x_min, lm.y - y_min)]

while True:
    ret, frame = cap.read()
    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            # Extract x and y coordinates of landmarks
            x = [lm.x for lm in hand_landmarks.landmark]
            y = [lm.y for lm in hand_landmarks.landmark]

            # Normalize the hand landmarks
            data_aux = normalize_landmarks(hand_landmarks.landmark, min(x), min(y))

            if len(data_aux) == 42:
                # Make prediction using the trained Random Forest model
                prediction = model.predict([np.asarray(data_aux)])

                # Get predicted character from the labels dictionary
                predicted_character = labels_dict.get(int(prediction[0]), "")

                if predicted_character in allowed_labels:
                    # Draw a bounding box around the hand
                    x1, y1 = int(min(x) * W) - 10, int(min(y) * H) - 10
                    x2, y2 = int(max(x) * W) + 10, int(max(y) * H) + 10
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3)

                    # Add new detected character to the word buffer
                    if predicted_character != last_character:
                        last_character = predicted_character

                        if predicted_character in allowed_labels:
                            word_buffer += predicted_character
                            print("Buffer:", word_buffer)

    # Display the frame with instructions
    cv2.putText(frame, "ESC to exit | ASL Characters A-Z", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

cap.release()
output_file.close()
cv2.destroyAllWindows()
