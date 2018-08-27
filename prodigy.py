#!/usr/bin/env python
import requests
import json
import argparse

playerUrl = "https://api.prodigygame.com/game-api/v2/characters/"
loginUrl = "https://api.prodigygame.com/game-api/v3/login"

def readDataFile():
  try:
    keyfile = open("keyfile", "r")
  except IOError:
    return ['']
  data = keyfile.read().split('\n')
  return data

def newDataFile(login):
  if not login:
    print("No previous user found: Specify user with --login")
    exit()
  keyfile = open("keyfile", "w")
  r = requests.post(loginUrl, data = {'username': login[0], 'password': login[1], 'clientVersion': '2-2-1'})
  data = "\n".join([r.json()['authToken'], str(r.json()['userID']), login[0], login[1]])
  keyfile.write(data)
  keyfile.close()
  return data

def keyExpired(loginData):
  r = requests.post(playerUrl + loginData[1], data = {'data': "{}", 'auth-key': loginData[0], 'token': loginData[0]})
  if(r.text == '{"code":"BadRequestError","message":"Bad request"}'):
    return True
  return False

def getLoginData(login):
  data = readDataFile()
  if len(data) < 4 or keyExpired(data):
    data = newDataFile(login)
  return data

def getPlayerData(logindata):
  r = requests.get(playerUrl + logindata[1], params = { 'fields': 'data', 'auth-key': logindata[0], 'token': logindata[0]})
  return r.json()[logindata[1]]['data']

def setProperty(args):
  logindata = getLoginData(args.login)
  player = getPlayerData(logindata)
  if args.property in player:
    player[args.property] = args.value
  sendData = {}
  sendData['data'] = player;
  r = requests.post(playerUrl + logindata[1], data = { 'data': json.dumps(sendData), 'auth-key': logindata[0], 'token': logindata[0]})

def showProperty(args):
  logindata = getLoginData(args.login)
  player = getPlayerData(logindata)
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
  parse_set.add_argument('property', default='', help='property help')
  parse_set.add_argument('value', default='', help='value help')
  parse_set.set_defaults(func=setProperty)

  args = parser.parse_args()
  args.func(args)

if __name__ == "__main__":
  main()
