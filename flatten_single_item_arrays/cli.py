from collections import defaultdict
from pprint import pprint
import click
import json


@click.command()
@click.version_option()
@click.argument("input_file", type=click.File("r"))
@click.option("--debug", is_flag=True)
def cli(input_file, debug):
    "Given a JSON list of objects, flatten any keys which always contain single item arrays to just a single value"
    data = json.load(input_file)
    assert isinstance(data, list), "Input should be a JSON array"
    assert all(
        (isinstance(d, dict) for d in data)
    ), "Input should be a JSON array of objects"
    # Seek out columns that are ALWAYS lists with a single item
    count_of_single_item_lists = defaultdict(int)
    count_of_present_keys = defaultdict(int)
    for item in data:
        for key, value in item.items():
            count_of_present_keys[key] += 1
            if isinstance(value, list) and len(value) == 1:
                count_of_single_item_lists[key] += 1
    keys_to_reformat = [
        k
        for k in count_of_single_item_lists
        if count_of_single_item_lists[k] == count_of_present_keys[k]
    ]

    if debug:
        click.echo("Item count: {}".format(len(data)), err=True)
        click.echo("count_of_single_item_lists", err=True)
        click.echo(json.dumps(count_of_single_item_lists, indent=4), err=True)
        click.echo("count_of_present_keys", err=True)
        click.echo(json.dumps(count_of_present_keys, indent=4), err=True)
        click.echo(
            "keys_to_reformat:\n{}".format(
                "\n".join("- {}".format(k) for k in keys_to_reformat)
            ),
            err=True,
        )
    # Now reformat the data
    for item in data:
        for key in keys_to_reformat:
            if key in item and isinstance(item[key], list) and len(item[key]) == 1:
                item[key] = item[key][0]

    click.echo(json.dumps(data, indent=4))
