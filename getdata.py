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
