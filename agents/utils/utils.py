from langchain.chains.llm import LLMChain, PromptTemplate
from langchain_openai import ChatOpenAI
import json
import os
from langchain_core.messages import HumanMessage,AIMessage
from agents.utils.models import CaseStudyModel
from langchain.output_parsers import PydanticOutputParser

# Define the prompt template that accepts conversation history as a list of message


def generate_scenario(topic,topic_data):
    # Define the prompt template for the interviewer agent
    interviewer_prompt = """

        {topic_data}
        
        Do not provide any clues or hints to help them answer.
        Do not add preamble. Just give the case study aka scenario. 
        It should be short, like 4-5 sentences. It would be concise and compact.
        Do not provide any additional information or context beyond what is presented in the case study.
        After presenting the scenario, generate {number_of_questions} follow-up questions that will encourage the user to deeply analyze the scenario. 
        Keep the questions tightly focused on the topic and the scenario.

        Generate a detailed scenario based on the following topic, then generate {number_of_questions} questions based on scenario to evaluate examinee knowledge:
        Topic: {topic}

        you will reply in json with keys : scenario and questions

        While generating scenario please keep in mind be user a part of  the scenario and make it as real as possible. 
        """
    
    parser = PydanticOutputParser(pydantic_object=CaseStudyModel)
    # Create the prompt template object
    prompt = PromptTemplate(input_variables=["topic","topic_data","number_of_questions"], template=interviewer_prompt)

    # Load the LLM (can use any model you are using in LangChain, for example OpenAI)
    llm = ChatOpenAI(temperature=0.9)

    number_of_questions = os.environ.get('question_count',10) 
    # Create the chain that uses the LLM and the prompt
    # interviewer_chain = LLMChain(llm=llm, prompt=prompt)

    interviewer_chain = LLMChain(llm=llm, prompt=prompt, output_parser=parser)

    # Run the chain and generate the case study
    case_study_output = interviewer_chain.run(topic=topic, topic_data=topic_data,number_of_questions=number_of_questions)

    
    return case_study_output






