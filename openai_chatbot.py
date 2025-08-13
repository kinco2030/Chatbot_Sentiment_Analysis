import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API")
# print(OPENAI_API_KEY)

import pandas as pd
import openai
import time
import json

def ask_gpt(client, prompt):
    start = time.time()
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        end = time.time()

        content = response.choices[0].message.content
        prompt_tokens = response.usage.completion_tokens
        completion_tokens = response.usage.prompt_tokens
        total_tokens = response.usage.total_tokens

        return content, prompt_tokens, completion_tokens, total_tokens, end - start
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return None, 0, 0, 0, 0

def main():
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # 착한 프롬프트
    # with open("data/kind_prompt.json", "r", encoding="utf-8") as f:
    #     prompts = json.load(f)

    # 나쁜 프롬프트
    with open("data/bad_prompt.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)

    results = []

    for prompt in prompts:
        print(f"실행 중: {prompt['type']} - {prompt['text']}")
        answer, prompt_tokens, completion_tokens, total_tokens, duration = ask_gpt(client, prompt["text"])
        results.append({
            "type": prompt["type"],
            "text": prompt["text"],
            "answer": answer,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "duration": duration
        })
    
    df = pd.DataFrame(results)
    # df.to_excel("result/openai_chatbot_results.xlsx", index=False, engine='openpyxl')
    df.to_excel("result/openai_chatbot_bad_results.xlsx", index=False, engine='openpyxl')

if __name__ == "__main__":
    main()