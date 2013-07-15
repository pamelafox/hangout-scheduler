import datetime

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import ndb

import util


# We set a parent key on the models to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.


class Topic(db.Model):
    creator = db.UserProperty()
    title = db.StringProperty()
    descrip = db.StringProperty(multiline=True)
    start = db.DateTimeProperty()  # UTC
    end = db.DateTimeProperty()  # UTC
    slot_capacity = db.IntegerProperty(default=6)
    slot_minutes = db.IntegerProperty()

    @property
    def full_link(self):
        return '%s/topic/%d' % (util.get_host(), self.key().id())

    @classmethod
    def get_for_user(cls, user):
        return cls.all().filter("creator = ", user).fetch(1000)

    @classmethod
    def get_parent_key(cls):
        return ndb.Key('TopicSlot', 'all')


class TopicSlot(db.Model):
    start = db.DateTimeProperty()
    topic = db.ReferenceProperty(Topic, collection_name="slots")
    counter = db.IntegerProperty(default=1)

    @property
    def id(self):
        return self.key().id()

    @property
    def end(self):
        return self.start + datetime.timedelta(minutes=self.topic.slot_minutes)

    @property
    def start_iso(self):
        return self.start.isoformat()

    @property
    def end_iso(self):
        return self.end.isoformat()

    @property
    def start_gcal(self):
        return self.start.strftime("%Y%m%dT%H%M%SZ")

    @property
    def end_gcal(self):
        return self.end.strftime("%Y%m%dT%H%M%SZ")

    @property
    def happening_now(self):
        right_now = datetime.datetime.now()
        loose_start = self.start - datetime.timedelta(minutes=10)
        loose_end = self.end + datetime.timedelta(minutes=30)
        return (right_now >= loose_start and right_now <= loose_end)

    @property
    def full_link(self):
        return '%s/topic/slot/%d' % (util.get_host(), self.key().id())

    @classmethod
    def get_between_times(cls, start, end):
        return cls.all().filter('start >=', start).filter('start <=', end).fetch(10000)

    @classmethod
    def get_parent_key(cls):
        return ndb.Key('TopicSlot', 'all')


class TopicRSVP(db.Model):
    attendee = db.UserProperty()
    slot = db.ReferenceProperty(TopicSlot, collection_name="rsvps")
    notified = db.BooleanProperty(default=False)
    notified_setup = db.BooleanProperty(default=False)
    notified_empty = db.BooleanProperty(default=False)
    local_time = db.StringProperty()

    @classmethod
    def get_for_user(cls, user):
        return cls.all().filter("attendee = ", user).fetch(1000)

    @classmethod
    def get_for_user_and_slot(cls, user, slot):
        return cls.all().filter("attendee = ", user).filter("slot = ", slot).get()

    @classmethod
    def get_parent_key(cls):
        return ndb.Key('TopicRSVP', 'all')
