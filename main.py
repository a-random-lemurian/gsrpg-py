"""
This is a Python program to assist in running a Sufficient Velocity-flavored GSRPG.
"""

import os
import sys
import json
from rich import print


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




app = typer.Typer(add_completion=True,no_args_is_help=True)
faction_data_access = typer.Typer(add_completion=True,no_args_is_help=True)

app.add_typer(faction_data_access,name='list')


with open(GSRPG_DATA_FILE_PATH, "r+", encoding="UTF-8") as gsrpg_file:
    gsrpg = json.load(gsrpg_file)

# HOW TO USE THIS
# If your GSRPG data is stored in a file that isn't gsrpg1.json,
# then change:
# with open('gsrpg1.json','r+',encoding='UTF-8') as gsrpg_file:
#            ^^^^^^^^^^^ your file here


factions = gsrpg["factions"]
buildings_data = gsrpg["buildings"]
turn = gsrpg["basic"]["turn"]

def check_persistence(order):
    try:
        pers = order['persistence'] != 0
        return True
    except KeyError:
        return False

def res_should_make_res(fac_res_comparison: dict,
                        consumption: dict):
    """Check whether to make resources or not.

    Args:
        fac_res_comparison (dict): Faction resource dict containing info about the resources needed.
        consumption (dict): Resources needed to make said resources.

    Returns:
        Boolean value, containing information about whether to produce resources or not.
    """
    for fac_res, value in fac_res_comparison.items():
        if value < consumption[fac_res]:
            produce_resources = False
            break
        else:
            produce_resources = True
        return produce_resources


def res_consume_resources(
    consumption: dict,
    faction_res: dict,
    mul: int):
    for consume in consumption:
        consum_res = consumption[consume]*mul
        faction_res[consume] -= consum_res
        gsrpg_reporter('Resource consumed',f'Consumed {consum_res} {consume}')


def order_execution(debug, faction_name, orders: list, order: dict):
    print('PRE-PROCESSED >',order,flush=True)
    idx = orders.index(order)
    type = str(order.get('order-type')).lower().strip()
    if type == 'newbuilding':
        orders_new_building(
            order_dict=order,
            faction_name=faction_name
                           )
    pers = order.get('persistent')
    if pers == 0 or pers is None:
        orders.pop(idx)
    else:
        orders.pop(0)


def res_produce_res(faction_res, mul, production):
    for produce in production:
        prod_res = production[produce]*mul
        try:
            faction_res[produce] += prod_res
        except KeyError:
            faction_res[produce] = 0 + prod_res
        gsrpg_reporter('Resource produced',f'Consumed {prod_res} {produce}')


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

        faction_res = factions[faction_name]["resources"]
        fac_res_comparison = {a: faction_res[a] for a in consumption}
        for fac_res, value in fac_res_comparison.items():
            if value < consumption[fac_res]:
                construct_building = False
                break
            else:
                construct_building = True

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

    gsrpg['basic']['turn'] += 1
    print(gsrpg['basic']['turn'])

    temp_dict = {}
    
    

    for faction in gsrpg['factions']:

        buildings = gsrpg['factions'][faction]['buildings']

        for building in buildings:
            mul = buildings[building]

            consumption = buildings_data[building]['consumption']
            production  = buildings_data[building]['production']
            
            resources = gsrpg['factions'][faction]['resources']
            #print(resources,flush=True)

            fac_res_comp = {consume: resources[consume] for consume in consumption}

            if debug:
                print('DEBUG: facres ',fac_res_comp)
                print('DEBUG: con ',consumption)

            bool_comps = [
                resources[consume] > consumption[consume]
                for consume in consumption
            ]

            if False not in bool_comps:
                res_consume_resources(
                    consumption = consumption,
                    faction_res = resources,
                    mul         = mul
                    )
                res_produce_res(
                    faction_res = resources,
                    mul = mul,
                    production = production
                )
        

        
        orders = gsrpg['factions'][faction]['orders']
        
        for order in orders:
            order_execution(
                debug = debug,
                faction_name = faction,
                orders = orders,
                order = order,
            )





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
