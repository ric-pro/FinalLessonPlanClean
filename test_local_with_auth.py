#!/usr/bin/env python3
"""
Local Server Test with Authentication
Tests the Google GenAI SDK integration on localhost
"""

import requests
import json
import tempfile
import os
from datetime import datetime

class LocalServerTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.auth_token = None
        self.tests_passed = 0
        self.tests_run = 0
    
    def log(self, message, success=None):
        """Log test result"""
        if success is True:
            print(f"[PASS] {message}")
            self.tests_passed += 1
        elif success is False:
            print(f"[FAIL] {message}")
        else:
            print(f"[INFO] {message}")
        if success is not None:
            self.tests_run += 1
    
    def test_signup(self):
        """Test user signup"""
        print("\n" + "="*60)
        print("TEST 1: User Signup")
        print("="*60)
        
        user_data = {
            "firstName": "Test",
            "lastName": "User",
            "email": f"test_{datetime.now().timestamp()}@example.com",
            "institution": "Test University",
            "department": "Computer Science",
            "password": "testpass123",
            "newsletter": False
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/auth/signup",
                json=user_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                self.log(f"Signup successful - Token: {self.auth_token[:20]}...", True)
                return True
            else:
                self.log(f"Signup failed - Status: {response.status_code}", False)
                return False
        except Exception as e:
            self.log(f"Signup error: {str(e)}", False)
            return False
    
    def test_options(self):
        """Test options endpoint"""
        print("\n" + "="*60)
        print("TEST 2: Get Options (No Auth Required)")
        print("="*60)
        
        try:
            response = requests.get(f"{self.api_url}/options", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log("Options endpoint accessible", True)
                
                # Check required fields
                if 'blooms_taxonomy' in data and len(data['blooms_taxonomy']) > 0:
                    self.log(f"Bloom's Taxonomy levels: {len(data['blooms_taxonomy'])}", True)
                else:
                    self.log("Bloom's Taxonomy missing", False)
                
                if 'aqf_levels' in data and len(data['aqf_levels']) > 0:
                    self.log(f"AQF levels: {len(data['aqf_levels'])}", True)
                else:
                    self.log("AQF levels missing", False)
                
                if 'lesson_durations' in data and len(data['lesson_durations']) > 0:
                    self.log(f"Lesson durations: {len(data['lesson_durations'])}", True)
                else:
                    self.log("Lesson durations missing", False)
                
                return True
            else:
                self.log(f"Options failed - Status: {response.status_code}", False)
                return False
        except Exception as e:
            self.log(f"Options error: {str(e)}", False)
            return False
    
    def test_lesson_plan_generation(self):
        """Test lesson plan generation with Google GenAI SDK"""
        print("\n" + "="*60)
        print("TEST 3: Generate Lesson Plan (Google GenAI SDK)")
        print("="*60)
        
        if not self.auth_token:
            self.log("No auth token - skipping", False)
            return False
        
        lesson_data = {
            "subject_name": "Computer Science",
            "lecture_topic": "Introduction to Python Programming",
            "focus_topic": "Variables and Data Types",
            "blooms_taxonomy": "Understand",
            "aqf_level": "AQF Level 7 - Bachelor Degree",
            "lesson_duration": "1 hour"
        }
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        try:
            print("Sending request to Google GenAI SDK...")
            response = requests.post(
                f"{self.api_url}/generate-lesson-plan",
                json=lesson_data,
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log("Lesson plan generated successfully!", True)
                
                if 'content' in data and len(data['content']) > 0:
                    content_preview = data['content'][:200]
                    print(f"\nGenerated Content Preview:")
                    print("-" * 60)
                    print(content_preview + "...")
                    print("-" * 60)
                    self.log(f"Content length: {len(data['content'])} characters", True)
                    return True
                else:
                    self.log("No content in response", False)
                    return False
            else:
                self.log(f"Generation failed - Status: {response.status_code}", False)
                try:
                    error = response.json()
                    print(f"Error detail: {error.get('detail', 'Unknown')}")
                except:
                    print(f"Response: {response.text[:200]}")
                return False
        except requests.exceptions.Timeout:
            self.log("Request timed out (LLM might be slow)", False)
            return False
        except Exception as e:
            self.log(f"Generation error: {str(e)}", False)
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("GOOGLE GENAI SDK - LOCAL SERVER TEST")
        print("="*60)
        print(f"Testing: {self.base_url}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run tests
        self.test_options()
        
        if self.test_signup():
            self.test_lesson_plan_generation()
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Tests Passed: {self.tests_passed}/{self.tests_run}")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\nAll tests passed! Google GenAI SDK is working correctly!")
            return 0
        else:
            print(f"\n{self.tests_run - self.tests_passed} test(s) failed.")
            return 1

if __name__ == "__main__":
    tester = LocalServerTest()
    exit_code = tester.run_all_tests()
    exit(exit_code)

