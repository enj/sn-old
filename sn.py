import os
import webapp2
import jinja2
from uuid import uuid3, NAMESPACE_DNS
from datetime import datetime, timedelta, date

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = \
            jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def headers(self, x, y):
        self.response.headers[x] = y
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):

        def sndate(year, week):
            ret = datetime.strptime('%04d-%02d-3' % (year, week), '%Y-%W-%w')
            if date(year, 1, 4).isoweekday() > 4:
                ret -= timedelta(days=7)
            return ret.strftime("%a, %d %b %Y")

        def snuuid(e):
            return uuid3(NAMESPACE_DNS, 'SecurityNowOld%s' % e)

        years = {
                2005 : [1, 20],
                2006 : [21, 72],
                2007 : [73, 124],
                2008 : [125, 176],
                2009 : [177, 229],
                2010 : [230, 281],
                2011 : [282, 333],
                2012 : [334, 384],
                2013 : [385, 436],
                2014 : [437, 488]
                }

        year = self.request.get("y")
        min_year = min(years)
        max_year = max(years)
        default_year = 2005
        mod = 0
        if not year.isdigit():
            year = default_year
        else:
            year = int(year)
            if year < min_year or year > max_year:
                year = default_year
        if year == 2005:
            mod = 32
        lower, upper = years[year]

        episodes = range(lower, upper + 1)
        episodes.reverse()
        week = lower - mod - 1

        total = [ ( e, str(e).zfill(3), snuuid(e), sndate(year, (e - week)) ) \
                    for e in episodes ]

        self.headers('Content-Type', 'application/xml')
        self.render("item.xml", total = total, year = year)

application = webapp2.WSGIApplication([('/', MainPage)], debug=True)