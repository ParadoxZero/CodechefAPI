import CodeChef

c = CodeChef.API('buildrit', 'CSEdepartment')
c.login()
f = open('test.cpp')
source = f.read()
id = c.submit('TEST', source, 'cpp')
c.check_result(id, 'TEST')
