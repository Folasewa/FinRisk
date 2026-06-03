import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def analyze_credit_risk(data):
    """
    Agent 2: Uses Claude to assess credit risk. 
    Combines internal policy from Agent 0 and live data from Agent 1
    Returns structured credit score and analysis
    """
    print(f"Analyzing credit risk for {data['company_name']}")

    system_prompt = """
    You are a senior credit risk analyst at a major investment bank.
    You assess the financial health and creditworthiness of companies.

    You must respond ONLY with a JSON object in this exact format,
    no extra text, no markdown, no backticks — raw JSON only:

    {
        "credit_score": <integer 0 to 100, where 100 is safest>,
        "rating": <one of: "AAA", "AA", "A", "BBB", "BB", "B", "CCC", "D">,
        "key_strengths": [<2-3 short strings>],
        "key_risks": [<2-3 short strings>],
        "revenue_trend": <one of: "growing", "stable", "declining", "unknown">,
        "analyst_summary": <2-3 sentence professional summary>
    }
    """
    user_message = f"""
    Analyze the following company: {data['company_name']}

    --Internal Credit Policy from our knowledge base --
    {data['internal_context']['credit_policy']}

    --Internal regulatory reference --
    {data['internal_context']['regulatory_policy']}

    -- Live financial information --
    {data['financial_info']}

    -- Recent News --
    {data['news_info']}

    Use the internal policy to ensure your assessment meets our
    institutional standards. Return your credit risk assessment as JSON.
    """
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    raw_text = response.content[0].text
    clean_text = raw_text.strip().strip("```json").strip("```").strip() #stripping any accidental markdown formatting that claude might add
    credit_analysis = json.loads(clean_text)
    print(f"Score: {credit_analysis['credit_score']}/100 | Rating: {credit_analysis['rating']}")
    data["credit_analysis"] = credit_analysis
    return data