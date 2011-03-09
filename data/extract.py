#!/usr/bin/env python

import json

import lxml.etree

class Node(object):
    children = []

    def __init__(self, element, url=None):
        self.element = element
        if url is not None:
            self.url = url

    def getchildtext(self, element, child):
        try:
            return element.xpath(child)[0].text.strip()
        except (AttributeError, IndexError):
            return ''

    def fixlink(self, link):
        url = self.url + link.lstrip("#~~/")
        if url == self.url:
            url = ''
        return url

    def dict(self):
        data = dict((child, self.getchildtext(self.element, child))
                for child in self.children)
        for link in self.links:
            data[link] = self.fixlink(data[link])

        return data

class PlayEntry(Node):
    children = ["PlayLink", "PlayEventTitle"]
    links = ["PlayLink"]

class Screening(Node):
    children = ["DateTime", "Venue", "VenueName", "VenueLink", "Price",
        "ScreeningCode"]
    links = ["VenueLink"]

    def dict(self):
        screening = Node.dict(self)
        screening["TicketButtonLink"] = self.fixlink(
            self.getchildtext(self.element, "TicketButton/Link"))
        return screening

class Event(Node):
    url = "http://filmguide.wifilmfest.org/"
    children = ["EventImage", "EventNumber", "EventType", "ContainerType",
        "ProgCode", "EventTitle", "EventLink", "EventSection", "Directors",
        "Countrys", "Year", "RunTime", "PrintFormat", "PlayEventTitle"]
    links = ["EventLink", "EventImage"]

    def dict(self):
        event = Node.dict(self)

        event["PlayEntrys"] = [PlayEntry(entry, self.url).dict() for entry \
            in self.element.xpath("PlayEntrys/PlayEntry")]
        event["Screenings"] = [Screening(entry, self.url).dict() for entry \
            in self.element.xpath("Screenings/Screening")]

        return event

def main(argv, stdout):
    tree = lxml.etree.parse(argv[1])
    root = tree.getroot()

    events = [Event(e).dict() for e in root.xpath("/Events/Event")]

    json.dump(events, stdout)

if __name__ == "__main__":
    import sys
    try:
        ret = main(sys.argv, sys.stdout)
    except KeyboardInterrupt:
        ret = None
    sys.exit(ret)
