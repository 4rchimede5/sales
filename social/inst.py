import os, datetime, csv, sqlite3
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
#the database gives a problem, it can find ./database/models
host='https://www.instagram.com/'

def Login(browser,user,pasw):
	browser.find_element_by_name('username').send_keys(user)
	browser.find_element_by_name('password').send_keys(pasw)
	browser.find_element_by_name('password').submit()

def Indicators(browser):
	data=browser.find_elements_by_class_name('_ac2a')
	posts=data[0]
	followers=data[1]
	following=data[2]
	return posts,followers,following

def People(browser,num_people,person_type):
	time.sleep(3)
	exit=browser.find_element_by_class_name('_ac7b._ac7d')

	popup=browser.find_element_by_class_name('_aano')

	for i in range(int(num_people)//5):
		popup.send_keys(Keys.END)
		time.sleep(1)

	data=browser.find_elements_by_class_name('x1yutycm')

	if int(num_people) == len(data):
		print('all %s accounted' % person_type)
	else:
		missing = int(num_people) - len(data)
		print("%d %s are missing" % (missing,person_type))
		followers(browser,num_people,person_type)

	return exit, data, person_type

def Clean_People(data, person_type, user, date):
	people={}
	for i in data:
		person=i.text
		person=person.split('\n')
		handle=person[0]
		name=person[1]
		people[handle]=name
	try:
		output = open("%s_%s_%s"%(person_type,user,date),'r')
	except:
		file=open("%s_%s_%s"%(person_type,user,date),'w')
		file.close()
		output=open("%s_%s_%s"%(person_type,user,date),'r')
	finally:
		current_person=output.read()
		current_person=current_person.split('\n')
		output.close()

	output=open("%s_%s_$s"%(person_type,user,date),'a')

	for i in people:
		if i in current_person:
			print('%s is already accounted'% i)
		else:
			output.write('%s \t %s\n'% (i,people[i]))

	print('all %s written to file' %person_type)

def Navigation(browser):
	buttons = browser.find_elements_by_class_name('_a6hd')

	while buttons[8].text != 'Profile':
		browser.set_context('chrome')
		browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL,'-')
		browser.set_context('content')
		buttons = browser.find_elements_by_class_name('_a6hd')
	return buttons

def Posts(browser,user,person_type,date):
	check=[]
	while check=='':
		check = browser.find_element_by_class_name('_aacl._aaco._aacw._aad3._aad6._aadb')
		browser.find_element_by_tag_name('body').send_keys(Keys.DOWN)
	images = browser.find_elements_by_tag_name('img')
	
	posts=[]
	for image in images:
		caption = image.get_property('alt')
		link = image.get_property('src')
		if 'profile picture' not in caption:
			if 'https' in link:
				posts.append([caption,link,image])

	output = open('%s_%s_%s_%s'%(user,person_type,date[0],date[1]),'w')
	for post in posts:
		output.write('%s\t%s\n'%(caption,link))	
	output.close()

def Populate_Database(user,person_type,date):
	path =os.path.join(os.getcwd(),(user+'.sqlite3'))
	connection = sqlite3.connect(path)
	cursor =connection.cursor()
	try:
		cursor.execute('''
				CREATE TABLE "%s_pull_dates" (
					id INTEGER PRIMARY KEY,
					date INTEGER,
					time INTEGER)''' % user)
	except:
		pass

	cursor.execute('SELECT * FROM "%s_pull_dates" WHERE date=? AND time=?, (date,time)')

	if not cursor.fetchone():
		cursor.execute('INSERT INTO "%s_pull_dates" (date,time) VALUES (?,?)' % user, date)


	cursor.execute('SELECT id FROM "%s_pull_dates" ORDER BY id DESC LIMIT 1'% user)
	
	pull_number = cursor.fetchone()[0]
	#print(pull_number)

	output=[]
	with open('%s_%s_%s_%s' % (user,person_type,date[0],date[1])) as file:
		data = csv.reader(file, delimiter='\t')
		[output.append((field[0],field[1],pull_number,pull_number)) for field in data]
	#	print(output)
		file.close()

	if person_type in ('followers','following'):
		try:
			cursor.execute('''
				CREATE TABLE "%s_%s__%d" (
					id INTEGER PRIMARY KEY,
					handle TEXT(50),
					name TEXT(50),
					date INTEGER,
					time INTEGER,
					FOREIGN KEY (date) REFERENCES "%s_pull_dates" (date)
					FOREIGN KEY (time) REFERENCES "%s_pull_dates" (time)
			 		)'''% (user,person_type,pull_number,user,user))
		except:
			pass

		cursor.executemany('INSERT INTO "%s_%s_%d" (handle,name,date,time) VALUES (?,?,?,?)'%(user,person_type,pull_number),persons)
	
	elif person_type in  ('posts'):
		try:
			cursor.execute('''
					CREATE TABLE "%s_%s_%d" (
						id  INTEGER PRIMARY KEY,
						caption TEXT(300),
						url TEXT(500),
						date INTEGER,
						time INTEGER,
						FOREIGN KEY (date) REFERENCES "%s_pull_dates" (date),
						FOREIGN KEY (date) REFERENCES "%_pull_dates" (time)
						)''' % (user,person_type,pull_number, user,user))
		except:
			pass

		cursor.executemany('INSERT INTO "%s_%s_%d" (caption,url,date,time)'% (user,person_type,pull_number))

	connection.commit()
	connection.close()

##########################

date=(datetime.datetime.now().date().strftime('%Y-%m-%d'), datetime.datetime.now().time().strftime('%H:%M'))
#print(date)

browser=webdriver.Firefox()
#browser.get(host+'/accounts/login/')

#############test subject
pro_ind={}
pro_ind['user']=''
#############
browser.implicitly_wait(10)

'''
user=''
pasw=''

Login(browser,user,pasw)

#donot remember signin
browser.find_element_by_class_name('_ac8f').click()
#donot turnon notifications
browser.find_element_by_class_name('_a9--._a9_1').click()

###############################
buttons=Navigation(browser)

home=buttons[1]
search=buttons[2]
explore=buttons[3]
reels=buttons[4]
messages=buttons[5]
notifications=buttons[6]
create=buttons[7]
profile=buttons[8]

profile.click()

#########################
pro_ind={}
posts_link,followers_link,following_link=Indicators(browser)
#print(post_link.text, followers_link.text, following_link.text)
pro_ind['posts']=posts_link.text
pro_ind['followers']=followers_link.text
pro_ind['following']=following_link.text
pro_ind['user']=browser.find_element_by_tag_name('h2').text
'''
###########################
'''
browser.get(host+pro_ind['user']+'/followers/')
follows=People(browser, pro_ind['followers'],'followers')
Clean_People(follows[1],follows[2],pro_ind['user'],date)
follows[0].click()

browser.get(host+pro_ind['user']+'/following/')
follow=People(browser,pro_ind['following'],'following')
Clean_People(follow[1],follow[2],pro_ind['user'],date)
follow[0].click()
'''

browser.get(host+pro_ind['user']+'/posts/')
posts=Posts(browser,pro_ind['user'],'posts',date)

#############################

#populate_database(user,'followers',(date[0],date[1]))
#populate_database(user,'following',(date[0],date[1]))
#populate_database(user,'posts',(date[0],[date[1]))

############################

post_rows=browser.find_elements_by_class_name('_ac7v._al3n')

