from typing import List
from arcgis.gis import GIS, Item
from arcgis.features import FeatureLayer
from copy import deepcopy


def update_aliases(gis: GIS, item_id: str, lookup_list: List):

    
    # Get layer count from service
    update_item = Item(gis, itemid=item_id)
    rest_layer_count = len(update_item.layers)

    looper = 0
    while rest_layer_count > 0:
        # Access the feature layer intended for updating
        search = gis.content.search("id:" + item_id, item_type="Feature Layer")
        #TODO: Test if search is empty

        featureLayer = FeatureLayer.fromitem(search[0], layer_id=looper)
        layerName = search[0].name
        print("Updating layer " + str(looper) + " on " + str(layerName) + "...")

        print("\tGetting field definitions from service...")
        # Loop through fields in service and store JSON for any that are going to be updated
        layerFields = featureLayer.manager.properties.fields

        print("\tFinding fields to update...")
        # Loop through the fields in the service
        updateJSON = []
        for field in layerFields:
            fieldName = field['name']
            for lookupField in lookup_list:
                # As you loop through the service fields, see if they match a field in the excel document
                if lookupField[0] == fieldName:
                    # store the field JSON from the online layer
                    fieldJSON = dict(deepcopy(field))
                    # assign the new alias name in JSON format
                    if lookupField[1]:
                        alias = lookupField[1]
                        fieldJSON['alias'] = alias
                    else:
                        alias = ""
                    # Assign field type, if specified
                    if lookupField[3]:
                        fldType = lookupField[3]
                    else:
                        fldType = ""
                    # assign the new field description in JSON format, if specified
                    if lookupField[2]:
                        longDesc = lookupField[2]
                        # Remove escape characters like double quotes, newlines, or encoding issues
                        if "<" in longDesc or ">" in longDesc:
                            print("Special character > or < found in field: " + fieldName)
                            print("Script will not run as expected. Please remove all hyperlinks or > < characters from your long description and rerun the script.")
                        longDesc = longDesc.replace('"', '\\\"').replace("\n", " ").replace("\t", " ").replace(u'\xa0', u' ').replace(">=", " greater than or equal to ").replace("<=", " less than or equal to ").replace(">", " greater than ").replace("<", " less than ")
                    else:
                        longDesc = ""
                    # Build the JSON structure with the proper backslashes and quotes
                    fieldJSON['description'] = f'{{"value":"{longDesc}","fieldValueType":"{fldType}"}}'
                    fieldJSON.pop('sqlType', None)
                    if alias != "":
                        print("\t\tField '" + fieldName + "' will be updated to get the alias name '" + alias + "'")
                    if longDesc != "":
                        print("\t\t\t\tThe long description for this field was also updated")
                    if fldType != "":
                        print("\t\t\t\tThe field type for this field was also updated to: " + fldType)
                    # Create a python list containing any fields to update
                    updateJSON.append(fieldJSON)

        if updateJSON:
            print("\tUpdating alias names of the REST service...")
            #jsonFormat =  json.dumps(updateJSON)
            aliasUpdateDict = {'fields': updateJSON}
            #aliasUpdateJSON = json.dumps(aliasUpdateDict)
            # Use the update definition call to push the new alias names into the service
            featureLayer.manager.update_definition(aliasUpdateDict)
            print("\tAlias names updated on service!")

        # Now check if the item has a pop-up configuration saving the alias names as well
        # First, grab the item JSON for the layer and create an item to hold the new edited JSON
        print("\tUpdating the alias names within the pop-up configuration on the item...")
        item = Item(gis, itemid=item_id)

        # Grab the existing JSON for the popup, store a copy, and edit the aliases
        itemJSON = item.get_data(try_json=True)
        # Loop through the existing layer and check if any alias names don't match
        counter = 0
        if itemJSON:
            print("\tFinding all replacements of alias names within pop-up...")
            newItemJSON = deepcopy(itemJSON)
            new_field_info = newItemJSON['layers'][looper]['popupInfo']['fieldInfos'][counter]
            print("\t\tUpdating alias names in popup fieldInfos...")
            for field_info in itemJSON['layers'][looper]['popupInfo']['fieldInfos']:
                fieldName2 = field_info['fieldName']
                for lookup in lookup_list:
                    if lookup[0] == fieldName2:
                        if lookup[1] != None:
                            new_field_info['label'] = lookup[1]
                        # Check if there is a decimal spec
                        if "format" in field_info and "places" in field_info["format"]:
                            # If a value is specified in the lookup doc, assign that
                            if lookup[4] != None:
                                new_field_info['format']['places'] = lookup[4]
                            # If a value is not specified and the decimals have defaulted to 6, change to 2
                            else:
                                if new_field_info['format']['places'] == 6:
                                    new_field_info['format']['places'] = 2
                        # Update thousands separator if lookup document specifies and if it exists in JSON
                        if lookup[5] != None and str(lookup[5]).lower() != "no" and str(lookup[5]).lower() != "false" and "format" in field_info and "digitSeparator" in field_info["format"]:
                            new_field_info['format']['digitSeparator'] = True


                counter += 1

            # Check if layer was updated in new Map Viewer and contains a popupElement JSON section with fieldInfos
            if 'popupInfo' in itemJSON['layers'][looper] and 'popupElements' in itemJSON['layers'][looper]['popupInfo'] and itemJSON['layers'][looper]['popupInfo']["popupElements"]:
                popup_element_index = 0
                for popup_element in itemJSON['layers'][looper]['popupInfo']["popupElements"]:
                    if popup_element['type'] == 'fields':
                        print("\t\tUpdating popupElement fieldInfo...")
                        #TODO: Check if fieldInfos exists in popupElement; Consider redesigning this section                       
                        counter2 = 0
                        if "fieldInfos" in itemJSON['layers'][looper]['popupInfo']["popupElements"][popup_element_index]:
                            for j in itemJSON['layers'][looper]['popupInfo']["popupElements"][popup_element_index]["fieldInfos"]:
                                fldName = j["fieldName"]
                                for lkup in lookup_list:
                                    if lkup[0] == fldName:
                                        if lkup[1] != None:
                                            newItemJSON['layers'][looper]['popupInfo']['popupElements'][popup_element_index]["fieldInfos"][counter2]['label'] = lkup[1]
                                        # Check if there is a decimal spec
                                        if "format" in j and "places" in j["format"]:
                                            # If a value is specified in the lookup doc, assign that
                                            if lkup[4] != None:
                                                newItemJSON['layers'][looper]['popupInfo']['popupElements'][popup_element_index]["fieldInfos"][counter2]['format']['places'] = lkup[4]
                                            # If a value is not specified and the decimals have defaulted to 6, change to 2
                                            else:
                                                if newItemJSON['layers'][looper]['popupInfo']['popupElements'][popup_element_index]["fieldInfos"][counter2]['format']['places'] == 6:
                                                    newItemJSON['layers'][looper]['popupInfo']['popupElements'][popup_element_index]["fieldInfos"][counter2]['format']['places'] = 2
                                        # Update thousands separator if lookup document specifies and if it exists in JSON
                                        if lkup[5] != None and str(lkup[5]).lower() != "no" and str(lkup[5]).lower() != "false" and "format" in j and "digitSeparator" in j["format"]:
                                            newItemJSON['layers'][looper]['popupInfo']['popupElements'][popup_element_index]["fieldInfos"][counter2]['format']['digitSeparator'] = True
                                counter2 += 1
                    popup_element_index += 1


            # Update json
            print("\tUpdating the alias names within the existing item pop-up...")
            update = item.update(item_properties={'text': newItemJSON})
            if update:
                print("\tSuccess! Your alias names have been updated. Please check your service to confirm.")
            else:
                print("\tUpdating pop-up failed.")
        else:
            print("\tNo pop-up JSON. Skipping.")

        looper += 1
        rest_layer_count -= 1