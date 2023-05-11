import glob
import os
import random
import re
import time

from utils.hvh.parse import getMinMaxValuesBySVG


def GET(self,dbCollection,search):

    files = glob.glob("uploaded/*.pdf")
    basefile = files[random.randint(0,len(files)-1)]
    print(basefile)
    # basefile = "uploaded/Stratus 130.pdf"


    # TODO: Handle file upload?
    t = round(time.time())
    os.system(f'mkdir uploaded/{t} && pdf2svg "{basefile}" uploaded/{t}/%d.svg all')

    all_lns = []

    scale = 3

    for file in glob.glob(f"uploaded/{t}/*.svg"):
        lns = []
        with open(file) as handler:
            lines = handler.read().split("\n")
            for line in lines:
                if re.search(r"fill:rgb\(50%,50%,50%\);",line) != None or \
                    re.search(r"fill:rgb\(83.59375%,83.59375%,83.59375%\)",line) != None:
                    dat = getMinMaxValuesBySVG(line.split(" d=\"")[1].split("\"")[0])
                    # min,max = dat
                    # lns.append({"min":min,"max":max})
                    lns.append(dat)
        if len(lns) > 10:
            min = [999999999,9999999999]
            for item in lns:
                if item[0]<min:
                    min[0] = item[0][0]
                    min[1] = item[0][1]
            # print(min)
            for idx,item in enumerate(lns):
                lns[idx][0][0] = (lns[idx][0][0] - min[0])*scale
                lns[idx][0][1] = (lns[idx][0][1] - min[1])*scale

                lns[idx][1][0] = (lns[idx][1][0] - min[0])*scale
                lns[idx][1][1] = (lns[idx][1][1] - min[1])*scale

            
            all_lns.append(lns)
    
    if len(all_lns)<=0:
        return {
            "_id": "-1",
            "info": {
                "basefile":basefile,
                "number_of_floorplans_in_file":len(all_lns),
                "chosen_plan":-1
            },
            "success": False,
            "name": "",
            "walls": [],
            "junctions": [],
            "rooms": [],
            "scale": -1
        }

    chosen_plan = random.randint(0,len(all_lns)-1)
    print(f"no {chosen_plan} of {len(all_lns)}")

    walls = []
    for wall in all_lns[chosen_plan]:
        isHorizontal = wall[1][0]-wall[0][0] > wall[1][1]-wall[0][1]
        
        depth = wall[1][0]-wall[0][0] if not isHorizontal else wall[1][1]-wall[0][1]

        walls.append({
            "fromPosition": {
                "x": wall[0][0],
                "y": wall[0][1]
            },
            "toPosition": {
                "x": wall[1][0],
                "y": wall[1][1]
            },
            "isHorizontal": isHorizontal,
            "isOuterWall": True,
            "features": [],
            "depth": depth,
            "height": 391
        })

    os.system(f"rm -rf uploaded/{t}")
    
    return {
        "_id": "-1",
        "info": {
            "basefile":basefile,
            "number_of_floorplans_in_file":len(all_lns),
            "chosen_plan":chosen_plan
        },
        "success": True,
        "name": basefile.split("/")[1].split(".")[0],
        "walls": walls,
        "junctions": [],
        "rooms": [],
        "scale": scale
    }
