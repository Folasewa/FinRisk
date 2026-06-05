import os
import json
import anthropic
from dotenv import load_dotenv
from datetime import date

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def write_report(data):
    """
    Agent 4: Synthesizes all findings into a professional analyst report
    """
    print(f"Writing final report for {data['company_name']}")
    
    system_prompt = """
    You are a financial analyst writing institutional-grade risk reports. 
    Write clearly, professionally, concisely. Use markdown formatting. 
    Structure your report with clear sections and a risk summary table. 
    """
    #Serialize the structured data as JSON strings  using json.dumps

    user_message = f"""
    Write a full financial risk report for {data['company_name']}
    Date: {date.today().strftime("%B %d, %Y")}

    --Credit Analysis--
    {json_block(data['credit_analysis'])}

    --Compliance Screening--
    {json_block(data['compliance_check'])}

    The report must include:
    1. Executive Summary (3-4 sentences)
    2. Credit Risk Assessment (use credit score and rating)
    3. Compliance and Regulatory Review (use compliance findings)
    4. Key risks and mitigants
    5. Overall recommendation (Approve / Conditional Approve / Decline)

    Make the report exactly like something a bank's credit committee would review
    """

    response = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=2000, system=system_prompt, messages = [{"role": "user", "content": user_message}])
    report_markdown = response.content[0].text

    print(f"Report written. ({len(report_markdown)} characters)")
    data["final_report"] = report_markdown
    
    return data

def json_block(obj):
    return json.dumps(obj, indent=2)