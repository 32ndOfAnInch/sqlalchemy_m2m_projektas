from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import Base, Type, Category

# creating db and declaring session
engine = create_engine('sqlite:///home_accounting.db', echo=True)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()


# filling type datatable
type = []
type.append(Type(id=1, operation_type="earnings"))
type.append(Type(id=2, operation_type="expenses"))
session.add_all(type)

# filling category datatable
category = []
category.append(Category(id=1, operation_category="salary", type_id=1))
category.append(Category(id=2, operation_category="small gig", type_id=1))
category.append(Category(id=3, operation_category="gift", type_id=1))
category.append(Category(id=4, operation_category="other", type_id=1))
category.append(Category(id=5, operation_category="municipal taxes", type_id=2))
category.append(Category(id=6, operation_category="food", type_id=2))
category.append(Category(id=7, operation_category="fuel", type_id=2))
category.append(Category(id=8, operation_category="clothing", type_id=2))
category.append(Category(id=9, operation_category="entertainment", type_id=2))
category.append(Category(id=10, operation_category="other", type_id=2))
session.add_all(category)

session.commit()