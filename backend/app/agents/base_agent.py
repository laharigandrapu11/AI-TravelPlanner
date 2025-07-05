import logging
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv

load_dotenv()

class BaseAgent(ABC):
    """Base class for all agents in the SmartTripPlanner system"""
    
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")
        self.logger.setLevel(logging.INFO)
        
        # Add console handler if not already present
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    @abstractmethod
    def process(self, data):
        """Main processing method that each agent must implement"""
        pass
    
    def log_info(self, message):
        """Log info message"""
        self.logger.info(f"[{self.name}] {message}")
    
    def log_error(self, message):
        """Log error message"""
        self.logger.error(f"[{self.name}] {message}")
    
    def log_warning(self, message):
        """Log warning message"""
        self.logger.warning(f"[{self.name}] {message}")
    
    def validate_input(self, data, required_fields):
        """Validate input data has required fields"""
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        return True 