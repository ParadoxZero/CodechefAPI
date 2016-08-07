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
import ExceptionSet

if sys.version_info[0] > 2:
    raise Exception("This API is designed for only python 2.7")
try:
    import mechanize
except ImportError:
    print "This API requires module: mechanize"

try:
    from bs4 import BeautifulSoup
except ImportError:
    print "This API requires module: BeautifulSoup(bs4)"

# To add support of more languages, just edit this:
language_list = {
    'cpp': '44',
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
        self.logout()

    def login(self):
        """
        This functions is used to login to CodeChef
        No error is raised in unsuccessful login, hence should be used carefully
        Instances of multiple login will create problem, so be sure to not be logged in somwehere else.
        (Sorry for the trouble, will fix it soon)
        """
        if self.__is_logged_in:
            raise ExceptionSet.AlreadyLoggedInException
        self._br.open(self.URL)
        self._br.select_form(nr=0)
        print self._br.form
        self._br.form['name'] = self._user
        self._br.form['pass'] = self._pass
        response = self._br.submit()
        # TODO implement method to check whether logged in
        # TODO handle multiple login
        self.__is_logged_in = True
        return True

    def logout(self):
        self._br.open(self.URL + '/logout')
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
            raise ExceptionSet.RequiresLoginException
        self._br.open(self.URL + '/submit/' + question_code)
        for form in self._br.forms():
            print form.name, form
        self._br.select_form(nr=0)
        self._br.form['program'] = source
        try:
            self._br.form['language'] = [language_list[lang]]
        except KeyError:
            raise ExceptionSet.IncorrectLanguageException
        self._br.submit()
        self._br.open(self.URL + '/logout')
        ''' The submission id'''
        return self._br.geturl().split('/')[-1]  # String

    def check_result(self, submission_id, question_code):
        """
        returns the result of a problem submission.
        :return: result codde
        RA - right answer
        WA - wrong answer
        CE - Compilation error
        RE - Runtime Error
        """
        response = self._br.open(self.URL + '/status/' + question_code)
        response = BeautifulSoup(response, 'html.parser')
