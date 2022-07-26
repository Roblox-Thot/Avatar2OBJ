import requests

sussion = requests.session()

def url(hash):
    # Returns the url needed from roblox's hash
    # Thanks to this sexy person: https://devforum.roblox.com/t/a/1274498/2 <3
    i = 31
    for char in hash[:32]:
        i ^= ord(char)  # i ^= int(char, 16) also works
    return f"https://t{i%8}.rbxcdn.com/{hash}"

# ask if the user wants to give username or userID
if input("(U)sername or user(I)D: ").lower() == "u":
    username = input("Username: ")
    try:
        userID = sussion.get("https://api.roblox.com/users/get-by-username?username=" + username).json()["Id"]
        userID = str(userID) # Converts userID to string
    except:
        print("Something went wrong. (user doesn't exist/banned)")
        exit()
else:
    userID = input("User ID: ")
    try:
        username = sussion.get("https://users.roblox.com/v1/users/" + userID).json()["name"]
    except:
        print("Something went wrong. (user doesn't exist/banned)")
        exit()

dataURL = sussion.get("https://thumbnails.roblox.com/v1/users/avatar-3d?userId=" + userID)
if dataURL.json()["state"] == "Blocked":
    # I think roblox blocks banned users from my tests
    print("Can't get avatar, user is banned?")
    exit()
elif dataURL.status_code != 200:
    print("Can't get avatar, something went wrong.")
    exit()

# Grab the data needed to download files later
data = sussion.get(dataURL.json()["imageUrl"]).json()

# Download the object file
with open(f"files/{username}.obj", "wb") as file:
    # Roblox changes this url from time to time, so we have to check for it
    objectData = sussion.get(url(data["obj"]))
    matHeader = bytes(f"mtllib {username}.mtl\n\n", 'utf-8')
    file.write(matHeader+objectData.content)

# Download the material file
with open(f"files/{username}.mtl", "wb") as file:
    materialData = sussion.get(url(data["mtl"]))
    file.write(materialData.content)

# Download the texture(s)
for list in data["textures"]:
    with open(f"files/{list}", "wb") as file:
        file.write(sussion.get(url(list)).content)

# TODO: #1 rename textures to match the name of the object
for list in range(len(data["textures"])):
   print(list, data["textures"][list])

