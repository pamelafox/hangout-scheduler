import webapp2
import datetime
import logging

from google.appengine.api import mail
from google.appengine.api import taskqueue

from models import TopicSlot

DOMAIN = 'hangout-scheduler'
SENDER = 'Hangout scheduler <noreply@%s.appspotmail.com>' % (DOMAIN)

REMINDER_SUBJECT = 'Reminder: Upcoming hangout on %s'
REMINDER_BODY = """
You signed up for a hangout discussion on %s.

At %s, please follow this link and join a hangout:
%s
"""


class RemindersHandler(webapp2.RequestHandler):

    def get(self):
        start_looking = datetime.datetime.now() + datetime.timedelta(minutes=120)
        stop_looking = start_looking + datetime.timedelta(minutes=60)
        slots = TopicSlot.all().filter('start >=', start_looking).filter('start <=', stop_looking).fetch(10000)
        for slot in slots:
            slot_subject = REMINDER_SUBJECT % (slot.topic.title)
            for rsvp in slot.rsvps.fetch(10000):
                if not rsvp.notified:
                    slot_body = REMINDER_BODY % (slot.topic.title, rsvp.local_time, slot.full_link)
                    taskqueue.add(url='/email/reminder', params={'email': rsvp.attendee, 'subject': slot_subject, 'body': slot_body})

            slot.notified = True
            slot.save()


class ReminderHandler(webapp2.RequestHandler):
    def post(self):
        mail.send_mail(sender=SENDER,
                       to=self.request.get('email'),
                       subject=self.request.get('subject'),
                       body=self.request.get('body'))

    def get(self):
        self.post()