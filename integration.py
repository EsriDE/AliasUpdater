import argparse
from getpass import getpass
import sys

from aliasupdater.login import authenticate
from aliasupdater.io import read_lookuptable
from aliasupdater.admin import update_aliases



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=False, help='Optional string. If URL is None, then the URL will be ArcGIS Online.')
    #parser.add_argument('--username', type=str, required=True, help='The name of the user.')
    #parser.add_argument('--password', type=str, required=True, help='The password of the user.')
    parser.add_argument('--item_id', type=str, required=True, help='The unique id of the portal item.')
    parser.add_argument('--lookup', type=str, required=True, help='The local filepath to the spreadsheet.')
    args = parser.parse_args()

    try:
        username = input("Enter username: ")
        password = getpass()
        login = authenticate(args.url, username, password)
    except Exception as ex:
        print(ex)
        sys.exit(-1)

    try:
        lookup_list = read_lookuptable(args.lookup)
        update_aliases(login, args.item_id, lookup_list)
    except Exception as ex:
        # TODO: Print to the user or logging!
        print(ex)
        sys.exit(-1)