from api import apikey
from flask import Flask, request, jsonify
import pandas as pd
from csv import writer

import os
import time
import bittensor as bt

import json
import jsonpickle

apikeys = apikey

app = Flask(__name__)

prompt = bt.BittensorLLM()
############## GPT PROMPT ####################
def bittensor(inp):
    systems = {"role":"system","content":"you're a crypto expert.guide the user about mining specially on TAO and Bittensor model."}
    new_inp = inp
    new_inp.insert(0,systems)
    ans = prompt(str(new_inp))
    return ans

############    GET CHATS BY USER ID ##################
def get_chats(id):
    path = str(os.getcwd())+'\\'+id+'.json'
    isexist = os.path.exists(path)
    if isexist:
        data = pd.read_json(id+".json")
        chats = data.chat
        return  list(chats)
    else:
        return "No Chat found on this User ID."





############### APPEND NEW CHAT TO USER ID JSON FILE #################
def write_chat(new_data, id):
    with open(id+".json",'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["chat"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)



################################ CHECK IF USER IS ALREADY EXIST IF NOT CREATE ONE ELSE RETURN GPT REPLY ##################
@app.route('/api', methods=['POST'])
def check_user():
    
    ids = request.json['user_id']
    prompt = request.json['prompt']
    print("asd")
    path = str(os.getcwd())+'\\'+ids+'.json'
    # path = str(os.getcwd())+'\\'+"5467484.json"
    isexist = os.path.exists(path)
    if isexist:
        # try:
        print(path," found!")
        write_chat({"role":"user","content":prompt},ids)
        chats = get_chats(ids)
        send = bittensor(chats)
        reply = send
        print("reply    ",reply)
        write_chat({"role":"assistant","content":reply},ids)
        return {"message":reply,"status":"OK"}
        # except:
        #     return {"message":"something went wrong!","status":"404"}

    else:
        print(path," Not found!")
        dictionary = {
        "user_id":ids,
        "chat":[]


        }
        
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
        
        # Writing to sample.json
        with open(ids+".json", "w") as outfile:
            outfile.write(json_object)
        reply = check_user()
        return reply

####################   NEW ENPOINT GET CHAT ##############################
@app.route('/get_chats', methods=['POST'])
def get_chatss():
    ids = request.json['user_id']
    return jsonpickle.encode(get_chats(ids))





if __name__ == '__main__':
    app.run()
    
