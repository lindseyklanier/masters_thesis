from pymongo import MongoClient
import datetime
import plotly
import random
from plotly.graph_objs import Scatter, Layout, Bar, Figure

# MongoDB Connection Details
localClient = MongoClient('localhost',27022) # establish a connection my local MongoDB instance
myLocalDB = localClient.thesis_githubResearch # get my thesis DB
repoCountByUser = myLocalDB.calculated_repoCountByUser # Count of Repos per User
userCountByCity = myLocalDB.calculated_userCountByCity # Count of users per city
languagePopularity = myLocalDB.calculated_languagePopularity # Count of programming language usage
memberForYears = myLocalDB.calculated_memberForYears # Number of days / milliseconds user has been a member of GitHub
originalRepos = myLocalDB.calculated_originalRepoCount
forkedRepos = myLocalDB.calculated_forkedRepoCount
mongoDBUsersCollection = myLocalDB.githubRTPUsers
userReposCollection = myLocalDB.githubRTPUsersRepos_Refresh1 # userRepos Collection
activeUsersCollection = myLocalDB.testCollection
githubRTPUsersPullReqs = myLocalDB.githubRTPUsersPullReqs
stargazersCollection = myLocalDB.calculated_totalStargazers

def shuffle_word(word):
    word = list(word)
    random.shuffle(word)
    return ''.join(word)

def repoCountByUser_BarChart():
    results = repoCountByUser.find({"count":{"$gte" : 150}})

    x = []
    y = []

    for i in results:
        shuffleID = shuffle_word(i['_id'])
        #x.append(shuffleID)
        x.append(i['_id'])
        y.append(i['count'])
        shuffleID = ''

    plotly.offline.plot({
    "data": [
        Bar(x=x, y=y)
    ],
    "layout": Layout(
        title="RTP Repository Count by User"
    )
    })

def pullReqCountByUser_BarChart():
    # results = githubRTPUsersPullReqs.find({"prcount":{"$gte" : 100}}).sort("prcount",-1)
    results = githubRTPUsersPullReqs.find().sort("prcount",-1)

    x = []
    y = []

    for i in results:
        #shuffleID = shuffle_word(i['login'])
        #x.append(shuffleID)
        x.append(i['login'])
        y.append(i['prcount'])
        # shuffleID = ''

    plotly.offline.plot({
    "data": [
        Bar(x=x, y=y)
    ],
    "layout": Layout(
        title="RTP - Number of Pull Requests by User"
    )
    })

def userCountByCity_BarChart():
    results = userCountByCity.find({"count":{"$gte" : 20}})

    x = []
    y = []

    for i in results:
        x.append(i['_id'])
        y.append(i['count'])

    plotly.offline.plot({
    "data": [
        Bar(x=x, y=y,
            marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5
            ),
        ),
        opacity=0.6)
    ],
    "layout": Layout(
        title="Number Of Users By City (User Count Greater Than 20)",
        annotations=[
        dict(
            x=xi,
            y=yi,
            text=str(yi),
            xanchor='center',
            yanchor='bottom',
            showarrow=False,
        ) for xi, yi in zip(x, y)]
    )
    })

def languagePopularity_BarChart():
    results = languagePopularity.find({"$and":[{"_id" : {"$ne":None} },{"count":{"$gte" : 100}}]}).sort("count",-1)

    x = []
    y = []

    for i in results:
        x.append(i['_id'])
        y.append(i['count'])

    plotly.offline.plot({
    "data": [
        Bar(x=x, y=y)
    ],
    "layout": Layout(
        title="Top GitHub Programming Languages in RTP"
    )
    })

def membershipStatistics_BarChart():
    results = memberForYears.find({"diff_days":{"$gte" : 7.5}}).sort("diff_days",-1)

    x = []
    y = []

    count=0
    for i in results:
        x.append(shuffle_word(i['item']))
        y.append(i['diff_days'])
        count+=1
    print count

    plotly.offline.plot({
    "data": [
        Bar(x=x, y=y)
    ],
    "layout": Layout(
        title="RTP Users - Number of Years as GitHub Member"
    )
    })

def active_oldUsers():
    d = datetime.datetime(2015, 8, 10, 12)
    results = memberForYears.find({"diff_days":{"$gte" : 7}}).sort("diff_days",-1)

    count = 0
    for i in results:
        totalCommits = activeUsersCollection.find({"owner_login":i['item']})
        for x in totalCommits:
            if x['last_commit_date'] > d:
                print 'Active: ', x['owner_login'], ' ', x['project_name'], ' ', x['last_commit_date']
                count += 1
        # print 'UserID: ', i['item'], '# Years: ', i['diff_days']

def originalVSForked_BarChart():
    # oRepos = originalRepos.find({'_id':'pixbit'})
    # fRepos = forkedRepos.find({'_id':'pixbit'})
    oRepos = []
    results = repoCountByUser.find({"count":{"$gte" : 100}},{"_id":1})
    for o in results:
        oRepos.append(originalRepos.find({"_id":o['_id']}).sort("_id",-1))
        # fRepos = forkedRepos.find({"count":{"$gte" : 10}}).sort("_id",-1)

    for k in oRepos:
        print k['count']

        '''
    x1 = []
    y1 = []

    for o in oRepos:
        x1.append(o['_id'])
        y1.append(o['count'])

    x2 = []
    y2 = []

    for f in fRepos:
        x2.append(f['_id'])
        y2.append(f['count'])

    trace1 = Bar(x=x1,y=y1,name='Original Repos')
    trace2 = Bar(x=x2, y=y2, name='Forked Repos')

    data = [trace1, trace2]
    layout = Layout(barmode='group')

    fig = Figure(data=data, layout=layout)

    plotly.offline.plot(fig)
'''

def avg_number_public_repos_byType(thetype):
    filteredUsersByType = mongoDBUsersCollection.find({"type":thetype},{"login":1} )

    myList = []
    x = []

    for i in filteredUsersByType:
        ##### Use the following to get where the user is owner #####
        #myList.append(userReposCollection.find({"owner.login":i['login']}))
        myList = userReposCollection.find({"owner.login":i['login']})

        for k in myList:
            # print k['name']
            x.append(k['name'])

    print x.__len__()

def project_commits_by_owner():
    results = activeUsersCollection.find({"commit_count":{"$gte" : 1000}}).sort("commit_count",-1)

    x = []
    y = []

    for i in results:
        x.append(i['owner_login'])
        y.append(i['commit_count'])

    plotly.offline.plot({
    "data": [
        Bar(x=x, y=y)
    ],
    "layout": Layout(
        title="Commits to Original Projects By Owner (>1000 commits)"
    )
    })

def project_commits_by_owner_6months():
    d = datetime.datetime(2015, 8, 10, 12)
    results = activeUsersCollection.find({"commit_count":{"$gte" : 1000}, "last_commit_date" : { "$gte" : d }}).sort("commit_count",-1)

    x = []
    y = []

    for i in results:
        # x.append(shuffle_word(i['owner_login']))
        x.append(i['owner_login'])
        y.append(i['commit_count'])

    plotly.offline.plot({
    "data": [
        Bar(x=x, y=y)
    ],
    "layout": Layout(
        title="Commits to Original Projects By Owner (>1000 commits, last 6 months)"
    )
    })

def stargazers():
    results = stargazersCollection.find({"count":{"$gte" : 600}})

    x = []
    y = []

    for i in results:
        shuffleID = shuffle_word(i['_id'])
        #x.append(shuffleID)
        x.append(i['_id'])
        y.append(i['count'])
        shuffleID = ''

    plotly.offline.plot({
    "data": [
        Bar(x=x, y=y)
    ],
    "layout": Layout(
        title="RTP Users and Count of Stargazers (Where # Stargazers is greater than 100)"
    )
    })
