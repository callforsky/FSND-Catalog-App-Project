from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Items, Base

engine = create_engine('sqlite:///shoecatalog4.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# load shoe categories into the category table
shoe_category_1 = Category(name= "Training")
session.add(shoe_category_1)
session.commit()

shoe_detail_1 = Items(category = shoe_category_1, 
					  name = "Air Jordan 12 Retro", 
					  description = "The return of Tinker Hatfield's " 
					  "celebrated 1996 design - the first debut of Zoom Air")

session.add(shoe_detail_1)
session.commit()

shoe_detail_2 = Items(category = shoe_category_1, 
					  name = "Reebok CrossFit Nano 7", 
					  description = "NanoWeave tech upper for " 
					  "breathability and comfort")

session.add(shoe_detail_2)
session.commit()

shoe_category_2 = Category(name= "Fashion")
session.add(shoe_category_2)
session.commit()

shoe_detail_3 = Items(category = shoe_category_2, 
					  name = "Booties", 
					  description = "Mink-Trim Suedue 100mm Bootie, Blue"
					  )

session.add(shoe_detail_3)
session.commit()

shoe_detail_4 = Items(category = shoe_category_2, 
					  name = "Loafer", 
					  description = "Polly Kiltie Leather 55mm Loafer"
					  )

session.add(shoe_detail_4)
session.commit()


shoe_category_3 = Category(name= "Kids")
session.add(shoe_category_3)
session.commit()

shoe_detail_5 = Items(category = shoe_category_3, 
					  name = "Gap Kids Solid Slip-On", 
					  description = "Cross-dyed cotton twill upper" 
					  )

session.add(shoe_detail_5)
session.commit()

shoe_detail_6 = Items(category = shoe_category_3, 
					  name = "Warm-lined Boots", 
					  description = "Anke boots in faux suede with a " 
					  "glittery bow at side")

session.add(shoe_detail_6)
session.commit()


print "Catalog initiated!"