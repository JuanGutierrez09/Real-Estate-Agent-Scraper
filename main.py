import requests 
import json
from bs4 import BeautifulSoup
import customtkinter

#access the list of realtors
URL = "https://devnetproject.netlify.app/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
table = soup.find("body")

#formats the realtor's info to json
body = table.find("script").text.replace(" ","").replace("name", '"name"').replace("phone", '"phone"').replace("specialization",'"speciaization"').replace("experience",'"experience"')[15:-331]
data= json.loads(body)


#instantiates fram class with all elements of the window
class myFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.entry = customtkinter.CTkEntry(self, placeholder_text = "search")
        self.button = customtkinter.CTkButton(self, text="Enter", command = self.buttonEvent)
        self.textbox = customtkinter.CTkTextbox(self, width=400,height=150, wrap="word")
        self.entry.pack(padx=20,pady=20)
        self.button.pack(side="top")
        self.textbox.pack(padx=20,pady=20)
        self.button = customtkinter.CTkButton(self, text="Formulate a Message", command = self.buttonEvent2)
        self.button.pack(padx=20,pady=20)

#formats the name inputted to the json, clears the texbox, accesses the phone number via the name inputted
    def buttonEvent(self):

        phoneNum = self.entry.get().replace("  " , " ")
        self.textbox.delete("0.0","end")
        found = False
        for table in data:
            if (table['name'].lower() == phoneNum.lower() or table['phone'] == phoneNum or table['speciaization'].lower() == phoneNum.lower()):
                nameNum = f"Name: {table['name']}\nPhone: {table['phone']}\nYears of Experiance: {table['experience']}\nSpecialization: {table['speciaization']}\n\n"
                self.textbox.insert("0.0", nameNum)
                found = True
        if found == False:
            self.textbox.insert("0.0", "No results found")
            
        # trying to get specialization input to work,print(table("speciaization"))

    def buttonEvent2(self):
        phoneNum = self.entry.get().replace("  " , " ")
        self.textbox.delete("0.0","end")

        found  = False
        for table in data:
             if (table['name'].lower() == phoneNum.lower() or table['phone'] == phoneNum or table['speciaization'].lower() == phoneNum.lower()):
                
                if phoneNum.lower() == table['speciaization'].lower():
                    message = f"Hello, I am looking for a realtor who specializes in {self.entry.get()}. Please contact me at your earliest convenience. Thank you!"
                elif phoneNum == table['phone']:
                    message = f'Hello {table['name']}, I am interested in your services. Please contact me at your earliest convenience. Thank you!'
                elif phoneNum.lower() == table['name'].lower():
                    message = f"Hello {self.entry.get()}, I am interested in your services. Please contact me at your earliest convenience. Thank you!"
             
                self.textbox.insert("0.0", message)
                found = True
                break
             
        if not found:
            self.textbox.insert("0.0", "Could not formulate a message. No results found.")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x350")
        self.my_frame = myFrame(master=self)
        self.my_frame.pack(expand = "True", fill= "both")
        self.title("Realtor Search")
        

app = App()
app.mainloop()

