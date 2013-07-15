import webapp2
import datetime
import logging

from google.appengine.api import mail
from google.appengine.api import taskqueue

from models import TopicSlot
import util


DOMAIN = 'hangout-scheduler'
SENDER = 'Hangout scheduler <noreply@%s.appspotmail.com>' % (DOMAIN)

REMINDER_SUBJECT = 'Reminder: Upcoming hangout on %s'
REMINDER_BODY = """
You signed up for a hangout discussion on %s.

At %s, please follow this link and join a hangout:
%s
"""

SETUP_REMINDER_SUBJECT = 'Reminder: Get ready for your hangout on %s'
SETUP_REMINDER_BODY = """
You signed up for a hangout discussion on %s.

It's starting in 5 minutes, so please start getting setup now. See instructions here:
%s

When it starts, you can join it here:
%s
"""

EMPTY_SUBJECT = 'Your hangout discussion slot on %s needs more signups'

EMPTY_BODY = """
You signed up for a hangout discussion on %s at %s.

However, nobody else has signed up for that slot yet, and it's starting in 24 hours.
You may want to revisit the signup page and find a lot that has other signups,
or suggest to people you know that they sign up for your slot:
%s
"""


class EmptyHangoutsHandler(webapp2.RequestHandler):

    def get(self):
        # look for slots starting in 24 hours, notify them that their slots are empty
        start_looking = datetime.datetime.now() + datetime.timedelta(minutes=60*24)
        stop_looking = start_looking + datetime.timedelta(minutes=60)
        slots = TopicSlot.get_between_times(start_looking, stop_looking)
        for slot in slots:
            if slot.topic.slot_capacity == 1:
                return
            slot_subject = EMPTY_SUBJECT % (slot.topic.title)
            rsvps = slot.rsvps.fetch(3)
            if len(rsvps) > 1:
                return
            for rsvp in rsvps:
                if not rsvp.notified_empty:
                    slot_body = EMPTY_BODY % (slot.topic.title, rsvp.local_time, slot.full_link)
                    taskqueue.add(url='/email/send', params={'email': rsvp.attendee, 'subject': slot_subject, 'body': slot_body})
                    rsvp.notified_empty = True
                    rsvp.save()


class SetupRemindersHandler(webapp2.RequestHandler):

    def get(self):
        start_looking = datetime.datetime.now() - datetime.timedelta(minutes=5)
        stop_looking = start_looking + datetime.timedelta(minutes=15)
        slots = TopicSlot.get_between_times(start_looking, stop_looking)
        for slot in slots:
            slot_subject = SETUP_REMINDER_SUBJECT % (slot.topic.title)
            for rsvp in slot.rsvps.fetch(10000):
                if not rsvp.notified_setup:
                    slot_body = SETUP_REMINDER_BODY % (slot.topic.title, util.get_host() + '/help/setup', slot.topic.full_link)
                    taskqueue.add(url='/email/send', params={'email': rsvp.attendee, 'subject': slot_subject, 'body': slot_body})
                    rsvp.notified_setup = True
                    rsvp.save()


class RemindersHandler(webapp2.RequestHandler):

    def get(self):
        start_looking = datetime.datetime.now() + datetime.timedelta(minutes=120)
        stop_looking = start_looking + datetime.timedelta(minutes=60)
        slots = TopicSlot.get_between_times(start_looking, stop_looking)
        for slot in slots:
            slot_subject = REMINDER_SUBJECT % (slot.topic.title)
            for rsvp in slot.rsvps.fetch(10000):
                if not rsvp.notified:
                    slot_body = REMINDER_BODY % (slot.topic.title, rsvp.local_time, slot.full_link)
                    taskqueue.add(url='/email/reminder', params={'email': rsvp.attendee, 'subject': slot_subject, 'body': slot_body})
                    rsvp.notified = True
                    rsvp.save()


class SendHandler(webapp2.RequestHandler):
    def post(self):
        logging.info(self.request.get('subject'))
        logging.info(self.request.get('body'))
        mail.send_mail(sender=SENDER,
                       to=self.request.get('email'),
                       subject=self.request.get('subject'),
                       body=self.request.get('body'))

    def get(self):
        self.post()