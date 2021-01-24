from ciscoconfparse import CiscoConfParse
import csv
import re

f1 = open ("Running.txt")
fread = f1.readlines()
parseddata = CiscoConfParse(fread)
f1.close()

f2 = open("Output.csv","w")
employee_writer = csv.writer(f2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

all_intf_objects = parseddata.find_objects(r"^interface [G|g|E|e|T|t|F|f|V|v].*")

employee_writer.writerow(["Interface","Status","Description","ISE","VLAN","Port"])

for obj in all_intf_objects:

    # For Description
    matchdesc = obj.re_match_iter_typed(r'description (.*)')
    interfacename = re.findall(r"interface (.*)",obj.text)
    if (matchdesc):
        matchdesc = matchdesc
    else:
        matchdesc = "None"

    #For ISE
    matchdot1x = obj.re_search_children("dot1x pae")
    if (matchdot1x):
        matchdot1x = "Dot1x"
    else:
        matchdot1x = "None"

    #For vlan
    matchvlan = obj.re_match_iter_typed(r'switchport access vlan (.*)')
    if(matchvlan):
        matchvlan = matchvlan
    else:
        matchvlan = "None"

    # Port type
    trunk = obj.re_search_children("switchport mode trunk")
    access = obj.re_search_children("switchport mode access")
    if (trunk):
        matchport = "Trunk"
    elif (access):
        matchport = "Access"
    else:
        matchport = "None"

    # Status
    matchshut = obj.re_search_children("shutdown")
    if (matchshut):
        matchshut = "Shutdown"
    else:
        matchshut = "up"

    #Print row to CSV
    employee_writer.writerow([interfacename[0],matchshut,matchdesc,matchdot1x,matchvlan,matchport])
f2.close()