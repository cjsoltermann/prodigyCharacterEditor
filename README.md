# Prodigy Character Editor

Tool to modify character data in Prodigy

## How to use

### Options

```-n --noexpand``` Don't expand properties  
```-v --value``` Specify value to set

### Examples

#### List all character properties

```
./prodigy.py --login [username] [password] get -n
```

Note: Your username and password will be saved, so they only need to be entered once

#### Show specific property

```
./prodigy.py get appearance gender
```
Result:
```
appearance
isMember
equipment
data
state
inventory
tutorial
pets
quests
house
achievements
```

#### Set specific property

```
./prodigy.py set data gold -v 5
```
Result:
```
(Displays ALL character data)
```

#### List subproperties

```
./prodigy.py get data -n
```
Result:
```
starlightFestivalDaily
emailPromptCounter
hp
isMember
allowsHouseVisitors
gold
loss
versionID
spellbook
rate
zone
school
microDetails
spells
bountyScore
tower
settings
level
stars
team
survey
dailyLoginBonus
rewardData
nm
```

#### View entire property

```
./prodigy.py get data
```
Result:
```
{
    "starlightFestivalDaily": {
        "date": {
            "d": 6,
            "y": 2017,
            "m": 11
        },
        "monsterID": 50,
        "dailyLocation": {
            "pathOffset": [
                90,
                30
            ],
            "lamplight-C3": [
                280,
                600
            ]
        },
        "isComplete": 0
    },
    "emailPromptCounter": 24,
    "hp": 5580,
    "isMember": true,
    "allowsHouseVisitors": false,
    "gold": 5,
    "loss": 1,
    "versionID": 20,
    "spellbook": [
        36,
        30,
        24,
        3,
        18,
        12
    ],
    "rate": 9999999,
    "zone": "lamplight-C3",
    "school": "none",
    "microDetails": {
        "firstOpenBreadcrumb": 0,
        "firstBoxBreadcrumb": 0
    },
    "spells": [
        13,
        7,
        1,
        14,
        21,
        4,
        28,
        35,
        32,
        31,
        8,
        17,
        5,
        19,
        6,
        34,
        2,
        3,
        9,
        10,
        11,
        12,
        15,
        16,
        18,
        20,
        22,
        23,
        24,
        25,
        26,
        27,
        29,
        30,
        33,
        36
    ],
    "bountyScore": 0,
    "tower": 100,
    "settings": {
        "bgmVolume": 0,
        "voiceVolume": 1,
        "sfxVolume": 0
    },
    "level": 1337,
    "stars": 9510,
    "team": 0,
    "survey": 2,
    "dailyLoginBonus": {
        "date": {
            "d": 6,
            "y": 2017,
            "m": 11
        },
        "day": 2,
        "session": 19
    },
    "rewardData": {
        "type": "gold",
        "N": 2000
    },
    "nm": 2
}
```
