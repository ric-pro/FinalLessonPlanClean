#!/usr/bin/env python3.11
"""
Test script to verify Google GenAI SDK integration
This script tests the basic functionality without requiring a full server setup
"""

import asyncio
import os
from google import genai
from google.genai import types

async def test_basic_genai():
    """Test basic Google GenAI functionality"""
    print("Testing Google GenAI SDK Integration")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("ERROR: No API key found in environment variables")
        print("Please set GOOGLE_API_KEY")
        return False
    
    print(f"API Key found: {api_key[:10]}...")
    
    try:
        # Initialize client
        print("\n1. Initializing Google GenAI client...")
        client = genai.Client(api_key=api_key)
        print("   Client initialized successfully")
        
        # Test basic generation
        print("\n2. Testing basic content generation...")
        config = types.GenerateContentConfig(
            system_instruction="You are a helpful assistant."
        )
        
        response = await client.aio.models.generate_content(
            model='gemini-2.0-flash',
            contents='Say hello in one sentence.',
            config=config
        )
        
        print(f"   Response: {response.text[:100]}...")
        print("   Basic generation successful")
        
        # Test chat creation
        print("\n3. Testing chat session creation...")
        chat = client.aio.chats.create(
            model='gemini-2.0-flash',
            config=types.GenerateContentConfig(
                system_instruction="You are an expert educational content analyzer."
            )
        )
        print("   Chat session created successfully")
        
        # Test chat message
        print("\n4. Testing chat message...")
        chat_response = await chat.send_message('What is your purpose?')
        print(f"   Response: {chat_response.text[:100]}...")
        print("   Chat message successful")
        
        print("\n" + "=" * 50)
        print("All tests passed successfully!")
        print("Google GenAI SDK is properly integrated")
        return True
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("\nTest failed!")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_basic_genai())
    exit(0 if result else 1)

