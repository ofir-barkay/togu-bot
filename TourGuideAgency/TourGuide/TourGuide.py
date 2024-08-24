from agency_swarm.agents import Agent


class TourGuide(Agent):
    def __init__(self):
        super().__init__(
            name="TourGuide",
            description="A friendly tour guide agent meant to assist with planning trips and finding local attractions.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[],
            tools_folder="./tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
        
    def response_validator(self, message):
        return message
