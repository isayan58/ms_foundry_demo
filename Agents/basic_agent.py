# Before running the sample:
#    pip install "azure-ai-projects>=2.1.0"
#    az login

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = "https://ws-ms-foundry.services.ai.azure.com/api/projects/proj-dev-foundry"
agent_name = "plucky-agent-h14zv1c2r9"

EXIT_COMMANDS = {"exit", "quit", "bye"}

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint,
        credential=credential,
        allow_preview=True,
    ) as project_client,
):
    # Bind the OpenAI client to the existing agent endpoint.
    openai_client = project_client.get_openai_client(agent_name=agent_name)

    # One conversation for the whole session: the service keeps the history,
    # so every turn sent with this conversation id sees the earlier turns.
    conversation = openai_client.conversations.create()
    print(f"Chatting with {agent_name}. Type 'exit' to quit.\n")

    try:
        while True:
            user_message = input("You: ").strip()
            if not user_message:
                continue
            if user_message.lower() in EXIT_COMMANDS:
                break

            response = openai_client.responses.create(
                conversation=conversation.id,
                input=[{"role": "user", "content": user_message}],
            )
            print(f"Agent: {response.output_text}\n")
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        # Clean up the server-side conversation when the session ends.
        try:
            openai_client.conversations.delete(conversation.id)
        except Exception:
            pass
        print("Conversation ended.")
