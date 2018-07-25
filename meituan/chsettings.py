
import optparse 

parser = optparse.OptionParser()

parser.add_option(
    "-p", "--period", default='',
    help="Period"
)

parser.add_option(
    "-d", "--database", default="sqlite",
    help="sqlite or mysql"
)

opts = parser.parse_args()[0]


# period
period = opts.period

assert period[-3:-1] == ':P' and period[-6] == '-'

print('The Period is:', period)


# database
db = opts.database
assert db in ['mysql', 'sqlite']

print('The Database is:', db)



###

with open('settings.py', 'r') as f:
    lines = f.readlines()


period_setting = 'PERIOD = "' + period + '"\n'
flag = 0
for ind in range(len(lines)):
    if 'PERIOD =' in lines[ind]:
        lines[ind] = period_setting
        flag = 1
        break
        
if flag == 0:
    lines.append(period_setting)
    

db_setting = 'DB = "' + db + '"\n'
flag = 0
for ind in range(len(lines)):
    if 'DB =' in lines[ind]:
        lines[ind] = db_setting
        flag = 1
        break
        
if flag == 0:
    lines.append(db_setting)
    
    
with open('settings.py', 'w') as f:
    for i in lines:
        f.write(i)