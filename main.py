
import webapp2

import pages
import emails

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', pages.DashboardPage),
    webapp2.Route('/topic/create', handler=pages.TopicCreatePage),
    webapp2.Route('/topic/<topic_id:\d+>', handler=pages.TopicSignupPage, name='topic_signup'),
    webapp2.Route('/topic/slot/<:\d+>', handler=pages.TopicSlotPage),
    webapp2.Route('/email/reminders', handler=emails.RemindersHandler),
    webapp2.Route('/email/reminder', handler=emails.ReminderHandler),
])
