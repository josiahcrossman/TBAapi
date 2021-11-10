import requests
import json
import pprint
import math
# MAIN FUNCTION
def offenseiveScore(individual, team, comp):
    finalVal = {
        "team": team,
        "climb%": 0,
        "auton%": 0,
        "knownScoreAverage":0,
        "autoShotsScore":0,
        "unknownScoreAverage":0,
        "plusMinus": 0
    }
    r = requests.get("https://www.thebluealliance.com/api/v3/team/"+team+"/event/"+comp+"/matches", headers={'X-TBA-Auth-Key': 'Zsss576vw4WjfhQB8wmoIrX1I9V7c7z8wD36YSll1tsfYFA7JdcZSZ4iJjHKDi0P'})
    a = r.json()
    # Initializing variables
    # number of matches in which the team climbed
    climbCount = 0
    # number of matches in which the team did teleop
    teleopCount = 0
    # list of traceable scores for each match
    confirmedScore = []
    # list of untracable scores for each match
    unknownScore = []
    averagePlusMinus = []
    climbList = []
    autoList = []
    autoScoreList = []
    # loops through each match
    for i in range(len(a)):
        blueAll = a[i]["alliances"]["blue"]["team_keys"]
        redAll = a[i]["alliances"]["red"]["team_keys"]
        # figures out team and robot number
        if blueAll.count(team) > 0:
            teamNum = blueAll.index(team) + 1
            color = "blue"
            oppColor = "red"
        else:
            teamNum = redAll.index(team) + 1
            color = "red"
            oppColor = "blue"
        # assumes bot didn't climb and played offense
        didClimb = False
        didAuto = False
        # getting team and individual scores for the match
        if a[i]["comp_level"] == "qm":
            individScore = 0
            scoreBreakdown = a[i]["score_breakdown"]
            averagePlusMinus.append(scoreBreakdown[color]["totalPoints"]-scoreBreakdown[oppColor]["totalPoints"])
            scoreBreakdown = a[i]["score_breakdown"][color]
            totalScore = scoreBreakdown["totalPoints"]
            totalScore -= int(scoreBreakdown["autoPoints"]-scoreBreakdown["autoInitLinePoints"])
            autoScoreList.append(int(scoreBreakdown["autoPoints"]-scoreBreakdown["autoInitLinePoints"]))
            # loops through each team and checks number, subtracts score from total and gets climb points
            for x in range(3):
                if scoreBreakdown["initLineRobot" + str(x+1)] == "Exited":
                    totalScore -= 5
                    if x+1 == teamNum:
                        individScore += 5
                        teleopCount += 1
                        didAuto = True
                if scoreBreakdown["endgameRobot" + str(x+1)] == "Hang":
                    totalScore -= 25
                    if x+1 == teamNum:
                        individScore += 25
                        climbCount += 1
                        didClimb = True
                        
                elif scoreBreakdown["endgameRobot" + str(x+1)] == "Park":
                    totalScore -= 5
                    if x+1 == teamNum:
                        individScore += 5
            if scoreBreakdown["endgameRungIsLevel"] == "IsLevel":
                totalScore -= 15
                if didClimb == True:
                    individScore += 15
            #makes sure all lists are the same size for looping
            if didClimb == True:
                climbList.append(True)
            else:
                climbList.append(False)
            if didAuto == True:
                autoList.append(True)
            else:
                autoList.append(False)
            if scoreBreakdown["foulPoints"] > 0:
                totalScore -= scoreBreakdown["foulPoints"]

            # adds the confirmed and unknown scores to the lists
            confirmedScore.append(individScore)
            unknownScore.append(totalScore)
        else:
            confirmedScore.append(404)
            unknownScore.append(404)
            averagePlusMinus.append(0)
            autoScoreList.append(404)
            if didClimb == True:
                climbList.append(True)
            else:
                climbList.append(False)
            if didAuto == True:
                autoList.append(True)
            else:
                autoList.append(False)

    # cycles through to calculate average scores
    individScore = 0
    totalScore = 0
    plusMinus = 0
    numOfFinals = 0 
    autoscore = 0
    # tracking scores
    for i in range(i+1):
        # makes sure match is at the qualifing level and not something else
        if (a[i]["comp_level"]) =="qm":
            individScore += confirmedScore[i]
            totalScore += unknownScore[i]
            autoscore += autoScoreList[i]
            if individual == True:
                print("Match: " + str(a[i]["match_number"]) + " plusMinus: " + str(averagePlusMinus[i]) + " climbs: " + str(climbList[i]) + " auto: " + str(autoList[i]))
        else: 
            numOfFinals += 1
        plusMinus += averagePlusMinus[i]
# changing variables in dictionary to new values
    finalVal["climb%"] = math.ceil(climbCount/(i+1-numOfFinals)*100)
    finalVal["auton%"] = math.ceil(teleopCount/(i+1-numOfFinals)*100)
    finalVal["knownScoreAverage"] = math.ceil(individScore/(i+1-numOfFinals))
    finalVal["autoShotsScore"] = math.ceil(autoscore/(i+1-numOfFinals))
    finalVal["unknownScoreAverage"] = math.ceil(totalScore/(i+1-numOfFinals))
    finalVal["plusMinus"] = math.ceil(plusMinus/(i+1-numOfFinals))
    if individual == True:
        print("Tha average plusMinus is " + str(finalVal["plusMinus"])) 
# returns json file
    if individual == False:
        return(finalVal)
# first variable is team name, second is event, and third is the matches they played defense on.
f = requests.get("https://www.thebluealliance.com/api/v3/event/2020orore/teams", headers={'X-TBA-Auth-Key': 'Zsss576vw4WjfhQB8wmoIrX1I9V7c7z8wD36YSll1tsfYFA7JdcZSZ4iJjHKDi0P'})
data = []
print("\n")
# checking for individual team analysis or group analysis
if input("individual team analysis or main event analysis? ").lower() == "individual" :
    tem = str(input("What team? Please put frc before the number. "))
    offenseiveScore(True, tem, "2020orore")
else:
    def myFunc(e):
        return e['plusMinus']
    for i in range(len(f.json())):
        team = f.json()[i]["key"]
        data.append(offenseiveScore(False, team, "2020orore"))
    data.sort(reverse=True, key=myFunc)
    for i in data:
        print(i) 


# TODO:
# edit TBA app source code?
# get data into graphs
# create weight settings