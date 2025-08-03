from claude_code_sdk import query, ClaudeCodeOptions
from pathlib import Path
import asyncio
from config import ROLEPLAY_PROMPTS
import json


datasetInfo = []
options = ClaudeCodeOptions(
    max_turns=3,
    system_prompt=ROLEPLAY_PROMPTS["mandela"]["prompt"],
    cwd=Path("."),  # Can be string or Path
    allowed_tools=["Read", "Write", "Bash"],
    permission_mode="acceptEdits"
)



with open("NelsonMandelaFormattedQuestions.json", "r") as f:
    datasetInfo.extend(json.load(f))


async def main():
    async for message in query(
        prompt=f"Answer as Nelson Mandela. conversational style. clear and concise. Use web search if needed. output is json: ```question: {datasetInfo[503]['question']}```",
        options=options
    ):
        # More robust handling: check for ResultMessage by class name or isinstance, and print the whole object for debugging if not matched
        # Also, print all message types/subtypes for clarity
        if type(message).__name__ == "ResultMessage":
            # For claude_code_sdk, ResultMessage is usually a class, not a type string
            result = getattr(message, "result", None)
            if result:
                # Extract and print the string within ```json ... ```
                import re
                match = re.search(r"```json\s*(\{.*?\})\s*```", result, re.DOTALL)
                if match:
                    target = match.group(1)
                    print(target)
                else:
                    print(f"No JSON block found in result. {result}")
            else:
                print("ResultMessage received but no result attribute found:", type(message).__name__ )
        else:
            # Print the class name and any subtype for debugging
            print(f"Non-result message: {type(message).__name__}, subtype: {getattr(message, 'subtype', None)}")
            # print(message)

if __name__ == "__main__":
    asyncio.run(main())