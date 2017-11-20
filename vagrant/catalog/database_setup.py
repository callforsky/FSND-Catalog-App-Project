from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

# declarative_base() callable returns a new base class from which all mapped 
# classes should inherit. It takes a pre-configured class of database from 
# sqlalchemy, saving time of setting up the database manually
# The declarative_base() base class contains a MetaData object where newly 
# defined Table objects are collected.
Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase+string.digits) for x in xrange(32))

# going to create 3 tables, one is the category, another is the items under 
# each category. Last one is the user info table 
# Below we create the metadata for these 2 tables

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String(32), index=True)

# create the category table
class Category(Base):
	__tablename__ = 'category'

	# define the header of each column
	# id colum is used to connect with other tables
	id = Column(Integer, primary_key=True)
	# the name of the categories
	name = Column(String(250), nullable=False)

	@property
	def serialize(self):
		return {
			'name'		: self.name,
			'id'		: self.id,
		}
	

# create the items table
class Items(Base):
	__tablename__ = 'items'

	# define the header of each column
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(250), nullable=False)
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)


	# a good tutorial on property(): https://goo.gl/uQzyjq
	# a good tutorial on decorator: https://goo.gl/RjzoXp
	@property
	def serialize(self):
		''' return object data in easily serializeable format'''
		return {
			'id'         : self.id,
			'name'         : self.name,
			'description'         : self.description,
		}

# produces an Engine object based on a URL. SQLite connects to file-based 
# databases, using the Python built-in module sqlite3 by default. As SQLite 
# connects to local files, the URL format is slightly different. The 'file' 
# portion of the URL is the filename of the database. For a relative file path, 
# this requires three slashes:
engine = create_engine('sqlite:///shoecatalog.db')

# we have defined some Table objects and their metadata above, now it is the 
# time to create the database with the metadata we set earlier
Base.metadata.create_all(engine)