import json
import time

venues = {
    "Bartell Theatre": "BARTELL",
    "Chazen Museum of Art": "CHAZEN",
    "Madison Museum of Contemporary Art": "MMOCA",
    "Monona Terrace Convention Center": "MONONA",
    "Orpheum Main Theatre": "ORPH",
    "Play Circle Theatre": "PLAY",
    "Stage Door Theatre": "STAGE",
    "UW Cinematheque": "CINEMA",
    "Wisconsin Union Theatre": "UNION",
}
screeningfmt = "%(DateTime)s %(RunTime)3s %(ShortVenue)7s %(ScreeningCode)s " \
    "%(NumberTickets)3s %(ASCIIEventTitle)s\n"

def restrftime(fmt, data, datafmt="%a, %b %d | %I:%M %p"):
    parsed = list(time.strptime(data, datafmt))
    parsed[0] = time.localtime().tm_year

    return time.strftime(fmt, parsed)

def main(argv, stdout):
    with open(argv[1]) as f:
        data = json.load(f)

    # XXX: load selections by ScreeningCode
    selections = {}
    with open(argv[2]) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            screening, people = [x.strip() for x in line.split(None, 1)]
            selections[screening] = people.split(',')
    cart = {}

    films = data
    filmtypes = ("F", "C")

    for film in films:
        if film["EventType"] not in filmtypes:
            continue
        for screening in film["Screenings"]:
            numtix = len(selections.get(screening["ScreeningCode"], []))
            if numtix == 0:
                continue
            data = screening.copy()
            data.update(film)
            data["DateTime"] = restrftime("%Y.%m.%d %H:%M %a",
                screening["DateTime"])
            data["ShortVenue"] = venues.get(data["VenueName"], data["VenueName"])
            data["ASCIIEventTitle"] = data["EventTitle"].encode("ascii", "ignore")
            data["NumberTickets"] = numtix
            if not data["TicketButtonLink"]:
                data["ASCIIEventTitle"] += "*"
            tix = data['TicketButtonLink']
            cart[tix] = cart.setdefault(tix, 0) + numtix

            stdout.write(screeningfmt % data)

    stdout.flush()
    stdout.write("\n")

    for link, count in cart.items():
        stdout.write("%4d %s\n" % (count, link))

if __name__ == "__main__":
    import sys
    try:
        ret = main(sys.argv, sys.stdout)
    except KeyboardInterrupt:
        ret = None
    sys.exit(ret)
