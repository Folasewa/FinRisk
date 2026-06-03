from rag.knowledge_base import build_index, query_knowledge_base

def retrieve_internal_context(data):
    """
    Agent 0: Queries the internal knowledge database before any web search
    """
    print(f"Retrieving internal knowledge about {data['company_name']}...")

    build_index() #builds index on the first run

    credit_context = query_knowledge_base(f"credit risk assessement standards corporate lending", n_results = 2)
    aml_context = query_knowledge_base(f"AML KYC due diligence screening requirements", n_results = 2)
    regulatory_context = query_knowledge_base(f"Basel III capital requirements stress testing leverage ratio", n_results = 2)

    data["internal_context"] = {"credit_policy": credit_context, "aml_policy": aml_context, "regulatory_policy": regulatory_context}

    print("Internal context retrieved")
    return data

