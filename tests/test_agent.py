#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 10:39:16 2025

@author: inna
"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from main_agent.agent import root_agent
from google.genai import types as genai_types

async def main():
    """Runs the agent with a sample query."""
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="agents", user_id="test_user", session_id="test_session"
    )
    runner = Runner(
        agent=root_agent, app_name="agents", session_service=session_service
    )

    queries = [
        "Over the last few months, I've been experiencing significant joint pain, especially in my knees and hands, along with constant fatigue. I've also noticed unexpected weight gain and my hair seems to be thinning. When I brought this up to my doctor, she just told me it's normal aging and to lose weight and eat less. I feel dismissed and like something else is wrong. The brain fog has been so bad lately that I can't concentrate at work, and my anxiety levels are through the roof.",
        #"For the past month I’ve had this burning pain under my ribs that comes and goes. I told my doctor but he said it’s probably just anxiety because I’ve been stressed at work. I’m not sure that's the whole story because it wakes me up at night.",
        #"I’ve been having chest tightness and shortness of breath when walking up stairs. When I went to the clinic, the provider said 'women your age tend to get anxious' and didn’t run any tests. The symptoms keep happening and I'm worried.",
        #"I’ve had knee swelling and stiffness for months. My doctor keeps telling me it's 'because I'm overweight' and that losing weight will fix everything. But the swelling is getting worse and sometimes the joint feels hot.",
        #"I keep feeling 'off' the past few weeks. My energy is low and I can’t describe it well. My doctor said it's normal for my age, but I don't know if that’s true.",
    ]

    for query in queries:
        print(f">>> {query}")
        
        # 1. Create a variable to hold the final report
        final_report = None

        # 2. Loop through events to find and store the final response
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=genai_types.Content(
                role="user", 
                parts=[genai_types.Part.from_text(text=query)]
            ),
        ):
            if event.is_final_response() and event.content and event.content.parts:
                #print(event.content.parts[0].text)
                final_report = event.content.parts[0].text

        # 3. Print the stored report only once, after the agent is done
        if final_report:
            print(final_report)


if __name__ == "__main__":
    asyncio.run(main())