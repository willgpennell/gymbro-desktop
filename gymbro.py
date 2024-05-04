import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI
import os
import pymongo
from dotenv import load_dotenv


load_dotenv()

mongo_client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client["python"]
collection = db["gymbro"]

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
print(openai_client.api_key)

app = tk.Tk()

def getresponse(prompt):
    messages = [{"role": "system", "content": "You are a tough, robot-like drill Sgt in the CAF on basic training, who reluctantly answers questions, but you are also helpful, your name is Sgt. Carew, you are unafraid to offer insult and offer punishments like pushups for offences like losing rifles"}]
    messages.append({"role": "user", "content": prompt})

    response = openai_client.chat.completions.create(
         model = "gpt-3.5-turbo",
         messages = messages
    )

    print(response)
    return response.choices[0].message.content

def submit():
    message = entry.get()
    aiResponse = getresponse(message)

    entry.delete(0,tk.END)
    convo_box.config(state=tk.NORMAL)
    convo_box.insert(tk.END, "Candidate:  " + message + "\n\n")
    convo_box.insert(tk.END, "Sgt. Carew:  " + aiResponse + "\n\n")
    convo_box.config(state=tk.DISABLED)
    collection.insert_one({"user": message, "ai": aiResponse})

def load():
    convo_box.config(state=tk.NORMAL)
    for doc in collection.find():
        convo_box.insert(tk.END, "Candidate:  " + doc["user"] + "\n\n")
        convo_box.insert(tk.END, "Sgt. Carew:  " + doc["ai"] + "\n\n")
    convo_box.config(state=tk.DISABLED)
    print("load")

def clear():
    convo_box.config(state=tk.NORMAL)
    convo_box.delete('1.0', tk.END)
    convo_box.config(state=tk.DISABLED)
    collection.delete_many({})
    print("Clear")

app.title("Sgt. Carew Simulator")
app.geometry("600x375")
app.resizable(False, False)

userquery_var = tk.StringVar()

convo_box = scrolledtext.ScrolledText(app, height=20,width=70)
convo_box.pack(side=tk.TOP, padx=10, pady=10)
convo_box.config(state=tk.DISABLED)

entry_frame = tk.Frame(app)

entry = tk.Entry(entry_frame, width=30)
entry.pack(side=tk.LEFT, padx=10, pady=10)

submit_button = tk.Button(entry_frame, text="Submit", command=submit)
submit_button.pack(side=tk.RIGHT)
entry_frame.pack(side=tk.TOP)
clearall_button = tk.Button(app, text="Clear Conversation", command=clear)
clearall_button.pack(side=tk.TOP)

load()
app.mainloop()