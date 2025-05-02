import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from google.adk import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


class StructuredOutput(BaseModel):
    city: str = Field(description="City where the event is taking place")
    date: str = Field(description="Date of the event")
    speakers: list[str] = Field(description="List of speakers at the event")
    event: str = Field(description="Name of the event")
    description: str = Field(description="Description of the event")


# 1. Load environment variables from the agent directory's .env file
load_dotenv()
google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
google_cloud_location = os.getenv("GOOGLE_CLOUD_LOCATION")
google_genai_use_vertexai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "1")
model_name = os.getenv("MODEL")

# 2. Define Your Agent
root_agent = Agent(
    model=model_name,
    name="Image_Description_Agent",
    instruction="You are an expert image description agent. You provide detailed descriptions of images.",
    # When you define an output schema, you cannot use tools or agent transfers.
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=StructuredOutput,
)

# 3. Create Session and Artifact Services and a Session
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()
session = session_service.create_session(app_name="ImageAgentApp", user_id="user1")

# 4. Create a Runner
runner = Runner(
    agent=root_agent,
    artifact_service=artifact_service,
    session_service=session_service,
    app_name="ImageAgentApp",
)


def load_image(image_path: str) -> bytes:
    """
    Load an image from a file and return its bytes.
    """
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    return image_bytes


if __name__ == "__main__":

    query = "Describe this image in detail."
    image_bytes = load_image("platformengnyc.png")
    
    # 5. Create a content object with the query and image bytes
    content = types.Content(
        role="user",
        parts=[
            types.Part(text=query),
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        ],
    )

    # 6. Run the query
    events = runner.run(session_id=session.id, user_id="user1", new_message=content)

    # 7. Process each response event, printing only the final response
    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print(final_response)
