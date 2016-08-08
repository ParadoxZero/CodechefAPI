# CodechefAPI

Version 0.9 beta <br>
stable enough to be used in development.


This is a python API for accessing CodeChef features namely :
* Submit a solution to a problem
* Retrieve the result

###Dependencies:
* Python 2.7
* mechanize
* BeautifulSoup4

####To install the dependencies :
<b> Ubuntu like os : </b>
> sudo apt-get install python-bs4 <br>
> sudo apt-get install python-mechanize

use coresponding method to install it in other systems.

###Usage:

Using this is simple:

first import CodeChef.py to your program.

In below example CodeChef.py is in same directory as the program.

<code>
import CodeChef

chef = CodeChef.API('buildrit', 'CSEdepartment')
chef.login()
file = open('test.cpp')
source = file.read()
submission_id = chef.submit('TEST', source, 'cpp')
print 'Id is :', submission_id
print chef.check_result(submission_id, 'TEST')
chef.logout()

</code>


sample is provided in the repositary to be tested.
