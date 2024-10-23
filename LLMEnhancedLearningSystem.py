from dotenv import load_dotenv
import google.generativeai as genai
import os
from typing import List, Dict, Any
import numpy as np
import ast
class LLMEnhancedLearningSystem:
    def __init__(self):
        load_dotenv()
        google_api_key=os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=google_api_key)
        
        self.content_library: Dict[str, Dict[str, Any]] = {}
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
       
    
    def add_content(self, content_id: str, title: str, description: str, skills: List[str]):
        self.content_library[content_id] = {
            "title": title,
            "description": description,
            "skills": skills
        }
        
    
    def add_user(self, user_id: str, goals: str, background: str):
        self.user_profiles[user_id] = {
            "goals": goals,
            "background": background,
            "skills": {}
        }
        
    
    def generate_learning_path(self, user_id: str, num_items: int = 5) -> List[Dict[str, Any]]:
        user_profile = self.user_profiles[user_id]
        prompt = f"""
        User Goals: {user_profile['goals']}
        User Background: {user_profile['background']}

        Based on the user's goals and background, generate a personalized learning path 
        with {num_items} items. For each item, provide the content ID, a brief explanation 
        of why it's recommended, and how it relates to the user's goals.

        Available Content:
        {self._format_content_for_prompt()}

        Format the response as a Python list of dictionaries, each containing 
        'content_id', 'explanation', and 'relevance_to_goals'.
        """
        model = genai.GenerativeModel("gemini-1.5-flash",system_instruction="You are an AI assistant that generates personalized learning paths.")
        response = model.generate_content(prompt)
        
        raw_text=response.text
        learning_path_str = raw_text.replace("```python", "").replace("```", "").strip()
    
        learning_path = ast.literal_eval(learning_path_str)

        return learning_path
        

    def recommend_content(self, user_id: str, num_recommendations: int = 3) -> List[Dict[str, Any]]:
        user_profile = self.user_profiles[user_id]
        prompt = f"""
        User Goals: {user_profile['goals']}
        User Background: {user_profile['background']}
        User Skills: {user_profile['skills']}

        Based on the user's profile, recommend {num_recommendations} pieces of content. 
        For each recommendation, provide the content ID, a brief explanation of why it's 
        recommended, and how it aligns with the user's current skills and goals.

        Available Content:
        {self._format_content_for_prompt()}

        Format the response as a Python list of dictionaries, each containing 
        'content_id', 'explanation', and 'skill_alignment'.
        """
    
        model = genai.GenerativeModel("gemini-1.5-flash",system_instruction="You are an AI assistant that provides personalized content recommendations.")
        response = model.generate_content(prompt)
        raw_text=response.text
        recommend_content_str = raw_text.replace("```python", "").replace("```", "").strip()
    
        recommend = ast.literal_eval(recommend_content_str)

       

        return recommend

    def assess_skills(self, user_id: str, content_id: str, user_response: str) -> Dict[str, Any]:
        content = self.content_library[content_id]
        prompt = f"""
        Content Title: {content['title']}
        Content Description: {content['description']}
        Related Skills: {', '.join(content['skills'])}

        User Response: {user_response}

        Based on the user's response, assess their understanding of the content and 
        the related skills. Provide a skill assessment for each related skill, 
        including a score from 0 to 1, and brief feedback on areas of strength 
        and areas for improvement.

        Format the response as a Python dictionary with keys for each skill, 
        where the values are dictionaries containing 'score' and 'feedback'.
        """

        
        model = genai.GenerativeModel("gemini-1.5-flash",system_instruction="You are an AI assistant that assesses user skills based on their responses.")
        response = model.generate_content(prompt)

        raw_text=response.text
        recommend_content_str = raw_text.replace("```python", "").replace("```", "").strip()

        assessment = ast.literal_eval(recommend_content_str)
        
        # Update user's skills in their profile
        for skill, data in assessment.items():
            if skill in self.user_profiles[user_id]['skills']:
                # If skill exists, update with a weighted average
                current_score = self.user_profiles[user_id]['skills'][skill]
                new_score = (current_score + data['score']) / 2
            else:
                new_score = data['score']
            self.user_profiles[user_id]['skills'][skill] = new_score

        return assessment

    def _format_content_for_prompt(self) -> str:
        return "\n".join([f"ID: {cid}, Title: {data['title']}, Skills: {', '.join(data['skills'])}" 
                          for cid, data in self.content_library.items()])
        
    
    
    
    
if __name__ == "__main__":
    learning_system = LLMEnhancedLearningSystem()

    # Add some sample content
    learning_system.add_content("PROG101", "Introduction to Programming", 
                                "Learn the basics of programming including variables, loops, and functions.", 
                                ["programming", "problem-solving"])
    learning_system.add_content("DS101", "Data Science Fundamentals", 
                                "Introduction to data analysis, statistics, and machine learning concepts.", 
                                ["data-analysis", "statistics", "machine-learning"])
    learning_system.add_content("AI101", "Artificial Intelligence Basics", 
                                "Overview of AI concepts, machine learning algorithms, and neural networks.", 
                                ["artificial-intelligence", "machine-learning"])

    # Add a user
    learning_system.add_user("user123", 
                             "Become proficient in AI and machine learning", 
                             "Beginner programmer with basic Python knowledge")

    # Generate a learning path
    learning_path = learning_system.generate_learning_path("user123", 3)
    print("Generated Learning Path:")
    for idx, item in enumerate(learning_path, 1):
        print(f"Item {idx}:")
        print(f"  Content ID       : {item['content_id']}")
        print(f"  Explanation      : {item['explanation']}")
        print(f"  Relevance to Goals: {item['relevance_to_goals']}")
        print()
        
        
    recommendations = learning_system.recommend_content("user123", 2)
    
    print("Content Recommendations:")
    for rec in recommendations:
        print(f"Content ID: {rec['content_id']}")
        print(f"Explanation: {rec['explanation']}")
        print(f"Skill Alignment: {rec['skill_alignment']}\n")
        
        
    # Assess user skills
    user_response = "I understand how to create variables and use loops in Python, but I'm still confused about functions."
    assessment = learning_system.assess_skills("user123", "PROG101", user_response)
    print("Skill Assessment:")
    print(assessment)
    # for skill, data in assessment.items():
    #     print(f"Skill: {skill}")
    #     print(f"Score: {data['score']}")
    #     print(f"Feedback: {data['feedback']}\n")
