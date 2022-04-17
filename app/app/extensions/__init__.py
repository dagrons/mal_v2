from flask_mongoengine import MongoEngine
from .neo4j import Neo

mongo = MongoEngine()
neo = Neo()
