#!/usr/bin/env python3
"""
Test script for Railway Document Intelligence System
"""

import requests
import json
import time
import os

# Configuration
BACKEND_URL = "http://localhost:5000/api"
TEST_FILES_DIR = "test_files"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_file_upload():
    """Test file upload functionality"""
    print("\n📤 Testing file upload...")
    
    # Create a test file if it doesn't exist
    if not os.path.exists(TEST_FILES_DIR):
        os.makedirs(TEST_FILES_DIR)
    
    test_file_path = os.path.join(TEST_FILES_DIR, "test.txt")
    with open(test_file_path, "w") as f:
        f.write("Railway Safety Manual\n\nThis is a test document for railway safety procedures.\nEmergency protocols and safety guidelines are outlined here.")
    
    try:
        with open(test_file_path, "rb") as f:
            files = {"files": ("test.txt", f, "text/plain")}
            data = {
                "ocrLanguage": "eng",
                "classificationMode": "railway"
            }
            
            response = requests.post(f"{BACKEND_URL}/upload", files=files, data=data)
            
        if response.status_code == 200:
            print("✅ File upload successful")
            return response.json()
        else:
            print(f"❌ File upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ File upload error: {e}")
        return None

def test_document_processing(upload_result):
    """Test document processing"""
    print("\n⚙️ Testing document processing...")
    
    if not upload_result:
        print("❌ Cannot test processing without upload result")
        return None
    
    try:
        payload = {
            "files": upload_result["files"],
            "ocr_language": "eng",
            "classification_mode": "railway"
        }
        
        response = requests.post(f"{BACKEND_URL}/process", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Document processing successful")
            print(f"   Document Type: {result.get('document_type', 'Unknown')}")
            print(f"   Classifications: {len(result.get('classification', []))}")
            print(f"   OCR Text Length: {len(result.get('ocr_text', ''))}")
            return result
        else:
            print(f"❌ Document processing failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Document processing error: {e}")
        return None

def test_chat_functionality(processed_data):
    """Test chat functionality"""
    print("\n💬 Testing chat functionality...")
    
    if not processed_data:
        print("❌ Cannot test chat without processed data")
        return False
    
    test_messages = [
        "What type of document is this?",
        "Summarize the main points",
        "Find safety information"
    ]
    
    for message in test_messages:
        try:
            payload = {
                "message": message,
                "processed_data": processed_data
            }
            
            response = requests.post(f"{BACKEND_URL}/chat", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Chat response for '{message}': {len(result.get('response', ''))} characters")
            else:
                print(f"❌ Chat failed for '{message}': {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Chat error for '{message}': {e}")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🚂 Railway Document Intelligence System - Test Suite\n")
    
    # Test 1: Health Check
    if not test_health_check():
        print("\n❌ Backend is not running or not responding")
        print("Please start the Flask server with: python app.py")
        return
    
    # Test 2: File Upload
    upload_result = test_file_upload()
    
    # Test 3: Document Processing
    processed_data = test_document_processing(upload_result)
    
    # Test 4: Chat Functionality
    chat_success = test_chat_functionality(processed_data)
    
    # Summary
    print("\n" + "="*50)
    print("🏁 Test Summary:")
    print("✅ Health Check: Passed")
    print(f"{'✅' if upload_result else '❌'} File Upload: {'Passed' if upload_result else 'Failed'}")
    print(f"{'✅' if processed_data else '❌'} Document Processing: {'Passed' if processed_data else 'Failed'}")
    print(f"{'✅' if chat_success else '❌'} Chat Functionality: {'Passed' if chat_success else 'Failed'}")
    
    if all([upload_result, processed_data, chat_success]):
        print("\n🎉 All tests passed! The system is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the backend setup and configuration.")
    
    # Cleanup
    if os.path.exists(TEST_FILES_DIR):
        import shutil
        shutil.rmtree(TEST_FILES_DIR)
        print(f"\n🧹 Cleaned up test files")

if __name__ == "__main__":
    main()