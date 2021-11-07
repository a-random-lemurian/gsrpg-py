"""
This is a Python program to assist in running a Sufficient Velocity-flavored GSRPG.
"""

import os
import sys
import json

import order_implementation as Ord

# This piece of code checks if Typer and
# Questionary are on the user's system
try:
    import questionary
    import typer
except ImportError:
    print("Warning: Questionary and Typer are not installed on your system.")
    print("Do you want to install? Y/N")
    print("You may choose N if you wish to customize the installation commands.")
    install_perm = input("> ")
    if install_perm.lower().strip() == "n":
        print("Cancelled. This GSRPG tool cannot run without these modules.")
        sys.exit()
    else:
        os.system("python3 -m pip install typer==0.4.0 && python3 -m pip install questionary==1.10.0")


GSRPG_DATA_FILE_PATH = 'gsrpg1.json'




app = typer.Typer(add_completion=True)
faction_data_access = typer.Typer(add_completion=True)

app.add_typer(faction_data_access,name='list')


with open(GSRPG_DATA_FILE_PATH, "r+", encoding="UTF-8") as gsrpg_file:
    gsrpg = json.load(gsrpg_file)

# HOW TO USE THIS
# If your GSRPG data is stored in a file that isn't gsrpg1.json,
# then change:
# with open('gsrpg1.json','r+',encoding='UTF-8') as gsrpg_file:
#            ^^^^^^^^^^^ your file here


factions = gsrpg["factions"]
turn = gsrpg["basic"]["turn"]
buildings_data = gsrpg["buildings"]


def gsrpg_reporter(event_type: str, msg: str):
    """
    Print out GSRPG update specifics.
    """
    print(f"{event_type:<40} | {msg}")


def gsrpg_header():
    """Print out a GSRPG header for the table."""
    print(f'{"Event":<40} {"Res":<5}')


@app.command()
def checkturn():
    """
    Check the current turn number of the GSRPG
    """
    print("Turn " + str(turn))


@app.command()
def update(
    force: bool = typer.Option(
        False, "-F", "--force", help="Eliminate the confirmation dialog"
    ),
 ):
    """Update all factions.\n
    WARNING: IT IS A BAD IDEA TO USE -F.
    """
    gsrpg_header()

    if force:
        print("Force")


    faction_names = list(factions.keys())

    for faction_name in faction_names:
        faction_res = factions[faction_name]["resources"]

        print(faction_name, " ", "=" * 50)

        buildings = factions[faction_name]["buildings"]
        for building in buildings:
            print(faction_res)

            production  = buildings_data[building]['production']
            consumption = buildings_data[building]['consumption']

            mul = buildings[building]

            fac_res_comparison = {a: faction_res[a] for a in consumption}

            for fac_res in fac_res_comparison:
                if fac_res_comparison[fac_res] < consumption[fac_res]:
                    produce_resources = False
                    break
                else:
                    produce_resources = True

            if produce_resources:
                for consume in consumption:
                    faction_res[consume] -= consumption[consume]*mul

                for produce in production:
                    faction_res[produce] += production[produce]*mul
            else:
                pass

            print(faction_res)

    gsrpg['basic']['turn'] += 1

    confirmed_update = questionary.confirm(
        "Confirm GSRPG update? Remember, review the logs!"
    ).ask()
    if confirmed_update is True or force is True:
        with open(GSRPG_DATA_FILE_PATH,'w') as gsrpg_fp:
            json.dump(gsrpg,gsrpg_fp,indent=2)
        if force is True:
            print('Usage of the -F flag is highly discouraged.')
    elif confirmed_update is False:
        print("Cancelled GSRPG update!")
        sys.exit()


@faction_data_access.command("names")
def list_names():
    """List faction names."""
    for fac_dict_idx, faction_data in enumerate(factions):
        print(f'{fac_dict_idx:<6} | {faction_data}')


@faction_data_access.command()
@app.command()
def sus():
    """Print sus."""
    print("SussyBaka")


if __name__ == "__main__":
    app()
