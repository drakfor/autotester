from pathlib import Path
import ollama
import logging


from autotester.format import GeneratedTests


logger = logging.getLogger(__name__)


system_prompt = """
You are a software testing assistant.
Generate comprehensive unit tests.
Always include edge cases.
Don't write any comments.
Don't forget to add values for testing functions.
Fill the formal args like in the header file.
Write test names without spaces.
If you generate array, it must be array, not string type.
"""


def get_tests(testing_file: Path) -> GeneratedTests:
    # ollama.create(
    #     model='test-generator',
    #     from_='qwen2.5-coder:14b',
    #     system=system_prompt
    # )

    test_case: str

    logger.info("Reading test file: %s", testing_file.name)
    with open(testing_file, "r") as file:
        test_case = file.read()

    logger.info("Waiting response...")
    response = ollama.chat(
        model='test-generator',
        messages=[
            {
                'role': 'user',
                'content': test_case
            }
        ],
        format=GeneratedTests.model_json_schema(),
        options={
            'temperature': 0
        }
    )

    logger.info("Get tests file")
    tests = GeneratedTests.model_validate_json(
        response.message.content
    )

    return tests