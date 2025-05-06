import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


def get_queries():
    """
    Retrieves the list of all queries based.

    Returns:
        list[(str, str)]: A list of tuples containing the query id and query description.
    """
    try:
        # Get the list of all queries
        queries = [
            ("1", "Describe this image in detail."),
            ("2", "What is the main subject of this image?"),
            ("3", "List the colors present in this image."),
            ("4", "What emotions does this image convey?"),
            ("5", "Identify any objects or people in this image."),
            ("6", "What is the setting of this image?"),
            ("7", "Describe the lighting in this image."),
            ("8", "What is the mood of this image?"),
            ("9", "What story does this image tell?"),
            ("10", "What is the significance of this image?"),
            ("11", "What is the historical context of this image?"),
            ("12", "What techniques were used to create this image?"),
            ("13", "What is the intended audience for this image?"),
            ("14", "What is the message of this image?"),
            ("15", "How does this image relate to current events?"),
            ("16", "What is the cultural significance of this image?"),
            ("17", "What is the artistic style of this image?"),
            ("18", "What is the purpose of this image?"),
            ("19", "What is the composition of this image?"),
            ("20", "What is the perspective of this image?"),
        ]

        return queries
    except Exception as e:
        return {"status": "error", "error_message": f"Error retrieving queries: {e}"}


# 1. Load environment variables from the agent directory's .env file
load_dotenv()
google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
google_cloud_location = os.getenv("GOOGLE_CLOUD_LOCATION")
google_genai_use_vertexai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "1")
model_name = os.getenv("MODEL")

# 2. Define Your Agent
root_agent = Agent(
    model=model_name,
    name="Query_Description_Agent",
    instruction="You are an expert query agent. Get the list of all queries, analyze returned queries and return most relevant based on the user's interests. Output in JSON format with original queries ids and descriptions.",
    tools=[get_queries],
)

# 3. Create Session and Artifact Services and a Session
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()
session = session_service.create_session(app_name="QueryAgentApp", user_id="user1")

# 4. Create a Runner
runner = Runner(
    agent=root_agent,
    artifact_service=artifact_service,
    session_service=session_service,
    app_name="QueryAgentApp",
)


if __name__ == "__main__":

    # query = "I'm interested in emotions and mood."
    query = "I'm interested in the artistic style"

    # 5. Create a content object with the query and image bytes
    content = types.Content(
        role="user",
        parts=[
            types.Part(text=query),
        ],
    )

    # 6. Run the query
    events = runner.run(session_id=session.id, user_id="user1", new_message=content)

    # 7. Process each response event, printing only the final response
    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print(final_response)
