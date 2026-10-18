import json, sys, os
order = json.load(open("grades/order.json")); key = {r["id"]: r for r in json.load(open("key.json"))}
for f in sys.argv[1:]:
    g = json.load(open(f))
    for p in g["pairs"]:
        o = order[p["pair"]]
        arm = {s: key[o[s]]["arm"] for s in "AB"}
        v = p["verdict"]; winner = arm[v] if v in "AB" else "tie"
        sc = {arm[s]: sum(p["scores"][s].values()) for s in "AB"}
        extra = ""
        if "caught" in p:
            extra = f" caught with={len(p['caught'][[s for s in 'AB' if arm[s]=='with'][0]])} without={len(p['caught'][[s for s in 'AB' if arm[s]=='without'][0]])} fp with={p['false_positives'][[s for s in 'AB' if arm[s]=='with'][0]]} without={p['false_positives'][[s for s in 'AB' if arm[s]=='without'][0]]}"
        print(f"{p['pair']:28} winner={winner:7} diff={p['difference']:5} score with={sc['with']} without={sc['without']}{extra}")
        print("   ", p["reasons"].replace("\n"," ")[:600])
