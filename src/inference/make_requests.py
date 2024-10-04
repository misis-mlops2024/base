import requests 
import random
from time import sleep
from loguru import logger


for _ in range(100):
    json = {
        "feat1": random.random(),
        "feat2": random.random(),
        "feat3": random.random(),
        "feat4": random.random(),
    }
    random_input = [[random.random() for _ in range(4)]]
    features = [f"feat{i+1}" for i in range(4)]
    
    response = requests.get("http://localhost:8000/predict/", 
                            json={"data": random_input, "features": features})
    logger.info(response.json())
    sleep(1)