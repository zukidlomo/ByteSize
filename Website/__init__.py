from flask import Flask
from .recommendation_system import LLMEnhancedRecommendationSystem


recommender = LLMEnhancedRecommendationSystem()
def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']= "HELLO"
    
    from .routesName import routesPages

    app.register_blueprint(routesPages)

    return app