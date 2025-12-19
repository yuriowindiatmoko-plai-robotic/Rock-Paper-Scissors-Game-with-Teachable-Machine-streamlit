import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os

# Custom compatible DepthwiseConv2D layer
class CompatibleDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        # Remove 'groups' parameter if present (not supported in current TF)
        if 'groups' in kwargs:
            kwargs.pop('groups')
        super().__init__(*args, **kwargs)

class TeachableMachineModel:
    def __init__(self):
        self.model = None
        self.labels = []
        self.loaded = False

    def load_model_from_files(self, model_path='keras_model.h5', labels_path='labels.txt'):
        """Load the original Teachable Machine model with compatibility fixes"""
        try:
            print("🤖 Loading original Teachable Machine model...")

            # Load labels first
            if os.path.exists(labels_path):
                with open(labels_path, 'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    self.labels = []
                    for line in lines:
                        # Extract gesture name (remove number prefix like "0 batu")
                        gesture = line.split(' ', 1)[1] if ' ' in line else line
                        self.labels.append(gesture)
                print(f"✅ Labels loaded: {self.labels}")
            else:
                print(f"⚠️ Labels file not found: {labels_path}")
                self.labels = ['batu', 'gunting', 'kertas']  # Default fallback

            # Try multiple approaches to load the model
            model_loaded = False

            # Approach 1: With custom objects
            try:
                self.model = tf.keras.models.load_model(
                    model_path,
                    compile=False,
                    custom_objects={
                        'DepthwiseConv2D': CompatibleDepthwiseConv2D
                    }
                )
                print("✅ Model loaded with custom DepthwiseConv2D")
                model_loaded = True
            except Exception as e1:
                print(f"❌ Approach 1 failed: {str(e1)[:100]}...")

                # Approach 2: Register custom objects globally
                try:
                    tf.keras.utils.get_custom_objects()['DepthwiseConv2D'] = CompatibleDepthwiseConv2D
                    self.model = tf.keras.models.load_model(model_path, compile=False)
                    print("✅ Model loaded with global custom objects")
                    model_loaded = True
                except Exception as e2:
                    print(f"❌ Approach 2 failed: {str(e2)[:100]}...")

                    # Approach 3: Try loading without compilation
                    try:
                        self.model = tf.keras.models.load_model(model_path, compile=False)
                        print("✅ Model loaded without compilation")
                        model_loaded = True
                    except Exception as e3:
                        print(f"❌ Approach 3 failed: {str(e3)[:100]}...")

            if model_loaded:
                self.loaded = True
                print(f"🎉 Model successfully loaded! Input shape: {self.model.input_shape}")
                return True
            else:
                print("❌ All loading approaches failed")
                return False

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False

    def preprocess_image(self, image):
        """Preprocess image for Teachable Machine model (224x224, normalized)"""
        try:
            # Convert PIL Image to numpy array
            if isinstance(image, Image.Image):
                img_array = np.array(image)
            else:
                img_array = image

            # Ensure RGB format
            if len(img_array.shape) == 3 and img_array.shape[2] == 4:
                img_array = img_array[:, :, :3]  # Remove alpha if present

            # Resize to 224x224 (Teachable Machine standard)
            img_resized = cv2.resize(img_array, (224, 224))

            # Convert RGB to BGR if needed (Teachable Machine models expect BGR)
            if len(img_resized.shape) == 3 and img_resized.shape[2] == 3:
                img_bgr = cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR)
            else:
                img_bgr = img_resized

            # Normalize pixel values to [0, 1]
            img_normalized = img_bgr / 255.0

            # Add batch dimension
            img_batch = np.expand_dims(img_normalized, axis=0)

            return img_batch

        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            return None

    def predict(self, image):
        """Predict gesture using the loaded Teachable Machine model"""
        if not self.loaded:
            print("❌ Model not loaded!")
            return None, 0.0

        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image)
            if processed_image is None:
                return None, 0.0

            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)

            # Get the predicted class and confidence
            predicted_class_index = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_index])

            # Get the label
            if predicted_class_index < len(self.labels):
                predicted_label = self.labels[predicted_class_index]
            else:
                predicted_label = 'unknown'

            return predicted_label, confidence

        except Exception as e:
            print(f"❌ Error making prediction: {e}")
            return None, 0.0

    def get_model_info(self):
        """Get information about the loaded model"""
        if self.loaded:
            info = {
                'loaded': True,
                'input_shape': self.model.input_shape,
                'output_shape': self.model.output_shape,
                'labels': self.labels,
                'num_classes': len(self.labels)
            }
        else:
            info = {
                'loaded': False,
                'error': 'Model not loaded'
            }
        return info

# Test function for model loading
def test_model_loading():
    """Test if the model can be loaded properly"""
    print("🧪 Testing model loading...")

    model_loader = TeachableMachineModel()

    # Try to load model (assuming files are in current directory)
    success = model_loader.load_model_from_files('keras_model.h5', 'labels.txt')

    if success:
        info = model_loader.get_model_info()
        print(f"✅ Model test successful!")
        print(f"   Input shape: {info['input_shape']}")
        print(f"   Labels: {info['labels']}")
        return model_loader
    else:
        print("❌ Model test failed")
        return None

# Create global instance
tm_model = None

def get_teachable_machine_model():
    """Get or create the Teachable Machine model instance"""
    global tm_model
    if tm_model is None:
        tm_model = TeachableMachineModel()
        # Try to load immediately
        tm_model.load_model_from_files('keras_model.h5', 'labels.txt')
    return tm_model

def predict_with_teachable_machine(image):
    """Convenience function to predict with the Teachable Machine model"""
    model = get_teachable_machine_model()
    return model.predict(image)