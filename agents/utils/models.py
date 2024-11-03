# Define Pydantic model for the output
from pydantic import BaseModel, ValidationError,Field
from typing import List,Optional
# Pydantic Model for Scenario and Questions
class CaseStudyModel(BaseModel):
    scenario: str = Field(description="A short case study based on a specific topic.")
    questions: list[str] = Field(description="A list follow-up questions related to the scenario.")


# class Answer(BaseModel):
#     """
#     Represents the user's response to a question, allowing for detailed categorization.
#     """
#     response_text: Optional[str] = Field(
#         description="The actual response text provided by the user. This can be empty if the user skipped the question."
#     )
#     response_type: Literal['answer', 'uncertainty', 'skip'] = Field(
#         description="Type of response given by the user. Can be 'answer' for direct answers, "
#                     "'uncertainty' for responses like 'I don’t know', or 'skip' for requests to skip the question."
#     )

# class QuestionAnswerPairs(BaseModel):
#     """
#     This model represents a list of questions tagged with respective answers provided by the user.
#     It includes cases where the user expresses uncertainty or requests to skip a question.
#     """
#     questions: List[str] = Field(
#         description="A list of questions asked in the examination."
#     )
#     answers: List[Answer] = Field(
#         description="A list of Answer objects corresponding to each question, containing "
#                     "the user's response text and response type. Includes responses indicating "
#                     "uncertainty or requests to skip."
#     )



class QuestionAnswerPairs(BaseModel):
    """
    This model represents a list of questions with respective answers provided by the user in a conversation setting.
    Each question is tagged with an answer that may represent a direct response, an expression of uncertainty, or a request to skip.

    **Model Fields:**

    - `questions`: A list of all questions asked during the interview or examination. Each question should correspond to an answer in the `answers` list, maintaining the same order.
    
    - `answers`: A list of responses provided by the user, where each response may fall into one of the following types:
        - **Direct Answer**: The user provides a specific answer to the question.
        - **Uncertainty**: The user expresses uncertainty or lack of knowledge (e.g., "I don’t know," "Not sure").
        - **Skip Request**: The user requests to move to the next question (e.g., "Next question, please," "Can we skip this one?").
      
      This list should align with the `questions` list in length and order, ensuring that each answer directly addresses the corresponding question.
    
    **Instructions for Usage**:
    
    1. **Extracting Responses**:
       - Each element in `answers` should reflect the user’s most relevant response to the corresponding question in `questions`.
       - Capture responses as they directly address the question, ignoring unrelated remarks.
    
    2. **Handling Uncertainty**:
       - If the user expresses uncertainty (e.g., “I don’t know”), include this verbatim as the response.
       - Set such responses explicitly, even if brief, to indicate the user's uncertainty.

    3. **Handling Skips**:
       - If the user requests to skip a question, include the exact phrase they used to skip (e.g., "Next question, please").
       - Avoid leaving empty fields; if a question is skipped, represent it clearly with the user’s wording.

    **Format Example**:

    ```json
    {
        "questions": [
            "What is your favorite color?",
            "Can you describe your work experience?",
            "Do you know how to code?",
            "Any additional comments?"
        ],
        "answers": [
            "Blue",
            "I have over 5 years of experience in marketing.",
            "I don’t know",
            "Next question, please"
        ]
    }
    ```

    **Notes**:
    - Ensure the lists `questions` and `answers` are aligned by index.
    - Responses should be concise and directly relevant to the questions, including any uncertainty or skip requests as explicit text.
    """

    questions: List[str] = Field(
        description="A list of questions asked during the interview or examination. "
                    "Each question corresponds to a user response in the 'answers' list."
    )
    
    answers: List[str] = Field(
        description="A list of responses to each question, maintaining alignment with the 'questions' list. "
                    "Responses can include direct answers, expressions of uncertainty (e.g., 'I don’t know'), "
                    "or skip requests (e.g., 'Next question, please'). Each response should reflect the user's "
                    "most relevant statement addressing the question."
    )


class EvaluationResult(BaseModel):
    """
    Represents the evaluation of a single question-answer pair in an examination or interview setting.

    **Fields**:
    - `question` (str): The original question posed to the user. This should match exactly with the question text
      provided in the conversation log.
    - `answer` (str): The user’s response to the question. This should be a concise representation of the answer, 
      as extracted directly from the user’s responses, capturing any expressions of uncertainty or requests to skip.
    - `score` (int): A numerical score from 0 to 10 assessing the quality of the response. The scoring criteria 
      are as follows:
        - 0-3: Incomplete or incorrect response, lacking accuracy, coherence, or relevance.
        - 4-6: Partially correct response with some relevant information but lacking coherence or completeness.
        - 7-8: Mostly correct response that is coherent and relevant but may lack some detail or depth.
        - 9-10: Fully correct and comprehensive response, demonstrating accuracy, clarity, and depth.
    - `feedback` (str): A brief explanation supporting the score. This should include specific observations regarding 
      correctness, coherence, and completeness of the response, identifying both strengths and weaknesses.
    - `suggestions` (Optional[str]): Optional field providing constructive suggestions for improvement.
      This may include tips on enhancing response accuracy, coherence, or completeness.

    **Example**:
    ```json
    {
        "question": "What is your favorite programming language?",
        "answer": "Python",
        "score": 10,
        "feedback": "The user provided a clear and relevant response that directly answered the question.",
        "suggestions": null
    }
    """
    question: str = Field(description="The question posed to the user.")
    answer: str = Field(description="The user's response to the question.")
    score: int = Field(description="Score (0-10) evaluating the answer's correctness, coherence, and completeness.")
    feedback: str = Field(description="Brief feedback describing the reasoning behind the score.")
    suggestions: Optional[str] = Field(
        None, 
        description="Optional suggestions for improvement based on the answer given."
    )

class EvaluationOutput(BaseModel):
    """
    The structured output containing evaluations for each question-answer pair.

    **Fields**:
    - `evaluations` (List[EvaluationResult]): A list of `EvaluationResult` objects, each corresponding to a 
      question-answer pair in the examination. Each entry provides a structured evaluation of the response,
      including the question text, user answer, score, feedback, and any improvement suggestions.
      
    **Usage Notes**:
    - Ensure that each `EvaluationResult` in `evaluations` aligns with a unique question-answer pair. Maintain
      the order of questions and answers as provided in the conversation log.
    - Use the scoring rubric provided in `EvaluationResult` for consistency in evaluation.
    - If a response lacks detail or accuracy, provide specific feedback in `feedback` and actionable suggestions in `suggestions`.

    **Example**:
    ```json
    {
        "evaluations": [
            {
                "question": "What is your favorite programming language?",
                "answer": "Python",
                "score": 10,
                "feedback": "The user provided a clear and relevant response that directly answered the question.",
                "suggestions": null
            },
            {
                "question": "What is your experience with machine learning?",
                "answer": "I have about 2 years of experience.",
                "score": 8,
                "feedback": "Good response, though additional details on specific projects would enhance completeness.",
                "suggestions": "Consider mentioning specific machine learning projects or techniques you have worked with."
            }
        ]
    }
    """
    evaluations: List[EvaluationResult] = Field(
        description="A list of evaluation results for each question-answer pair."
    )