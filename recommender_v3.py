# -*- coding: utf-8 -*-

PREF_FILE = 'musicrecplus.txt'

def loadUsers(fileName):
    '''Reads in a file of stored users' preferences stored in the file 'filename'.
    Returns a dictionary containing a mapping of usernames to a list of preferred
    artists'''
    try:
        file = open(fileName, 'r')
        userDict = {}
        for line in file:
            # Read and parse a single line
            [userName, bands] = line.strip().split(':')
            bandList = bands.split(',')
            bandList.sort()
            userDict[userName] = bandList
        file.close()
        return userDict
    

    except FileNotFoundError:
        print('File does not exist. Creating new file.')
        file = open(fileName, 'w')
        file.close()
        return loadUsers(fileName)


    
def getPreferences(userName, userMap):
    '''Returns a list of the user's preferred artists. If the system already knows about
    the user, it gets the preferences out of the userMap dictionary and then asks if she
    has additional preferences. If the user is new, it simply asks the user for her
    preferences'''

    newPref = ''
    prefs = []
    newPref = input('Enter an artist that you like (Enter to finish): ')
    while newPref != '':
        prefs.append(newPref.strip().title())
        newPref = input('Enter an artist that you like (Enter to finish): ')

    #Always keep the lists in sorted order for ease of comparison
    prefs.sort()
    saveUserPreferences(userName, prefs, userMap, 'musicrecplus.txt')
    return prefs


def getRecommendations(currUser, prefs, userMap):
    '''Gets recommendations for a user (currUser) based on the users in userMap (a dictionary)
    and the user's preferences in pref (a list). Returns a list of recommended artists'''

    recommendations = []
    if len(userMap) <= 1:
        return recommendations

    bestUser = findBestUser(currUser, prefs, userMap)
    recommendations = drop(prefs, userMap[bestUser])
    return recommendations

def findBestUser(currUser, prefs, userMap):
    '''Find the user whos tastes are closest to the current user. Return the best user's
    name (a string)'''

    publicUsers = {}
    for user in userMap:
        if user[-1] != '$':
            publicUsers[user] = userMap[user]

    nonEncompassedUsers = {}
    for user in publicUsers:
        if all(item in userMap[currUser] for item in publicUsers[user]) == False:
            nonEncompassedUsers[user] = publicUsers[user]

    users = nonEncompassedUsers.keys()
    bestUser = None
    bestScore = -1
    for user in users:
        score = numMatches(prefs, userMap[user])
        if score > bestScore and currUser != user:
            bestScore = score
            bestUser = user
    return bestUser

def drop(list1, list2):
    '''Return a new list that contains only the elements in list2 that were NOT in list1'''

    list3 = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            list3.append(list2[j])
            j += 1
    # Add the rest of list2 if there's anything left
    while j < len(list2):
        list3.append(list2[j])
        j += 1
    return list3

def numMatches(list1, list2):
    '''Return the number of elements that match between two sorted lists'''

    matches = 0
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            matches += 1
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return matches

def saveUserPreferences(userName, prefs, userMap, fileName):
    '''Writes all of the user preferences to the file. Returns nothing'''

    userMap[userName] = prefs
    file = open(fileName, 'w')
    for user in userMap:
        toSave = str(user) + ':' + ','.join(userMap[user]) + '\n'
        file.write(toSave)
    file.close()


def userLikesMostArtists(currUser, userMap):
    publicUsers = {}
    for user in userMap:
        if user == currUser:
            publicUsers[user] = userMap[user]
        elif user[-1] != '$':
            publicUsers[user] = userMap[user]
    if publicUsers == {}:
        return 'Sorry, no user found.'

    mostLikes = -1
    mostLikedUser = ''
    for user in publicUsers:
        if len(publicUsers[user]) >= mostLikes:
            mostLikes = len(publicUsers[user])
            mostLikedUser = user
    return mostLikedUser


def votes(userMap):
    '''Returns a dictionary of artists ranked in decending order by number of votes'''

    users = userMap.keys()
    bands = []
    for user in users:
        for artist in range(len(userMap[user])): #You have to use the range function for this loop to work
            bands.append(userMap[user][artist])

    votes = {}
    for artist in bands:
        if artist not in votes:
            votes[artist] = 1
        else:
            votes[artist] += 1
    return dict(sorted(votes.items(), key = lambda x:x[1], reverse=True))


def showMostPopularArtist(userMap):
    '''Counts the number of times an artist is liked by the userbase
    and prints the artists that are liked by the most users'''
    
    GOATS = votes(userMap) #GOATS is a dictionary
    GOATlist = list(GOATS.keys())

    #Print out the top three artists (If there are artists in the userMap)
    if len(GOATlist) == 0:
        print('Sorry, no artists found.')
    else:
        count = 0
        for i in range(len(GOATlist)):
            print(GOATlist[i])
            count += 1
            if count == 3:
                break

def howPopular(userMap):
    '''Prints the number of likes the most popular artist received'''

    GOATS = votes(userMap)
    GOATlist = list(GOATS.keys())
    mostPopular = max(GOATS, key=GOATS.get)
    
    if len(GOATlist) == 0:
        print('Sorry, no artists found.')
    else:
        likes = GOATS.values()
        print(max(likes))

def main():
    '''The main recommendation function'''

    userMap = loadUsers(PREF_FILE)
    print("Welcome to the Jungle baby! You're gonna die!! (Just kidding, welcome to the \
music recommender system!)")

    userName = input('Please enter your name: ')
    print('Welcome, ', userName)

    prefs = []
    option = ''
    while True:  
        option = input('Please enter a letter to choose an option:\ne - \
Enter preferences\nr - Get recommendations\np - Show most popular artists\nh - \
How popular is the most popular\nm - Which user has the most likes\nq - Save and quit: ')

        if option == 'e':
            prefs = getPreferences(userName, userMap)
        elif option == 'r':
            
            recs = getRecommendations(userName, prefs, userMap)
            if len(recs) == 0:
                print("No recommendations available at this time.")
            else:
                print(userName + ",", "based on the users I currently know about, I believe you might like: ")
                for artist in recs:
                    print(artist)
        elif option == 'p':
            showMostPopularArtist(userMap)
        elif option == 'h':
            howPopular(userMap)
        elif option == 'm':
            print(userLikesMostArtists(userName, userMap))
        elif option == 'q':
            saveUserPreferences(userName, prefs, userMap, PREF_FILE)
            break
        

if __name__ == '__main__': main()
        
#userDict = loadUsers(PREF_FILE)
#getPreferences('Anne Adamant', userDict)
