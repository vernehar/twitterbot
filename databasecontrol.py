import psycopg2
import time
import calendar

#open connection to database
def openConnection():
    connection = psycopg2.connect(
    host="ec2-34-251-115-141.eu-west-1.compute.amazonaws.com",
    database="dffsuc2s86o960",
    user="tyymzbzidvowkg",
    password="1d51ace4d9e9ecf1c77161abfe492c58593a701c243ce5467125f1121cd09ca9",
    sslmode="require")
    
    return connection

#When a new influencer is added, add it to table "influencers" and make two tables, one to hold all the followings over
#time of that influencer, another to hold followings since last update
def appendInfulencer(_name):
    connection = openConnection()
    c = connection.cursor()
    currentInfluencers = getCurrentInfluencers()
    if (_name not in currentInfluencers):
        c.execute("INSERT INTO influencers VALUES('"+_name+"')")
    else:
        print("Twitter handle already added")
    _name = checkName(_name)
    c.execute("CREATE TABLE IF NOT EXISTS "+_name+" (follows text UNIQUE, time int)")
    newFollowsTableName = _name + "newfollows"
    c.execute("CREATE TABLE IF NOT EXISTS "+newFollowsTableName+" (follows text UNIQUE, time int)")
    connection.commit()
    connection.close()

#return list of currently followed influencers
def getCurrentInfluencers():
    connection = openConnection()
    currentInfluencers = []
    c = connection.cursor()
    c.execute("SELECT name FROM influencers")
    currentInfluencers = [item for item, in c]
    return currentInfluencers

#Get the current follows of influencers followed
def getCurrentInfluencerFollows(_influencer):
    connection = openConnection()
    _influencer = checkName(_influencer)
    c = connection.cursor()
    c.execute("SELECT follows FROM "+_influencer)
    currentFollows = [item for item, in c]
    return currentFollows

#When a new follow is found it is added to both the influencer specific table containing all follows 
#and the temporary one holding the ones since last update. NewInfluencer is set to true if the influencer is just added
#to avoid a huge data dump to telegram, e.g. when a new follower is added the current follows by that account are not 
#considered new
def newFollow(_influencer, _newFollowing, newInfluencer = False):
    connection = openConnection()
    _influencer = checkName(_influencer)
    newtuple = []
    newtuple.append((_newFollowing, calendar.timegm(time.gmtime())))
    c = connection.cursor()
    c.executemany("INSERT INTO "+_influencer+" VALUES(%s,%s)", newtuple)
    if not newInfluencer:
        c.executemany("INSERT INTO "+_influencer+"newfollows VALUES(%s,%s)", newtuple)
    connection.commit()


#empty the [influencer]newfollows tables when update is requested from tg
def emptyNewFollows():
    connection = openConnection()
    currentInfluencers = getCurrentInfluencers()
    print(currentInfluencers)
    c = connection.cursor()
    for i in range(len(currentInfluencers)):
        currentInfluencers[i] = checkName(currentInfluencers[i])
        c.execute("DELETE FROM "+currentInfluencers[i]+"newfollows")
    connection.commit()
    connection.close()

#dump new follows as a dict to for a message from these to telegram
def dumpNewFollows():
    connection = openConnection()
    newFollows = {}
    currentInfluencers = getCurrentInfluencers()
    for i in range(len(currentInfluencers)):
        currentInfluencers[i] = checkName(currentInfluencers[i])
        c = connection.cursor()
        c.execute("SELECT follows FROM "+currentInfluencers[i]+"newfollows")
        changeloglist = [item for item, in c]
        if changeloglist:
            currentInfluencers[i] = returnNameToNormal(currentInfluencers[i])
            newFollows.update({currentInfluencers[i]: changeloglist})
    emptyNewFollows()
    return newFollows

def GetRecentFollows(_timePeriod):
    _timePeriod = _timePeriod*3600
    connection = openConnection()
    newFollows = {}
    currentInfluencers = getCurrentInfluencers()
    for i in range(len(currentInfluencers)):
        changeloglist = []
        currentInfluencers[i] = checkName(currentInfluencers[i])
        c = connection.cursor()
        c.execute("SELECT * FROM "+currentInfluencers[i]+" WHERE time>"+str(calendar.timegm(time.gmtime())-_timePeriod))
        changeloglist = c.fetchall()
        if changeloglist:
            currentInfluencers[i] = returnNameToNormal(currentInfluencers[i])
            newFollows.update({currentInfluencers[i]: changeloglist})
    return newFollows

def GetInfluencerFollowsByHandle(_handle):
    connection = openConnection()
    followsByInfluencer = {}
    currentInfluencers = getCurrentInfluencers()
    for i in range(len(currentInfluencers)):
        currentInfluencers[i] = checkName(currentInfluencers[i])
        c = connection.cursor()
        c.execute("SELECT time FROM "+currentInfluencers[i]+" WHERE follows LIKE '"+_handle+"' ORDER BY time")
        timeStampOfFollow = [item for item, in c.fetchall()]
        if timeStampOfFollow:
            currentInfluencers[i] = returnNameToNormal(currentInfluencers[i])
            followsByInfluencer.update({currentInfluencers[i]: timeStampOfFollow})
    followsByInfluencer = {key: val for key, val in sorted(followsByInfluencer.items(), key = lambda ele: ele[1])}
    return followsByInfluencer


def trendingWithinTimePeriod(_hours):
    seconds = _hours * 3600
    connection = openConnection()
    all24hFollows = []
    trending = {}
    currentInf = getCurrentInfluencers()
    for i in range(len(currentInf)):
        c = connection.cursor()
        currentInf[i] = checkName(currentInf[i])
        c.execute("SELECT follows FROM "+currentInf[i]+" WHERE time>"+str(calendar.timegm(time.gmtime())-seconds))
        follows = [item for item, in c.fetchall()]
        all24hFollows.extend(follows)

    for j in range(len(all24hFollows)):
        count = all24hFollows.count(all24hFollows[j])
        if count > 2:
            trending.update({all24hFollows[j]:count})
    return trending

#return the current influencers as a parsed string, not so database related
def getCurrentInfluencersString():
    currentInfluencers = getCurrentInfluencers()
    influencerString = "\n"
    for i in range(len(currentInfluencers)):
        influencerString = influencerString + currentInfluencers[i] + "\n"
    return influencerString

#check that the account name does not stat with a number, if it does, add prefix NUM to the name to avoid sql error
def checkName(_name):
    if _name[0].isdigit():
        _name = "NUM" + _name
    return _name


#Remove the prefix for printing purposes
def returnNameToNormal(_name):
    if "NUM" in _name[0:3]:
        _name = _name.replace("NUM","")
        return _name
    else:
        return _name



