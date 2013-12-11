import urllib, urllib2, cookielib
from BeautifulSoup import BeautifulSoup

class login():
    '''Class initializes urllib2 with cookies associated with cybercommons login'''
    def __init__(self,username,password,login_url='http://apps.cybercommons.org/accounts/login/'):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        url = urllib2.urlopen(login_url)
        html = url.read()
        doc = BeautifulSoup(html)
        csrf_input = doc.find(attrs = dict(name = 'csrfmiddlewaretoken'))
        csrf_token = csrf_input['value']
        params = urllib.urlencode(dict(username = username, password=password,
                 csrfmiddlewaretoken = csrf_token))
        url = urllib2.urlopen(login_url, params)

    def get(self):
        '''Returns urllib2 with cookies from cybercommons login'''
        return urllib2
