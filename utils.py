import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import streamlit as st
from simple_classifier import get_classifier

# Custom DepthwiseConv2D layer to handle compatibility issues
class CompatibleDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        # Remove 'groups' from kwargs if present (not supported in current TF version)
        if 'groups' in kwargs:
            kwargs.pop('groups')
        super().__init__(*args, **kwargs)

# Global variables for model and labels
_model = None
_labels = None

def load_model():
    """Load the TensorFlow model and labels"""
    global _model, _labels

    # Always load labels first
    try:
        with open('labels.txt', 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            _labels = []
            for line in lines:
                # Extract gesture name (remove number prefix)
                gesture = line.split(' ', 1)[1] if ' ' in line else line
                _labels.append(gesture)
        print(f"Labels loaded successfully: {_labels}")
    except Exception as e:
        print(f"Error loading labels: {e}")
        _labels = ['batu', 'gunting', 'kertas']  # Default fallback
        print("Using default labels")

    # Try loading model only if not already attempted
    if _model is None:
        try:
            # First attempt: with compatible custom objects
            _model = tf.keras.models.load_model(
                'keras_model.h5',
                compile=False,
                custom_objects={
                    'DepthwiseConv2D': CompatibleDepthwiseConv2D
                }
            )
            print("Model loaded successfully with compatible custom objects")
        except Exception as first_error:
            print(f"First attempt failed: {first_error}")
            try:
                # Second attempt: with legacy DepthwiseConv2D
                tf.keras.utils.get_custom_objects()['DepthwiseConv2D'] = CompatibleDepthwiseConv2D
                _model = tf.keras.models.load_model('keras_model.h5', compile=False)
                print("Model loaded successfully with legacy custom objects")
            except Exception as second_error:
                print(f"Second attempt failed: {second_error}")
                try:
                    # Third attempt: try different loading method
                    _model = tf.keras.models.load_model('keras_model.h5')
                    print("Model loaded successfully with default loading")
                except Exception as third_error:
                    print(f"Third attempt failed: {third_error}")
                    # If all attempts fail, set model to None for demo mode
                    _model = None
                    print("Model loading failed, using demo mode")

    return True

def preprocess_image(image):
    """Preprocess image for model prediction"""
    try:
        # Convert PIL Image to numpy array
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image

        # Resize to 224x224 (standard for Teachable Machine models)
        img_resized = cv2.resize(img_array, (224, 224))

        # Convert RGB to BGR if needed (Teachable Machine models expect BGR)
        if len(img_resized.shape) == 3 and img_resized.shape[2] == 3:
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR)

        # Normalize pixel values to [0, 1]
        img_normalized = img_resized / 255.0

        # Add batch dimension
        img_batch = np.expand_dims(img_normalized, axis=0)

        return img_batch
    except Exception as e:
        st.error(f"Error preprocessing image: {e}")
        return None

def predict_gesture(image):
    """Predict the gesture from the image"""
    if _model is None or _labels is None:
        load_model()

    try:
        # If model is None (demo mode), try simple classifier
        if _model is None:
            try:
                # Use simple classifier as fallback
                classifier = get_classifier()
                prediction, confidence = classifier.predict(image)
                return prediction, confidence
            except Exception as e:
                st.error(f"Simple classifier failed: {e}")
                return None, 0

        # Try using original model first
        try:
            # Preprocess the image
            processed_image = preprocess_image(image)
            if processed_image is None:
                return None, 0

            # Make prediction
            predictions = _model.predict(processed_image)

            # Get the predicted class and confidence
            predicted_class_index = np.argmax(predictions[0])
            confidence = predictions[0][predicted_class_index]

            # Get the label
            predicted_label = _labels[predicted_class_index]

            return predicted_label, confidence

        except Exception as model_error:
            print(f"Original model prediction failed: {model_error}")
            # Fallback to simple classifier
            classifier = get_classifier()
            prediction, confidence = classifier.predict(image)
            return prediction, confidence

    except Exception as e:
        st.error(f"Error making prediction: {e}")
        return None, 0

def manual_gesture_selection(player_name):
    """Manual gesture selection for demo mode"""
    st.info(f"🎮 Mode Demo: Silakan pilih secara manual untuk {player_name}")

    choice = st.radio(
        f"Pilih {player_name}:",
        ["🗿 Batu", "✌️ Gunting", "✋ Kertas"],
        key=f"manual_choice_{player_name}",
        index=0  # Default selection
    )

    # Extract just the gesture name from the choice
    if "Batu" in choice:
        return "batu", 1.0
    elif "Gunting" in choice:
        return "gunting", 1.0
    else:
        return "kertas", 1.0

def determine_winner(player1_choice, player2_choice):
    """
    Determine the winner based on Rock-Paper-Scissors rules
    Returns: (winner, winner_text, result_text)
    """
    if player1_choice == player2_choice:
        return 'tie', None, "Seri! Keduanya memilih yang sama."

    # Rock (Batu) beats Scissors (Gunting)
    if player1_choice == 'batu' and player2_choice == 'gunting':
        return 'player1', 'Batu menghancurkan Gunting!', 'Batu menghancurkan Gunting!'

    if player1_choice == 'gunting' and player2_choice == 'batu':
        return 'player2', 'Batu menghancurkan Gunting!', 'Batu menghancurkan Gunting!'

    # Scissors (Gunting) beats Paper (Kertas)
    if player1_choice == 'gunting' and player2_choice == 'kertas':
        return 'player1', 'Gunting memotong Kertas!', 'Gunting memotong Kertas!'

    if player1_choice == 'kertas' and player2_choice == 'gunting':
        return 'player2', 'Gunting memotong Kertas!', 'Gunting memotong Kertas!'

    # Paper (Kertas) beats Rock (Batu)
    if player1_choice == 'kertas' and player2_choice == 'batu':
        return 'player1', 'Kertas membungkus Batu!', 'Kertas membungkus Batu!'

    if player1_choice == 'batu' and player2_choice == 'kertas':
        return 'player2', 'Kertas membungkus Batu!', 'Kertas membungkus Batu!'

    # Fallback (shouldn't reach here)
    return 'tie', None, "Hasil tidak dapat ditentukan.", "Hasil tidak dapat ditentukan."

def get_emoji_for_choice(choice):
    """Get emoji representation for each choice"""
    emoji_map = {
        'batu': '✊',
        'gunting': '✌️',
        'kertas': '✋'
    }
    return emoji_map.get(choice, '❓')