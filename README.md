# GSRPG.py - A helpful tool for you, the Gamemaster.
Spend the time you allot to your Gamemaster duties:
- Writing more lore.
- Recruiting players.
- Brainstorming.

And hopefully spend less time:
- Fixing update errors.
- Arguing with players over update errors.
- Keying in values into a spreadsheet program or calculator.

All that's needed is to learn:
- How to install the Python interpreter on your computer (it's simple, don't worry)
- How to be a better Gamemaster
- Basic knowledge of your Terminal or Command Prompt
- JSON syntax

Support for:
- Characters*
- Factions
- Buildings
- Resources
- Player Orders*
> Note: This GSRPG tool is tailored towards the specific needs of the GSRPG subforum on Sufficient Velocity. An effort has been made to ensure this tool's adaptability however.

> **Link**: https://forums.sufficientvelocity.com

# Warnings
## Extremely important fine print
```
* Does not support battles between characters.
* Some player orders may be impossible to implement
```
## User warnings
- This GSRPG automation tool only supports the Gregorian calendar. Due to the intense difficulty of handling leap years, the supported units of time are 1 month, 1 year, and 1 day (for the latter, the script will not calculate the year.)
- Use of this tool requires at least a basic understanding of the use of command line interfaces and a data exchange format known as JSON (it's easy to learn JSON, don't worry).
- This GSRPG automation tool will not host your game for you. Think of it as a Co-Gamemaster.
- This GSRPG automation tool was developed on a MacBook Air running macOS 11.4 "Big Sur". It has not been tested on Windows.
- This tool was mainly developed using Python 3.10 - this has not been tested in earlier versions.
- Make sure your current working directory is in the same folder as where you install the tool when you make use of it, otherwise it will cause a FileNotFound error since the file opening operations are relative to the tool's directory.

# Get started
## Download
Depending on your theme, you may see a green/orange 'Code' button. Click it and download the .zip file for a potentially unstable release.
For a more stable release, go to the Releases tab. Then, click "Download source code (zip)" or download the tar.gz (your choice).
## Installation
With your `.zip` or `.tar.gz`, move it to a directory of your choice and unzip it in that directory.
### After installation
On Windows, open up your command prompt.

On Mac, if you do not have a terminal emulator, then:
- Hit `Cmd`+`Space` to enter Spotlight Search
- Type "Terminal.app"
- Then, click on it.

Look for the directory where you installed the program and then copy it's path.
You will be able to run the program properly if you see:

In Windows:

`PS [ABSOLUTE_PATH]>` where ABSOLUTE_PATH is the directory path relative to `C:`

Mac/Linux:

If you see the name of the directory where you installed the program, say if you put the program in a directory called `gsrpgautomator`, if you see gsrpgautomator as the "CWD" in the prompt, then you are all set.

**Note**: What you see may differ based on your settings. Your Mac/Linux prompt may further be different based on your shell config files.

Now that you are ready to automate your GSRPG (or try it out), create a file named `gsrpg1.json`. In the section "Basic data" you will find instructions on how to set it up.
## Basic data
First of all, create a new file named `gsrpg1.json` and then open it with your editor of choice. Fill in the data you need.

See section JSON GSRPG syntax for further details.

An example is provided below:
### Code example
```json
{
	"basic": {
		"name": "Name of your GSRPG",
		"turn": 0
	},
	"factions": {
		"Stack Overflow": {
			"factionName": "Stack Overflow",
			"power": 50000,
			"buildings": { "Copy-paste House": 8, "Power Plant": 8 },
			"resources": { "Electricity": 32, "SO code snippet": 5 }
		}
	},
	"persons": {
		"Example Person 1": {
			"name": "Example Person 1",
			"age": 123,
			"gender": "Male",
			"position": "Example person",
			"species": "Homo sapiens code-samplus"
		}
	},
	"buildings": {
		"Copy-paste House": {
			"name":"Copy-paste House",
			"production": { "SO code snippet": 12 },
			"consumption": { "Electricity": 86 }
		},
		"Power Plant": {
			"name":"Power Plant",
			"production":{ "Electricity": 90 },
			"consumption":{ "SO code snippet": 1 }
		}
	}
}
```
# Commands
If using Windows, use `py -3` instead of `python3`.
## Update
**Syntax**
`python3 main.py update [-F]`
### About
This command runs a sequence of updates such as resource deduction and creation (from the 'buildings' your players have built.) and increments the turn count by 1.
### Options
`-F`: Forcefully update, without confirming any changes to the dictionary. This is EXTREMELY DANGEROUS but still included for the Gamemaster that needs to update quickly (remember that a good Gamemaster is one that has patience). Using -F will always print a warning message.
# JSON GSRPG Syntax
Legend: `{mandatory attribute}` `<optional attribute>` `[unimplemented]`
## Root level
```json
{
	"basic": {

	},

	"factions": {

	},

	"persons": {

	},

	"buildings": {

	}
}
```
## Basic
```json
"basic": {
	"name": "[name]",
	"turn": "{turn}",
	"turn-length": "[turn-length]"
}
```
| Attribute | Example | Description
|---|---|---|
|`name`|My Awesome GSRPG Game|The name of your GSRPG.
|`turn`|69|The current turn your GSRPG is in.
|`turn-length`|1-month|The length of a turn in your game, in the Gregorian calendar.
## Buildings
```json
"{name}": {
			"name":"{name}",
			"production":{ "See section Resources" },
			"consumption":{ "See section Resources" }
		}
```
__**WARNING**__: As of version `0.1.0`, the script does not support empty `production` and `consumption` attributes. You may insert `"nothing-resource": 0` or anything with a zero value as a placeholder.

**Note**: The `production` and `consumption` attributes support more than 1 value. If you input more than one value into these attributes, you must separate them with the comma character, otherwise it is invalid JSON and cannot be read properly by the program.

| Attribute | Example | Description
|---|---|---|
|`name`|My Awesome Building|The name of the building.
|`production`|`"Silk": 43`|A list of resource/s this building will produce.
|`consumption`|`"Silkworm Eggs": 10`|A list of resource/s this building will use.
## Persons
```json
"{name}": {
	"name": "{name}",
	"age": "{age}",
	"gender": "{gender}",
	"position": "{position}",
	"species": "{species}"
}
```
| Attribute | Example | Description
|---|---|---|
|`name`|`"John Doe"`|The full name of the character. Factions require at least 1 leader.
|`age`|69|The age of the character in real-life Earth years. Do not include prefixes such as 'His Excellency' or 'Her Excellency'.
|`gender`|Male|The character's gender at the present turn. If neither male or female, specify `Non-Binary`. Supported types (case sensitive) are `Female`, `Male`, and `Non-Binary`.
|`position`|Intern|Highest rank of authority this person holds, like President, Prime Minister, Fleet Admiral, Knight, and similar titles.
|`species`|Homo sapiens sapiens|Species of the character. Scientific names are preferred.
## Factions
```json
"{name}": {
	  "factionName": "{name}",
	  "power": "[power]",
	  "buildings": { "See section Resources for resource syntax" },
	  "resources": { "See section Resources for resource syntax" }
	}
```
| Attribute | Example | Description
|---|---|---|
`name`| Confederacy of Foo | Faction's name. Preferrably, a common name, for example `Philippines` instead of `Republic of the Philippines`.
`power`|40000| Currently unimplemented. The power mechanic may be used as a measure of military strength in future versions.
`buildings`|`{"power-station": 44}`|All buildings under the control of the faction expressed in the form of a Python dictionary.
`resources`|`{"Silk": 803}`|All resources under the control of the faction expressed in the form of a Pyhton dictionary.
## Shared
### Resources
```json
{
	"{resource}": "{qty}"
}
```
| Attribute | Example | Description
|---|---|---|
|`resource`| Silk | Any given resource. Preferrably, the resource should be tangible, have intrinsic value, or if non-tangible, be unique (such as an NFT), meaning that resources such as "bitcoin", "Discord Nitro" are discouraged but "Iron ore", "Silver", and "Fruit" accepted.
|`qty`| 438 | Amount of resource expressed in metric tons or a similar unit of measure (not necessarily the same scale as a metric ton).