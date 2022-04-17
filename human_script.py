import json

def get_data():
    with open("data/leaderboard.json", "r") as f:
        data = json.load(f)
    
    return data

def update_data(user, change = 0):
    users = get_data()

    users[str(user)]["pins"] += change

    with open("data/leaderboard.json", "w") as f:
        json.dump(users, f)


while True:
    alt_names = ["am", "dwal", "feet", "cat", "alk", "tem", "keth"]
    IDs = [466693193002647583, 263021997406158848, 273453312303693824, 193715376884809728, 170905343197577217, 368423564229083137, 204380480672366593]
    #get input from the user
    person = input("person: ")
    
    for x in range(len(alt_names)):
        if person == alt_names[x]:
            person = IDs[x]
            break
    
    print(person)
    
    update_data(person, 1)