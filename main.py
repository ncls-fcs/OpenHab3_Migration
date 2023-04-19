THING_TYPE = 0
THING_ID = 1


class Thing:
    id = ""
    label = ""
    address = ""
    type = ""


def OH2_KNX_lightThingConfigToOH3_KNX_ChannelConfig(configFile):
    thingList = []

    with open(configFile, 'r') as file:

        for line in file:
            currentThing = Thing()

            isInLabel = False
            isInAddress = False
            isInKNX = False
            if line.isspace() or line.startswith("//"):
                continue

            for index, word in enumerate(line.split(" ")):
                if word == "Switch":
                    currentThing.type = "Switch"
                elif word == "Rollershutter":
                    currentThing.type = "Rollershutter"

                if word == "":
                    continue

                if word.startswith("{"):
                    isInAddress = True

                if word.endswith("}"):
                    isInAddress = False

                if (word.startswith("\"") or isInLabel) and not isInAddress and not word.endswith("\""):
                    isInLabel = True
                    currentThing.label += word.strip("\"") + " "

                if word.endswith("\"") and not isInAddress:
                    isInLabel = False
                    currentThing.label += word.strip("\"")

                elif not word.startswith("\"") and not word.startswith("<") and not word.startswith(
                        "(") and not word.startswith("{") and not word.endswith(
                        ")") and not isInAddress and not isInLabel:
                    currentThing.id = word

                if word.startswith("knx=") or isInKNX:
                    currentThing.address += word.strip("knx=\",")
                    if word.endswith(","):
                        isInKNX = True
                        currentThing.address += "+"
                    else:
                        isInKNX = False

            thingList.append(currentThing)
    return thingList


def thingObjectToOH3Channel(thing):
    #outputs channel string to put in the MainUI Code for an already created Thing (everything throug MainUI)
    with open("output.txt", "a") as file:
        file.write(
            "  - id: " + thing.id + "\n    channelTypeUID: knx:" + thing.type + "\n    label: " + thing.label + "\n    description: \"\"\n    configuration:\n      ga: " + thing.address + "\n")

#functions for formatting to JSON to be inserted directly into "org.openhab.core.thing.Thing.json"

def thingObjectToOH3Thing(thing):
    # converts internal thingObject to a JSON String readable by OpenHab3 that describes this internal thingObject with one Channel, where the ID of the OHThing and the ID of the OHChannel are the same
    with open("OH3ThingBlueprint.txt", "r") as blueprint:
        with open("thing_output.txt", "a") as output:
            blueprintString = blueprint.read()
            result = blueprintString % {"itemType": thing.type, "id": thing.id, "channelTypeUID": thing.type.lower(), "label": thing.label, "configuration": formatChannelConfiguration(thing)}

            output.write(result)

def formatChannelConfiguration(thing):
    if thing.type == "Switch":
        return "\"ga\": \"" + thing.address + "\""
    elif thing.type == "Rollershutter":
        return "\"upDown\": \"" + thing.address + "\""


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    thingsList = OH2_KNX_lightThingConfigToOH3_KNX_ChannelConfig('EIB.txt')
    for thing in thingsList:
    #    print("Type: " + thing.type + ", id: " + thing.id + ", Label: " + thing.label + ", address: " + thing.address)
        if thing.type == "Switch" or thing.type == "Rollershutter":
            thingObjectToOH3Thing(thing)
