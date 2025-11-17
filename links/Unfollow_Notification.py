from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from tqdm.auto import tqdm
import random

with open('C:/Users/Kostas/Desktop/Codes/Unfollow Notification/Email-Password-Profile.txt','r') as file: 
    lines=file.readlines()
    email=lines[0]
    password=lines[1]
    profile_name=lines[2]

# Setup
options=webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver=webdriver.Chrome(service=Service('C:/Users/Kostas/Downloads/old_chromedriver.exe'),options=options)
driver.maximize_window()
driver.get('https://www.instagram.com/accounts/login/?next=%2F'+profile_name+'%2F&source=omni_redirect')

# Accepts cookies
while True:
    try:      
        time.sleep(1)
        driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]').click()
        break
    except NoSuchElementException:
        pass

# Inputs Email-Password
while True:
    try:
        time.sleep(1)
        driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[1]/div/label/input').send_keys(email)
        driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[2]/div/label/input').send_keys(password)
        break
    except NoSuchElementException:
        pass

# Clicks enter
time.sleep(1)
actions=ActionChains(driver)
actions.send_keys(Keys.ENTER).perform()

# Clicks Not Now
while True:
    try:
        time.sleep(1)
        driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div').click()
        break
    except NoSuchElementException:
        pass

# Gets follower count and goes on the follower page
while True:
    try:
        time.sleep(1)
        follower_count=driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span').text
        break
    except NoSuchElementException:
        pass
driver.get('https://www.instagram.com/'+profile_name+'/followers/')

# Gets Followers
followers=[]
i=1
count=0
time.sleep(1)
with tqdm(total=int(follower_count),desc='Followers') as pbar: # For the progress bar
    while len(followers)<int(follower_count): # Until it has gotten every follower, it takes multiple attempts
        while True:
            try:
                if driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div['+str(i)+']/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a/span/div').text not in followers:
                    followers.append(driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div['+str(i)+']/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a/span/div').text)
                    pbar.update(1)
                count=0
                i+=1
                driver.execute_script("arguments[0].scrollIntoView();",driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div['+str(i)+']/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a/span/div'))
                time.sleep(random.uniform(0,2))
                break
            except NoSuchElementException:
                count+=1
                if count==500: # If it has caught 500 exceptions in a row, it means that it has reached the end so we can reset it
                    i=1
                    # Updates follower count
                    driver.get('https://www.instagram.com/'+profile_name+'/')
                    while True:
                        try:
                            time.sleep(1)
                            follower_count=driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span').text
                            break
                        except NoSuchElementException:
                            pass
                    driver.get('https://www.instagram.com/'+profile_name+'/followers/')
                pass

# Gets following count and goes on the following page
while True:
    try:
        time.sleep(1)
        following_count=driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span').text
        break
    except NoSuchElementException:
        pass
driver.get('https://www.instagram.com/'+profile_name+'/following/')

print('\n')
# Gets Following
following=[]
i=1
count=0
time.sleep(1)
with tqdm(total=int(following_count),desc='Following') as pbar: # For the progress bar
    while len(following)<int(following_count): # Until it has gotten every following user, it takes multiple attempts
        while True:
            try:
                if driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div['+str(i)+']/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a/span/div').text not in following:
                    following.append(driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div['+str(i)+']/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a/span/div').text)
                    pbar.update(1)
                count=0
                i+=1
                driver.execute_script("arguments[0].scrollIntoView();",driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div['+str(i)+']/div/div/div/div[2]/div/div/span[1]/span/div/div/div/a/span/div'))
                time.sleep(random.uniform(0,2))
                break
            except NoSuchElementException:
                count+=1
                if count==500: # If it has caught 500 exceptions in a row, it means that it has reached the end so we can reset it
                    i=1
                    # Updates following count
                    driver.get('https://www.instagram.com/'+profile_name+'/')
                    while True:
                        try:
                            time.sleep(1)
                            following_count=driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span').text
                            break
                        except NoSuchElementException:
                            pass
                    driver.get('https://www.instagram.com/'+profile_name+'/following/')
                pass
driver.quit()

unfollowed=[]
# Compares old followers with the new to find if somebody has unfollowed
for i in range(len(following)):
    if following[i] not in followers:
        unfollowed.append(following[i])

print('Snake List:',*unfollowed,sep=' | ',end='')
print(' |')
input('\nPress any key to exit the program... ')
