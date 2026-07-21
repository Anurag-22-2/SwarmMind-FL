from autourgos_openaichat import OpenAIChatModel

llm = OpenAIChatModel(
    model="google/gemma-4-e2b",        # use whatever model name LM Studio shows
    api_key="lm-studio",        # any string — ignored locally
    base_url="http://localhost:1234/v1",
)

while True:
    query = input("Enter your query: ")
    reply = llm.invoke(query)
    print("Model reply:", reply)