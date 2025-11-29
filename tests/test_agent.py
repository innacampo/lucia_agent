#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 10:39:16 2025

@author: inna
"""
import asyncio
import uuid
from dotenv import load_dotenv
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from main_agent.agent import root_agent
from google.genai import types as genai_types
import warnings
warnings.filterwarnings("ignore")


async def main():
    session_id = str(uuid.uuid4())
    """Runs the agent with a sample query."""
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="agents", user_id="test_user", session_id=session_id
    )
    print (session_id)
    runner = Runner(
        agent=root_agent, app_name="agents", session_service=session_service
    )
    
    queries = [
        #"Over the last few months, I've been experiencing significant joint pain, especially in my knees and hands, along with constant fatigue. I've also noticed unexpected weight gain and my hair seems to be thinning. When I brought this up to my doctor, she just told me it's normal aging and to lose weight and eat less. I feel dismissed and like something else is wrong. The brain fog has been so bad lately that I can't concentrate at work, and my anxiety levels are through the roof.",
        "I've been waking up with stiff, swollen joints in my hands and feet for three months. The fatigue is so bad I have to nap in my car at lunch. I saw a new doctor today. I tried to show him the swelling, but he barely looked. He told me that at 48, this is just classic perimenopause and 'empty nest syndrome' making me depressed. He didn't order any blood work. He just told me to lose 10 pounds and try meditation to calm my 'nerves' because women get so anxious at this stage of life.",    
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
            session_id=session_id,
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
