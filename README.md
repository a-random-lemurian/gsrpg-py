# GSRPG.py - A helpful tool to automate GSRPGs.
> Note: This GSRPG tool is tailored towards the specific needs of the GSRPG subforum on Sufficient Velocity.

> **Link**: https://forums.sufficientvelocity.com

# Warnings
- This GSRPG automation tool only supports the Gregorian calendar. Due to the intense difficulty of handling leap years, the supported units of time are 1 month, 1 year, and 1 day (for the latter, the script will not calculate the year.)
- Use of this tool requires at least a basic understanding of the use of command line interfaces and a data exchange format known as JSON (it's easy to learn JSON, don't worry).
- This GSRPG automation tool will not host your game for you. Think of it as a Co-Gamemaster.
- This GSRPG automation tool was developed on a MacBook Air running macOS 11.4 "Big Sur". It has not been tested on Windows.
- This tool was mainly developed using Python 3.10 - this has not been tested in earlier versions.
- Make sure your current working directory is in the same folder as where you install the tool when you make use of it, otherwise it will cause a FileNotFound error since the file opening operations are relative to the tool's directory.

# Get started
First of all, create a new file named `gsrpg1.json` and then open it with your editor of choice. Fill in the data you need. An example is provided below:

## Code example
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
`python3 main.py update <-F>`
### About
This command runs a sequence of updates such as resource deduction and creation (from the 'buildings' your players have built.) and increments the turn count by 1.
### Options
`-F`: Forcefully update, without confirming any changes to the dictionary. This is EXTREMELY DANGEROUS but still included for the Gamemaster that needs to update quickly (remember that a good Gamemaster is one that has patience)