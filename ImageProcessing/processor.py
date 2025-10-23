import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
from typing import Union, Tuple

class ImageProcessor:
    """
    Enhanced image processor for OCR optimization
    Handles both Aadhaar cards and membership forms
    """
    
    @staticmethod
    def preprocess_aadhaar_image(image_file) -> bytes:
        """
        Preprocess Aadhaar card images for better OCR
        Focus: Sharpening, contrast enhancement, noise reduction
        """
        try:
            # Read image bytes
            image_bytes = image_file.read()
            
            # Convert to PIL Image
            img = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to optimal dimensions (keep aspect ratio)
            img = ImageProcessor._resize_image(img, max_size=1024)
            
            # Enhance contrast for better text visibility
            contrast_enhancer = ImageEnhance.Contrast(img)
            img = contrast_enhancer.enhance(1.3)
            
            # Enhance sharpness for crisp text
            sharpness_enhancer = ImageEnhance.Sharpness(img)
            img = sharpness_enhancer.enhance(1.5)
            
            # Apply slight denoising
            img = img.filter(ImageFilter.SMOOTH_MORE)
            
            # Convert back to bytes
            output_buffer = io.BytesIO()
            img.save(output_buffer, format='PNG', optimize=True, quality=95)
            
            return output_buffer.getvalue()
            
        except Exception as e:
            print(f"Error processing Aadhaar image: {e}")
            # Return original bytes if processing fails
            image_file.seek(0)
            return image_file.read()
    
    @staticmethod
    def preprocess_form_image(image_file) -> bytes:
        """
        Preprocess membership form images for better OCR
        Focus: Binarization, deskewing, noise removal, contrast enhancement
        """
        try:
            # Read image bytes
            image_bytes = image_file.read()
            
            # Convert to OpenCV format
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("Could not decode image")
            
            # Resize to optimal dimensions
            img = ImageProcessor._resize_opencv_image(img, max_size=1024)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Deskew the image (correct rotation)
            gray = ImageProcessor._deskew_image(gray)
            
            # Apply adaptive thresholding for better text contrast
            # This is crucial for forms with uneven lighting or faint text
            binary = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                35, 11
            )
            
            # Remove noise using morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
            
            # Convert back to PIL for final enhancements
            pil_img = Image.fromarray(binary)
            
            # Enhance sharpness for handwritten text
            sharpness_enhancer = ImageEnhance.Sharpness(pil_img)
            pil_img = sharpness_enhancer.enhance(2.0)
            
            # Convert back to bytes
            output_buffer = io.BytesIO()
            pil_img.save(output_buffer, format='PNG', optimize=True)
            
            return output_buffer.getvalue()
            
        except Exception as e:
            print(f"Error processing form image: {e}")
            # Return original bytes if processing fails
            image_file.seek(0)
            return image_file.read()
    
    @staticmethod
    def _resize_image(img: Image.Image, max_size: int = 1024) -> Image.Image:
        """Resize PIL image while maintaining aspect ratio"""
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        return img
    
    @staticmethod
    def _resize_opencv_image(img: np.ndarray, max_size: int = 1024) -> np.ndarray:
        """Resize OpenCV image while maintaining aspect ratio"""
        height, width = img.shape[:2]
        
        if max(height, width) <= max_size:
            return img
        
        if width > height:
            new_width = max_size
            new_height = int((height * max_size) / width)
        else:
            new_height = max_size
            new_width = int((width * max_size) / height)
        
        return cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    
    @staticmethod
    def _deskew_image(image: np.ndarray) -> np.ndarray:
        """
        Correct skewed/rotated documents using Hough Line Transform
        """
        try:
            # Create a copy to work with
            skewed = image.copy()
            
            # Apply edge detection
            edges = cv2.Canny(skewed, 50, 150, apertureSize=3)
            
            # Detect lines using Hough Line Transform
            lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
            
            if lines is not None and len(lines) > 0:
                # Calculate the most common angle
                angles = []
                for line in lines:
                    rho, theta = line[0]
                    angle = theta * 180 / np.pi
                    # Convert to rotation angle
                    if angle < 45:
                        angles.append(angle)
                    elif angle > 135:
                        angles.append(angle - 180)
                    else:
                        angles.append(angle - 90)
                
                if angles:
                    # Use median angle to avoid outliers
                    rotation_angle = np.median(angles)
                    
                    # Only rotate if angle is significant (> 0.5 degrees)
                    if abs(rotation_angle) > 0.5:
                        # Get image center and rotation matrix
                        (h, w) = image.shape[:2]
                        center = (w // 2, h // 2)
                        rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
                        
                        # Perform rotation
                        rotated = cv2.warpAffine(
                            image, rotation_matrix, (w, h),
                            flags=cv2.INTER_CUBIC,
                            borderMode=cv2.BORDER_REPLICATE
                        )
                        return rotated
            
            return image
            
        except Exception as e:
            print(f"Deskewing failed: {e}")
            return image
    
    @staticmethod
    def encode_to_base64(image_bytes: bytes) -> str:
        """Convert processed image bytes to base64 string"""
        return base64.b64encode(image_bytes).decode("utf-8")