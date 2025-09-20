#!/usr/bin/env python3
"""
Test script for AI Chat functionality
Run this after starting the backend server to test chat responses
"""

import requests
import json
import time

# Configuration
API_BASE = "http://localhost:5000/api"

def test_chat_functionality():
    """Test the AI chat functionality with sample processed data"""
    
    print("🧪 Testing AI Chat Functionality")
    print("=" * 50)
    
    # Sample processed data to simulate a processed document
    sample_processed_data = {
        "document_type": "Railway Safety Manual",
        "summary": "This document outlines safety protocols for railway operations including emergency procedures, equipment maintenance guidelines, and passenger safety measures. Key sections cover operational safety, equipment inspection schedules, and regulatory compliance requirements.",
        "classification": [
            {
                "category": "Safety Protocols",
                "confidence": 0.95,
                "keywords": ["safety", "emergency", "procedures", "protocols"]
            },
            {
                "category": "Equipment Manual",
                "confidence": 0.87,
                "keywords": ["maintenance", "inspection", "equipment", "guidelines"]
            }
        ],
        "key_information": {
            "safety_level": "Critical",
            "document_version": "v2.1",
            "effective_date": "2025-01-01",
            "review_cycle": "Annual"
        },
        "ocr_text": "RAILWAY SAFETY MANUAL Version 2.1 Effective Date: January 1, 2025 1. INTRODUCTION This manual provides comprehensive safety guidelines for railway operations. All personnel must adhere to these protocols to ensure safe operations. 2. EMERGENCY PROCEDURES In case of emergency, follow these steps: - Immediately stop all train movements - Contact control center - Evacuate passengers if necessary 3. EQUIPMENT MAINTENANCE Regular inspection of railway equipment is mandatory: - Daily visual inspections - Weekly operational tests - Monthly comprehensive checks 4. REGULATORY COMPLIANCE This manual complies with: - Railway Safety Act 2023 - Transportation Safety Standards - Emergency Response Guidelines All staff must complete safety training annually."
    }
    
    # Test questions to ask
    test_questions = [
        "What type of document is this?",
        "What are the main safety requirements?",
        "When was this document last updated?",
        "What maintenance schedules are mentioned?",
        "What regulatory standards does this comply with?",
        "Summarize the emergency procedures"
    ]
    
    print(f"📋 Testing with sample document: {sample_processed_data['document_type']}")
    print()
    
    for i, question in enumerate(test_questions, 1):
        print(f"🤔 Question {i}: {question}")
        
        try:
            # Make chat request
            response = requests.post(
                f"{API_BASE}/chat",
                json={
                    "message": question,
                    "processed_data": sample_processed_data
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"🤖 AI Response: {data['response']}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection Error: {e}")
            print("💡 Make sure the backend server is running on localhost:5000")
            break
        
        print("-" * 80)
        time.sleep(1)  # Small delay between requests
    
    print()
    print("✅ Chat testing completed!")
    print()
    print("💡 Tips for better AI responses:")
    print("   - Ensure GITHUB_TOKEN is set in .env file")
    print("   - Ask specific, detailed questions")
    print("   - Process real documents for better context")

def test_health():
    """Test if the backend is running"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print(f"❌ Backend returned {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to backend server")
        print("💡 Start the backend with: python app.py")
        return False

if __name__ == "__main__":
    print("🚂 Railway Document Intelligence - AI Chat Tester")
    print()
    
    if test_health():
        print()
        test_chat_functionality()
    else:
        print("\n🔧 Please start the backend server first:")
        print("   python app.py")