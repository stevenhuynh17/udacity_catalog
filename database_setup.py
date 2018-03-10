import os
import sys
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


engine = create_engine('sqlite:///data.db')

Base.metadata.create_all(engine)

print "Database setup complete!"
