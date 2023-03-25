import os
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

host='https://www.instagram.com/'

def login(browser,user,pasw):
	browser.find_element_by_name('username').send_keys(user)
	browser.find_element_by_name('password').send_keys(pasw)
	browser.find_element_by_name('password').submit()

def indicators(browser):
	data=browser.find_elements_by_class_name('_ac2a')
	posts=data[0]
	followers=data[1]
	following=data[2]
	return posts,followers,following

def people(browser,num_people,person_type):
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

def clean_people(data, person_type, user):
	people={}
	for i in data:
		person=i.text
		person=person.split('\n')
		handle=person[0]
		name=person[1]
		people[handle]=name

	try:
		output = open("%s_%s"%(person_type,user),'r')
	except:
		file=open("%s_%s"%(person_type,user),'w')
		file.close()
		output=open("%s_%s"%(person_type,user),'r')
	finally:
		current_person=output.read()
		current_person=current_person.split('\n')
		output.close()

	output=open("%s_%s"%(person_type,user),'a')

	for i in people:
		if i in current_person:
			print('%s is already accounted'% i)
		else:
			output.write('%s \t %s\n'% (i,people[i]))

	print('all %s written to file' %person_type)

def navigation(browser):
	buttons = browser.find_elements_by_class_name('_a6hd')

	while buttons[8].text != 'Profile':
		browser.set_context('chrome')
		browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL,'-')
		browser.set_context('content')
		buttons = browser.find_elements_by_class_name('_a6hd')
	return buttons

browser=webdriver.Firefox()
browser.get('https://www.instagram.com/accounts/login/')

browser.implicitly_wait(10)
user=''
pasw=''

login(browser,user,pasw)

#donot remember signin
browser.find_element_by_class_name('_ac8f').click()
#donot turnon notifications
browser.find_element_by_class_name('_a9--._a9_1').click()

buttons=navigation(browser)

home=buttons[1]
search=buttons[2]
explore=buttons[3]
reels=buttons[4]
messages=buttons[5]
notifications=buttons[6]
create=buttons[7]
profile=buttons[8]

profile.click()

pro_ind={}
posts_link,followers_link,following_link=indicators(browser)
#print(post_link.text, followers_link.text, following_link.text)
pro_ind['posts']=posts_link.text
pro_ind['followers']=followers_link.text
pro_ind['following']=following_link.text
pro_ind['user']=browser.find_element_by_tag_name('h2').text	

browser.get(host+pro_ind['user']+'/followers/')
follows=people(browser, pro_ind['followers'],'followers')
clean_people(follows[1],follows[2],pro_ind['user'])
follows[0].click()

browser.get(host+pro_ind['user']+'/following/')
follow=people(browser,pro_ind['following'],'following')
clean_people(follow[1],follow[2],pro_ind['user'])
follow[0].click()

post_rows=browser.find.elements_by_class_name('_ac7v._al3n')
