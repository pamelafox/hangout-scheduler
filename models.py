import datetime

from google.appengine.ext import db
from google.appengine.api import users

import util


class Topic(db.Model):
    creator = db.UserProperty()
    title = db.StringProperty()
    descrip = db.StringProperty(multiline=True)
    start = db.DateTimeProperty()  # UTC
    end = db.DateTimeProperty()  # UTC
    slot_capacity = db.IntegerProperty()
    slot_minutes = db.IntegerProperty()

    @property
    def full_link(self):
        return '%s/topic/%d' % (util.get_host(), self.key().id())

    @classmethod
    def get_for_user(cls, user):
        return cls.all().filter("creator = ", user).fetch(1000)


class TopicSlot(db.Model):
    start = db.DateTimeProperty()
    topic = db.ReferenceProperty(Topic, collection_name="slots")
    counter = db.IntegerProperty(default=1)

    @property
    def id(self):
        return self.key().id()

    @property
    def start_iso(self):
        return self.start.isoformat()

    @property
    def end_iso(self):
        end = self.start + datetime.timedelta(minutes=self.topic.slot_minutes)
        return end.isoformat()

    @property
    def full_link(self):
        return '%s/topic/slot/%d' % (util.get_host(), self.key().id())


class TopicRSVP(db.Model):
    attendee = db.UserProperty()
    slot = db.ReferenceProperty(TopicSlot, collection_name="rsvps")
    notified = db.BooleanProperty(default=False)
    local_time = db.StringProperty()

    @classmethod
    def get_for_user(cls, user):
        return cls.all().filter("attendee = ", users.get_current_user()).fetch(1000)
