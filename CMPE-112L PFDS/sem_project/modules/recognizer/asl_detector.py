# ASL Detector wrapper for SignBridge
import os
import cv2
import numpy as np
import logging
from typing import Tuple, Optional, List

logger = logging.getLogger("ASLDetector")

# We import tensorflow lazily so the app can start instantly and handle import errors
tf_available = False
try:
    import tensorflow as tf
    tf_available = True
except ImportError:
    logger.warning("TensorFlow not installed. Running in Mock Mode.")

class ASLDetector:
    """Wraps the TensorFlow/Keras CNN sign recognition model (200x200 RGB).
    Gracefully falls back to simulation mode if the model file is missing.
    """

    def __init__(self, model_dir: str = "model") -> None:
        self.model_dir = model_dir
        self.model_path = os.path.join(model_dir, "asl_model.h5")
        self.labels_path = os.path.join(model_dir, "labels.txt")
        self.model = None
        self.labels: List[str] = []
        self.model_loaded = False
        
        self.load_model_and_labels()

    def load_model_and_labels(self) -> None:
        """Attempts to load the pre-trained Keras CNN model and class labels."""
        # Load labels first
        if os.path.exists(self.labels_path):
            try:
                with open(self.labels_path, "r", encoding="utf-8") as f:
                    self.labels = [line.strip().upper() for line in f if line.strip()]
            except Exception as e:
                logger.error("Failed to read labels file: %s", str(e))
        
        # If labels empty, use default A-Z
        if not self.labels:
            self.labels = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

        # Check if TensorFlow and model file are available
        if not tf_available:
            logger.warning("TensorFlow is unavailable. ASLDetector running in MOCK mode.")
            return

        if not os.path.exists(self.model_path):
            logger.warning("Model file not found at %s. ASLDetector running in MOCK mode.", self.model_path)
            return

        # Load the model in a background thread to ensure instant app startup
        import threading
        def _load_model_thread():
            try:
                # Load Keras model
                self.model = tf.keras.models.load_model(self.model_path)
                self.model_loaded = True
                logger.info("Successfully loaded ASL model from %s in background", self.model_path)
            except Exception as e:
                logger.error("Error loading ASL model in background: %s. Falling back to MOCK mode.", str(e))
                self.model_loaded = False

        threading.Thread(target=_load_model_thread, daemon=True).start()

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[str], float]:
        """Processes a webcam frame, runs prediction if model loaded, and overlays HUD.
        Returns (annotated_frame, predicted_label, confidence).
        """
        h, w, _ = frame.shape
        
        # Define a standard Region of Interest (ROI) box in the center of the frame
        box_size = 200
        start_x = (w - box_size) // 2
        start_y = (h - box_size) // 2
        end_x = start_x + box_size
        end_y = start_y + box_size
        
        # Draw bounding box in BGR (Highlight color: #e94560 -> BGR is approx (96, 69, 233))
        roi_color = (96, 69, 233)
        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), roi_color, 2)
        
        # Crop the ROI
        roi = frame[start_y:end_y, start_x:end_x]
        
        predicted_label = None
        confidence = 0.0

        if self.model_loaded and self.model is not None:
            try:
                # Preprocess ROI: convert to RGB, resize to 200x200, normalize, expand dimensions
                rgb_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                resized = cv2.resize(rgb_roi, (200, 200))
                normalized = resized.astype(np.float32) / 255.0
                input_tensor = np.expand_dims(normalized, axis=0) # shape (1, 200, 200, 3)
                
                # Predict using __call__ for much faster real-time inference (no predict() overhead)
                predictions = self.model(input_tensor, training=False).numpy()
                class_idx = int(np.argmax(predictions[0]))
                confidence = float(predictions[0][class_idx])
                
                if class_idx < len(self.labels):
                    predicted_label = self.labels[class_idx]
            except Exception as e:
                logger.error("Error during prediction: %s", str(e))
        else:
            # Mock mode: return None or let the UI handle mock simulation
            predicted_label = None
            confidence = 0.0
            
        # Draw text overlay if we have a prediction
        if predicted_label:
            text = f"Sign: {predicted_label} ({confidence*100:.1f}%)"
            # Draw overlay on frame
            cv2.putText(frame, text, (start_x, start_y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 212, 170), 2) # Success green color
        else:
            if not self.model_loaded:
                cv2.putText(frame, "MOCK MODE (No Model)", (start_x, start_y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 170, 255), 1) # Warning orange
                            
        return frame, predicted_label, confidence
