import urllib.request
import icalendar
import models

# pull events into local file
url = "https://engagexu.campusgroups.com/ical/ical_xavier.ics"
urllib.request.urlretrieve(url, "global_events.ics")

e = open('global_events.ics', 'rb')
ecal = icalendar.Calendar.from_ical(e.read())
for component in ecal.walk():
    if component.name == "VEVENT":
        newEvent = models.CalendarEvent(
            name=component.get("name"),
            description=component.get("description"),
            organizer=component.get("organizer"),
            location=component.get("location"),
            startTime=component.decoded("dtstart"),
            endTime=component.decoded("dtend")
        )
        newEvent.save()
e.close()
