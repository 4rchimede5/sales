from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import os
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def primary_filter(browser):
	pfilter=browser.find_elements_by_class_name('search-reusables__primary-filter')
	return pfilter

def secondary_filter(browser):
	sfilter=browser.find_elements_by_class_name('search-reusables__value-label')
	return sfilter

def page_change(browser,i):
	page_numbers=browser.find_elements_by_class_name('artdeco-pagination__indicator.artdeco-pagination__indicator--number.ember-view')
	button_next=browser.find_elements_by_class_name('artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view')
	#for page in page_numbers:
	#	page.text
	lenght = len(page_numbers)
	#print(lenght)
	max_page=page_numbers[lenght-1].text
	
	if i == 0:
		return max_page, button_next
	else:
		return button_next

email=""
passw=""

# initialize Firefox driver
#options=FirefoxOptions()
#options.add_argument("--headless")
browser = webdriver.Firefox()

print("firefox fired up")
browser.implicitly_wait(60)
# navigate to LinkedIn login page
browser.get('https://www.linkedin.com/login')

# find email and password fields, and enter credentials
browser.find_element_by_id('username').send_keys(email)
password=browser.find_element_by_id('password')
password.send_keys(passw)
password.submit()
print("sign in")
#find the search bar and enter the subject
#browser.find_element_by_class_name('search-global-typeahead__collapsed-search-button').click()
search=browser.find_element_by_class_name('search-global-typeahead__input')
Search.send_keys('')
search.send_keys(Keys.RETURN)


#first loop filter for people, companies, etc
#secon loop filter connections, location, company, etc
print("start filter")
for i in range(2):
	pfilter=primary_filter(browser)
	for j in range(len(pfilter)):
		print(j,pfilter[j].text)

	#selection=input("Enter filter")
	#pfilter[int(selection)].click()
	pfilter[i].click()
	

#select which connections or enter a location
sfilter =secondary_filter(browser)
for i in range(len(sfilter)):
	print(i,sfilter[i].text)

#selection=input("select:")
sfilter[1].click()

show=browser.find_element_by_class_name('artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.ml2')
show.click()

print("finished filters")
#when done with filters scrap data
i=0

browser.find_element_by_class_name('scaffold-layout.scaffold-layout--breakpoint-xl.scaffold-layout--main-aside.scaffold-layout--reflow.search__srp--has-right-rail-top-offset')
browser.execute_script("window.scrollBy(0,1500);")

max_page, button_next = page_change(browser,i)
#pages=browser.find_elements_by_class_name('artdeco-pagination__indicator.artdeco-pagination__indicator--number.ember-view')

output=open('contacts','w')

for page in range(int(max_page)):
	print("page "+str(page+1))
	results=browser.find_elements_by_class_name('reusable-search__result-container')
	for result in results:
		text = result.text.split('\n')
		name = text[0]
		if text[0] != text[1]:
			current_position = text[4]
			past_position= text[6]
			location = text[5]
		else:
			current_position = text[5]
			past_position= text[7]
			location = text[6]
		output.write(name+'\t'+current_position+'\t'+past_position+'\t'+location+'\n\n')
	button_next[0].click()
	i=1

	browser.find_element_by_class_name('scaffold-layout.scaffold-layout--breakpoint-xl.scaffold-layout--main-aside.scaffold-layout--reflow.search__srp--has-right-rail-top-offset')
	browser.execute_script("window.scrollBy(0,1500);")
	button_next=page_change(browser,i)

output.close()

# close the browser window
#driver.quit()

'''
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.open("https://www.kaggle.com/datasets")
a=browser.response()
print(a)
for i in a:
	print(i)

#browser.select_form(class_='hero-cta-form')

#browser["session_key"] = email
#browser["session_password"] = passw
#output = browser.submit()


#content=browser.response()

#for i in content:
#	print(i)

'''
'''
client = requests.Session()

login_url = 'https://www.linkedin.com/uas/login'
login_page= client.get(login_url)

soup = bs(login_page.content,'html.parser')
csrf = soup.find('input',{'name':'loginCsrfParam'}).get('value')

login_info = {
	'sesion_key':email,
	'session_password':passw,
	'loginCsrfParam':csrf,
}

#print(login_info)

client.post(login_url, data=login_info)

home_page = client.get('https://www.linkedin.com/in/zeusa')

if 'Sign Out' in home_page.text:
	print('Login successful')
else:
	print('Login failed.')
'''