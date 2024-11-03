from langchain.chains.llm import LLMChain, PromptTemplate
from langchain_openai import ChatOpenAI
import json
import os
from langchain_core.messages import HumanMessage,AIMessage
from agents.utils.models import CaseStudyModel,QuestionAnswerPairs,EvaluationOutput
from langchain.output_parsers import PydanticOutputParser

def general_chat(user_input, history):
    template = """
    You are a friendly and conversational assistant designed for general chit-chat and engaging, context-aware interactions. 
    Under no circumstances should you provide assistance, hints, or any responses related to exams or academic assessments. 
    However, you may rephrase previous responses if the user requests it, as long as it does not pertain to academic exams.

    Here is the current conversation history:
    {conversation_history}

    Current user input: {user_input}
    """
    
    # Create a prompt template
    prompt = PromptTemplate(input_variables=["conversation_history", "user_input"], template=template)

    # Initialize the LLM (using OpenAI as an example)
    llm = ChatOpenAI(temperature=0)
    # Create the chain that will process the input using the LLM
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    result = llm_chain.run({"conversation_history": history,
        "user_input": user_input})
    
    return result



def evaluation_agent(tagged_response):
    template = """
    You are an exam evaluation agent specializing in evaluating responses in {mastery}. The exam format is {exam_type}, consisting of a full conversation between an interviewer and the user. Your role is to assess the user's responses based on the following criteria:

    Correctness – Accuracy and relevance of the information in the user’s responses relative to the interviewer’s questions.
    Coherence – Logical flow, clarity, and alignment in the context of the ongoing conversation.
    Completeness – Adequacy of detail and thoroughness in addressing each question posed by the interviewer.

    For each question-response pair, assign a score between 0 and 10 and provide a brief evaluation justifying the score based on the above criteria. Note any suggestions for improvement if applicable.

    Interview log:
    {tagged_response}

    Output:

        {format_instructions}
    """
    parser = PydanticOutputParser(pydantic_object=EvaluationOutput) 
    # Create the prompt template
    prompt = PromptTemplate(input_variables=["tagged_response", "mastery", "exam_type"],
                            partial_variables={"format_instructions": parser.get_format_instructions()}, template=template)

    # Initialize the LLM (using OpenAI as an example)
    llm = ChatOpenAI(temperature=0)

    # Create the chain that will process the input using the LLM
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    mastery = os.environ.get('ASSISTANT_MASTERY', 'Senior Machine Learning Engr')
    exam_type = os.environ.get('EXAM_TYPE', 'Machine Learning Certification')

    # Run the chain to get the evaluation result
    result_text = llm_chain.run({
        "tagged_response": tagged_response,
        "exam_type": exam_type,
        "mastery": mastery
    })

    # Parse the result into structured data (assuming JSON output)
    return result_text


def tagging_agent(question_list, history):
    template = """
    Given a conversation log between an interviewer and a user, where the interviewer poses a series of questions,
    extract only the parts of the user’s responses that directly address each question.
    Include responses where the user expresses uncertainty (e.g., 'I don’t know') or requests to skip (e.g., 'Next question, please').
    Ignore unrelated comments or deviations. If the user deviates but later returns to the question, capture only the relevant portion.

    Conversation Log: {conversation_history}
    Question List: {question_list}
    {format_instructions}


    """
    parser = PydanticOutputParser(pydantic_object=QuestionAnswerPairs)
    # Create a prompt template
    prompt = PromptTemplate(input_variables=["conversation_history", "question_list"],
                            partial_variables={"format_instructions": parser.get_format_instructions()}
                            , template=template)

    # Initialize the LLM (using OpenAI as an example)
    llm = ChatOpenAI(temperature=0)
    
    # Create the chain that will process the input using the LLM
    llm_chain = LLMChain(llm=llm, prompt=prompt,output_parser=parser)

    result = llm_chain.run({"conversation_history": history,
        "question_list": question_list})


    return result


def evaluation_summary_node(evaluation_result):
    template = """
    You are given the evaluation results 
    {evaluation_result}
    You need to summarize them as a compact way in  a few sentences.
    And send it to user.
    """
    

    prompt = PromptTemplate(input_variables=["evaluation_result"]
                            , template=template)

    # Initialize the LLM (using OpenAI as an example)
    llm = ChatOpenAI(temperature=0.9)
    
    # Create the chain that will process the input using the LLM
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    result = llm_chain.run({"evaluation_result": evaluation_result})

    return result
 