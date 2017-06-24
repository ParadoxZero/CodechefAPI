"""
Copyright 2016 Sidhin S Thomas <sidhin.thomas@gmail.com>

This code is free to be used/modified or distributed.
if you liked it, be sure to give back to the community one day.
if you didn't like the code do improve it.
Send pull request in github : https://github.com/ParadoxZero/CodechefAPI


Features of this API:
* Login to Codechef
* Submit solution
* Check result of submitted solution

Possible future additions:
* User stats
* Searching to specific users
* Searching for specific questions

"""

import sys
from bs4 import BeautifulSoup as bs

if sys.version_info[0] > 2:
    raise Exception("This API is designed for only python 2.7")
try:
    import mechanize
except ImportError:
    raise Exception("This API requires module: mechanize")


class AlreadyLoggedInException(Exception): pass
class RequiresLoginException(Exception): pass
class IncorrectLanguageException(Exception): pass
class InternetConnectionFailedException(Exception): pass

# To add support of more languages, just edit this:
language_list = {
    'cpp': '44',
    'c': '11',
    'c#': '27',
    'java': '10',
    'php': '29',
    'python3': '116',
    'python2': '4'
}


class API:
    """
    The main class to be instantiated. This class provides the interface to interact with codeChef
    """
    URL = "https://www.codechef.com"
    _user = ""
    _pass = ""
    _br = mechanize.Browser()
    __is_logged_in = False

    def __init__(self, username, password):
        self._br.set_handle_robots(False)
        self._user = username
        self._pass = password

    def __del__(self):
        if self.__is_logged_in:
            try:
                self.logout()
            except InternetConnectionFailedException:
                sys.exit(1)

    def login(self):
        """
        This functions is used to login to CodeChef
        No error is raised in unsuccessful login, hence should be used carefully
        Instances of multiple  login will create problem, so be sure to not be logged in somwehere else.
        (Sorry for the trouble, will fix it soon)
        """
        if self.__is_logged_in:
            raise AlreadyLoggedInException
        try:
            self._br.open(self.URL)
        except Exception:  # TODO get more specific exception for better stack trace
            raise InternetConnectionFailedException
        self._br.select_form(nr=0)
        self._br.form['name'] = self._user
        self._br.form['pass'] = self._pass
        try:
            response = self._br.submit()
        except Exception:
            raise InternetConnectionFailedException



        forms_list = [i for i in self._br.forms()]
        if len(forms_list) > 0:
            return False
        # TODO handle multiple login
        # removing extra sessions using simple scraping and form handling
        while self._br.geturl() == 'https://www.codechef.com/session/limit':
            self._br.select_form(
                predicate=lambda frm: 'id' in frm.attrs and frm.attrs['id'] == 'session-limit-page')
            soup = bs(response, 'html5lib')
            value = soup.find('input', attrs={'class', 'form-radio'})['value']
            self._br.form['sid'] = [value]
            self._br.method = "POST"
            response = self._br.submit()

        self.__is_logged_in = True
        return True

    def logout(self):
        try:
            self._br.open(self.URL + '/logout')
        except Exception:
            raise InternetConnectionFailedException
        self.__is_logged_in = False
        return True

    def submit(self, question_code, source, lang):
        """
        This method is to submit an answer to codechef
        :param question_code: String - The unique question code in CodeChef
        :param source: String - Source code content being submitted
        :param lang: String - Should be present in the dictionary-> language_list else exception raised
        :return: String - Submission id to be used for checking result
        """
        if not self.__is_logged_in:
            raise RequiresLoginException
        try:
            self._br.open(self.URL + '/submit/' + question_code)
        except Exception:  # TODO get more specific exception for better stack trace
            raise InternetConnectionFailedException
        self._br.select_form(nr=0)
        self._br.form['program'] = source
        try:
            self._br.form['language'] = [language_list[lang]]
        except KeyError:
            raise IncorrectLanguageException
        response = self._br.submit()
        ''' The submission id'''
        return str(response.geturl()).split('/')[-1]  # String

    def check_result(self, submission_id, question_code):
        """
        returns the result of a problem submission.
        :return: result codde
        RA - right answer
        WA - wrong answer
        CE - Compilation error
        RE - Runtime Error
        """

        try:
            response = self._br.open(self.URL + '/status/' + question_code)
        except Exception:  # TODO get more specific exception for better stack trace
            raise InternetConnectionFailedException
        response_html = response.read()
        start = response_html.find(submission_id)
        response_html = response_html[start:]
        while not response_html.startswith("span"):
            response_html = response_html[1:]
        while response_html[0] != '=':
            response_html = response_html[1:]
        response_html = response_html[2:]
        ans = ""
        while response_html[0] != "'":
            ans += response_html[0]
            response_html = response_html[1:]
        return ans + '\0'
