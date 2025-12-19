# 🎮 BATU GUNTING KERTAS - ORIGINAL TEACHABLE MACHINE MODEL
# Copy and paste this into Google Colab to use your original keras_model.h5 model

# Step 1: Upload your model files first!
from google.colab import files
import os

print("📤 Upload model files terlebih dahulu:")
print("1. Upload keras_model.h5")
print("2. Upload labels.txt")
uploaded = files.upload()

# Step 2: Install dependencies
print("\n🔧 Installing dependencies...")
!pip install tensorflow opencv-python numpy pillow matplotlib -q

import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
from google.colab import files
import io
import warnings
warnings.filterwarnings('ignore')

print("✅ All imports successful!")

# Step 3: Define compatible model loader
class CompatibleDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        if 'groups' in kwargs:
            kwargs.pop('groups')
        super().__init__(*args, **kwargs)

class TeachableMachineModel:
    def __init__(self):
        self.model = None
        self.labels = []
        self.loaded = False

    def load_model_from_files(self, model_path='keras_model.h5', labels_path='labels.txt'):
        try:
            print("🤖 Loading original Teachable Machine model...")

            # Load labels
            if os.path.exists(labels_path):
                with open(labels_path, 'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    self.labels = []
                    for line in lines:
                        gesture = line.split(' ', 1)[1] if ' ' in line else line
                        self.labels.append(gesture)
                print(f"✅ Labels loaded: {self.labels}")
            else:
                print(f"⚠️ Labels file not found: {labels_path}")
                self.labels = ['batu', 'gunting', 'kertas']

            # Try multiple approaches to load the model
            model_loaded = False

            # Approach 1: With custom objects
            try:
                self.model = tf.keras.models.load_model(
                    model_path,
                    compile=False,
                    custom_objects={'DepthwiseConv2D': CompatibleDepthwiseConv2D}
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
        try:
            if isinstance(image, Image.Image):
                img_array = np.array(image)
            else:
                img_array = image

            if len(img_array.shape) == 3 and img_array.shape[2] == 4:
                img_array = img_array[:, :, :3]

            img_resized = cv2.resize(img_array, (224, 224))

            if len(img_resized.shape) == 3 and img_resized.shape[2] == 3:
                img_bgr = cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR)
            else:
                img_bgr = img_resized

            img_normalized = img_bgr / 255.0
            img_batch = np.expand_dims(img_normalized, axis=0)

            return img_batch

        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            return None

    def predict(self, image):
        if not self.loaded:
            print("❌ Model not loaded!")
            return None, 0.0

        try:
            processed_image = self.preprocess_image(image)
            if processed_image is None:
                return None, 0.0

            predictions = self.model.predict(processed_image, verbose=0)

            predicted_class_index = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_index])

            if predicted_class_index < len(self.labels):
                predicted_label = self.labels[predicted_class_index]
            else:
                predicted_label = 'unknown'

            return predicted_label, confidence

        except Exception as e:
            print(f"❌ Error making prediction: {e}")
            return None, 0.0

# Step 4: Initialize model
print("\n🚀 Loading your original Teachable Machine model...")
print("="*60)

tm_model = TeachableMachineModel()
success = tm_model.load_model_from_files('keras_model.h5', 'labels.txt')

print("\n" + "="*60)
if success:
    print("🎉 MODEL LOADED SUCCESSFULLY!")
    print("="*60)
    print(f"📊 Model Info:")
    print(f"   Input Shape: {tm_model.model.input_shape}")
    print(f"   Output Shape: {tm_model.model.output_shape}")
    print(f"   Number of Classes: {len(tm_model.labels)}")
    print(f"   Labels: {tm_model.labels}")
    print(f"\n✅ Original Teachable Machine model is ready!")
else:
    print("❌ MODEL LOADING FAILED!")
    print("="*60)
    print("💡 Make sure keras_model.h5 and labels.txt are uploaded!")

# Step 5: Game class
class BatuGuntingKertasGame:
    def __init__(self, model_instance):
        self.model = model_instance
        self.player1_choice = None
        self.player2_choice = None
        self.player1_image = None
        self.player2_image = None
        self.player1_confidence = 0
        self.player2_confidence = 0
        self.player1_score = 0
        self.player2_score = 0

    def get_emoji(self, choice):
        emoji_map = {
            'batu': '✊',
            'gunting': '✌️',
            'kertas': '✋'
        }
        return emoji_map.get(choice, '❓')

    def predict_gesture(self, image):
        if self.model and self.model.loaded:
            return self.model.predict(image)
        else:
            print("❌ Model not loaded!")
            return None, 0.0

    def determine_winner(self, player1_choice, player2_choice):
        if player1_choice == player2_choice:
            return 'tie', "Seri! Keduanya memilih yang sama."

        if player1_choice == 'batu' and player2_choice == 'gunting':
            return 'player1', '🗿 Batu menghancurkan Gunting!'
        if player1_choice == 'gunting' and player2_choice == 'batu':
            return 'player2', '🗿 Batu menghancurkan Gunting!'

        if player1_choice == 'gunting' and player2_choice == 'kertas':
            return 'player1', '✌️ Gunting memotong Kertas!'
        if player1_choice == 'kertas' and player2_choice == 'gunting':
            return 'player2', '✌️ Gunting memotong Kertas!'

        if player1_choice == 'kertas' and player2_choice == 'batu':
            return 'player1', '✋ Kertas membungkus Batu!'
        if player1_choice == 'batu' and player2_choice == 'kertas':
            return 'player2', '✋ Kertas membungkus Batu!'

        return 'tie', 'Hasil tidak dapat ditentukan.'

    def reset_round(self):
        self.player1_choice = None
        self.player2_choice = None
        self.player1_image = None
        self.player2_image = None
        self.player1_confidence = 0
        self.player2_confidence = 0

# Initialize game
if 'tm_model' in locals() and tm_model.loaded:
    game = BatuGuntingKertasGame(tm_model)
    print("✅ Game initialized with original Teachable Machine model!")
else:
    print("❌ Cannot initialize game - model not loaded!")

# Step 6: Upload and detection functions
def upload_player_image(player_num):
    print(f"\n📸 Upload foto untuk Pemain {player_num}:")
    print("📝 Petunjuk:")
    print("   • 🗿 Batu: Kepal tangan (fist)")
    print("   • ✌️ Gunting: 2 jari (peace sign)")
    print("   • ✋ Kertas: Tangan terbuka (open hand)")
    print("")

    uploaded = files.upload()

    if uploaded:
        filename = list(uploaded.keys())[0]
        image = Image.open(io.BytesIO(uploaded[filename]))

        if image.mode != 'RGB':
            image = image.convert('RGB')

        # AI Prediction dengan ORIGINAL MODEL
        print(f"🤖 Original Teachable Machine Model sedang menganalisis gambar Pemain {player_num}...")
        prediction, confidence = game.predict_gesture(image)

        # Simpan hasil
        if player_num == 1:
            game.player1_image = image
            game.player1_choice = prediction
            game.player1_confidence = confidence
        else:
            game.player2_image = image
            game.player2_choice = prediction
            game.player2_confidence = confidence

        # Tampilkan hasil
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(image)
        plt.title(f'📸 Foto Pemain {player_num}', fontsize=14, weight='bold')
        plt.axis('off')

        plt.subplot(1, 2, 2)
        emoji = game.get_emoji(prediction)
        plt.text(0.5, 0.6, emoji, fontsize=100, ha='center')
        plt.text(0.5, 0.3, prediction.upper(), fontsize=24, ha='center', weight='bold')
        plt.text(0.5, 0.1, f'Original AI Confidence: {confidence:.1%}', fontsize=16, ha='center', color='green')
        plt.text(0.5, 0.0, '🤖 Teachable Machine Model', fontsize=12, ha='center', style='italic')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.axis('off')
        plt.title('🧠 Original AI Detection Result', fontsize=14, weight='bold')

        plt.tight_layout()
        plt.show()

        print(f"✅ Pemain {player_num}: {emoji} {prediction.upper()} (Original AI Confidence: {confidence:.1%})")
        return True
    else:
        print(f"❌ Tidak ada file yang diupload untuk Pemain {player_num}")
        return False

def show_results():
    if game.player1_choice and game.player2_choice:
        # Tentukan pemenang
        winner, result_text = game.determine_winner(game.player1_choice, game.player2_choice)

        # Update skor
        if winner == 'player1':
            game.player1_score += 1
            winner_display = "🎉 PEMAIN 1 MENANG! 🎉"
            color = 'green'
        elif winner == 'player2':
            game.player2_score += 1
            winner_display = "🎉 PEMAIN 2 MENANG! 🎉"
            color = 'blue'
        else:
            winner_display = "🤝 SERI! 🤝"
            color = 'orange'

        # Tampilkan hasil
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'🏆 {winner_display}', fontsize=28, weight='bold', color=color)

        # Pemain 1
        if game.player1_image:
            axes[0, 0].imshow(game.player1_image)
            axes[0, 0].set_title('👤 Pemain 1', fontsize=16, weight='bold')
            axes[0, 0].axis('off')

            emoji1 = game.get_emoji(game.player1_choice)
            axes[1, 0].text(0.5, 0.6, emoji1, fontsize=120, ha='center')
            axes[1, 0].text(0.5, 0.3, f'{game.player1_choice.upper()}', fontsize=20, ha='center', weight='bold')
            axes[1, 0].text(0.5, 0.1, f'AI Confidence: {game.player1_confidence:.1%}', fontsize=14, ha='center')
            axes[1, 0].text(0.5, 0.0, '🤖 Original Model', fontsize=12, ha='center', style='italic')
            axes[1, 0].set_xlim(0, 1)
            axes[1, 0].set_ylim(0, 1)
            axes[1, 0].axis('off')

        # Pemain 2
        if game.player2_image:
            axes[0, 1].imshow(game.player2_image)
            axes[0, 1].set_title('👥 Pemain 2', fontsize=16, weight='bold')
            axes[0, 1].axis('off')

            emoji2 = game.get_emoji(game.player2_choice)
            axes[1, 1].text(0.5, 0.6, emoji2, fontsize=120, ha='center')
            axes[1, 1].text(0.5, 0.3, f'{game.player2_choice.upper()}', fontsize=20, ha='center', weight='bold')
            axes[1, 1].text(0.5, 0.1, f'AI Confidence: {game.player2_confidence:.1%}', fontsize=14, ha='center')
            axes[1, 1].text(0.5, 0.0, '🤖 Original Model', fontsize=12, ha='center', style='italic')
            axes[1, 1].set_xlim(0, 1)
            axes[1, 1].set_ylim(0, 1)
            axes[1, 1].axis('off')

        plt.tight_layout()
        plt.show()

        # Tampilkan hasil text
        print(f"\n{'='*80}")
        print(f"🏆 HASIL PERTANDINGAN - ORIGINAL TEACHABLE MACHINE MODEL")
        print(f"{'='*80}")
        print(f"👤 Pemain 1: {game.get_emoji(game.player1_choice)} {game.player1_choice.upper()} (AI Confidence: {game.player1_confidence:.1%})")
        print(f"👥 Pemain 2: {game.get_emoji(game.player2_choice)} {game.player2_choice.upper()} (AI Confidence: {game.player2_confidence:.1%})")
        print(f"\n🎯 Hasil: {result_text}")
        print(f"\n📈 SKOR SAAT INI:")
        print(f"   👤 Pemain 1: {game.player1_score}")
        print(f"   👥 Pemain 2: {game.player2_score}")
        print(f"\n🤖 AI Model: Original Teachable Machine (keras_model.h5)")
        print(f"{'='*80}")

    else:
        print("❌ Belum semua pemain mengupload foto!")
        print("💡 Pastikan kedua pemain sudah mengupload foto sebelum melihat hasil.")

# Step 7: Game function
def play_round_with_original_model():
    """Main game function using original Teachable Machine model"""
    if not ('tm_model' in locals() and tm_model.loaded):
        print("❌ Model not loaded! Upload keras_model.h5 and labels.txt first.")
        return

    # Reset ronde
    game.reset_round()

    print(f"\n📈 SKOR TOTAL: P1: {game.player1_score} | P2: {game.player2_score}")
    print("\n" + "="*60)
    print("🤖 Menggunakan Original Teachable Machine Model")
    print("="*60 + "\n")

    # Pemain 1 upload
    player1_success = upload_player_image(1)

    if player1_success:
        print("\n" + "="*50)
        print("✅ Pemain 1 berhasil! Sekarang giliran Pemain 2...")
        print("="*50)

        # Pemain 2 upload
        player2_success = upload_player_image(2)

        if player2_success:
            print("\n" + "="*50)
            print("✅ Kedua pemain berhasil! Menentukan pemenang...")
            print("🧠 Menggunakan Original Teachable Machine AI")
            print("="*50)

            # Show results
            show_results()

            print(f"\n🔄 Mau main lagi dengan original AI?")
            print("📍 Ketik play_round_with_original_model() lagi untuk ronde baru")

print("\n" + "="*70)
print("🎮 BATU GUNTING KERTAS - ORIGINAL TEACHABLE MACHINE MODEL")
print("="*70)
print("🤖 Menggunakan model asli Anda (keras_model.h5)")
print("="*70 + "\n")

print("🚀 **Ready to play with your original model!**")
print("📌 Ketik: play_round_with_original_model() untuk memulai permainan")
print("="*70)