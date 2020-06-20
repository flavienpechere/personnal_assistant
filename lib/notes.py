import os

def start_note():
    try:
        f = open("notes.txt", "x", encoding='utf-8')
        print("'notes.txt' has been created successfully")
    except FileExistsError:
        print("'notes.txt' already exists")
    
def append_note(string, special=0):
    if special != 0:
        try:
            switch = {
                1: "\n" + string.upper() + "\n", 
                2: "\n" + "- " + string + "\n"
            }
            string = switch.get(special, lambda: "Invalid argument 'special'")
            f = open("notes.txt", "a", encoding='utf-8')
            f.write(string)
            f.close()
        except TypeError:
            print("Invalid argument")
    else:    
        f = open("notes.txt", "a", encoding='utf-8')
        f.write(string + ". ")
        f.close()

def read_note():
    #open and read the file after the appending:
    f = open("notes.txt", "r", encoding='utf-8')
    return f.read()    

def delete_note():
    if os.path.exists("notes.txt"):
        os.remove("notes.txt")
    else:
        pass