"""
This is a Python program to assist in running a Sufficient Velocity-flavored GSRPG.
"""

import os
import sys
import json



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
        os.system("""
                  python3 -m pip install typer==0.4.0 && 
                  python3 -m pip install questionary==1.10.0
                  """
                    )


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


def orders_new_building(order_dict: dict, faction_name: str):
    """Executes `newBuilding` orders.

    Args:
        order_dict (dict): [description]
        faction_name (str): [description]
    """
    for building in order_dict['construction']:
        bldg = building['building']
        qty = building['qty']
        consumption = buildings_data[bldg]['build-cost']
        print(consumption)
        faction_res = factions[faction_name]["resources"]
        fac_res_comparison = {a: faction_res[a] for a in consumption}
        for fac_res, value in fac_res_comparison.items():
            if value < consumption[fac_res]:
                construct_building = False
                break
            else:
                construct_building = True
        print(construct_building)
        if construct_building:
            try:
                factions[faction_name]['buildings'][bldg] += qty
            except KeyError:
                factions[faction_name]['buildings'][bldg] = 0 + qty


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
    debug: bool = typer.Option(
        False, "-D", "--debug", help="Print out the raw faction data for debugging."
    )
 ):
    """Update all factions.\n
    WARNING: IT IS A BAD IDEA TO USE -F.
    """
    gsrpg_header() # Print the GSRPG header to list events
    faction_names = list(factions.keys())

    #print(factions)

    for faction_name in faction_names:

        faction_res = factions[faction_name]["resources"]

        print(faction_name, " ", "=" * 50)

        buildings = factions[faction_name]["buildings"]
        # Add and deduct resources
        for building in buildings:
            #print(faction_res)

            production  = buildings_data[building]['production']
            consumption = buildings_data[building]['consumption']

            mul = buildings[building]

            fac_res_comparison = {a: faction_res[a] for a in consumption}

            for fac_res, value in fac_res_comparison.items():
                if value < consumption[fac_res]:
                    produce_resources = False
                    break
                else:
                    produce_resources = True

            if produce_resources:
                for consume in consumption:
                    consum_res = consumption[consume]*mul
                    faction_res[consume] -= consum_res
                    gsrpg_reporter('Resource consumed',f'Consumed {consum_res} {consume}')

                for produce in production:
                    prod_res = production[produce]*mul
                    try:
                        faction_res[produce] += prod_res
                    except KeyError:
                        faction_res[produce] = 0 + prod_res
                    gsrpg_reporter('Resource produced',f'Consumed {prod_res} {produce}')
        # Execute orders
        orders = factions[faction_name]["orders"]

        for order in orders:
            order_type = order['order-type'].lower().strip()

            if order_type == 'newbuilding':
                orders_new_building(order, faction_name)

            orders.pop(0) # We're done with the order, so
                          # it's time to delete it using pop.




    gsrpg['basic']['turn'] += 1

    confirmed_update = questionary.confirm(
        "Confirm GSRPG update? Remember, review the logs!"
    ).ask()
    if confirmed_update is True or force:
        with open(GSRPG_DATA_FILE_PATH,'w') as gsrpg_fp:
            json.dump(gsrpg,gsrpg_fp,indent=2)
        if force:
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
