# working with lists in python: http://www.tutorialspoint.com/python/python_lists.htm

import csv
import pymongo
from pymongo import MongoClient

### CONNECTION TO LOCALHOST ###
localClient = MongoClient('localhost',27022) # establish a connection to my local MongoDB instance
myLocalDB = localClient.thesis_githubResearch # create a database object
myLocalCollection = myLocalDB.githubRTPUsers # create a collection object
myLocalCollectionCount = myLocalCollection.count() # query the collection

### CONNECTION TO GHTORRENT ###
ghtorrentClient = MongoClient('localhost',27017) # establish a connection to GHTorrent
ghtorrentAuth = ghtorrentClient.github.authenticate('ghtorrentro','ghtorrentro')
ghtorrentDB = ghtorrentClient.github # create a database object
ghtorrentCollection = ghtorrentDB.users # create a collection object

### LOCAL CSV READER ###
myCSV = 'C:\Users\linds_000\Documents\ECU-GradSchool\Thesis\Data Sources\GitHub\ghtorrent\RTP Users.csv'

mylist = []

with open(myCSV) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        mylist.append(row['login'])

"Starting!"
i = 1
for loginid in mylist:
    try:
        myLocalCollection.insert(ghtorrentCollection.find({'login' : loginid}))
        print str.format("Login {0} inserted, counter: {1}", loginid, i)
        i += 1
    except Exception, e:
        print str.format("Error inserting {0}, message is {1}", loginid, e)
        i += 1

print "Done! Closing connections."
localClient.close()
ghtorrentClient.close()


# debugging - local connection
'''
print "localclient connection!"
print localClient
print myLocalDB
print myLocalCollection
print myLocalCollectionCount

print "--------"

print "ghtorrent connection!"
print ghtorrentClient
print ghtorrentAuth
print ghtorrentDB
print ghtorrentCollection

print "mylist count: ", len(mylist)
print "number2 in mylist is: ", mylist[2]
'''

