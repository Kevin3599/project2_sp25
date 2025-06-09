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
            return data.get(username)
    return None


def move_user(data, current, move):
    """Returns next room name based on current room and move direction"""
    room = data.get(current, {})
    return room.get("moves", {}).get(move, current)


def get_random_start(data):
    """Returns a random starting room excluding FINISH"""
    rooms = [room for room in data.keys() if room != FINISH]
    return random.choice(rooms)


def describe(data, current):
    """
    Returns a formatted description of the current room, including objects and move options.
    """
    room = data.get(current)
    if room is None:
        return "Location does not exist"

    parts = []
    # Room text
    text = room.get("text", "").strip()
    if text:
        parts.append(text)
    # Objects
    objs = room.get("objects", [])
    if objs:
        names = [obj.get("name") for obj in objs if obj.get("name")]
        if names:
            parts.append(f"You see {', '.join(names)}.")
    # Combine into one paragraph
    description = " ".join(parts)

    # Build lines
    lines = [description]
    # Always show options header
    lines.append("")
    lines.append("Your options are:")
    for direction, dest in room.get("moves", {}).items():
        lines.append(f"'{direction}' to go to {dest}")

    return "\n".join(lines)


def play_game(data):
    print("Welcome to the Suzhou Adventure Game!\nExplore the beautiful gardens, ancient streets, and cultural landmarks of Suzhou.\n")
    username = input("Please enter your name, traveler: ").strip()
    current = load_user_position(username)
    if not current or current == FINISH:
        current = START

    while True:
        print("\n" + "="*50)
        print(f"Current location: {current}")
        print(describe(data, current))
        if current == FINISH:
            print("\nCongratulations! You've completed your journey through Suzhou!\nYou've arrived at the peaceful water town of Tongli!")
            save_user_position(username, FINISH)
            break

        choice = input("\nWhich direction would you like to go? (or 'quit' to exit): ").strip().lower()
        if choice in ("quit", "exit"):
            print("\nThank you for visiting Suzhou. Come back soon!")
            save_user_position(username, current)
            break
        new_room = move_user(data, current, choice)
        if new_room == current:
            print("\nYou cannot go that way. Please choose a valid direction.")
        else:
            current = new_room
            save_user_position(username, current)

if __name__ == '__main__':
    data = load_data()
    play_game(data)
