from selenium import webdriver
import pandas as pd
import time
import getDetails

# Base file USTechKick
# Filter the data to get required details
DataFile= pd.read_excel('USTechKick.xlsx')
DataFile= DataFile.loc[DataFile['state']=='successful']
DataFile = DataFile.loc[(DataFile['deadlineDate']>='2015') &(DataFile['deadlineDate']<='2018') ]
DataFile = DataFile.loc[(DataFile['Duration']==30)]

# Fields to retrieve
name = []
blurb = []
description = []
imageText = []
backers = []
pledge = []
goal = []
comments = []
updates = []
state = []
urls = []
gamificationGoals = []
gamificationList = []
creatorURL = []
numberOfProjectsCreated = []
creatorName = []
creatorBio = []
creatorSocialMedia = []
startDate = []
deadline = []
duration = []
currency = []

# Keep track of what's getting retrieved
ls = DataFile.shape
dfno = 0
crno = 0

# Get Project level details
for each_url in DataFile['urls']:
    browser = webdriver.Chrome()
    try:
        print("Getting Data :" + str(dfno))
        browser.get(each_url)
        time.sleep(10)
        upd = getDetails.get_updates(browser)
        comm = getDetails.get_comments(browser)
        number_of_goals, goals, desc = getDetails.get_pledge_goals(browser)
        imaget = getDetails.get_image_text(browser)
        print(" Data retrieved successfully" + str(dfno))
    except:
        upd = 'NA'
        comm = 'NA'
        number_of_goals = 'NA'
        goals = 'NA'
        desc = 'NA'
        imaget = 'NA'
        print(" Data not retrieved successfully" + str(dfno))

    updates.append(upd)
    comments.append(comm)
    gamificationGoals.append(number_of_goals)
    gamificationList.append(goals)
    description.append(desc)
    imageText.append(imaget)
    dfno = dfno + 1
    browser.close()

# Get Creator Info
for each_url in DataFile['CreatorURL']:
    browser = webdriver.Chrome('/Users/shreyanavelkar/Downloads/chromedriver')
    try:
        print("Getting Data :" + str(crno))
        created_projects, creator_bio, creator_sm = getDetails.get_creator_info(each_url,browser)
        print(" Data retrieved successfully" + str(crno))
    except:
        created_projects = 'NA'
        creator_bio = 'NA'
        creator_sm = 'NA'
        print(" Data not retrieved successfully" + str(crno))

    numberOfProjectsCreated.append(created_projects)
    creatorBio.append(creator_bio)
    creatorSocialMedia.append(creator_sm)
    crno = crno + 1
    browser.close()

name = DataFile['name']
blurb = DataFile['blurb']
backers = DataFile['backers_count']
pledge = DataFile['converted_pledged_amount']
goal = DataFile['goal']
state = DataFile['state']
urls = DataFile['urls']
creatorURL = DataFile['CreatorURL']
creatorName = DataFile['CreatorName']
startDate = DataFile['LaunchDate']
deadline = DataFile['deadlineDate']
duration = DataFile['Duration']
currency = DataFile['current_currency']


# Creating the Data File
KickstarterData = pd.DataFrame({'Name': name, 'Text': blurb, 'State': state, 'Pledged Amount': pledge, 'Goal': goal,
                                'Comments': comments, 'Updates': updates, 'Backers': backers,
                                'Project Description': description,
                                'Images Text': imageText, 'Creator Link': creatorURL, 'Creator Name': creatorName,
                                'Created Projects': numberOfProjectsCreated, 'CreatorBio': creatorBio,
                                'creatorSocialMedia': creatorSocialMedia,
                                'Gamification goals': gamificationGoals, 'Gamification Pledges': gamificationList,
                                'Launch Date': startDate, 'Deadline': deadline, 'Currency': currency})

KickstarterData.to_excel('KickStarterData.xlsx')
