# working with lists in python: http://www.tutorialspoint.com/python/python_lists.htm

import csv
import pymongo
from pymongo import MongoClient

### CONNECTION TO LOCALHOST ###
localClient = MongoClient('localhost',27022) # establish a connection my local MongoDB instance
myLocalDB = localClient.thesis_githubResearch # create a database object
myLocalCollection = myLocalDB.githubRTPProjectCommits # create a collection object
myLocalCollectionCount = myLocalCollection.count() # query the collection

### CONNECTION TO GHTORRENT ###
ghtorrentClient = MongoClient('localhost',27017) # establish a connection my local MongoDB instance
ghtorrentAuth = ghtorrentClient.github.authenticate('ghtorrentro','ghtorrentro')
ghtorrentDB = ghtorrentClient.github # create a database object
ghtorrentCollection = ghtorrentDB.commits # create a collection object

### LOCAL CSV READER ###
# myCSV = 'C:\Users\linds_000\Documents\ECU-GradSchool\Thesis\Data Sources\GitHub\ghtorrent\ghtorrent-final\ghtorrent-rtpusers.csv'
# myCSV = 'C:\Users\linds_000\Documents\ECU-GradSchool\Thesis\Data Sources\GitHub\ghtorrent\ghtorrent-final\ghtorrent-more-unietc.csv'
myCSV = 'C:\Users\linds_000\OneDrive\Documents\ECU-GradSchool\Thesis\Data Sources\GitHub\ghtorrent\RTP Commits.csv'

mylist = []

print 'Creating a huge list of sha'
with open(myCSV) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        mylist.append(row['sha'])

i = 1
for sha in mylist:
    try:
        myLocalCollection.insert(ghtorrentCollection.find({"sha":sha}))
        print 'Copied', i
        i += 1
    except Exception, e:
        print str.format("Error inserting {0}, message is {1}", sha, e)
        i += 1

print "Done! Closing connections."
localClient.close()
ghtorrentClient.close()

