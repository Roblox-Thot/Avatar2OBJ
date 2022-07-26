import requests

sussion = requests.session()

# ask if the user wants to give username or userID
if input("(U)sername or user(I)D: ").lower() == "u":
    username = input("Username: ")
    userID = sussion.get("https://api.roblox.com/users/get-by-username?username=" + username).json()["Id"]
    userID = str(userID) # Converts userID to string
else:
    userID = input("User ID: ")
    username = sussion.get("https://users.roblox.com/v1/users/" + userID).json()["name"]

dataURL = sussion.get("https://thumbnails.roblox.com/v1/users/avatar-3d?userId=" + userID).json()
if dataURL["state"] == "Blocked":
    print("Can't get avatar, user is banned?")
    exit()

data = sussion.get(dataURL["imageUrl"]).json()

materialData = sussion.get("https://t0.rbxcdn.com/" + data["mtl"])

with open(f"files/{username}.mtl", "wb") as file:
    file.write(materialData.content)

with open(f"files/{username}.obj", "wb") as file:
    # Roblox changes this url from time to time, so we have to check for it
    for i in range(1,6):
        objectData = sussion.get(f"https://t{i}.rbxcdn.com/" + data["obj"])
        if objectData.status_code == 200:
            matHeader = bytes(f"mtllib {username}.mtl\n\n", 'utf-8')
            file.write(matHeader+objectData.content)
            break

for list in data["textures"]:
    with open(f"files/{list}", "wb") as file:
        file.write(sussion.get("https://t2.rbxcdn.com/" + list).content)

# TODO: #1 rename textures to match the name of the object
# for list in range(len(data["textures"])):
#    print(list)

