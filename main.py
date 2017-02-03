#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

def build_page(error_username='', error_password='',
                error_verify='', error_email='',
                 username='', email=''):
    stylecss = """
    <style type='text/css'>
        #error {color: red}
    </style>
    """
    usr_name_label = "<td><lable>UserName</lable></td>"
    pwd_label = "<td><lable>Password</lable></td>"
    ver_pwd_lable = "<td><lable>Verify Password</lable></td>"
    email_lable = "<td><lable>Email (optional)</lable></td>"

    usr_name_inp = "<td><input name='username' type='text' value='" + username + "' required></td>"
    pwd_inp = "<td><input name='password' type='password'  required></td>"
    ver_pwd_inp = "<td><input name='verify' type='password' required></td>"
    email_inp = "<td><input name='email' type='text' value='" + email + "'></td>"

    error_username = "<td id='error'>" + error_username + "</td>" 
    error_password = "<td id='error'>" + error_password + "</td>" 
    error_verify = "<td id='error'>" + error_verify + "</td>" 
    error_email = "<td id='error'>" + error_email + "</td>" 
    
    sub_btn = "<input type='submit'>"
    head = "<h1>Signup!</h1>"
    br = "<br>"

    form = head + stylecss + ("<form action='/welcome' method='post'> <table> <tr>" + 
        usr_name_label + usr_name_inp + error_username + "</tr>" + 
        "<tr>" +pwd_label + pwd_inp + error_password + "</tr> <tr>" + 
        ver_pwd_lable + ver_pwd_inp + error_verify + "</tr>" + 
        "<tr>" +email_lable + email_inp + error_email + "</tr></table>" + 
        sub_btn + "</form>")
    return form

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(build_page())   

class Welcome(webapp2.RequestHandler):
    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
            email = email)

        content = "<h1>Welcome, " + username + "!</h1>"
        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            params['username'] = ''
            have_error = True
        else:
            params['error_username'] = ''

        if not valid_password(password):
            params['error_password'] = "That's not a valid password."
            have_error = True
        else:
            params['error_password'] = ''

        if password != verify:
            params['error_verify'] = "Your Password didnt match."
            have_error = True
        else:
            params['error_verify'] = ''

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            params['email'] = ''
            have_error = True
        else:
            params['error_email'] = ''
        
        # error = self.request.get("error")

        if have_error:
            # error = ?error
            #self.redirect("/?error=" + params['error_verify'])
            self.response.write(build_page(params['error_username'],
                params['error_password'],params['error_verify'],
                params['error_email'], params['username'], params['email']))
        else:
            self.response.write(content)

class ErrPage(webapp2.RequestHandler):
    def get(self):
        content = "<h1>error, !</h1>"
        self.response.write(build_page())

app = webapp2.WSGIApplication([
    ('/', MainHandler), 
    ('/welcome', Welcome),
    ('/errpage', ErrPage)
], debug=True)
