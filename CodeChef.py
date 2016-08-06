"""
Copyright 2016 Sidhin S Thomas <sidhin.thomas@gmail.com>

This code is free to be used/modified or distributed.
if you liked it, be sure to give back to the community one day.
if you didn't like the code do improve it.
Send pull request in github


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
    import BeautifulSoup
except ImportError:
    print "This API requires module: BeautifulSoup"


# To add support of more languages, just edit this:
language_list = {
    '44': 'cpp',
}


class API:
    '''
    The main class to be instantiated. This class provides the interface to interact with codeChef
    '''
    URL = "https://www.codechef.com"
    _user = ""
    _pass = ""
    _br = mechanize.Browser()
    __is_logged_in = False

    def __init__(self):
        self._br.set_handle_robots(False)

    def login(self, username, password):
        '''
        This functions is used to login to CodeChef
        No error is raised in unsuccessful login, hence should be used carefully
        (Sorry for the trouble, will fix it soon)
        :param username: String
        :param password: String
        '''
        if self.__is_logged_in:
            raise ExceptionSet.AlreadyLoggedInException
        self._br.open(self.URL)
        self._br.select_form(nr=0)
        self._br.form['name'] = password
        self._br.form['pass'] = username
        response = self._br.submit()
        # TODO implement method to check whether logged in
        self.__is_logged_in = True

    def submit(self, question_code, source, lang):
        '''
        This method is to submit an answer to codechef
        :param question_code: String - The unique question code in CodeChef
        :param source: String - Source code content being submitted
        :param lang: String - Should be present in the dictionary-> language_list else exception raised
        :return: String - Submission id to be used for checking result
        '''
        if not self.__is_logged_in:
            raise ExceptionSet.RequiresLoginException
        self._br.open(self.URL + '/submit/' + question_code)
        self._br.select_form(nr=0)
        self._br.form['program'] = source
        try:
            self._br.form['language'] = [language_list[lang]]
        except KeyError:
            raise ExceptionSet.IncorrectLanguageException
        self._br.submit()
        ''' The submission id'''
        return self._br.geturl().split('/')[-1] # String

