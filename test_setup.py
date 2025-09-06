#!/usr/bin/env python3
"""
Test script to verify the AI agent setup.
"""

import sys
from pathlib import Path
from datetime import date

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def test_agent():
    """Test tennis agent functionality."""
    print("\n🤖 Testing tennis agent...")

    from agent.agent import AIAgent

    try:
        # Create agent with dummy API key for testing
        agent = AIAgent("dummy-key")
        print("✅ AI agent created successfully")

        # Test request parsing
        test_message = "I want to eat dinner in Rome."
        request = agent._parse_user_request(test_message)

        if request.target_date:
            print(f"✅ Request parsing works: {request.target_date}")

        return True
    except Exception as e:
        print(f"❌ Agent error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing AI Agent Setup\n")

    tests = [
        test_agent
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The setup is working correctly.")
        print("\nTo run the application:")
        print("1. Create a .env file with your OPENAI_API_KEY")
        print("2. Run: python run.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
