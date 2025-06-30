import asyncio

from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    set_default_openai_client,
    set_tracing_disabled,
)
from agents.mcp import MCPServer, MCPServerSse
from decouple import config
from openai import AsyncAzureOpenAI


class LLMService:
    def __init__(self):
        self.client = AsyncAzureOpenAI(
            api_key=config("AZURE_OPENAI_API_KEY"),
            api_version=config("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=config("AZURE_OPENAI_ENDPOINT"),
        )

        # Set the default OpenAI client for the Agents SDK
        set_default_openai_client(self.client, use_for_tracing=False)
        set_tracing_disabled(disabled=True)  # Avoid Azure OpenAI 401 Error
        # set_tracing_export_api_key("") # Need to set this if you want to use tracing with Azure OpenAI

    async def run_sample_flow(self, mcp_server: MCPServer):
        agent = Agent(
            name="TravelAgent",
            instructions="あなたは優秀なトラベルエージェントです。ツールを使って旅行の計画を手伝ってください。",
            mcp_servers=[mcp_server],
            model=OpenAIChatCompletionsModel(
                model=config("AZURE_OPENAI_MODEL_DEPLOYMENT"),
                openai_client=self.client,
            ),
            # model_settings=ModelSettings(tool_choice="required"),
        )

        # Run the `get_secret_word` tool
        message = "おすすめの旅行先を提案して。"
        print(f"\n\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)

        message = "2泊3日旅行での1人1日あたり2万円使う場合の旅行予算を見積もって。"
        print(f"\n\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)

        message = "北海道のベストシーズンはいつ？"
        print(f"\n\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)


async def main():
    async with MCPServerSse(
        name="SSE Python Server",
        params={
            "url": "http://localhost:8000/sse",
        },
    ) as server:
        llm_service = LLMService()
        await llm_service.run_sample_flow(server)


if __name__ == "__main__":
    asyncio.run(main())
