#!/usr/bin/env python
import requests
import json
import argparse

playerUrl = "https://api.prodigygame.com/game-api/v2/characters/"
loginUrl = "https://api.prodigygame.com/game-api/v3/login"

def keyExpired(loginData):
  r = requests.post(playerUrl + loginData[1], data = {'data': "{}", 'auth-key': loginData[0], 'token': loginData[0]})
  if(r.text == '{"code":"BadRequestError","message":"Bad request"}'):
    return True
  return False

def newLoginData(login):
  if not login:
    print("No previous user found: Specify new user with --login")
    exit()
  keyfile = open("keyfile", "w")
  r = requests.post(loginUrl, data = {'username': login[0], 'password': login[1], 'clientVersion': '2-2-1'})
  keyfile.write("\n".join([r.json()['authToken'], str(r.json()['userID']), login[0], login[1]]))
  keyfile.close()
  return open("keyfile", "r")

def getLoginData(login):
  try:
    keyfile = open("keyfile", "r")
  except IOError:
    keyfile = newLoginData(login)

  data = keyfile.read().split('\n')
  if(len(data) < 4):
    keyfile.close()
    keyfile = newLoginData(login)
    data = keyfile.read().split('\n')

  return data

def getPlayerData(logindata):
  r = requests.get(playerUrl + logindata[1], params = { 'fields': 'data', 'auth-key': logindata[0], 'token': logindata[0]})
  return r.json()[logindata[1]]['data']

def setProperty(args):
  print("LATER")

def showProperty(args):
  data = getLoginData(args.login)
  if keyExpired(data):
    newLoginData(args.login)
  player = getPlayerData(data)
  if args.property:
    if not args.property in player:
      print("There is no property named",args.property)
      
    print(player[args.property])
  else:
    print(player)

def main():

  parser = argparse.ArgumentParser()

  parser.add_argument('--login', nargs=2, metavar=("USERNAME", "PASSWORD"))

  subparsers = parser.add_subparsers(dest='command')
  subparsers.required = True

  parse_show = subparsers.add_parser('show', help='Show property of player')
  parse_show.add_argument('--property', default='', help='property help')
  parse_show.set_defaults(func=showProperty)

  parse_set = subparsers.add_parser('set', help='Set property of player')
  parse_set.add_argument('--property', default='', help='property help')
  parse_set.set_defaults(func=setProperty)

  args = parser.parse_args()
  args.func(args)

if __name__ == "__main__":
  main()


"""
loginUrl = "https://api.prodigygame.com/game-api/v3/login"
playerUrl = "https://api.prodigygame.com/game-api/v2/characters/"

if(len(sys.argv) < 2):
  print("USAGE:",sys.argv[0],"[COMMAND]")
  exit()

commands = ("show")
command = sys.argv[1]
option = "" if len(sys.argv) < 3 else sys.argv[2]

if not (command in commands):
  print(sys.argv[1],"not a valid command!")
  exit()

if(command == "show"): 
  r = requests.post(loginUrl, data = {'username': 'christians940', 'password': 'apple5', 'clientVersion': '2-2-1'})
  playerdata = r.json()['data']
  if(option):
    print(playerdata[option])
    exit()
  print(playerdata)
  exit()

if(command == "set"):
  if(option):

r = requests.post(loginUrl, data = {'username': 'christians940', 'password': 'apple5', 'clientVersion': '2-2-1'})
data = r.json()

authkey = data['authToken']
playerid = data['userID']
playerdata = data['data']

print(playerdata)

senddata = {
  "appearance":
  {
    "name":
    {
      "last":874,
      "first":122,
      "middle":780,
      "nick":1,
    },
    "hair":
    {
      "color":3,
      "style":16
    },
    "face":4,
    "gender":"male",
    "eyeColor":6,
    "skinColor":1
  },
  "data":
  {
    "settings":
    {
      "bgmVolume":0,
      "voiceVolume":1,
      "sfxVolume":0
    },
    "level":1337,
    "starlightFestivalDaily":
    {
      "date":
      {
        "d":6,"y":2017,"m":11
      },
      "monsterID":50,
      "dailyLocation":
      {
        "pathOffset":[90,30],
        "lamplight-C3":[280,600]
      },
      "isComplete":0
    },
    "emailPromptCounter":24,
    "hp":5580,
    "stars":9510,
    "team":0,
    "allowsHouseVisitors":False,
    "gold":1000022490,
    "loss":1,
    "versionID":20,
    "spellbook":[36,30,24,3,18,12],
    "rate":9999999,
    "zone":"lamplight-A3","school":"none",
    "survey":2,
    "microDetails":
    {
      "firstOpenBreadcrumb":0,
      "firstBoxBreadcrumb":0
    },
    "spells":[13,7,1,14,21,4,28,35,32,31,8,17,5,19,6,34,2,3,9,10,11,12,15,16,18,20,22,23,24,25,26,27,29,30,33,36],
    "dailyLoginBonus":
    {
      "date":{"d":6,"y":2017,"m":11},
      "day":2,
      "session":10
    },
    "bountyScore":0,
    "tower":100,
    "rewardData":
    {
      "type":"gold",
      "N":2000
    }
  },
  "tutorial":
  {
    "zones":{},
    "menus":
    {
      "3":[1,1,2],
      "6":[1],
      "14":[1],
      "23":[1]
    }
  },
  "achievements":
  {
    "kills":6,
    "progress":{"1":1,"2":3,"4":3,"5":3,"8":1,"9":5,"10":4,"14":1,"15":1,"16":1,"20":1,"25":1,"29":1,"30":3,"31":4,"34":1},
    "qC":7,
    "gS":2200,
    "gE":5002025295
  },
  "state":
  {
    "zone":
    {
      "house":
      {
        "quest":
        {
          "ID": 5
        }
      }
    }
  }
}

#playerdata['gold'] = 12345678

#newdata = { }
#newdata['data'] = playerdata

sendData = { 'data': json.dumps(senddata), 'auth-key': authkey, 'token': authkey }

r = requests.post(playerUrl + str(playerid), sendData)
print(r.text)
"""
