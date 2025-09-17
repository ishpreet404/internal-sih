import os
import pymupdf  # PyMuPDF
import pytesseract
from PIL import Image
import cv2
import numpy as np
from langdetect import detect_langs
import json
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentOCR:
    def __init__(self, tesseract_langs='mal+eng'):
        """
        Initialize OCR service
        Args:
            tesseract_langs: Languages for Tesseract OCR (default: Malayalam + English)
        """
        self.tesseract_langs = tesseract_langs
        
    def extract_text_from_pdf(self, pdf_path: str, output_dir: str) -> Dict[int, Dict]:
        """
        Extract text from PDF using PyMuPDF first, fall back to OCR for low-text pages
        
        Args:
            pdf_path: Path to PDF file
            output_dir: Directory to save extracted page texts
            
        Returns:
            Dictionary with page numbers as keys and page info as values
        """
        page_texts = {}
        
        try:
            # Open PDF with PyMuPDF
            doc = pymupdf.open(pdf_path)
            
            for page_num, page in enumerate(doc, 1):
                logger.info(f"Processing page {page_num}/{len(doc)}")
                
                # First try to extract text directly
                text = page.get_text()
                
                # Check if page has meaningful text (threshold: 50 characters)
                if len(text.strip()) < 50:
                    logger.info(f"Page {page_num} has low text content, running OCR...")
                    text = self._ocr_pdf_page(page, page_num)
                
                # Detect language
                language = self._detect_language(text)
                
                # Add page marker
                marked_text = f"[p{page_num}]\n{text}"
                
                page_info = {
                    'page_num': page_num,
                    'text': text,
                    'marked_text': marked_text,
                    'language': language,
                    'method': 'ocr' if len(text.strip()) < 50 else 'direct'
                }
                
                page_texts[page_num] = page_info
                
                # Save individual page text
                self._save_page_text(output_dir, page_num, page_info)
                
            doc.close()
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
            
        return page_texts
    
    def extract_text_from_image(self, image_path: str, output_dir: str) -> Dict[int, Dict]:
        """
        Extract text from image file using OCR
        
        Args:
            image_path: Path to image file
            output_dir: Directory to save extracted text
            
        Returns:
            Dictionary with single page (page 1)
        """
        try:
            # Read and preprocess image
            image = cv2.imread(image_path)
            processed_image = self._preprocess_image(image)
            
            # Convert to PIL Image for Tesseract
            pil_image = Image.fromarray(processed_image)
            
            # Run OCR
            text = pytesseract.image_to_string(pil_image, lang=self.tesseract_langs)
            
            # Detect language
            language = self._detect_language(text)
            
            # Add page marker
            marked_text = f"[p1]\n{text}"
            
            page_info = {
                'page_num': 1,
                'text': text,
                'marked_text': marked_text,
                'language': language,
                'method': 'ocr'
            }
            
            # Save page text
            self._save_page_text(output_dir, 1, page_info)
            
            return {1: page_info}
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise
    
    def _ocr_pdf_page(self, page, page_num: int) -> str:
        """
        Convert PDF page to image and run OCR
        
        Args:
            page: PyMuPDF page object
            page_num: Page number
            
        Returns:
            Extracted text
        """
        try:
            # Convert page to image (high resolution for better OCR)
            mat = pymupdf.Matrix(300/72, 300/72)  # 300 DPI
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to numpy array
            img_data = pix.tobytes("png")
            nparr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Preprocess image
            processed_img = self._preprocess_image(img)
            
            # Convert to PIL Image
            pil_image = Image.fromarray(processed_img)
            
            # Run OCR
            text = pytesseract.image_to_string(pil_image, lang=self.tesseract_langs)
            
            return text
            
        except Exception as e:
            logger.error(f"Error in OCR for page {page_num}: {str(e)}")
            return ""
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply adaptive thresholding for better text extraction
        thresh = cv2.adaptiveThreshold(
            denoised, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Deskew if needed (optional, can add if performance allows)
        # angle = self._get_skew_angle(thresh)
        # if abs(angle) > 0.5:
        #     thresh = self._rotate_image(thresh, angle)
        
        return thresh
    
    def _detect_language(self, text: str) -> str:
        """
        Detect primary language of text
        
        Args:
            text: Input text
            
        Returns:
            Language code ('en', 'ml', or 'mixed')
        """
        if not text or len(text.strip()) < 10:
            return 'unknown'
        
        try:
            langs = detect_langs(text)
            
            # Get top language
            if langs:
                primary_lang = langs[0]
                
                # Check if Malayalam
                if primary_lang.lang == 'ml' and primary_lang.prob > 0.7:
                    return 'ml'
                # Check if English
                elif primary_lang.lang == 'en' and primary_lang.prob > 0.7:
                    return 'en'
                # Mixed content
                else:
                    return 'mixed'
            
            return 'unknown'
            
        except Exception as e:
            logger.warning(f"Language detection failed: {str(e)}")
            return 'unknown'
    
    def _save_page_text(self, output_dir: str, page_num: int, page_info: Dict):
        """
        Save page text and metadata to file
        
        Args:
            output_dir: Output directory
            page_num: Page number
            page_info: Page information dictionary
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Save text file
        text_path = os.path.join(output_dir, f"page_{page_num}.txt")
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(page_info['marked_text'])
        
        # Save metadata
        meta_path = os.path.join(output_dir, f"page_{page_num}_meta.json")
        meta_info = {
            'page_num': page_info['page_num'],
            'language': page_info['language'],
            'method': page_info['method'],
            'char_count': len(page_info['text'])
        }
        
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta_info, f, indent=2)
    
    def combine_page_texts(self, page_texts: Dict[int, Dict]) -> str:
        """
        Combine all page texts into single document with page markers
        
        Args:
            page_texts: Dictionary of page texts
            
        Returns:
            Combined text with page markers
        """
        combined_text = ""
        
        for page_num in sorted(page_texts.keys()):
            if combined_text:
                combined_text += "\n\n"
            combined_text += page_texts[page_num]['marked_text']
        
        return combined_text
    
    def get_page_languages(self, page_texts: Dict[int, Dict]) -> Dict[str, List[int]]:
        """
        Get language distribution across pages
        
        Args:
            page_texts: Dictionary of page texts
            
        Returns:
            Dictionary with languages as keys and page numbers as values
        """
        lang_distribution = {}
        
        for page_num, info in page_texts.items():
            lang = info['language']
            if lang not in lang_distribution:
                lang_distribution[lang] = []
            lang_distribution[lang].append(page_num)
        
        return lang_distribution


# Convenience functions for direct use
def extract_document_text(file_path: str, output_dir: str, tesseract_langs='mal+eng') -> Tuple[Dict[int, Dict], str]:
    """
    Extract text from document (PDF or image)
    
    Args:
        file_path: Path to document
        output_dir: Directory to save outputs
        tesseract_langs: Languages for Tesseract
        
    Returns:
        Tuple of (page_texts dictionary, combined_text)
    """
    ocr = DocumentOCR(tesseract_langs=tesseract_langs)
    
    # Check file type
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.pdf':
        page_texts = ocr.extract_text_from_pdf(file_path, output_dir)
    elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
        page_texts = ocr.extract_text_from_image(file_path, output_dir)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")
    
    # Get combined text
    combined_text = ocr.combine_page_texts(page_texts)
    
    return page_texts, combined_text