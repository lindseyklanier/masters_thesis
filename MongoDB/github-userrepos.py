# working with lists in python: http://www.tutorialspoint.com/python/python_lists.htm

import csv
import pymongo
from pymongo import MongoClient

### CONNECTION TO LOCALHOST ###
localClient = MongoClient('localhost',27022) # establish a connection my local MongoDB instance
myLocalDB = localClient.thesis_githubResearch # create a database object
myLocalCollection = myLocalDB.githubRTPUsersRepos_Refresh # create a collection object
myLocalCollectionCount = myLocalCollection.count() # query the collection

### CONNECTION TO GHTORRENT ###
ghtorrentClient = MongoClient('localhost',27017) # establish a connection my local MongoDB instance
ghtorrentAuth = ghtorrentClient.github.authenticate('ghtorrentro','ghtorrentro')
ghtorrentDB = ghtorrentClient.github # create a database object
ghtorrentCollection = ghtorrentDB.repos # create a collection object

### LOCAL CSV READER ###
# myCSV = 'C:\Users\linds_000\Documents\ECU-GradSchool\Thesis\Data Sources\GitHub\ghtorrent\ghtorrent-final\ghtorrent-rtpusers.csv'
# myCSV = 'C:\Users\linds_000\Documents\ECU-GradSchool\Thesis\Data Sources\GitHub\ghtorrent\ghtorrent-final\ghtorrent-more-unietc.csv'
myCSV = 'C:\Users\linds_000\OneDrive\Documents\ECU-GradSchool\Thesis\Data Sources\GitHub\ghtorrent\RTP Repos.csv'

mylist = []

with open(myCSV) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        mylist.append(row['name'])

"Starting!"
i = 1
for reponame in mylist:
    try:
        myLocalCollection.insert(ghtorrentCollection.find({'Repo' : reponame}))
        print str.format("Repo {0} inserted, counter: {1}", reponame, i)
        i += 1
    except Exception, e:
        print str.format("Error inserting {0}, message is {1}", reponame, e)
        i += 1

print "Done! Closing connections."
localClient.close()
ghtorrentClient.close()