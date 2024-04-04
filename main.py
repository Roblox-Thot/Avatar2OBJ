from requests import session

session = session()

def url(hash:str) -> str:
    """
    Returns the url needed from Roblox's hash.

    Args:
        hash (str): The hash from Roblox.

    Returns:
        str: The generated URL based on the hash.
    """
    i = 31
    for char in hash[:32]:
        i ^= ord(char)
    return f"https://t{i%8}.rbxcdn.com/{hash}"

# Ask if the user wants to give username or userID
if input("(U)sername or user(I)D: ").lower() == "u":
    username = input("Username: ")
    try:
        userID = session.get(
            f"https://api.roblox.com/users/get-by-username?username={username}"
        ).json()["Id"]
        userID = str(userID) # Converts userID to string
    except Exception:
        print("Something went wrong. (user doesn't exist/banned)")
        exit()
else:
    userID = input("User ID: ")
    try:
        username = session.get(
            f"https://users.roblox.com/v1/users/{userID}"
        ).json()["name"]
    except Exception:
        print("Something went wrong. (user doesn't exist/banned)")
        exit()

dataURL = session.get(
    f"https://thumbnails.roblox.com/v1/users/avatar-3d?userId={userID}"
)
if dataURL.json()["state"] == "Blocked":
    # I think roblox blocks banned users from my tests
    print("Can't get avatar, user is banned?")
    exit()
elif dataURL.status_code != 200:
    print("Can't get avatar, something went wrong.")
    exit()

# Grab the data needed to download files later
try:
    data = session.get(dataURL.json()["imageUrl"]).json()
except Exception:
    dataURL = session.get(
        f"https://thumbnails.roblox.com/v1/users/avatar-3d?userId={userID}"
    )
    data = session.get(dataURL.json()["imageUrl"]).json()

# Download the object file
with open(f"files/{username}.obj", "wb") as file:
    print("Downloading object file...                ", end="\r")
    # Roblox changes this url from time to time, so we have to check for it
    objectData = session.get(url(data["obj"]))
    matHeader = bytes(f"mtllib {username}.mtl\n\n", 'utf-8')
    file.write(matHeader+objectData.content)

# Download the material file
with open(f"files/{username}.mtl", "w") as file:
    print("Downloading material file...              ", end="\r")
    materialData = session.get(url(data["mtl"])).text
    for list in range(len(data["textures"])):
        materialData = materialData.replace(data["textures"][list], f"{username}_{str(list)}.png")
    file.write(materialData)

# Download the texture(s)
for list in range(len(data["textures"])):
    print("Downloading textures...                   ",end="\r")
    with open(f"files/{username}_{str(list)}.png", "wb") as file:
        file.write(session.get(url(data["textures"][list])).content)

print("Done, files are in files folder.")
