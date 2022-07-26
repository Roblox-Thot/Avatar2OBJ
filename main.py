import requests

sussion = requests.session()

# ask if the user wants to give username or userID
if input("(U)sername or user(I)D: ").lower() == "u":
    userID = sussion.get("https://api.roblox.com/users/get-by-username?username=" + input("Username: ")).json()["Id"]
    userID = str(userID) # Converts userID to string
else:
    userID = input("User ID: ")

dataURL = sussion.get("https://thumbnails.roblox.com/v1/users/avatar-3d?userId=" + userID).json()["imageUrl"]
data = sussion.get(dataURL).json()

materialData = sussion.get("https://t0.rbxcdn.com/" + data["mtl"])
objectData = sussion.get("https://t1.rbxcdn.com/" + data["mtl"])

# TODO: rename textures to match the name of the object
#for list in data["textures"]:
#    print(list)

