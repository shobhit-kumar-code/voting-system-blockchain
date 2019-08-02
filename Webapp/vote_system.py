import pymongo
class Voting:
    uid,fname,lname,age,address,photo,criminal_records=('',)*7
    def __init__(self):
        self.uid="XXXX"
        self.fname="default"
        self.lname="default"
        self.age=21
        self.address="default"
        self.photo="pic.jpg"
        self.criminal_records="default"
    #perform validation on the front end itself and carry on.
    def register_candidate(self,uid,fname,lname,age,address,photo,criminal_records): #additional details are needed for this operation.
        self.uid,self.fname,self.lname,self.age=uid,fname,lname,age
        self.register_db()
        #make call to blockchain registercandidate function
    def register_voter(self,uid,fname,lname,age):
        self.uid,self.fname,self.lname,self.age=uid,fname,lname,age
        #make call to blockchain registervoter function
    def cast_vote(self,uid,fname,lname,vote_uid):
        #make call to blockchain cast_vote function with true for vote variable
        pass
    def register_db(self):
        import pdb; pdb.set_trace()
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["codefundo"]
        mycol=mydb['cand_reg']
        mycol.insert_one({"UID":self.uid,"First Name":self.fname,"Last Name":self.lname,"Age":self.age,"Address":self.address,
                        "Photo":self.photo,"Criminal":self.criminal_records})
