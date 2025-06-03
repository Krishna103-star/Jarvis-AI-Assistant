from openai import OpenAI

client = OpenAI(
    api_key="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",
)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant Jarvis."},
        {
            "role": "user",
            "content": "What is coding?"
        }
    ]
)

print(completion.choices[0].message.content)


# pip install openai