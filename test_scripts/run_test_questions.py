import sys
import os
import json

# Make sure we can import from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from rag_pipeline import query_rag

def run_tests():
    test_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_questions.json"))
    with open(test_file_path, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)

    passed = 0
    failed = 0

    for test in test_cases:
        test_id = test.get("id", "N/A")
        question = test["question"]
        expected_contains = test.get("expected_answer_contains", [])
        expected_not_contains = test.get("expected_answer_not_contains", [])

        print(f"\n🔍 Running Test: {test_id}")
        print(f"Q: {question}")

        answer = query_rag(question)

        print(f"🧠 Answer: {answer}")

        success = True

        for term in expected_contains:
            if term.lower() not in answer.lower():
                print(f"❌ Missing expected term: '{term}'")
                success = False

        for term in expected_not_contains:
            if term.lower() in answer.lower():
                print(f"❌ Found forbidden term: '{term}'")
                success = False

        if success:
            print(f"✅ Test {test_id} passed.")
            passed += 1
        else:
            print(f"❌ Test {test_id} failed.")
            failed += 1

    print("\n📊 Test Summary:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"🧪 Total: {passed + failed}")

if __name__ == "__main__":
    run_tests()