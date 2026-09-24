from tools import search_web, calculator, get_definitions


def choose_tool(question):

    question_lower = question.lower()

    if any(word in question_lower for word in [
        "calculate", "math", "expression"
    ]):
        return "calculator", question

    elif any(word in question_lower for word in [
        "define", "definition", "meaning"
    ]):
        return "get_definitions", question

    else:
        return "search_web", question


def extract_term(question):

    question_lower = question.lower()

    if "rag" in question_lower:
        return "rag"

    elif "agentic ai" in question_lower:
        return "agentic ai"

    elif "transformer" in question_lower:
        return "transformer"

    return question


def research_agent(question):

    print("\nQuestion:", question)

    # 1. Decide which tool to use
    tool, argument = choose_tool(question)

    print("Agent's decision:", tool)

    # 2. Prepare the correct argument
    if tool == "get_definitions":
        argument = extract_term(question)

    # 3. Select the tool
    if tool == "search_web":
        tool_function = search_web

    elif tool == "calculator":
        tool_function = calculator

    elif tool == "get_definitions":
        tool_function = get_definitions

    else:
        return "No suitable tool found."

    print("Tool argument:", argument)

    # 4. Execute the tool
    result = tool_function(argument)

    # 5. Observe result
    print("\nObservation:")
    print(result)

    return result


def main():

    question = input("\nEnter your question: ")

    result = research_agent(question)

    print("\nFinal answer:")
    print(result)


if __name__ == "__main__":
    main()