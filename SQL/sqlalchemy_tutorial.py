from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationships, backref, relationship

Base = declarative_base()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    employees = relationship('Employee', secondary='department_employee')


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey('department.id'))
    # 建立引用关系--通过Department可以查到employees
    department = relationship(Department, backref=backref('employees', uselist=True))


from sqlalchemy import  create_engine
engine = create_engine('sqlite:///')

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

s = session()
john = Employee(name='john')
s.add(john)

it_department = Department(name='IT')
it_department.employees.append(john)
s.add(it_department)
s.commit()