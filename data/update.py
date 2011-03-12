import json
import time

venues = {
    "Bartell Theater": "BARTELL",
    "Chazen Museum of Art": "CHAZEN",
    "Madison Museum of Contemporary Art": "MMOCA",
    "Monona Terrace Convention Center": "MONONA",
    "Orpheum Main Theater": "ORPH",
    "Play Circle Theater": "PLAY",
    "Stage Door Theater": "STAGE",
    "UW Cinematheque": "CINEMA",
    "Wisconsin Union Theater": "UNION",
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

    films = (e for e in data if e["EventType"] in ("M", "F"))

    for film in films:
        for screening in film["Screenings"]:
            data = screening.copy()
            data.update(film)
            data["DateTime"] = restrftime("%Y.%m.%d %H:%M %a",
                screening["DateTime"])
            data["ShortVenue"] = venues.get(data["VenueName"], data["VenueName"])
            data["ASCIIEventTitle"] = data["EventTitle"].encode("ascii", "ignore")
            data["NumberTickets"] = "NNN"
            if not data["TicketButtonLink"]:
                data["ASCIIEventTitle"] += "*"

            stdout.write(screeningfmt % data)

if __name__ == "__main__":
    import sys
    try:
        ret = main(sys.argv, sys.stdout)
    except KeyboardInterrupt:
        ret = None
    sys.exit(ret)
