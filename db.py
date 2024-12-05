from peewee import *
from peewee import Expression # the building block for expressions
#import bcrypt
import os
import datetime as dt
import uuid

DB_PATH=os.path.dirname(__file__)
print(f"DB location at:-> {DB_PATH}")
master_db=SqliteDatabase(DB_PATH+'/Master.db')




class Student(Model):
    name = CharField()
    semester = IntegerField(constraints=[Check('semester >= 0'), Check('semester <= 7')])
    faculty=CharField(constraints = [Check("faculty IN ('BE.COMP', 'BE.CIVIL', 'BE.ARCH')")])
    fp_template=CharField(null=True) 
    vend_month=IntegerField(default=0,constraints=[Check('vend_month >= 0'), Check('vend_month <= 11')])
    vend_amount=IntegerField(default=0)

    class Meta:
        database = master_db # This model uses the "people.db" database.


class VendingMachine(Model):
    name= CharField(null=False)
    api_key=CharField(null=False)
    capacity=IntegerField(default=0)
    def gen_api_key():
        return str(uuid.uuid4())
    class Meta:
        database = master_db # This model uses the "people.db" database.

def start():
    if(not os.path.isfile(DB_PATH+"/Master.db")):
        master_db.create_tables([Student,VendingMachine])

start()
if __name__=="__main__":    
    a=Student.create(id=119579,name="Saloni Rauniyar",fp_template="saloni.bin",semester=2,faculty="BE.COMP")
   # b=VendingMachine.create(name="ran",api_key= VendingMachine.gen_api_key())
    print(a)
    pass


