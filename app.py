#!/usr/bin/env python3

import os
import configparser
from typing import List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sources.llm_provider import Provider
from sources.interaction import Interaction
from sources.agents import CasualAgent, CoderAgent, FileAgent, PlannerAgent, BrowserAgent
from sources.browser import Browser, create_driver
from sources.utility import pretty_print
from sources.logger import Logger
from sources.schemas import QueryRequest, QueryResponse

config = configparser.ConfigParser()
config.read('config.ini')
app = FastAPI(title="AgenticSeek API", version="0.1.0")
logger = Logger("backend.log")

app.mount("/screenshots", StaticFiles(directory=".screenshots"), name="screenshots")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def initialize_system():
    stealth_mode = config.getboolean('BROWSER', 'stealth_mode')
    personality_folder = "jarvis" if config.getboolean('MAIN', 'jarvis_personality') else "base"
    languages = config["MAIN"]["languages"].split(' ')

    provider = Provider(
        provider_name=config["MAIN"]["provider_name"],
        model=config["MAIN"]["provider_model"],
        server_address=config["MAIN"]["provider_server_address"],
        is_local=config.getboolean('MAIN', 'is_local')
    )
    logger.info(f"Provider initialized: {provider.provider_name} ({provider.model})")

    browser = Browser(
        create_driver(headless=config.getboolean('BROWSER', 'headless_browser'), stealth_mode=stealth_mode),
        anticaptcha_manual_install=stealth_mode
    )
    logger.info("Browser initialized")

    agents = [
        CasualAgent(
            name=config["MAIN"]["agent_name"],
            prompt_path=f"prompts/{personality_folder}/casual_agent.txt",
            provider=provider, verbose=False
        ),
        CoderAgent(
            name="coder",
            prompt_path=f"prompts/{personality_folder}/coder_agent.txt",
            provider=provider, verbose=False
        ),
        FileAgent(
            name="File Agent",
            prompt_path=f"prompts/{personality_folder}/file_agent.txt",
            provider=provider, verbose=False
        ),
        BrowserAgent(
            name="Browser",
            prompt_path=f"prompts/{personality_folder}/browser_agent.txt",
            provider=provider, verbose=False, browser=browser
        ),
        PlannerAgent(
            name="Planner",
            prompt_path=f"prompts/{personality_folder}/planner_agent.txt",
            provider=provider, verbose=False, browser=browser
        )
    ]
    logger.info("Agents initialized")

    interaction = Interaction(
        agents,
        tts_enabled=config.getboolean('MAIN', 'speak'),
        stt_enabled=config.getboolean('MAIN', 'listen'),
        recover_last_session=config.getboolean('MAIN', 'recover_last_session'),
        langs=languages
    )
    logger.info("Interaction initialized")
    return interaction

interaction = initialize_system()
is_generating = False

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/screenshot")
async def get_screenshot():
    logger.info("Screenshot endpoint called")
    if os.path.exists(".screenshots"):
        screenshot = interaction.current_agent.browser.get_screenshot()
        return JSONResponse(
            status_code=200,
            content={"screenshot": screenshot}
        )
    else:
        logger.error("No browser agent available for screenshot")
        return JSONResponse(
            status_code=400,
            content={"error": "No browser agent available"}
        )

@app.get("/is_active")
async def is_active():
    logger.info("Is active endpoint called")
    return {"is_active": interaction.is_active}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    global is_generating
    logger.info(f"Processing query: {request.query}")
    query_resp = QueryResponse(
        done="false",
        answer="Waiting for agent...",
        agent_name="Waiting for agent...",
        success="false",
        blocks={}
    )
    if is_generating:
        logger.warning("Another query is being processed, please wait.")
        return JSONResponse(
            status_code=429,
            content=query_resp.jsonify()
        )
    try:
        interaction.tts_enabled = request.tts_enabled
        interaction.stt_enabled = request.stt_enabled
        interaction.last_query = request.query
        logger.info("Agents request is being processed")
        is_generating = True
        success = interaction.think()
        is_generating = False
        if not success:
            query_resp.answer = "Error: No answer from agent"
            return JSONResponse(
                status_code=400,
                content=query_resp.jsonify()
            )
        if interaction.current_agent:
            blocks_json = {f'{i}': block.jsonify() for i, block in enumerate(interaction.current_agent.get_blocks_result())}
        else:
            logger.error("No current agent found")
            blocks_json = {}
            return JSONResponse(
                status_code=400,
                content=query_resp.jsonify()
            )
        logger.info(f"Answer: {interaction.last_answer}")
        logger.info(f"Blocks: {blocks_json}")
        query_resp.done = "true"
        query_resp.answer = interaction.last_answer
        query_resp.agent_name = interaction.current_agent.agent_name
        query_resp.success = str(success)
        query_resp.blocks = blocks_json
        logger.info("Query processed successfully")
        return JSONResponse(
            status_code=200,
            content=query_resp.jsonify()
        )
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        if config.getboolean('MAIN', 'save_session'):
            interaction.save_session()
        raise e
    finally:
        logger.info("Processing finished")
        if config.getboolean('MAIN', 'save_session'):
            interaction.save_session()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)