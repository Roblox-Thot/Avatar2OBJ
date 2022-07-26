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
    # I think roblox blocks banned users from my tests
    print("Can't get avatar, user is banned?")
    exit()

data = sussion.get(dataURL["imageUrl"]).json()

def url(hash):
    # Returns the url needed from roblox's hash
    # Thanks to this sexy person: https://devforum.roblox.com/t/a/1274498/2 <3
    i = 31
    for char in hash[:32]:
        i ^= ord(char)  # i ^= int(char, 16) also works
    return f"https://t{i%8}.rbxcdn.com/{hash}"

with open(f"files/{username}.mtl", "wb") as file:
    materialData = sussion.get(url(data["mtl"]))
    file.write(materialData.content)

with open(f"files/{username}.obj", "wb") as file:
    # Roblox changes this url from time to time, so we have to check for it
    objectData = sussion.get(url(data["obj"]))
    matHeader = bytes(f"mtllib {username}.mtl\n\n", 'utf-8')
    file.write(matHeader+objectData.content)

for list in data["textures"]:
    with open(f"files/{list}", "wb") as file:
        file.write(sussion.get(url(list)).content)

# TODO: #1 rename textures to match the name of the object
# for list in range(len(data["textures"])):
#    print(list)

