import json
import os
import random

START = "Humble Administrator's Garden"
FINISH = "Tongli Ancient Town"
SAVE_FILE = "save.json"
DATA_FILE = "custom.json"

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_user_position(username, position):
    data = {}
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
    data[username] = position
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_user_position(username):
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get(username, None)
    return None

def move_user(data, current, move):
    """Returns next room name based on current room and move direction"""
    if current in data and "moves" in data[current]:
        moves = data[current]["moves"]
        if move in moves:
            return moves[move]
    return current

def get_random_start(data):
    """Returns a random starting room excluding FINISH"""
    valid_rooms = [room for room in data.keys() if room != FINISH]
    return random.choice(valid_rooms)

def describe(data, current):
    """Returns room description with available moves and objects"""
    if current not in data:
        return "Location does not exist"
    
    result = []
    if "text" in data[current]:
        result.append(data[current]["text"])

    if "moves" in data[current]:
        moves = list(data[current]["moves"].keys())
        if moves:
            result.append("\nPossible directions: " + ", ".join(moves))
        else:
            result.append("\nThis is your final destination!")

    if "objects" in data[current]:
        objects = data[current]["objects"]
        if objects:
            object_names = [obj["name"] for obj in objects]
            if len(object_names) == 1:
                result.append(f"\nYou see a {object_names[0]}.")
            else:
                items_text = " and ".join([", ".join(object_names[:-1]), object_names[-1]])
                result.append(f"\nYou see: {items_text}.")
            
            # Show collectible items
            special_items = [obj["name"] for obj in objects if obj.get("type") == "special"]
            if special_items:
                result.append("Collectible treasures: " + ", ".join(special_items))
    
    return "\n".join(result)

def play_game(data):
    print('Welcome to the Suzhou Adventure Game!\n')
    print('Explore the beautiful gardens, ancient streets, and cultural landmarks of Suzhou.\n')
    
    username = input("Please enter your name, traveler: ").strip()
    current = load_user_position(username)
    
    # Start from beginning if no save or completed
    if current is None or current == FINISH:
        current = START
    
    while True:
        print("\n" + "="*50)
        print(f"Current location: {current}")
        print(describe(data, current))
        
        if current == FINISH:
            print("\nCongratulations! You've completed your journey through Suzhou!")
            print("You've arrived at the peaceful water town of Tongli!")
            save_user_position(username, FINISH)
            break
        
        move = input("\nWhich direction would you like to go? (or 'quit' to exit): ").strip().lower()
        
        if move in ["quit", "exit"]:
            print("\nThank you for visiting Suzhou. Come back soon!")
            save_user_position(username, current)
            break
            
        new_room = move_user(data, current, move)
        if new_room == current:
            print("\nYou cannot go that way. Please choose a valid direction.")
        else:
            current = new_room
            save_user_position(username, current)

if __name__ == '__main__':
    data = load_data()
    play_game(data)