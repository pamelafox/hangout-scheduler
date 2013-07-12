import os
import datetime
import webapp2
import jinja2
import logging

from google.appengine.api import users
from webapp2_extras.appengine.users import login_required


from models import Topic, TopicSlot, TopicRSVP
import util


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates/"),
    extensions=['jinja2.ext.autoescape'])


class BasePage(webapp2.RequestHandler):
    """The base class for actual pages to subclass."""

    def get(self):
        self.render(self.get_template_filename(), self.get_template_values())

    def get_template_values(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            loggedin = 'true'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            loggedin = 'false'

        template_values = {
            'user': users.get_current_user(),
            'loggedin': loggedin,
            'login_url': url,
            'login_text': url_linktext,
        }
        return template_values

    def get_template_filename(self):
        return 'base.html'

    def render(self, filename, template_values):
        template = JINJA_ENVIRONMENT.get_template(filename)
        self.response.write(template.render(template_values))


class DashboardPage(BasePage):

    def get(self):
        user = users.get_current_user()
        user_topics = Topic.get_for_user(user)
        user_rsvps = []
        for rsvp in TopicRSVP.get_for_user(user):
            rsvp.topic = rsvp.slot.topic
            user_rsvps.append(rsvp)
        template_values = self.get_template_values()
        template_values['topics'] = user_topics
        template_values['rsvps'] = user_rsvps
        self.render('dashboard.html', template_values)


class TopicSignupPage(BasePage):

    def render_signup(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic_slots = topic.slots
        user_rsvps = [rsvp.slot.id for rsvp in TopicRSVP.get_for_user(users.get_current_user())]
        slots = []
        for slot in topic_slots:
            slot.rsvp_count = slot.rsvps.count() or 0
            slot.user_rsvped = (slot.id in user_rsvps)
            slots.append(slot)
        slots = sorted(slots, key=lambda slot: slot.start)
        template_values = self.get_template_values()
        template_values['topic'] = topic
        template_values['topic_slots'] = slots
        self.render('signup.html', template_values)

    @login_required
    def get(self, topic_id):
        self.render_signup(topic_id)

    def post(self, topic_id):
        slot_id = int(self.request.get("slot_id"))
        local_time = self.request.get("local_time")
        action = self.request.get("action")
        topic_slot = TopicSlot.get_by_id(slot_id)
        rsvp = TopicRSVP.all().filter("attendee = ", users.get_current_user()).filter("slot = ", topic_slot).get()
        if not rsvp and action == "signup":
            rsvp = TopicRSVP(slot=topic_slot, attendee=users.get_current_user(), local_time=local_time)
            rsvp.put()
            self.redirect("/")
        if rsvp and action == "unsignup":
            rsvp.delete()
            self.render_signup(topic_id)


class TopicSlotPage(BasePage):

    def render_slot_page(self, slot):
        topic = slot.topic
        template_values = self.get_template_values()
        template_values['slot'] = slot
        template_values['topic'] = topic
        self.render('slot.html', template_values)

    @login_required
    def get(self, slot_id):
        topic_slot = TopicSlot.get_by_id(int(slot_id))
        self.render_slot_page(topic_slot)

    def post(self, slot_id):
        topic_slot = TopicSlot.get_by_id(int(slot_id))
        counter = self.request.get("counter")
        if counter:
            topic_slot.counter = int(counter)
            topic_slot.save()
        self.render_slot_page(topic_slot)


class TopicCreatePage(BasePage):

    @login_required
    def get(self):
        self.render('create.html', self.get_template_values())

    def post(self):
        creator = users.get_current_user()
        title = self.request.get('title')
        descrip = self.request.get('descrip')
        start = util.convert_htmldatetime(self.request.get('start'))
        end = util.convert_htmldatetime(self.request.get('end'))
        slot_minutes = int(self.request.get('slot_minutes'))

        topic = Topic(
            creator=creator,
            title=title,
            descrip=descrip,
            start=start,
            end=end,
            slot_minutes=slot_minutes)
        topic.put()

        # Now create slots
        current_slot = start
        while (current_slot < end):
            slot = TopicSlot(start=current_slot, topic=topic)
            slot.put()
            current_slot += datetime.timedelta(minutes=slot_minutes)
        self.redirect(topic.full_link)
