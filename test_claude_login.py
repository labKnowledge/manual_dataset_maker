#!/usr/bin/env python3
"""
Test script for Claude Login integration

Q: Why can os.getenv not find the CLAUDE_COOKIE even though it's in .env?
A: There are several common reasons:
   1. The .env file is not in the same directory as this script, or not in the current working directory when you run the script.
   2. The .env file is named incorrectly (should be exactly ".env").
   3. The .env file does not have the correct format (should be CLAUDE_COOKIE=your_cookie_value, no quotes, no spaces around the =).
   4. The environment variable is not being loaded before os.getenv is called.
   5. You are running the script in an environment (like some IDEs or notebooks) that does not automatically load .env files.
   6. There are invisible characters or line endings in your .env file.
   7. You are running the script with a different user or in a subprocess that does not inherit the environment.

Troubleshooting steps:
- Print the current working directory and check if .env is there.
- Print out os.environ to see if CLAUDE_COOKIE is present after load_dotenv().
- Try running `python -m dotenv.cli get CLAUDE_COOKIE` to see if dotenv can find it.
- Double-check the .env file for typos or formatting issues.

Example debug code:
    import os
    from dotenv import load_dotenv
    print("CWD:", os.getcwd())
    print(".env exists:", os.path.exists(".env"))
    load_dotenv()
    print("CLAUDE_COOKIE in env:", "CLAUDE_COOKIE" in os.environ)
    print("CLAUDE_COOKIE value:", os.getenv("CLAUDE_COOKIE"))

Below is the original test script:
"""

import os
from dotenv import load_dotenv
from claude_api import Client

load_dotenv()

def test_claude_login():
    """Test Claude login with cookie authentication"""
    
    
    cookie = os.getenv("CLAUDE_COOKIE")
    if not cookie:
        print("❌ CLAUDE_COOKIE not found in .env file")
        print("\nTo get your Claude cookie:")
        print("1. Go to https://claude.ai and login")
        print("2. Open browser developer tools (F12)")
        print("3. Go to Application/Storage tab")
        print("4. Find 'sessionKey' cookie")
        print("5. Copy its value to .env file as CLAUDE_COOKIE=your_cookie_value")
        print("\nDebug info:")
        print("CWD:", os.getcwd())
        print(".env exists:", os.path.exists(".env"))
        print("CLAUDE_COOKIE in env:", "CLAUDE_COOKIE" in os.environ)
        print("os.environ.get('CLAUDE_COOKIE'):", os.environ.get("CLAUDE_COOKIE"))
        return False
    
    try:
        client = Client(cookie)
        
        # Test basic functionality
        print("✅ Claude login successful!")
        
        # Test creating a conversation
        conversation_id = client.create_new_chat()
        print(f"✅ Created conversation: {conversation_id}")
        
        # Test sending a message
        response = client.send_message(
            prompt="Hello! Please respond with a simple greeting.",
            conversation_id=conversation_id,
            timeout=60
        )
        
        print("✅ Message sent successfully!")
        print(f"Response: {response[:100]}...")
        
        # Clean up
        client.delete_conversation(conversation_id)
        print("✅ Conversation cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Claude login failed: {e}")
        print("\nPossible issues:")
        print("1. Invalid or expired cookie")
        print("2. Network connectivity issues")
        print("3. Claude service temporarily unavailable")
        return False

def get_cookie_instructions():
    """Show instructions for getting Claude cookie"""
    print("\n📋 How to get your Claude cookie:")
    print("=" * 50)
    print("1. Go to https://claude.ai and login to your account")
    print("2. Open browser developer tools (F12)")
    print("3. Go to 'Application' tab (Chrome) or 'Storage' tab (Firefox)")
    print("4. In the left sidebar, expand 'Cookies'")
    print("5. Click on 'https://claude.ai'")
    print("6. Find the cookie named 'sessionKey'")
    print("7. Copy its value")
    print("8. Add to your .env file: CLAUDE_COOKIE=your_cookie_value")
    print("\n⚠️  Important:")
    print("- Keep your cookie secure and don't share it")
    print("- Cookies expire periodically, you may need to refresh them")
    print("- This method uses the web interface, so it's subject to rate limits")

if __name__ == "__main__":
    print("🧪 Testing Claude Login Integration...")
    print()
    
    # Test login
    success = test_claude_login()
    
    if not success:
        get_cookie_instructions()
    else:
        print("\n🎉 Claude login test passed! You're ready to use main_claude_login.py") 