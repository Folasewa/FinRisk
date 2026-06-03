import os
import json
import anthropic
from dotenv import load_dotenv
load_dotenv

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def check_compliance(data):
    """
    Agent 3: Uses Claude to perform KYC/AML compliance screening. 
    References the internal AML policy from Agent 0 alongside the live web data
    """
    print(f"Running kyc/aml compliance screening for {data['company_name']}")

    system_prompt = """
    You are a senior compliance officer specializing in AML, KYC, and sanctions screening at a financial institution.
    Respond ONLY with a JSON object in this format, no extra text, no markdown, no backticks — raw JSON only:

    {
    "sanctions_risk": <one of: "none", "low", "medium", "high">,
        "aml_risk": <one of: "none", "low", "medium", "high">,
        "pep_exposure": <true or false>,
        "regulatory_flags": [<list of specific concerns, or empty list>],
        "jurisdiction_risk": <one of: "low", "medium", "high">,
        "overall_compliance_rating": <one of: "PASS", "REVIEW", "FAIL">,
        "compliance_notes": <2-3 sentence summary of findings>
    }
    """

    user_message = f"""
    Company under compliance screening review: {data['company_name']}

    --Internal AML/KYC Policy from our knowledge base --
    {data['internal_context']['aml_policy']}

    --Leadership and Ownership from the web--
    {data['leadership_info']}

    -- Recent News (Check for legal or regulatory issues) --
    {data['news_info']}

    --Credit analyst notes --
    {data['credit_analysis']['analyst_summary']}

    Apply our internal AML policy to screen this company.
    Return your compliance findings as JSON.

    """
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    raw_text = response.content[0].text
    clean_text = raw_text.strip().strip("```json").strip("```").strip()
    compliance_check = json.loads(clean_text)

    print(f"Compliance rating: {compliance_check['overall_compliance_rating']}")
    data['compliance_check'] = compliance_check
    return data
