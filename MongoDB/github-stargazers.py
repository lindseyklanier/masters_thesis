# working with lists in python: http://www.tutorialspoint.com/python/python_lists.htm

import csv
import pymongo
from pymongo import MongoClient

### CONNECTION TO LOCALHOST ###
localClient = MongoClient('localhost',27022) # establish a connection my local MongoDB instance
myLocalDB = localClient.thesis_githubResearch # create a database object
myLocalCollection = myLocalDB.githubRTPStargazers # create a collection object
myLocalCollectionCount = myLocalCollection.count() # query the collection

### CONNECTION TO GHTORRENT ###
ghtorrentClient = MongoClient('localhost',27017) # establish a connection my local MongoDB instance
ghtorrentAuth = ghtorrentClient.github.authenticate('ghtorrentro','ghtorrentro')
ghtorrentDB = ghtorrentClient.github # create a database object
ghtorrentCollection = ghtorrentDB.watchers # create a collection object

### LOCAL CSV READER ###
# myCSV = 'C:\Users\linds_000\Documents\ECU-GradSchool\Thesis\Data Sources\GitHub\ghtorrent\ghtorrent-final\ghtorrent-rtpusers.csv'
# myCSV = 'C:\Users\linds_000\Documents\ECU-GradSchool\Thesis\Data Sources\GitHub\ghtorrent\ghtorrent-final\ghtorrent-more-unietc.csv'
myCSV = 'C:\Users\linds_000\OneDrive\Documents\ECU-GradSchool\Thesis\Data Sources\GitHub\ghtorrent\RTP Repos.csv'

mylist = []
userList = []

print "Creating my List of repos and owners first.."
with open(myCSV) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        mylist.append(row['name'])
        userList.append(row['owner_login'])

print "Ok, let's go."
i = 1
for reponame, ownerlogin in zip(mylist,userList):
   # print reponame + ' ' + ownerlogin
    try:
        myLocalCollection.insert(ghtorrentCollection.find({'repo' : reponame, 'owner':ownerlogin}))
        print str.format("Owner {0}'s Repo {1} and inserted, counter: {2}", reponame, ownerlogin, i)
        i += 1
    except Exception, e:
        print str.format("Error inserting {0}, message is {1}", reponame, e)
        i += 1

print "Done! Closing connections."
localClient.close()
ghtorrentClient.close()