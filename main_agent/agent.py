#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 14:21:28 2025
@author: inna campo
""" 

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent

def get_bias_implications(bias_type: str) -> str:
    """Looks up the clinical implications of a specific diagnostic bias."""
    bias_database = {
        "psychologizing_bias": "This can lead to delayed diagnosis for underlying physical conditions, as symptoms are incorrectly attributed to mental stress.",
        "gender_bias": "Often results in women's pain being taken less seriously or misdiagnosed, particularly in cardiovascular and autoimmune diseases.",
        "weight_bias": "The tendency to attribute a wide range of symptoms to a patient's weight without a full workup. This can cause clinicians to miss underlying metabolic, orthopedic, or endocrine disorders.",
        "ageism_bias": "Dismissing a patient's medical concerns as a normal or inevitable part of aging. This can prevent the timely diagnosis and treatment of serious conditions like heart disease, cancer, or neurological issues.",
        "confirmation_bias": "The tendency for a clinician to focus on evidence that supports their initial hypothesis while ignoring evidence that contradicts it. This can lead to a premature or incorrect diagnosis.",
        "racial_or_ethnic_bias": "Occurs when clinical judgments are influenced by stereotypes. This can lead to the undertreatment of pain and misdiagnosis of conditions that present differently across populations, such as dermatological or cardiac symptoms."
    }
    return bias_database.get(bias_type, "No specific information found for this bias type.")


# --- Worker Agent 1: Symptom Analysis ---
symptom_analyzer_instruction = """Act as a clinical NLP specialist.
You will receive a raw patient narrative.
Your sole task is to analyze it and output ONLY a single JSON object with a 'symptomMapping' key.

Example Input:
"I'm always tired and have a stabbing feeling in my side."

Example Output:
{
    "symptomMapping": {
        "fatigue_cluster": ["always tired"],
        "pain_cluster": ["stabbing feeling"]
    }
}"""

symptom_analyzer_agent = LlmAgent(
    model='gemini-2.5-flash-lite',
    name='symptom_analyzer_agent',
    description='Analyzes a patient narrative to extract and cluster symptoms.',
    instruction=symptom_analyzer_instruction,
    output_key="symptom_analysis" 
)
# --- Worker Agent 2: Bias Analysis ---
bias_analyzer_instruction = """Act as a bias-aware AI agent.
You will receive a raw patient narrative.
First, identify potential biases like 'gender_bias' or 'psychologizing_bias'.
Second, use the `get_bias_implications` tool to find the clinical implications of that bias.
Finally, output a single JSON object with a 'biasAwareness' key that includes both the bias and its implication.
"""

bias_analyzer_agent = LlmAgent(
    model='gemini-2.5-flash-lite',
    name='bias_analyzer_agent',
    tools=[get_bias_implications],
    description='Analyzes a patient narrative for potential diagnostic bias and dismissal.',
    instruction=bias_analyzer_instruction,
    output_key="bias_analysis"
)

# --- Worker Agent 3: Advocacy Generation ---
advocacy_generator_instruction = """Act as a patient advocate.
You will receive a context containing 'symptom_analysis' and 'bias_analysis' JSON objects.
Your task is to analyze these objects and generate a list of advocacy questions.
You must output ONLY a JSON object with a single 'structuredAdvocacy' key.

Example Input Context:
{
    "symptom_analysis": {
        "symptomMapping": { "fatigue_cluster": ["always tired"] }
    },
    "bias_analysis": {
        "biasAwareness": "The patient's fatigue was dismissed as 'stress'..."
    }
}

Example Final Output:
{
    "structuredAdvocacy": [
        "Since my fatigue has been persistent, what else could we explore besides stress?"
    ]
}"""

advocacy_generator_agent = LlmAgent(
    model='gemini-2.5-flash-lite',
    name='advocacy_generator_agent',
    description='Generates patient advocacy questions based on symptom and bias analysis.',
    instruction=advocacy_generator_instruction,
    output_key="advocacy_analysis",
)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file defines the main `root_agent` as a sequence.
"""
# --- Define the Orchestrator Steps ---

# STEP 1: Run symptom and bias analysis in parallel
parallel_analysis_step = ParallelAgent(
    name='parallel_analysis_step',
    sub_agents=[
        symptom_analyzer_agent,
        bias_analyzer_agent,
    ],
)

# --- Worker Agent 4: Final Report Formatting  ---
# This agent takes all previous outputs and formats them into a professional report.
professional_report_instruction = """Your sole job is to synthesize the clinical analysis from the previous steps into a professional, patient-facing report.
The context you receive will contain 'symptom_analysis', 'bias_analysis', and 'advocacy_analysis' objects.
You must extract the relevant data from these objects and output ONLY a single, well-formatted string. Follow this exact structure, replacing the bracketed placeholders with the corresponding data:

**Patient Advocacy & Consultation Aid**

**Disclaimer:** This report is generated to assist in patient-doctor communication and is not medical advice. Always consult a qualified healthcare professional for diagnosis and treatment.

**1. Summary of Reported Symptoms:**
[Insert the value of symptom_analysis['symptomMapping'] here]

**2. Communication & Bias Insights:**
[Insert the value of bias_analysis['biasAwareness'] here]

**3. Suggested Questions for Your Doctor:**
[Insert the value of advocacy_analysis['structuredAdvocacy'] here, formatted as bullet points]
"""
report_formatter_agent = LlmAgent(
    name="report_formatter_agent",
    model="gemini-2.5-flash-lite",
    instruction=professional_report_instruction,
)

# --- Define the Root Agent as a Single Sequence ---
# This runs all the steps in order, ending with the new formatting agent.
root_agent = SequentialAgent(
    name='root_agent',
    sub_agents=[
        parallel_analysis_step,
        advocacy_generator_agent,
        report_formatter_agent  
    ],
    description='A workflow that analyzes a patient narrative and generates a formatted text report.',
)
