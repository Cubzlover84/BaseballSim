

''' Not sure what happened to all the planning I had and ideas, but now that I think about it making it an interactive webpage would be pretty difficult and require
# a lot of HTML, so I think it might work interestingly if I made it just so that you could open up the file and play a quick season or two. I'd have it so you could
# change lineups, pitching staffs, make substitutions etc but it really wouldnt be able to make trades or anything like that. I'd have a menu section in the code so
# that you would be able to type 'stats' or 'roster' or something and it would tell it to you. It would take a lot of time working on the simualation engine itself,
# but it would be a nice project to undertake and help me learn about python at the same time. I'd have to figure out how to store stats, sort standings, all sorts
# of stuff, but again I think it will be fun. Interface-wise it would be really simple, but that's what I would want in a simulation like this.
# Or at this point just do javascript since you've started to learn that but tbh it would take a ton of work to try and transfer stuff over from python AND have it be
# interactive and have aesthetic. So, I think I'll keep working on this for now. At this point it's much less an exercise in learing python (basically a bunch of while
# loops and whatnot) but more in the sort of problem-solving code and the whole operations research thing that you're more interested in. Sure you could probably learn
# More code but that's why you're taking webtech. 

# To-do list
      - Web Scrap for Data for all teams and/or more teams in the database
      - Add a speed rating + stolen base numbers + baserunning
          - Would require revamping the bases system
      - Real-time standings function
          - Allowing OOTP-style simming of seasons by the week or month
      - Clean up single-game stats to only show relevant info
          - Including adding pitcher linescores
      - Starting vs Relieving selection
          - If in bullpen, how to prevent double selection?
      - Adjust ratings
          - Is power too important?
    
      
      
ok bottom line outcomes are still too random. You can define probabilities but even over 600+ PA season things get a little out of wack imo. I guess with this you won't
get uber-consistent guys like Freddie Freeman who put up like the exact same numbers every year. Maybe try recording BABIP as a way to track randomness
 '''
# New Version History Starting 6.8.2020
# 6.8.2020: Significant updates to the code, including implementation of player ratings affecting outcomes, tracking some stats (HR only), added walk-off ending
# 6.10.2020: Removed redundant variable assignments and simplified the game code using functions, added season-long stat tracking for all major stats
# 6.11.2020: Data is now read from a CSVfile, ratings can be created randomly using createPlayers, runPlayerSeasons simulates x seasons for player with those ratings
# 6.16.2020: Added 2 new teams, more functions to clean up code, began implementing an algorithm to generate a random schedule
# 10.20.2020 Added a preset schedule while algo is still buggy, made major appearance upgrades to the sim, including adding linescores and detailed text scenarios
# 10.21.2020 More text upgrades, created rough approximations of real player ratings, added a test-season function for various needs, interface is now usable multiple times
# 11.09.2020 Data structure was switched from lists to dictionary, effiency improvements, basic stealing functionality, simple lineup-selecting AI, WAR calculation
# 11.24.2020 Basic pitching functionality added, simple stats (IP, Runs, ERA) recorded, outcomes are determined by both pitcher and hitter ratings



# Game Code
from time import *
from tabulate import tabulate
#from math import *
import csv
import pandas as pd
import itertools
import numpy as np

def readCSV(batters, pitchers):
    with open(batters, 'r') as data:
        data = csv.DictReader(data)
        data = list(data)
        teams = ["Chicago Cubs", "St. Louis Cardinals", "New York Yankees", "Boston Red Sox"]
        leagueData = {"Teams": {}}
        for i in range(4):
            info = {"Teamname": teams[i], "Wins": 0, "Losses":0, "Players" : {}, "Pitchers": {}}
            leagueData["Teams"][i] = info
            j = 0
            for line in data:
                if i == 0:
                    line.pop("ï»¿A")
                line["G"] = int(line["G"])
                line["PA"] = int(line["PA"])
                line["AB"] = int(line["AB"])
                line["H"] = int(line["H"])
                line["2B"] = int(line["2B"])
                line["3B"] = int(line["3B"])
                line["HR"] = int(line["HR"])
                line["SO"] = int(line["SO"])
                line["BB"] = int(line["BB"])
                line["RBI"] = int(line["RBI"])
                line["AVG"] = float(line["AVG"])
                line["OBP"] = float(line["OBP"])
                line["SLG"] = float(line["SLG"])
                line["OPS"] = float(line["OPS"])
                line["OPS+"] = float(line["OPS"])
                line["WAR"] = float(line["WAR"])
                line["SB"] = float(line["SB"])
                if line["Team"] == teams[i]:
                    leagueData["Teams"][i]["Players"][j] = line
                    j+=1
    with open(pitchers, 'r') as data:
        data = csv.DictReader(data)
        data = list(data)
        for i in range(4):
            j = 0
            for line in data:
                if i == 0:
                    line.pop("ï»¿A")
                line["G"] = int(line["G"])
                line["GS"] = int(line["GS"])
                line["IP"] = int(line["IP"])
                line["K"] = int(line["K"])
                line["HR"] = int(line["HR"])
                line["BB"] = int(line["BB"])
                line["Runs"] = int(line["Runs"])
                line["ERA"] = int(line["ERA"])
                line["Pitches"] = int(line["Pitches"])
                if line["Team"] == teams[i]:
                    leagueData["Teams"][i]["Pitchers"][j] = line
                    j+=1
    #print(leagueData)
    return leagueData

def writeCSV(file): #Re-Writes the Data to a new file for viewing
    return true

def createPlayers(leagueData): # Re-writes the 3 rating data to be random (later will also have random players too)
    import random
    for h in range(4): # Teams
        for j in range(9): # Players per team
            for i in range(3): # Each Random name
                leagueData[h][j+1][i+1] = round(random.normalvariate(55,15), 0)# Normal distribution (not just pure random)
                #leagueData[h][j+1][i+1] = 100
    return leagueData

def genSchedule(teams):
    import random
    teams = list(teams)
    gen = False
    trials = 0
    while gen == False: # While a valid schedule has not been generated
        trials +=1 # number of times generated
        homeTeam = []
        awayTeam = []
        for j in range(27): # Adds each team as the home team 81 times
            for i in teams:
                homeTeam.append(i)
                homeTeam.append(i)
                homeTeam.append(i)# Adds teams in order but 3 times to mimick a series
                data = list.copy(teams) # New List of Teams
                data.remove(i) # Removes the element where teams play against each other
                available = False
                while available == False: # If there are no games available
                    for add in data:
                        if awayTeam.count(add) < 81: # If the team being added has less than 81 scheduled
                            awayTeam.append(add)
                            awayTeam.append(add)
                            awayTeam.append(add)
                            available = True
                    available = True
        #print(len(homeTeam))

        # Verifies if the schedule is valid
        valid = 0
        for i in teams:
            #print(awayTeam.count(i))
            if awayTeam.count(i) == 81:
                valid += 1
        if valid == len(teams):
            gen = True
    random.shuffle(awayTeam)
    random.shuffle(homeTeam)
    return awayTeam, homeTeam

def showBoxScore(leagueData, awayTeamData, homeTeamData, awayBatterList, homeBatterList):
        leagueData = calcStats(leagueData)        
        print("\n")
        printData = []
        header = []
        for key in awayTeamData["Players"][0].keys():
            header.append(key)
        print(awayTeamData["Teamname"], "Box Score")
        for i in range(len(awayBatterList)):
            printData.append([])
            for stats in awayBatterList[i].values():
                printData[i].append(stats)
        print(tabulate(printData, headers = header))
        printData = []
        print(awayTeamData["Teamname"], "Box Score")
        for i in range(len(homeBatterList)):
            printData.append([])
            for stats in homeBatterList[i].values():
                printData[i].append(stats)
        print(tabulate(printData, headers = header))
        
        
def setProb(contact, power, discipline, stuff, movement, control): # Sets the probabilities of outcomes based on the batters ratings
        baseHR = 0.025 # Base values for each outcome based on league data
        base3B = 0.002
        base2B = 0.05
        base1B = 0.153
        baseBB = 0.08
        baseFO = 0.25
        baseGO = 0.245
        baseK = 0.20
        conBonus = contact - stuff # Establishes how high or below league average the value is 
        powBonus = power - movement
        disBonus = discipline - control
        probHR = baseHR + baseHR*(powBonus*0.04) # new probability is the based probability plus the bonus* a constant 
        if probHR < 0: # Prevents negative counting stats (lol)
                probHR = 0.0001
        prob3B = base3B + base3B*(conBonus*0.002 + powBonus*0.005)
        if probHR < 0:
                prob3B = 0.0001
        prob2B = base2B + base2B*(conBonus*0.01 + powBonus*0.0015)
        if prob2B < 0:
                prob2B = 0.0001
        prob1B = base1B + base1B*(conBonus*0.007)
        if prob1B < 0:
                prob1B = 0.0001
        probBB = baseBB + baseBB*(disBonus*0.027)
        if probBB < 0.025:
                probBB = 0.025
        probK = baseK + baseK*(conBonus*-0.015) #disBonus*-0.005)
        if probK < 0.05:
                probK = 0.05
        # To get the probabilities for the Ball in play, out(s), it's the total change in probability for the other outcomes split between the two
        probFO = baseFO -0.5*(probHR + prob3B + prob2B + prob1B + probBB + probK - baseHR - base3B - base2B - base1B - baseBB - baseK)
        probGO = baseGO -0.5*(probHR + prob3B + prob2B + prob1B + probBB + probK - baseHR - base3B - base2B - base1B - baseBB - baseK)
        #print(probHR + prob3B + prob2B + prob1B + probBB + probFO + probGO + probK)
        return probHR, prob3B, prob2B, prob1B, probBB, probFO, probGO, probK

def playAtBat(probHR, prob3B, prob2B, prob1B, probBB, probFO, probGO, probK):
        a = 0
        import random # Imports a random number
        a = random.uniform(0,1) # Between 1 and 0
        total = 0
        outcome = "bruh"
        '''if a < probHR: # Odds of certain events occuring in the game, tailored to batter ability
                outcome = "Homerun"
        total += probHR # Adds the running total of all events that have happened so far
        if total < a < total + prob3B: 
                outcome = "Triple"
        total += prob3B
        if total < a < total + prob2B:
                outcome = "Double"
        total += prob2B
        if total < a < total + prob1B:
                outcome = "Single"
        total += prob1B
        if total < a < total + probBB:
                outcome = "Walk"
        total += probBB       
        if total < a < total + probFO:
                outcome = "Flyout"
        total += probFO
        if total < a < total + probGO:
                outcome = "Groundout"
        total += probGO
        if total < a < total + probK:  
                outcome = "Strikeout"
        return outcome'''
        probs = [probHR, prob3B, prob2B, prob1B, probBB, probFO, probGO, probK]
        outcome = random.choices(["Homerun", "Triple", "Double", "Single", "Walk", "Flyout", "Groundout", "Strikeout"],weights = probs)[0]
        return outcome

def scoreRuns(runs, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher):
    if topOrBottom == "Top":
        awayRuns = awayRuns + runs
        linescore[0][halfInning//2+1] += runs
        if isLive == True:
            if awayRuns > homeRuns:
                if awayRuns == runs:
                    print(awayTeam, "take a ", awayRuns, "-", homeRuns, "lead")
                else:
                    print(awayTeam,"extend their lead to", awayRuns, "-", homeRuns)
            elif homeRuns > awayRuns:
                print("That will cut the lead to", homeRuns, "-", awayRuns)
            else:
                print("The game is tied", awayRuns, "-", homeRuns)
    else:
        homeRuns = homeRuns + runs
        linescore[1][halfInning//2+1] += runs
        if isLive == True:
            if awayRuns > homeRuns:
                print(homeTeam, "cut the lead to", awayRuns, "-", homeRuns)
            elif homeRuns > awayRuns:
                if homeRuns == runs:
                    print(homeTeam, "score", runs,"to make it", homeRuns, "-", awayRuns)
                else:
                    print(homeTeam, "add on to make it", homeRuns, "-", awayRuns)
            else:
                print("The game is tied", awayRuns, "-", homeRuns)

    currentPitcher["Runs"] += runs
    currentBatter["RBI"] += runs
    return awayRuns, homeRuns, currentBatter

def calcStats(leagueData):
    for j in range(4):
        for i in range(len(leagueData["Teams"][j]["Players"])):
            batter = leagueData["Teams"][j]["Players"][i]
            if batter["PA"] != 0:
                avg = batter["H"]/batter["AB"]
                batter["AVG"] = round(avg, 3)
                obp = (batter["H"]+batter["BB"])/batter["PA"]
                batter["OBP"] = round(obp, 3)
                slg = (batter["2B"]*2 + batter["3B"]*3 + batter["HR"]*4 + (batter["H"] - batter["2B"] - batter["3B"] - batter["HR"]))/batter["AB"]
                batter["SLG"] = round(slg, 3)
                batter["OPS"] = round(obp + slg, 3)
                batter["OPS+"] = 100*round((obp/0.315 + slg/0.396 -1), 2)
                batter["WAR"] = round(((batter["OPS+"] -100)/12 + 2)*(batter["PA"]/650),1)
        for i in range(len(leagueData["Teams"][j]["Pitchers"])):
            pitcher = leagueData["Teams"][j]["Pitchers"][i]
            if pitcher["IP"] != 0:
                era = pitcher["Runs"]*9/pitcher["IP"]
                pitcher["ERA"] = round(era, 2)
    return leagueData

def setLineups(awayTeamData, homeTeamData):
    import random
    awayBatterList = {}
    weightedRatings = []
    nums = []
    for i in awayTeamData["Players"].items():
        weightedRatings.append((int(i[1]["Contact"]) + int(i[1]["Power"]) + int(i[1]["Discipline"]))/3)
    total = sum(weightedRatings)
    for i in range(len(weightedRatings)):
        weightedRatings[i] = weightedRatings[i]/total
        nums.append(i)
    a = np.random.choice(nums,9,p = weightedRatings, replace = False) # Now that there are more than 9 players it has to select them for a game, will eventually be AI-like
    for i in range(len(a)):
        num = a[i]
        awayBatterList[i] = awayTeamData["Players"][num]
        awayTeamData["Players"][num]["G"] +=1 # Everyone in the lineup gets a game credited to them

    homeBatterList = {} # 
    weightedRatings = []
    nums = []
    for i in homeTeamData["Players"].items():
        weightedRatings.append((int(i[1]["Contact"]) + int(i[1]["Power"]) + int(i[1]["Discipline"]))/3)
    total = sum(weightedRatings)
    for i in range(len(weightedRatings)):
        weightedRatings[i] = weightedRatings[i]/total
        nums.append(i)
    b = np.random.choice(nums,9, p =weightedRatings, replace = False)
    for i in range(len(b)):
        num = b[i]
        homeBatterList[i] = homeTeamData["Players"][num]
        homeTeamData["Players"][num]["G"] +=1

    awayPitcherList = []
    homePitcherList = []
    for i in awayTeamData["Pitchers"].values(): # Adds pitchers to an array
        awayPitcherList.append(i)
    for i in awayPitcherList: # Reset Pitches to 0 every game (duh)
        i["Pitches"] = 0
    awayStarters = awayPitcherList[0:5] # Selects top 5 as starters and selects a random one
    awayRelievers = awayPitcherList[5:] # Adds the rest to the pen
    awayPitcher = random.choice(awayStarters) # in the future needs to be an ordered sequence
    awayPitcher["G"] += 1
    awayPitcher["GS"] +=1
    for i in homeTeamData["Pitchers"].values():
        homePitcherList.append(i)
    for i in homePitcherList:
        i["Pitches"] = 0
    homeStarters = homePitcherList[0:5]
    homeRelievers = homePitcherList[5:]
    homePitcher = random.choice(homeStarters)
    homePitcher["G"] += 1
    homePitcher["GS"] +=1
    return awayBatterList, homeBatterList, awayTeamData, homeTeamData, awayPitcher, homePitcher, awayStarters, awayRelievers, homeStarters, homeRelievers

def playGame (awayTeam,homeTeam, playSpeed, isLive, leagueData):
        import time
        import random
        
        # Getting gameplay data for the teams playing
        awayTeamData = leagueData["Teams"][awayTeam] #Two-long array of team and batters
        awayTeam = awayTeamData["Teamname"] # Then sets the team name and all the batters
        homeTeamData = leagueData["Teams"][homeTeam]    
        homeTeam = homeTeamData["Teamname"]
        
        awayBatterList, homeBatterList, awayTeamData, homeTeamData, awayPitcher, homePitcher, awayStarters, awayRelievers, homeStarters, homeRelievers = setLineups(awayTeamData, homeTeamData)
        #Start of Actual Simulation
        homeBatterNumber = 1 #Starts with leadoff hitter
        awayBatterNumber = 1
        currentBatter = 0 #The batter at the plate, used to determine stats
        currentPitcher = 0 # Will swap between away pitcher and home pitcher, with subs based on pitch count eventually
        halfInning = 0
        maxInning = 18 # The maximum half inning that the game will be played to, which is typically 18 (18/2 = 9 innings) unless it is a tie game
        homeRuns = 0 # Not to be confused with balls hit out of the ballpark; the number of runs scored by the home team
        awayRuns = 0
        homeHits = 0
        awayHits = 0
        linescore = [[awayTeam],[homeTeam]]
        pitches = 0
        
        if isLive == True:
                print("\n")
                time.sleep(playSpeed)
                print("Here are the lineups for today's game")
                print("Away Team:", awayTeam)
                for i in range(9):
                    print(awayBatterList[i]["Name"])
                time.sleep(playSpeed)
                print("\n")
                print("Home Team:", homeTeam)
                for i in range(9):
                    print(homeBatterList[i]["Name"])
                print("\n")
                time.sleep(playSpeed*2)
                print("Let's get ready for some baseball!")
                time.sleep(playSpeed)
        while halfInning < maxInning: #18 half-innings = 9 innings total
                if halfInning%2 == 0: #Even numbers = Top of inning, Odd Numbers = bottom of inning
                        topOrBottom = "Top"
                        linescore[0].append(0) # Adds a new column to the linescore
                        linescore[1].append(0)
                        if isLive == True: # Number suffixes
                                if halfInning//2 == 0:
                                    t = "st"
                                elif halfInning//2 == 1:
                                    t = "nd"
                                elif halfInning//2 == 2:
                                    t = "rd"
                                else:
                                    t = "th"
                                inning = str(halfInning//2 + 1)
                                print("\n")
                                print("Top of the", inning + t) #Determines inning by dividing the half inning by 2, then adding one so it starts at the 1st inning
                else:
                        topOrBottom = "Bottom"
                        if isLive == True:
                                if halfInning//2 == 0:
                                    t = "st"
                                elif halfInning//2 == 1:
                                    t = "nd"
                                elif halfInning//2 == 2:
                                    t = "rd"
                                else:
                                    t = "th"
                                inning = str(halfInning//2 + 1)
                                print("\n")
                                print("Bottom of the", inning + t)
                outs = 0
                runnerOnFirst = False #Sets all bases empty at the start of each inning
                runnerOnSecond = False
                runnerOnThird = False

                while outs < 3: # While there are less then 3 outs (i.e. in the inning)
                        if isLive == True:
                                time.sleep(2*playSpeed)
                                if runnerOnFirst == False and runnerOnSecond == False and runnerOnThird == False:
                                    basesText = random.choice(["Bases empty", "Nobody on", "Bases clear"])
                                elif runnerOnFirst == False and runnerOnSecond == False and runnerOnThird != False:
                                    basesText = random.choice(["Runner at third", "Runner at third, watch for the wild pitch", "Runner leads off from 3rd"])
                                elif runnerOnFirst == False and runnerOnSecond != False and runnerOnThird == False:
                                    basesText = random.choice(["Chance to score here with a runner on 2nd", "Runner on 2nd", "One in scoring postion"])
                                elif runnerOnFirst != False and runnerOnSecond == False and runnerOnThird == False:
                                    if outs < 2:
                                        basesText = random.choice(["Runner on first", "One aboard", "Runner on, could try to steal", "Double play chance"])
                                    else:
                                        basesText = random.choice(["Runner on first", "One aboard", "Runner on, could try to steal", "Runner On"])
                                elif runnerOnFirst == False and runnerOnSecond != False and runnerOnThird != False:
                                    basesText = random.choice(["Big spot with two in scoring position", "Two runners on", "2nd and third here"])
                                elif runnerOnFirst != False and runnerOnSecond != False and runnerOnThird == False:
                                    basesText = random.choice(["Runners on first and second", "Looking to rally here with two on", "Two on"])
                                elif runnerOnFirst != False and runnerOnSecond == False and runnerOnThird != False:
                                    basesText = random.choice(["First and third", "Runners at the corners"])
                                if runnerOnFirst != False and runnerOnSecond != False and runnerOnThird != False:
                                    basesText = random.choice(["Bases Juiced", "Bases loaded", "Bags are full"])
                                    if outs < 2:
                                        basesText = random.choice(["Bases Juiced", "Bases loaded, a double play would be huge here", "Bags are full"])
                                    else:
                                        basesText = random.choice(["Bases Juiced", "Bases loaded", "Bags are full"])
                        if topOrBottom == "Top":
                                currentBatter = awayBatterList[awayBatterNumber-1]
                                currentPitcher = homePitcher
                        else:
                                currentBatter = homeBatterList[homeBatterNumber-1]
                                currentPitcher = awayPitcher
                                
                        if isLive == True:
                                print("\n" + basesText)
                                time.sleep(playSpeed)
                                text = ["is at the plate", "steps up", "gets ready to hit", "steps into the box", "adjusts his batting gloves"]
                                print(currentBatter["Name"], random.choice(text))
                                time.sleep(playSpeed)
                                print(currentPitcher["Name"], "is on the mound")
                                #if playSpeed != 1 and isLive == True:
                                    #pause = input("")
                                print(random.choice(["Here's the pitch..", "The windup, and the delivery..", "The pitcher fires...", "Here it comes..", "The full-count delivery..."]))
                                time.sleep(playSpeed*2) # Extra delay before the ball is hit

                        # Steal Mechanism
                        
                        if runnerOnFirst == True and runnerOnSecond == False:
                            z= random.uniform(0,1)
                            if z < 0.2:
                                if isLive == True:
                                    print(random.choice(["Runner goes...", "He takes off from first...", "He'll try to steal!"]))
                                    time.sleep(playSpeed)
                                a = random.uniform(0,1)
                                if a < 0.7:
                                    if isLive == True:
                                        print("Safe!")
                                    runnerOnFirst = False
                                    runnerOnSecond = True
                                    currentBatter["SB"] +=1
                                else:
                                    if isLive == True:
                                        print("Out!")
                                    outs = outs + 1
                                    runnerOnFirst = False
                                time.sleep(playSpeed)
                                if outs < 3: # If the inning did not end on a steal
                                    if isLive == True:
                                        print("Let's try this again.")
                                        time.sleep(playSpeed)
                                        print(random.choice(["Here's the pitch..", "The windup, and the delivery..", "The pitcher fires...", "Here it comes..", "The full-count delivery..."]))
                                        time.sleep(playSpeed)
                        # Start of all the game code
                        # First it sets the outcomes based on the batter
                        # Then creates tiers of results based on rng (like a stacked frequency chart)
                        # Or not guess we used a new random choice function which works the exact same way

                        probHR, prob3B, prob2B, prob1B, probBB, probFO, probGO, probK = setProb(float(currentBatter["Contact"]), float(currentBatter["Power"]), float(currentBatter["Discipline"]), float(currentPitcher["Stuff"]), float(currentPitcher["Movement"]), float(currentPitcher["Control"]))
                        outcome = playAtBat(probHR, prob3B, prob2B, prob1B, probBB, probFO, probGO, probK)
                        if outs == 3: # If the inning ends on a baserunning mistake the AB will not happen
                            outcome = "steal"
                        currentPitcher["Pitches"] += random.choice([1,2,3,4,5,6])

                        if outcome == "Flyout": # Inputs sacrifice flies and other base runner movement from flyouts
                                if isLive == True:
                                    print(random.choice(["Hit in the air to", "Popped up to", "Fly ball towards", "Line drive to"]), random.choice(['left', 'center', 'right', 'left-center', 'right-center']))
                                    time.sleep(playSpeed)
                                    print(random.choice(["Gonna be an easy play", "Routine", "Outfielder dives... and makes a great catch!"]))
                                    #time.sleep(playSpeed)
                                    #print(outcome)
                                currentBatter["PA"] += 1
                                currentBatter["AB"] += 1
                                if runnerOnFirst == False:
                                    if runnerOnSecond == False:
                                        if runnerOnThird == False: # Bases Empty
                                            outs = outs + 1
                                        else: # Runner on third that can score from a sac fly
                                            if outs < 2:
                                                if isLive == True:
                                                        time.sleep(playSpeed)
                                                        print("Runner tags... and scores!")
                                                        time.sleep(playSpeed)
                                                        print("Sacrifice Fly!")
                                                        time.sleep(playSpeed)
                                                awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore,currentPitcher)
                                                outs = outs + 1
                                                runnerOnThird = False
                                            else:
                                                outs = outs + 1 
                                    else: # Runner on 2nd but not first
                                        if runnerOnThird == False: # Third is open so the runner moves to 3rd on a flyout
                                            runnerOnSecond = False
                                            runnerOnThird = True
                                            outs = outs + 1 
                                        else: # 2nd and third, both runners advance
                                            if outs < 2:
                                                if isLive == True:
                                                        time.sleep(playSpeed)
                                                        print("Runner tags... and scores!")
                                                        time.sleep(playSpeed)
                                                        print("Sacrifice Fly!")
                                                        time.sleep(playSpeed)
                                                        print("Runner on second also advances")
                                                        time.sleep(playSpeed)
                                                awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                                outs = outs + 1
                                                runnerOnSecond = False
                                                runnerOnThird = True
                                            else: # If 2 outs, no runner changes (they will be reset anyway)
                                                outs = outs + 1
                                else: # Runner on first
                                    if runnerOnSecond == False:
                                        if runnerOnThird == False: # Just a runner on first, nothing happens
                                                outs = outs + 1    
                                        else: # First and third
                                            if outs < 2:
                                                if isLive == True:
                                                        time.sleep(playSpeed)
                                                        print("Runner tags... and scores!")
                                                        time.sleep(playSpeed)
                                                        print("Sacrifice Fly!")
                                                        time.sleep(playSpeed)
                                                awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                                outs = outs + 1
                                                runnerOnThird = False
                                            else:
                                                outs = outs + 1 
                                    else:# First and 2nd
                                        if runnerOnThird == False: # 3rd is open so runner on 2nd advances
                                            if outs < 2:
                                                outs = outs + 1
                                                if isLive == True:
                                                    time.sleep(playSpeed)
                                                    print("Runner tags....safe at third")
                                                runnerOnSecond = False
                                                runnerOnThird = True
                                            else:
                                                outs = outs + 1 
                                        else: # Bases loaded
                                            if outs < 2:
                                                if isLive == True:
                                                        time.sleep(playSpeed)
                                                        print("Runner tags... and scores!")
                                                        time.sleep(playSpeed)
                                                        print("Sacrifice Fly!")
                                                        time.sleep(playSpeed)
                                                        print("Runner on second also advances")
                                                        time.sleep(playSpeed)
                                                awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                                outs = outs + 1
                                                runnerOnFirst = True
                                                runnerOnSecond = False
                                                runnerOnThird = True # 3rd stays true here even if technically the runners are different (will be updated in the future)
                                            else:
                                                outs = outs + 1
                                                
                        elif outcome == "Groundout": #Double Plays and other baserunner movements from groundouts
                            currentBatter["PA"] += 1
                            currentBatter["AB"] += 1
                            if isLive == True:
                                #time.sleep(playSpeed)
                                direction = random.choice(['first', 'second', 'short', 'third', 'the pitcher'])
                                print(random.choice(['Grounded to', 'Hit hard but right to', 'Chopped toward', 'Tapped softly to']), direction)
                            if runnerOnFirst == False:
                                if runnerOnSecond == False:
                                    if runnerOnThird == False: # Bases empty, nothing happens
                                        if isLive == True:
                                                time.sleep(playSpeed)
                                                print(random.choice(["Routine", "Fires to first for an easy out", "The throw is close but gets him by a step!"]))
                                        outs = outs + 1
                                    else: # Runner just on third
                                        if outs < 2:
                                            if random.uniform(0,1) < 0.5:
                                                if isLive == True:
                                                    time.sleep(playSpeed)
                                                    print("Runner breaks for home... and scores!")
                                                    time.sleep(playSpeed)
                                                awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                                outs = outs + 1
                                                runnerOnFirst = False
                                                runnerOnSecond = False
                                                runnerOnThird = False
                                            else:
                                                
                                                outs += 1 
                                        else: # If two outs
                                            outs = outs + 1 
                                else: # Runner on 2nd
                                    if runnerOnThird == False: # If third is open, runner advances to third 
                                        runnerOnSecond = False
                                        runnerOnThird = True
                                        if isLive == True:
                                                time.sleep(playSpeed)
                                                print(random.choice(["Routine", "Fires to first for an easy out", "The throw is close but gets him by a step!"]))
                                        outs = outs + 1 
                                    else: # Runners on 2nd and third
                                        if outs < 2:
                                            if isLive == True:
                                                time.sleep(playSpeed)
                                                print("Runner breaks for home... and scores!")
                                                time.sleep(playSpeed)
                                            awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                            outs = outs + 1
                                            runnerOnSecond = False
                                            runnerOnThird = True # Different runners but result is the same
                                        else:
                                            outs = outs + 1 
                            else: # Runner on first
                                if runnerOnSecond == False:
                                    if runnerOnThird == False: # Just on first
                                        if outs < 2:
                                            outs = outs + 2
                                            if isLive == True:
                                                    time.sleep(playSpeed)
                                                    print("They'll try to turn it...")
                                                    time.sleep(playSpeed)
                                                    print("Double Play!")
                                                    time.sleep(playSpeed)
                                            runnerOnFirst = False
                                        else: # No double play with 2 outs
                                            if isLive == True:
                                                time.sleep(playSpeed)
                                                print(random.choice(["Routine", "Fires to first for an easy out", "The throw is close but gets him by a step!"]))
                                            outs = outs + 1
                                            runnerOnFirst = False    
                                    else: # Runner on first and third
                                        if outs == 0: # Run will score on a double play
                                            outs = outs + 2
                                            if isLive == True:
                                                    time.sleep(playSpeed)
                                                    print("Runner breaks for home..")
                                                    time.sleep(playSpeed)
                                                    print("They'll try to turn it...")
                                                    time.sleep(playSpeed)
                                                    print("Double Play!")
                                                    time.sleep(playSpeed)
                                                    print("But a run scores")
                                                    time.sleep(playSpeed)
                                            awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                            runnerOnFirst = False
                                            runnerOnSecond = False
                                            runnerOnThird = False   
                                        elif outs == 1:
                                            if isLive == True:
                                                    time.sleep(playSpeed)
                                                    print("They'll try to turn it...")
                                                    time.sleep(playSpeed)
                                                    print("Double Play!")
                                                    time.sleep(playSpeed)
                                            outs = outs + 2
                                        else:
                                            if isLive == True:
                                                time.sleep(playSpeed)
                                                print(random.choice(["Routine", "Fires to first for an easy out", "The throw is close but gets him by a step!"]))
                                            outs = outs + 1
                                            
                                            
                                else: # Runner on first and 2nd to start
                                    if runnerOnThird == False: 
                                        if outs < 2:
                                            if isLive == True:
                                                    time.sleep(playSpeed)
                                                    print("They'll try to turn it...")
                                                    time.sleep(playSpeed)
                                                    print("Double Play!")
                                                    if outs == 0:
                                                        time.sleep(playSpeed)
                                                        print("Runner advances to third")
                                            outs = outs + 2
                                            runnerOnFirst = False
                                            runnerOnSecond = False
                                            runnerOnThird = True
                                        else:
                                            outs = outs + 1 
                                    else: # Bases loaded
                                        if outs == 0:
                                            outs = outs + 2 # Changed from 1 to 2 outs added
                                            if isLive == True:
                                                    time.sleep(playSpeed)
                                                    print("They'll try to turn it...")
                                                    time.sleep(playSpeed)
                                                    print("Double Play!")
                                                    time.sleep(playSpeed)
                                                    print("Runner advances to third")
                                                    time.sleep(playSpeed)
                                            awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                            runnerOnFirst = False
                                            runnerOnSecond = False
                                            runnerOnThird = True
                                        elif outs == 1:
                                            outs = outs + 2
                                            if isLive == True:
                                                    time.sleep(playSpeed)
                                                    print("They'll try to turn it...")
                                                    time.sleep(playSpeed)
                                                    print("Double Play!")
                                        else:
                                            outs = outs + 1 
                        elif outcome == "Strikeout":
                            if isLive == True:
                                print(random.choice(['Swing and a miss!', 'Got him swinging!', "Got him looking!", "Called Strike Three!"]))
                                time.sleep(playSpeed)
                                print(random.choice([currentBatter["Name"].split()[0] + " goes down on strikes", "That'll go in as a K", currentBatter["Name"].split()[1] + " strikes out"]))
                            currentBatter["PA"] += 1 
                            currentBatter["AB"] += 1
                            currentBatter["SO"] += 1
                            currentPitcher["K"] += 1
                            outs = outs + 1 # If the batter makes an out, the number of outs in the inning increases by one
                        elif outcome == "Single":
                            if isLive == True:
                                print(random.choice(["Hit hard", "Line drive", "Blooper"]), random.choice(["to left", "up the middle", "to right"]))
                                time.sleep(playSpeed)
                                print(random.choice(["That's a basehit", "He'll be on board with a single", currentBatter["Name"].split()[1] + " with a base knock"]))
                            currentBatter["PA"] += 1
                            currentBatter["AB"] += 1
                            currentBatter["H"] += 1
                            if topOrBottom == "Top":
                                awayHits = awayHits + 1
                            else:
                                homeHits = homeHits + 1
                            if runnerOnFirst == False: # Whether or not a runner is on first base
                                if runnerOnSecond == False: # Whether or not a runner is on second base
                                    if runnerOnThird == False: # Whether or not a runner is on third base
                                        runnerOnFirst = True # Sets the runners at their bases based on the outcome
                                    else: # Runner on third
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI single for " + currentBatter["Name"], "That drives in a run!", "One run will score"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = True
                                        runnerOnSecond = False
                                        runnerOnThird = False
                                else: # Runner on 2nd, not first
                                    if runnerOnThird == False: # Runner will always score from 2nd (will be changed later)
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI Single for " + currentBatter["Name"], "That drives in a run!", "One run will score"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = True
                                        runnerOnSecond = False
                                        runnerOnThird = False
                                    else: # Runners on 2nd and third, 2 runs will score
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["2-run Single for " + currentBatter["Name"], "That drives in 2 runs!", "One run will score... here comes another!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(2, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = True
                                        runnerOnSecond = False
                                        runnerOnThird = False
                            else: # Runner on first
                                if runnerOnSecond == False:
                                    if runnerOnThird == False:
                                        runnerOnFirst = True
                                        runnerOnSecond = True
                                        runnerOnThird = False
                                    else: # Runner on first and third: run scores, runner advances
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI Single for " + currentBatter["Name"], "That drives in a run!", "One run will score"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = True
                                        runnerOnSecond = True
                                        runnerOnThird = False
                                else: # Runner on first and 2nd 
                                    if runnerOnThird == False:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI Single for " + currentBatter["Name"], "That drives in a run!", "One run will score"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = True
                                        runnerOnSecond = True
                                        runnerOnThird = False
                                    else: # Bases Loaded
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["2-run Single for " + currentBatter["Name"], "That drives in a pair!", "Here comes one... then another!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(2, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = True
                                        runnerOnSecond = True
                                        runnerOnThird = False
                        elif outcome == "Walk":
                            if isLive == True:
                                a = random.uniform(0,1)
                                if a > 0.9:
                                    print("And it hits him in the " + random.choice(["arm", "leg", "head", "foot", "balls!"]))
                                    time.sleep(playSpeed)
                                    print(currentBatter["Name"].split()[0] + " will limp to first")
                                else:
                                    print(random.choice(["Looks at a pitch outside...", "Checks his swing...", "That one misses badly"]), random.choice(["and he'll take his base", "for Ball 4"]))
                                    time.sleep(playSpeed)
                                    print(currentBatter["Name"].split()[1] + random.choice([" draws the walk", " takes the free pass", " is on board"]))
                            currentBatter["PA"] += 1
                            currentBatter["BB"] += 1
                            currentPitcher["BB"] += 1
                            if runnerOnFirst == False:
                                if runnerOnSecond == False:
                                    if runnerOnThird == False: # Nobody on base
                                        runnerOnFirst = True
                                    else: # Runner on third
                                        runnerOnFirst = True
                                else: # Runner on 2nd
                                    if runnerOnThird == False:
                                        runnerOnFirst = True
                                        runnerOnSecond = True
                                    else: # 2nd and third -> bases loaded
                                        runnerOnThird = True
                            else: # Runner on first
                                if runnerOnSecond == False:
                                    if runnerOnThird == False: # Advances one base
                                        runnerOnSecond = True
                                    else: # First and third -> bases loaded
                                        runnerOnFirst = True
                                        runnerOnSecond = True
                                        runnerOnThird = True
                                else: # First and 2nd
                                    if runnerOnThird == False:
                                        runnerOnThird = True
                                    else:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice([currentBatter["Name"] + " walks in a run!", "A run will score"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = True
                                        runnerOnSecond = True
                                        runnerOnThird = True
                        elif outcome == "Double":
                            if isLive == True:
                                direction = random.choice(["left", "center field", "right", "left-center", "the right-center gap"])
                                DoubleType = random.choice(["grounder", "liner", "flyball"])
                                if DoubleType == "grounder":
                                    time.sleep(playSpeed)
                                    print("hit on the ground to", random.choice(["first", "third"]))
                                    time.sleep(playSpeed)
                                    print(random.choice(["and through! It's down the line in to the corner", "Fair Ball! Might be extra bases"]))
                                elif DoubleType == "liner":
                                    time.sleep(playSpeed)
                                    print(random.choice(["line drive to", "hit hard into"]), direction)
                                    time.sleep(playSpeed)
                                    print(random.choice(["It'll get down", "Could be extra bases"]))
                                else:
                                    time.sleep(playSpeed)
                                    print(random.choice(["High fly ball into", "Hit well into", "In the air towards"]), direction)
                                    time.sleep(playSpeed)
                                    print(random.choice(["Going back it is.... Off the wall!", "It'll get down!", "it one-hops the wall"]))
                                time.sleep(playSpeed)
                                print(currentBatter["Name"], "rounds first and heads for second")
                                time.sleep(playSpeed)
                                print(random.choice(["And makes it easily", "Here comes the throw to second... Safe!"]))
                                time.sleep(playSpeed)
                                print(outcome)
                            currentBatter["PA"] +=1
                            currentBatter["AB"] +=1
                            currentBatter["H"] +=1
                            currentBatter["2B"] +=1
                            if topOrBottom == "Top":
                                awayHits = awayHits + 1
                            else: homeHits = homeHits + 1
                            if runnerOnFirst == False:
                                if runnerOnSecond == False:
                                    if runnerOnThird == False: # Nobody on
                                        runnerOnSecond = True
                                    else: # Runner on third
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI double for " + currentBatter["Name"], "That drives in a run!", "One run will score!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnSecond = True
                                        runnerOnThird = False
                                else: # Runner on 2nd
                                    if runnerOnThird == False:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI double for " + currentBatter["Name"], "That drives in a run!", "One run will score!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        # No base running changes (batter and runner "swap" places
                                    else: # Runner 2nd and 3rd
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["2-run double by " + currentBatter["Name"], "2 runs will score!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(2, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnThird = False
                            else: #Runner on first to start
                                if runnerOnSecond == False:
                                    if runnerOnThird == False: # Just on first, runner will advance to third
                                        runnerOnFirst = False
                                        runnerOnSecond = True
                                        runnerOnThird = True
                                    else: # First and third
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI double for " + currentBatter["Name"], "That drives in a run!", "One run will score!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnSecond = True
                                        runnerOnThird = True
                                else: # First and 2nd
                                    if runnerOnThird == False:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI double for " + currentBatter["Name"], "That drives in a run!", "One run will score!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnSecond = True
                                        runnerOnThird = True
                                    else: # Bases loaded
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["2-run double for " + currentBatter["Name"], "That knocks in a pair!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(2, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnSecond = True
                                        runnerOnThird = True
                        elif outcome == "Triple":
                            if isLive == True:
                                direction = random.choice(["left", "center field", "right", "left-center", "the right-center gap"])
                                DoubleType = random.choice(["grounder", "liner", "flyball"])
                                if DoubleType == "grounder":
                                    time.sleep(playSpeed)
                                    print("Hit on the ground to", random.choice(["first", "third"]))
                                    time.sleep(playSpeed)
                                    print(random.choice(["and through! It's down the line in to the corner", "Fair Ball! Might be extra bases"]))
                                elif DoubleType == "liner":
                                    time.sleep(playSpeed)
                                    print(random.choice(["line drive to", "hit hard into"]), direction)
                                    time.sleep(playSpeed)
                                    print(random.choice(["It'll get down", "Could be extra bases"]))
                                else:
                                    time.sleep(playSpeed)
                                    print(random.choice(["High fly ball into", "Hit well into", "In the air towards"]), direction)
                                    time.sleep(playSpeed)
                                    print(random.choice(["Going back it is.... Off the wall!", "It'll get down!", "it one-hops the wall"]))
                                time.sleep(playSpeed)
                                print(currentBatter["Name"], "rounds first and heads for second")
                                time.sleep(playSpeed)
                                print(random.choice(["It's bouncing around", "And it's bobbled in the outfield!"]))
                                time.sleep(playSpeed)
                                print(currentBatter["Name"], random.choice(["is going to try for third!", "turns on the jets around second!"]))
                                time.sleep(playSpeed)
                                print("SAFE!")
                                time.sleep(playSpeed)
                                print(outcome)
                            currentBatter["PA"] +=1
                            currentBatter["AB"] +=1
                            currentBatter["H"] +=1
                            currentBatter["3B"] +=1
                            if topOrBottom == "Top":
                                awayHits = awayHits + 1
                            else: homeHits = homeHits + 1
                            if runnerOnFirst == False:
                                if runnerOnSecond == False:
                                    if runnerOnThird == False: # Nobody on
                                        runnerOnThird = True
                                    else: # Runner on third, then they swap places
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI Triple for " + currentBatter["Name"], "That drives in a run!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                else: # Runner on 2nd
                                    if runnerOnThird == False:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI Triple for " + currentBatter["Name"], "That drives in a run!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnSecond = False
                                        runnerOnThird = True
                                    else: # 2nd and third
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI Triple for " + currentBatter["Name"], "That drives in 2 runs!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(2, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnSecond = False
                                        runnerOnThird = True
                            else: # Runner on first
                                if runnerOnSecond == False:
                                    if runnerOnThird == False:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI Triple for " + currentBatter["Name"], "That drives in a run!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnThird = True
                                    else: # First and third
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["2 run triple by " + currentBatter["Name"], "That drives in a pair!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(2, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnThird = True
                                else: # First and 2nd
                                    if runnerOnThird == False:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["2-RBI Triple for " + currentBatter["Name"], "That drives in 2 runs!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(2, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnSecond = False
                                        runnerOnThird = True
                                    else: # Bases loaded -> Bases clearing triple
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(random.choice(["RBI Triple for " + currentBatter["Name"], "That clears the bases!", "3 runs will score!"]))
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(3, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnSecond = False
                                        runnerOnThird = True
                        elif outcome == "Homerun":
                            if isLive == True:
                                time.sleep(playSpeed)
                                print(random.choice(["High flyball to", "In the air to", "Well-hit towards", "That ball is CRUSHED to DEEP"]), random.choice(["left", "center", "right"]))
                                time.sleep(playSpeed)
                                print(random.choice(["Back to the wall, he looks up...","Still going, still going", "WAAYYYY BACK THERE"]))
                                time.sleep(playSpeed)
                                print(random.choice(["Gone!","Home Run!", "Outta Here!", "Bye Bye Baseball!"]))
                            currentBatter["PA"] +=1
                            currentBatter["AB"] +=1
                            currentBatter["H"] +=1
                            currentBatter["HR"] +=1
                            currentPitcher["HR"] +=1
                            if topOrBottom == "Top":
                                awayHits = awayHits + 1
                            else: homeHits = homeHits + 1
                            if runnerOnFirst == False: 
                                if runnerOnSecond == False:
                                    if runnerOnThird == False: # Solo Homer
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print("Solo Shot by", currentBatter["Name"])
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(1, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                    else:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(currentBatter["Name"], "delivers with a two-run bomb!")
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(2, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                else: # Runner on 2nd
                                    if runnerOnThird == False:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(currentBatter["Name"], "delivers with a two-run bomb!")
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(2, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnSecond = False
                                    else: # 2nd and third
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(currentBatter["Name"], "with a 3-run homer!")
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(3, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnSecond = False
                                        runnerOnThird = False
                            else: # Runner on first
                                if runnerOnSecond == False:
                                    if runnerOnThird == False:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(currentBatter["Name"], "delivers with a two-run bomb!")
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(2, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                    else: # First and third
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(currentBatter["Name"], "with a 3-run homer!")
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(3, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnThird = False
                                else: # First and 2nd
                                    if runnerOnThird == False:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            print(currentBatter["Name"], "with a 3-run homer!")
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(3, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnSecond = False
                                        runnerOnThird = False
                                        
                                    else:
                                        if isLive == True:
                                            time.sleep(playSpeed)
                                            if topOrBottom == "top":
                                                team = awayTeam
                                            else:
                                                team = homeTeam
                                            time.sleep(playSpeed)
                                            print("GRAND SLAM!")
                                            time.sleep(playSpeed)
                                            print(currentBatter["Name"], "has put 4 runs on the board for", team)
                                            time.sleep(playSpeed)
                                        awayRuns, homeRuns, currentBatter = scoreRuns(4, topOrBottom, awayRuns, homeRuns, isLive, awayTeam, homeTeam, currentBatter, halfInning, linescore, currentPitcher)
                                        runnerOnFirst = False
                                        runnerOnSecond = False
                                        runnerOnThird = False
                        elif outcome == "steal":
                            if isLive == True:
                                print("Inning ends on steal")
                        else:
                            pass

                        # After outcome is played out
                        if topOrBottom == "Top":
                            if outcome == "steal": # If the inning ends on the bases 
                                pass
                            else:
                                awayBatterNumber = awayBatterNumber + 1
                            if awayBatterNumber > 9:
                                awayBatterNumber = 1
                        else:
                            if outcome == "steal":
                                pass
                            else:
                                homeBatterNumber = homeBatterNumber + 1 # Once it reaches the end of the batting order, it will return to the 1st batter
                            if homeBatterNumber > 9:
                                homeBatterNumber = 1
                        if halfInning > 16: # Ends the game on a walk-off if the game is in the 9th or later and the home team gets the lead
                            if halfInning%2 == 1:
                                if homeRuns > awayRuns:
                                        outs = 3
                                        maxInning = halfInning
                                        if isLive == True:
                                            print("WALK-OFF!!!!!")
                                            time.sleep(playSpeed)
                                            print(currentBatter["Name"], "with the game-winner!")
                        if isLive == True:
                            time.sleep(playSpeed)
                            if outs == 0:
                                print(random.choice(["Nobody out", "No outs"]))
                            elif outs == 1:
                                print(random.choice(["1 away", '1 out', '1 down here']))
                            elif outs == 2:
                                print(random.choice(["2 outs now", "2 away", "2 outs"]))
                            else:
                                pass
                if isLive == True:
                        #time.sleep(playSpeed)
                        print("Inning Over.", awayTeam, awayRuns,"-",homeRuns, homeTeam)
                        time.sleep(2*playSpeed)
                # Pitching Changes
                currentPitcher["IP"] += 1
                pitchLimit = 100
                if awayPitcher["Pitches"] > pitchLimit:
                    if isLive == True:
                        print("Pitching Change")
                    if len(awayRelievers) > 1:
                        #awayPitcherList.remove(awayPitcher)
                        awayPitcher = random.choice(awayRelievers)
                        awayPitcher["G"] += 1
                        pitchLimit = 20
                elif homePitcher["Pitches"] > pitchLimit:
                    if isLive == True:
                        print("Pitching Change")
                    if len(homeRelievers) > 1: # If there are more pitchers available
                        #homePitcherList.remove(homePitcher)
                        homePitcher = random.choice(homeRelievers)
                        homePitcher["G"] += 1
                        pitchLimit = 20
                        
                halfInning = halfInning + 1 # Adds a half-inning every time 3 outs are recorded
                if halfInning == 17: # If it is the top of the ninth inning or later and the home team is leading, the home team will not bat
                    if halfInning%2 == 1:
                        if homeRuns > awayRuns:
                            maxInning = halfInning
                if halfInning > 17: # If the game is tied after regulation, an extra inning will continue to be added until the game is over
                    if maxInning%2 == 0:    
                        if homeRuns == awayRuns:
                                maxInning = maxInning + 2
        if homeRuns > awayRuns:
                winner = homeTeam
                loser = awayTeam
                homeTeamData["Wins"] += 1
                awayTeamData["Losses"] += 1
        elif awayRuns > homeRuns:
                winner = awayTeam
                loser = homeTeam
                homeTeamData["Losses"] += 1
                awayTeamData["Wins"] += 1
                
        linescore[0].extend([awayRuns, awayHits, 0])
        linescore[1].extend([homeRuns, homeHits, 0])
        headerList = ["Teams"]
        if halfInning%2 == 1:
            halfInning += 1
        for i in range(halfInning//2):
            headerList.append(i+1)
        headerList.extend(["Runs", "Hits", "Errors"])
        if isLive == True:
                print("Game Over")
                print("Final Score:", awayTeam, awayRuns, homeTeam, homeRuns)
                print("The ", awayTeam, " had ", awayHits, "hits")         
                print("The ", homeTeam, " had ", homeHits, "hits")
                print(winner,"win!")
                print("\n")
                print(tabulate(linescore, headers = headerList))
                showBoxScore(leagueData, awayTeamData, homeTeamData, awayBatterList, homeBatterList)
        return winner, leagueData

def runPlayerSeason(contact, power, discipline, Seasons):
    totalData = []
    for j in range(Seasons):
        simData = [contact, power, discipline]
        for i in range(13):
            simData.append(0)
        for i in range(700):
            probHR, prob3B, prob2B, prob1B, probBB, probFO, probGO, probK = setProb(contact, power, discipline, 50,50,50)
            outcome = playAtBat(probHR, prob3B, prob2B, prob1B, probBB, probFO, probGO, probK)
            simData[3] += 1
            if outcome != "Walk":
                simData[4] += 1
            if outcome == "Single":
                simData[5] += 1
            if outcome == "Double":
                simData[5] += 1
                simData[6] += 1
            if outcome == "Triple":
                simData[5] += 1
                simData[7] += 1
            if outcome == "Homerun":
                simData[5] += 1
                simData[8] += 1
            if outcome == "Walk":
                simData[9] += 1
            if outcome == "Strikeout":
                simData[10] += 1
        batter = simData
        avg = batter[5]/batter[4]
        batter[11] = round(avg, 3)
        obp = (batter[5]+batter[9])/batter[3]
        batter[12] = round(obp, 3)
        slg = (batter[6]*2 + batter[7]*3 + batter[8]*4 + (batter[5] - batter[6] - batter[7] - batter[8]))/batter[4]
        batter[13] = round(slg, 3)
        batter[14] = round(obp + slg, 3)
        batter[15] = 100*round((obp/0.315 + slg/0.396 -1), 2)
        totalData.append(simData)
    print(tabulate(totalData, headers = ["Contact", "Power", "Discipline", "PA", "AB", "H", "2B", "3B", "HR", "BB", "SO", "BA", "OBP", "SLG", "OPS", "OPS+"]))

def main():
    menu = True
    while menu == True:
        print("Welcome to CubzGm!")
        print("s to start a season")
        print("f to play a single full game")
        print("r to run a single player season")
        print("t to test a bunch of games")
        print("e to exit the game")
        gameType = input("")
        if gameType == "f":
            playAgain = True
            while playAgain == True:
                    print("Cubs = 1")
                    print("Cardinals = 2")
                    print("Yankees = 3")
                    print("Red Sox = 4")
                    awayTeam = int(input("What team would you like to play as?")) - 1
                    homeTeam = int(input("Who would you like the opponent to be?")) - 1
                    playSpeed = float(input("How fast would you like to play? (Pick a 0 or 1)")) # 1 = about 600 seconds, 0.5 = 300, etc etc
                    leagueData = readCSV("BaseballSimBatters.csv", "BaseballSimPitchers.csv")
                    #leagueData = createPlayers(leagueData)
                    playGame(awayTeam,homeTeam, playSpeed, True, leagueData)
                    again = input("Would you like to play again? y/n")
                    if again == "n":
                        playAgain = False
            print("Thanks for playing")
        elif gameType == "s": # Season is more difficult, as you'd have to ask the user to choose a team, sim games, maybe even manage lineups?s
            playAgain = True
            while playAgain == True:
                playSpeed = 0
                leagueData = readCSV("BaseballSimBatters.csv","BaseballSimPitchers.csv")
                #leagueData = createPlayers(leagueData)
                awaySchedule, homeSchedule = genSchedule(leagueData["Teams"].keys())
                for i in range(len(homeSchedule)):
                    winner, leagueData = playGame(awaySchedule[i],homeSchedule[i], playSpeed, False, leagueData)
                leagueData = calcStats(leagueData)

                #Formatting Stats
                for j in range(4): 
                    header1 = []
                    printData1 = []
                    header2 = []
                    printData2 = []
                    for key in leagueData["Teams"][j]["Players"][0].keys():
                        header1.append(key)
                    for i in range(len(leagueData["Teams"][j]["Players"])):
                        printData1.append([])
                        for stats in leagueData["Teams"][j]["Players"][i].values():
                            printData1[i].append(stats)
                    for key in leagueData["Teams"][j]["Pitchers"][0].keys():
                        header2.append(key)
                    for i in range(len(leagueData["Teams"][j]["Pitchers"])):
                        printData2.append([])
                        for stats in leagueData["Teams"][j]["Pitchers"][i].values():
                            printData2[i].append(stats)
                    print(tabulate(printData1, headers = header1))
                    print(tabulate(printData2, headers = header2))
                print("The Cubs finish with a record of ", leagueData["Teams"][0]["Wins"], "-", leagueData["Teams"][0]["Losses"])
                print("The Cardinals finish with a record of ", leagueData["Teams"][1]["Wins"], "-", leagueData["Teams"][1]["Losses"])
                print("The Yankees finish with a record of ", leagueData["Teams"][2]["Wins"], "-", leagueData["Teams"][2]["Losses"])
                print("The Red Sox finish with a record of ", leagueData["Teams"][3]["Wins"], "-", leagueData["Teams"][3]["Losses"])
                again = input("Would you like to play again? If not, press n to escape")
                if again == "n":
                    playAgain = False
            print("Thanks for playing")
        elif gameType == "r":
            playAgain = True
            while playAgain == True:
                contact = int(input("Enter in the contact rating"))
                power = int(input("Enter in the power rating"))
                discipline = int(input("Enter in the discipline rating"))
                seasons = int(input("Enter in the number of seasons you would like to sim"))
                runPlayerSeason(contact, power, discipline, seasons)
                again = input("Would you like to play again? If not, press n to escape")
                if again == "n":
                    playAgain = False
        elif gameType == "t":
                leagueData = readCSV("BaseballSimBatters.csv", "BaseballSimPitchers.csv")
                #print(leagueData["Teams"][0]["Pitchers"])
                #leagueData = createPlayers(leagueData)
                #winner, leagueData = playGame(0,1,0, False, leagueData)
        elif gameType == "e":
            exit()
        else:
            print("Error")
    
main()

        
        

    
    

    

    

