from dotenv import load_dotenv
import google.generativeai as genai
import os
from typing import List, Dict, Any
import ast

class LLMEnhancedQuizPlatform:
    def __init__(self):
        load_dotenv()
        google_api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=google_api_key)
        
        self.quizzes: Dict[str, Dict[str, Any]] = {}
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
    
    def create_quiz(self, quiz_id: str, topic: str, difficulty: str, num_questions: int) -> Dict[str, Any]:
        prompt = f"""
        Create a quiz on the topic of {topic} with {num_questions} questions.
        The difficulty level should be {difficulty}.
        For each question, provide:
        1. The question text
        2. Four multiple-choice options (A, B, C, D)
        3. The correct answer (A, B, C, or D)
        4. A brief explanation of the correct answer

        Format the response as a Python list of dictionaries, each containing
        'question', 'options', 'correct_answer', and 'explanation'.
        """
        
        
        
        model = genai.GenerativeModel("gemini-1.5-pro", system_instruction="""
You are a teacher creating mathematical and logical quiz questions. Your task:
1. Summarize the key concepts that the quiz should test.
2. Identify the problem type (e.g., arithmetic, logic, geometry).
3. Formulate a clear, concise quiz question.
4. Provide an answer key with an explanation for each step.

Ensure simplicity, clarity, and correctness in both the question and the explanation. Each task should be done in the given order and separately.
""")
        response = model.generate_content(prompt)
        
        raw_text = response.text
        quiz_content = ast.literal_eval(raw_text.replace("```python", "").replace("```", "").strip())
        
        self.quizzes[quiz_id] = {
            "topic": topic,
            "difficulty": difficulty,
            "questions": quiz_content
        }
        
        return self.quizzes[quiz_id]
    
    def take_quiz(self, user_id: str, quiz_id: str, user_answers: List[str]) -> Dict[str, Any]:
        quiz = self.quizzes[quiz_id]
        score = 0
        feedback = []
        
        for i, (question, answer) in enumerate(zip(quiz['questions'], user_answers)):
            is_correct = answer.upper() == question['correct_answer']
            score += 1 if is_correct else 0
            feedback.append({
                'question_number': i + 1,
                'is_correct': is_correct,
                'correct_answer': question['correct_answer'],
                'explanation': question['explanation']
            })
        
        result = {
            'user_id': user_id,
            'quiz_id': quiz_id,
            'score': score,
            'total_questions': len(quiz['questions']),
            'feedback': feedback
        }
        
        self._update_user_profile(user_id, quiz_id, result)
        
        return result
    
    def _update_user_profile(self, user_id: str, quiz_id: str, result: Dict[str, Any]):
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {'quiz_history': []}
        
        self.user_profiles[user_id]['quiz_history'].append({
            'quiz_id': quiz_id,
            'score': result['score'],
            'total_questions': result['total_questions']
        })
    
    def get_personalized_feedback(self, user_id: str, quiz_id: str) -> str:
        user_profile = self.user_profiles.get(user_id, {})
        quiz_result = next((q for q in user_profile.get('quiz_history', []) if q['quiz_id'] == quiz_id), None)
        
        if not quiz_result:
            return "No quiz result found for this user and quiz combination."
        
        quiz = self.quizzes[quiz_id]
        
        prompt = f"""
        Quiz Topic: {quiz['topic']}
        Quiz Difficulty: {quiz['difficulty']}
        User's Score: {quiz_result['score']} out of {quiz_result['total_questions']}
        
        Based on the user's performance, provide personalized feedback and suggestions for improvement.
        Include:
        1. An overall assessment of their performance
        2. Specific areas where they excelled
        3. Areas that need improvement
        4. Recommended next steps or topics to study
        """
        
        model = genai.GenerativeModel("gemini-1.5-pro", system_instruction="You are an AI assistant that provides personalized educational feedback.")
        response = model.generate_content(prompt)
        
        return response.text
    
    def recommend_next_quiz(self, user_id: str) -> str:
        user_profile = self.user_profiles.get(user_id, {})
        quiz_history = user_profile.get('quiz_history', [])
        
        if not quiz_history:
            return "No quiz history found. Please take a quiz first."
        
        prompt = f"""
        User's Quiz History:
        {quiz_history}
        
        Available Quizzes:
        {[{quiz_id: info['topic']} for quiz_id, info in self.quizzes.items()]}
        
        Based on the user's quiz history and available quizzes, recommend the next quiz they should take.
        Provide the quiz ID and a brief explanation for your recommendation.
        """
        
        model = genai.GenerativeModel("gemini-1.5-pro", system_instruction="You are an AI assistant that provides personalized quiz recommendations.")
        response = model.generate_content(prompt)
        
        return response.text

# Example usage
if __name__ == "__main__":
    quiz_platform = LLMEnhancedQuizPlatform()
    
    # Create a quiz
    new_quiz = quiz_platform.create_quiz("PYTHON101", "Python Basics", "Beginner", 5)
    print("New Quiz Created:", new_quiz)
    
    # # Simulate a user taking the quiz
    # user_answers = []
    
    # index = 0
    # while index <=5:
    #      answer = input("Enter your answer (A/B/C/D): ").upper()
    #      if answer in ["A", "B", "C", "D"]:
    #          user_answers.append(answer)
    #          index += 1
    #      else:
    #         print("Invalid answer. Please enter A, B, C, or D.")
    
    # quiz_result = quiz_platform.take_quiz("user123", "PYTHON101", user_answers)
    # print("Quiz Result:", quiz_result)
    
    # # Get personalized feedback
    # feedback = quiz_platform.get_personalized_feedback("user123", "PYTHON101")
    # print("Personalized Feedback:", feedback)
    
    # # Get recommendation for next quiz
    # next_quiz = quiz_platform.recommend_next_quiz("user123")
    # print("Next Quiz Recommendation:", next_quiz)