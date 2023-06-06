import openai

OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

def get_summary():
    system = """与えられた日本語をを英語で何というか教えてください．"""

    text = f"私はコンピュータビジョン分野の研究者です．"
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': text}
                ],
                temperature=0.25,
            )
    summary = response['choices'][0]['message']['content']

    return summary

print(get_summary())
