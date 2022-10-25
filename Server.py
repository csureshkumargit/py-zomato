
from flask import Flask,Response,request
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)

### Connecting to Mongo DB ###
try:
    mongo = pymongo.MongoClient(host="localhost", port=27017)
    db = mongo.py_Zomato_DB
    mongo.server_info()
    print("Connection Succeeded")
except Exception as ex:
    print("Exception", ex)
###############################

### Router ###
@app.route('/',methods=['GET'])
def getWelcomeMessage() :
    return "Welcome to Zomato-Python DB Services"
##############

### Router Get Locations #######
@app.route('/location',methods=['GET'])
def getLocations() :
    dbResponse=list(db.location.find());
    for location in dbResponse :
        location["_id"]=str(location["_id"])
    return Response(
        response=json.dumps(dbResponse),
        status=200,
        mimetype="application/json"
    )
################################

### Router Get Meal Types #######
@app.route('/mealtype',methods=['GET'])
def getMealTypes() :
    dbResponse=list(db.mealtype.find());
    for mealtype in dbResponse :
        mealtype["_id"]=str(mealtype["_id"])
    return Response(
        response=json.dumps(dbResponse),
        status=200,
        mimetype="application/json"
    )
################################

### Router Get Restaurants #######
@app.route('/restaurant',methods=['GET'])
def getRestaurant() :
    dbResponse=list(db.restaurant.find());
    for restaurant in dbResponse :
        restaurant["_id"]=str(restaurant["_id"])
    return Response(
        response=json.dumps(dbResponse),
        status=200,
        mimetype="application/json"
    )
################################

### Router Get Restaurant By Location #######
@app.route('/restaurant/location/<locId>',methods=['GET'])
def getRestaurantByLocation(locId) :
    dbResponse=list(db.restaurant.find({"location_id":int(locId)}));
    for location in dbResponse :
        location["_id"]=str(location["_id"])
    return Response(
        response=json.dumps(dbResponse),
        status=200,
        mimetype="application/json"
    )
################################

### Router for User Sign up #######
@app.route('/user/signup',methods=['POST'])
def addUser() :
    contentType=request.headers.get('content-type')
    if contentType=="application/json" :
       dbUserCheck=db.users.find_one({"email":request.json["email"]})
       if(dbUserCheck) :
             return Response(
            response=json.dumps({"message":"Email already exist"}),
            status=200,
            mimetype="application/json"
                )
       dbResponse=db.users.insert_one(request.json)
       return Response(
        response=json.dumps({"message":"User Added Successfully"}),
        status=200,
        mimetype="application/json"
    )
################################

### Router for Delete User #######
@app.route('/user',methods=["DELETE"])
def deleteUser() :
       email=request.args.get('email');
       print(type(email))
       dbResponse = db.users.delete_one({"email":email});
       if dbResponse :
           return Response(
           response=json.dumps({"message":"User Deleted Successfully"}),
           status=200,
           mimetype="application/json"
           )
################################

### Router for Delete User #######
@app.route('/user',methods=["PATCH"])
def updateUser() :
       email=request.args.get('email');
       userName=request.args.get('username');
       print(type(email))
       dbResponse = db.users.update_one({"email":email},{'$set':{"username":userName}})
       if dbResponse :
           return Response(
           response=json.dumps({"message":"User Updated Successfully"}),
           status=200,
           mimetype="application/json"
           )
################################

### Service Listener ###
if __name__ == "__main__":
    app.run(host="localhost", port=8090, debug=True)
#########################