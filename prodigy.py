#!/usr/bin/env python
import requests
import json
import argparse

playerUrl = "https://api.prodigygame.com/game-api/v2/characters/"
loginUrl = "https://api.prodigygame.com/game-api/v3/login"
validFields = ('appearance','isMember','equipment','data','state','inventory','tutorial','pets','quests','house','achievements')

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
  r = requests.post(loginUrl, data = {'username': login[0], 'password': login[1], 'clientVersion': '2-4-2'})
  data = "\n".join([r.json()['authToken'], str(r.json()['userID']), login[0], login[1]])
  keyfile.write(data)
  keyfile.close()
  return data

def keyExpired(loginData):
  r = requests.post(playerUrl + loginData[1], data = {'data': "{}", 'auth-key': loginData[0], 'token': loginData[0]})
  if(r.text == '{"message":"Nothing to update"}'):
    return False
  return True

def getLoginData(login):
  data = readDataFile()
  if len(data) < 4 or keyExpired(data):
    data = newDataFile(login)
  return data

def getPlayerData(logindata, field):
  if field in validFields:
    r = requests.get(playerUrl + logindata[1], params = { 'fields': field, 'auth-key': logindata[0], 'token': logindata[0]})
  elif field == '':
    r = requests.get(playerUrl + logindata[1], params = { 'fields': ','.join(validFields), 'auth-key': logindata[0], 'token': logindata[0]})
  else:
    print(field,"is not a valid field")
    exit()
  return r.json()[logindata[1]]

def setProperty(args):
  logindata = getLoginData(args.login)
  player = getPlayerData(logindata, args.property[0])
  value = int(args.value) if args.value.isdigit() else args.value
  returnObject = player
  lastObject = player
  setKey = ''

  for prop in args.property:
    if prop in lastObject:
      if type(lastObject[prop]) is list or type(lastObject[prop]) is dict:
        lastObject = lastObject[prop]
      else:
        setkey = prop
    elif type(lastObject) is list and prop.isdigit() and 0 < int(prop) < len(lastObject):
      if type(lastObject[int(prop)]) is list or type(lastObject[int(prop)]) is dict:
        lastObject = lastObject[int(prop)]
      else:
        setkey = int(prop)
    else:
      print(prop,"is not a valid property")
      exit()

  lastObject[setkey] = value
  print(json.dumps(returnObject, indent=4))
    

  r = requests.post(playerUrl + logindata[1], data = { 'data': json.dumps(returnObject), 'auth-key': logindata[0], 'token': logindata[0]})

def getProperty(args):
  logindata = getLoginData(args.login)
  player = getPlayerData(logindata, '' if len(args.property) == 0 else args.property[0])
  returnValue = player
  for prop in args.property:
    if prop.isdigit() and 0 < int(prop) < len(returnValue):
      returnValue = returnValue[int(prop)]
    elif prop in returnValue:
      returnValue = returnValue[prop]
    else:
      print("Property",prop,"does not exist")
      exit();
  if args.noexpand:
    if len(args.property) == 0:
      for field in validFields:
        print(field)
      exit()
    if type(returnValue) is dict:
      for key, value in returnValue.items():
        print(key)
    elif type(returnValue) is list:
      print("List of",len(returnValue))
  else:
    print(json.dumps(returnValue, indent=4))

def main():

  parser = argparse.ArgumentParser()

  parser.add_argument('--login', nargs=2, metavar=("USERNAME", "PASSWORD"))

  subparsers = parser.add_subparsers(dest='command')
  subparsers.required = True

  parse_get = subparsers.add_parser('get', help='get property of player')
  parse_get.add_argument('property', nargs='*', help='property help')
  parse_get.add_argument('--noexpand', '-n', action='store_true')
  parse_get.set_defaults(func=getProperty)

  parse_set = subparsers.add_parser('set', help='Set property of player')
  parse_set.add_argument('property', nargs='+', help='property help')
  parse_set.add_argument('--value', '-v', required=True, help='value help')
  parse_set.set_defaults(func=setProperty)

  args = parser.parse_args()
  args.func(args)

if __name__ == "__main__":
  main()
