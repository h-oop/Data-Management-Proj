# DATA MANAGEMENT PROJECT

#to do:
#DONE Sort song by: Title, Artist, Genre
#DONE display all songs
#DONE generate array of all items with each item being dictionary
#DONE Filter by title, artist, etc
#DONE Add to playlist
#DONE remove from playlist (LOOK AT NIC GEN)
#DONE display list

#above and beyond:
#login system with persistent playlist

#setup
import json

songsli = []
accounts = []
playlist = []



def main():

    #generate list from songlist.txt
    with open("songlist.txt", "r") as file:
        for line in file:
            #split the line by semicolons to identify the key value of title, artist, and genre, make new dict for each line
            #strip() removes \n inserted by loading that defines each line
            title, artist, genre = line.strip().split(";")

            song_dict = add_song(title, artist, genre)

            songsli.append(song_dict)
    

    print(songsli)

    

    accounts_saved = False
    user_logged_in = False

    
    #TESTS FOR IF THERE ARE ACCOUNTS TO BE UPLOADED, if not forces user to make one
    try:
        with open("JSON/acc-list.json", "r") as file:
            accounts = json.load(file)
    except json.JSONDecodeError:
        print("cool theres no users")
        accounts = []
        accounts_saved = True

        while user_logged_in == False:
            print("\nWelcome, please make an account:")
            user_logged_in = new_user(accounts)


    #GIVE USER THE OPTION TO LOG IN IF THERE ARE ACCOUNTS TO LOG INTO OR TO MAKE NEW ACCOUNT
    if not accounts_saved:
        openmenu = True
        while openmenu:
            print("\nPlease login or create an account to add songs to your playlist.")
            print("1: Login")
            print("2: Create account")
            selection = input("> ")
            if selection == "1":
                #logging in, when logged in properly it turns off this menu loop
                user_logged_in = login(accounts)
                if user_logged_in:
                    openmenu = False

            elif selection == "2":
                #making a new account, when it
                user_logged_in = new_user(accounts)
                if user_logged_in:
                    openmenu = False


            else:
                print("ERR, enter valid num.")


    menuloop = True
    print(user_logged_in)


    #menu loop
    while menuloop:

        print("\n-PLAYLIST CRAFTER-")
        print("1: BROWSE ALL SONGS")
        print("2: SEARCH")
        print("3: SORT BY PROPERTY")
        print("4: SHOPPING CART")
        print("5: SAVE")
        print("0: SAVE AND EXIT")
        #INPUT
        selection = input("> ")

        #ACTION
        #BROWSE SONG LIST AS IS
        if selection == "1":
            browse_list(songsli)
            add_to_playlist(songsli)

        #SEARCH
        elif selection == "2":
            item = input("\nWhat is your search criteria?\n> ")

            sortedlist = linear_search(songsli, item)

            if sortedlist == -1:
                print("Your criteria couldn't be found.")
            else:
                browse_list(sortedlist)
                add_to_playlist(sortedlist)

        #SORT BY KEY
        elif selection == "3":
            menu3 = True
            while menu3:
                print("\nSort by:")
                print("1. Title")
                print("2. Artist")
                print("3. Genre")
                opt = input("> ")
                if opt == "1":
                    sorted = insertion_sort(songsli, "title")
                    browse_list(sorted)
                    add_to_playlist(sorted)
                    break
                if opt == "2":
                    sorted = insertion_sort(songsli, "artist")
                    browse_list(sorted)
                    add_to_playlist(sorted)
                    break
                if opt == "3":
                    sorted = insertion_sort(songsli, "genre")
                    browse_list(sorted)
                    add_to_playlist(sorted)
                    break
                else:
                    print("Bad input, try again")

        #BROWSE AND EDIT YOUR PLAYLIST
        elif selection == "4":
            browse_list(playlist)
            if playlist:
                select = input("\nWould you like to edit your playlist? [Y/N]\n> ")
                if select.lower() == "y":
                    remove_from_playlist()
            else:
                print("hey DUMMY go put some stuff in your playlist")

        #SAVE
        elif selection == "5":
            print("\nSaving...")
            save_function(user_logged_in,accounts,playlist)

        #SAVE AND EXIT
        elif selection == "0":
            print("\nSaving...")
            menuloop = False

            save_function(user_logged_in,accounts,playlist)

            print("\nCome again soon!")

        #ERROR MESSAGE FOR NON APPLICABLE INPUTS
        else:
            print("\nERR please enter a valid number")

        #wait before continuing
        input("\n[press enter]")





            
#~~~~~FUNCTION DEFINITIONS~~~~~~~
######################################################################################

#generates the song dictionaries and adds to 
def add_song(title, artist, genre):
    return {"title": title, 
            "artist": artist, 
            "genre": genre}

#make new user
def new_user(array):
    usernamein = input("Create a username: ")
    passwordin = input("Create a password: ")

    #check if the account is in the thing and prevent adding it if it isnt
    for i in array:
        if i['username'] == usernamein:
            print("Nice try chuckleknuts. Invalid username.")
            return False
    

    #otherwise generates a new account dictionary with a blank playlist and appends it to the list
    new_acc = {
		'username': usernamein,
		'password': passwordin,
		'playlist': []
	}

    array.append(new_acc)
    
    print(f"New user created, {usernamein}")
    return (usernamein, passwordin)


def login(list_of_dicts):
    uservar = input("Enter your username: ")
    passvar = input("Enter your password: ")
    global playlist

    #Check each dictionary for if it has the username and password and return that combo if it exists
    for dictvar in list_of_dicts:
        if dictvar['username'] == uservar and dictvar['password'] == passvar:
            print(f"Welcome back {uservar}")
            playlist = list_of_dicts[list_of_dicts.index(dictvar)]['playlist']
            load_account(uservar, passvar, accounts)
            return (uservar, passvar)

    print("Invalid username or password. Please try again.")
    return None
    

def load_account(uservar, passvar, accounts):
    for account in accounts:
        if account['username'] == uservar and account['password'] == passvar:
            # Update the loaded account's playlist with the current playlist
            account['playlist'] = playlist
            print("Account loaded.")
            return account

    return None


def browse_list(list):
    #quick variable set to find each dictionary key *value* at each position, then print with a +1 Index for UI
    for i in range(len(list)):
        x = list[i]
        t = x['title']
        a = x['artist']
        g = x['genre']
        print(f"\n{i+1}. {t} (by {a}, {g})")


def linear_search(array, item):
    #moves applicable items to a filtered dictionary which can then be browsed, and used as reference for shopping add
    filtered = []
    for dict in array:

        for key in dict:

            if item.lower() in dict[key].lower():
                filtered.append(dict)
                break

    if filtered:
        return filtered
    else:
        return -1


def insertion_sort(list_of_dicts, key):
    
    temp = list_of_dicts
    for i in range(1, len(temp)):
        insert_pos = i
        insert_val = temp[insert_pos]

       
        while insert_pos > 0 and temp[insert_pos - 1][key] > insert_val[key]:
            #take item at insert position and make it the item to the left
            temp[insert_pos] = temp[insert_pos - 1]
            insert_pos -= 1

        temp[insert_pos] = insert_val

    return temp


def add_to_playlist(shop_list):
    ynselect = input("\nWould you like to shop? [Y/N]\n> ")
    if ynselect.lower() == "y":
        num = int(input("What song # would you like?\n> "))
        try:
            if shop_list[num - 1] in playlist:
                print("Hey silly that's a repeat ',:(")
            else:
                playlist.append(shop_list[num - 1])

                print(f"{shop_list[num-1]['title']} added")
        except IndexError:
            print("Invalid.")
    

def remove_from_playlist():
    num = int(input("\nWhat number song do u want GONE\n> "))

    try:
        print(f"SICK. {playlist[num-1]['title']} is outta here.")
        playlist.remove(playlist[num - 1])
    #this checks for if you input a bad number that isn't present
    except IndexError:
        print("Hey silly that's a NONEXISTANT ',:(")


def save_function(useraccount, array, playlist):

    (uservar, passvar) = useraccount

    #Update the dictionary of the current user to the accounts list, then update the json with the updated list
    for dict in array:
        
        if dict['username'] == uservar and dict['password'] == passvar:
            dict['playlist'] = playlist


    with open("JSON/acc-list.json", "w") as file_object:
        json.dump(array, file_object)



#run main
main()




