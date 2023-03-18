import os
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def login(broswer,user,pasw):
	browser.find_element_by_name('username').send_keys(user)
	browser.find_element_by_name('password').send_keys(pasw)
	browser.find_element_by_name('password').submit()

def indicators(browser):
	data=browser.find_elements_by_class_name('_ac2a')
	posts=data[0]
	followers=data[1]
	following=data[2]
	return posts,followers,following

def followers(browser,followers_link,num_followers):
	followers_link.click()
	time.sleep(3)
	exit=browser.find_element_by_class_name('_ac7b._ac7d')

	bubble=browser.find_element_by_class_name('_aano')
	for i in range(int(num_followers)//5):
		bubble.send_keys(Keys.END)
		time.sleep(1)
	data=browser.find_elements_by_class_name('x1yutycm')
	if int(num_followers) == len(data):
		print('all followers accounted')
	else:
		missing = int(num_followers) - len(data)
		print("%d followers are missing"% missing)
	return data	

def clean_follows(follows):
	people={}
	for i in follows:
		info=i.text
		info=info.split('\n')
		handle=info[0]
		name=info[1]
		people[handle]=name
	return people
	
		

browser=webdriver.Firefox()
browser.get('https://www.instagram.com/accounts/login/')

browser.implicitly_wait(30)
user='zforero@live.com'
pasw='Followfollow5!'

login(browser,user,pasw)

#donot remember signin
browser.find_element_by_class_name('_ac8f').click()
#donot turnon notifications
browser.find_element_by_class_name('_a9--._a9_1').click()

#build navigation
buttons = browser.find_elements_by_class_name('_a6hd')
#for i in buttons:
#	print(i.text)
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

follows=followers(browser, followers_link,pro_ind['followers'])

handle_name=clean_follows(follows)

try:
	follower_out = open('followers','r')
except:
	file=open('followers','w')
	file.close()
	follower_out=open('followers','r')
finally:
	current_follower=follower_out.read()
	current_follower=current_follower.split('\n')
	follower_out.close()

follower_out=open('followers','a')

for i in handle_name:
	if i in current_follower:
		print('%s is already accounted'% i)
	else:
		follower_out.write('%s	%s\n'% (i,handle_name[i]))

#follow=following(browser)
