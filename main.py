
import webapp2

import pages
import emails

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', pages.DashboardPage),
    webapp2.Route('/help/setup', handler=pages.HelpSetupPage),
    webapp2.Route('/topic/create', handler=pages.TopicCreatePage),
    webapp2.Route('/topic/<topic_id:\d+>', handler=pages.TopicSignupPage),
    webapp2.Route('/topic/slot/<:\d+>', handler=pages.TopicSlotPage),
    webapp2.Route('/email/setup-reminders', handler=emails.SetupRemindersHandler),
    webapp2.Route('/email/empty-reminders', handler=emails.EmptyHangoutsHandler),
    webapp2.Route('/email/reminders', handler=emails.RemindersHandler),
    webapp2.Route('/email/send', handler=emails.SendHandler),
])
