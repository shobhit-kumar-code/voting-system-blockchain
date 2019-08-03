import pymongo
import re
class Voting:
    uid,fname,lname,age,address,photo,criminal_records=('',)*7
    def __init__(self):
        self.uid="XXXX"
        self.fname="default"
        self.lname="default"
        self.age=21
        self.address="default"
        self.photo="pic.jpg"
        
    #perform validation on the front end itself and carry on.
    def register_candidate(self,uid,fname,lname,age,address,photo,criminal_records): #additional details are needed for this operation.
        self.uid,self.fname,self.lname,self.age,self.address,self.photo,self.criminal_records=uid,fname,lname,age,address,photo,criminal_records
        return (self.validate("candidate") and self.register_db("candidate"))
        
        #make call to blockchain registercandidate function
    def validate(self,category):
        # import pdb; pdb.set_trace()
        if category=="candidate":
            if re.match(r'\b\d{12}\b',self.uid) and int(self.age)>=25 and self.address!="default" and self.fname!="default" and self.lname!="default" and self.photo!="pic.jpg":
                return True
            else:
                return False
        else:
            if re.match(r'\b\d{12}\b',self.uid) and int(self.age)>=18 and self.address!="default" and self.fname!="default" and self.lname!="default" and self.photo!="pic.jpg":
                return True
            else:
                return False
    def register_voter(self,uid,fname,lname,age,address,photo):
        self.uid,self.fname,self.lname,self.age,self.address,self.photo=uid,fname,lname,age,address,photo
        return (self.validate("voter") and self.register_db("voter"))
        #make call to blockchain registervoter function
    def cast_vote(self,uid,fname,lname,vote_uid):
        #make call to blockchain cast_vote function with true for vote variable
        pass
    def register_db(self,category):
        # import pdb; pdb.set_trace()
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["codefundo"]
        if category=="candidate":
            mycol=mydb['cand_reg']
            mycol.insert_one({"UID":self.uid,"First Name":self.fname,"Last Name":self.lname,"Age":self.age,"Address":self.address,
                        "Photo":self.photo,"Criminal":self.criminal_records})
        else:
            mycol=mydb['vote_reg']
            mycol.insert_one({"UID":self.uid,"First Name":self.fname,"Last Name":self.lname,"Age":self.age,"Address":self.address,
                        "Photo":self.photo})
        return True