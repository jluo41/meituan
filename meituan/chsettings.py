
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

parser.add_option(
    "-n", "--citydbname", default="sz",
    help="sqlite or mysql"
)



opts = parser.parse_args()[0]




# period
period = opts.period

assert period[-3:-1] == ':P' and period[-6] == '-'

print('The Period is:          ', period)


# database
db = opts.database
assert db in ['mysql', 'sqlite']

print('The Database is:        ', db)


# city
city = opts.citydbname
assert city in ['sz', 'zk']
print('The Database name is:   ', city)


saflog = 'log/' + city + '/saflog.txt'

print('The SA FoodType log is: ', saflog)



###

with open('meituan/settings.py', 'r') as f:
    lines = f.readlines()


# PERIOD
period_setting = 'PERIOD = "' + period + '"\n'
flag = 0
for ind in range(len(lines)):
    if 'PERIOD =' in lines[ind]:
        lines[ind] = period_setting
        flag = 1
        break
        
if flag == 0:
    lines.append(period_setting)
    

# DATABASE
db_setting = 'DB = "' + db + '"\n'
flag = 0
for ind in range(len(lines)):
    if 'DB =' in lines[ind]:
        lines[ind] = db_setting
        flag = 1
        break
        
if flag == 0:
    lines.append(db_setting)
   

# CITY
city_setting = 'CITYDBNAME = "' + city + '"\n'
flag = 0
for ind in range(len(lines)):
    if 'CITYDBNAME = ' in lines[ind]:
        lines[ind] = city_setting
        flag = 1
        break
        
if flag == 0:
    lines.append(city_setting)
 
    
# SAFLOG
saflog_setting = 'SAFLOGFILE = "' + saflog + '"\n'
flag = 0
for ind in range(len(lines)):
    if 'SAFLOGFILE = "' in lines[ind]:
        lines[ind] = saflog_setting
        flag = 1
        break
        
if flag == 0:
    lines.append(saflog_setting)
 


with open('meituan/settings.py', 'w') as f:
    for i in lines:
        f.write(i)