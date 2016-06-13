# working with lists in python: http://www.tutorialspoint.com/python/python_lists.htm

import pymongo
from pymongo import MongoClient
import MySQLdb

### MONGODB CONNECTION INFORMATION ###
localClient = MongoClient('localhost',27022) # establish a connection my local MongoDB instance
myLocalDB = localClient.thesis_githubResearch # get my thesis DB
githubRTPUsers = myLocalDB.githubRTPUsers # userRepos Collection
githubRTPUsersPullReqs = myLocalDB.githubRTPUsersPullReqs # Collection from local MongoDB


### MYSQL CONNECTION INFORMATION ###
mySqlDB = MySQLdb.connect(host="localhost", port=33306, user="ghtorrent", passwd="gz259Bfg", db="ghtorrent")

def getPullReqs():

    query = "(select u.login, p.name, count(*) as 'prcount', 'head' as 'repotype'"\
            " from projects p, users u, pull_requests pr"\
            " where p.owner_id = u.id"\
            " and pr.head_repo_id = p.id"\
            " and p.deleted is false"\
            " and p.forked_from is null"\
            " and u.login = %s"\
            " group by p.id"\
            " order by count(*) desc)"\
            " UNION"\
            " (select u.login, p.name, count(*) as 'prcount', 'base' as 'repotype'"\
            " from projects p, users u, pull_requests pr"\
            " where p.owner_id = u.id"\
            " and pr.base_repo_id = p.id"\
            " and p.deleted is false"\
            " and p.forked_from is null"\
            " and u.login = %s"\
            " group by p.id"\
            " order by count(*) desc)"

    myUsers = githubRTPUsers.find({},{"login":1}) # first find all usernames

    i = 0
    try:
        for x in myUsers:
            mySqlCursor = mySqlDB.cursor()
            mySqlCursor.execute(query,(x['login'],x['login']))
            data = mySqlCursor.fetchall()
            for row in data:
                myLocalDB.calculated_pullReqByUser.insert([
                    {"login":row[0],
                    "name": row[1],
                    "prcount": row[2],
                    "repotype": row[3]}])
                print "done with ", x['login'], i
            i+=1
    except Exception, e:
        print e
        myLocalDB.rejects.insert({"failed":i})


getPullReqs()