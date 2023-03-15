from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

class Bot():
  def __init__(self, poll_name, email, netid, password, default_timeout, interval):
    """
    Handles initializing a Bot instance

    poll_name: the polleve poll name
    email: cornell student email
    netid: cornell netid
    password: cornell student password
    default_timeout: the amount of time in ms to allow for searching for an
      elementbefore throwing an exception 
    interval: the interval at which to poll the polleve
    """
    self.driver =  webdriver.Firefox()
    self.poll_name = poll_name
    self.email = email
    self.netid = netid 
    self.password = password
    self.default_timeout = default_timeout
    self.interval = interval
  

  def login(self):
    """
    Handles logging into a polleve account. Requires that the credentials are 
    a Cornell student (it is unlikely that the webflow is similar across
    different colleges).
    """
    print("logging in...")
    self.driver.get(f'https://pollev.com/home')

    print("sending click to login")
    login = self.driver.find_element(By.XPATH, "/html/body/pe-application/div/nav-wrapper/pe-navigation/nav/div[1]/pe-navigation-item[4]/div")
    login.click()
    
    print("sending click to sign in with google")
    signin_w_google = self.driver.find_element(By.XPATH, "/html/body/main/div/div[3]/form[1]/button/span[3]")
    signin_w_google.click()

    print("entering email to email input")
    google_email_input = self.driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    google_email_input.send_keys(f"{self.email}")

    print("sending click to next")
    next_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span")
    next_btn.click()

    print("entering netid to netid input")
    netid_input = WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
    netid_input.send_keys(f"{self.netid}")

    print("entering password to password input")
    password_input = self.driver.find_element(By.XPATH, '//*[@id="password"]')
    password_input.send_keys(f"{self.password}")

    print("sending click to login")
    login = self.driver.find_element(By.XPATH, "/html/body/div[2]/main/article/div/div[1]/form/fieldset/div/div[1]/input")
    login.click()

    print("waiting for 2FA")

    print("sending click to trust browser")
    trust = WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located((By.XPATH, '//*[@id="trust-browser-button"]')))
    trust.click()

    print("sending click to login with cornell id")
    login_w_cornell = WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/main/div/div[1]/p/a[1]')))
    login_w_cornell.click()
    
    print("entering poll name")
    poll_name = WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/pe-application/div/div/div/layout-plain/section/div/main/pollev-home-join/form/pe-text-field/div/label/input')))
    poll_name.send_keys(f"{self.poll_name}")

    print("sending click to join")
    join = self.driver.find_element(By.XPATH, '/html/body/pe-application/div/div/div/layout-plain/section/div/main/pollev-home-join/form/button')
    join.click()


  def poll_mc(self):
    """
    Periodically (specified in self.interval) sends a click to a polleve 
    multiple choice component. 
    """
    while True:
      try:
        print("waiting for mc...")
        mc = WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'component-response-multiple-choice__option__value')))
        mc.click()
        print("sending click to mc")

        print("pausing search...")
        time.sleep(self.interval)

      except KeyboardInterrupt:
        print("raising exception to quit")
      
      
  def end_session(self):
    """
    Terminates the webdriver (self.driver)
    """
    print("closing...")
    self.driver.close()
    print("successfully closed")
    

class Credentials():
  def __init__(self):
    print("looking for a credential file...")

    if not self.is_credential_valid():
      print("credential file doesn't exist \n creating credential file")
      self.create_credential()
    else:
      print("credential file already exists")
    
    print("reading credential contents...")
    credentials = self.read_credentials()

    self.poll_name = credentials["poll_name"]
    self.email = credentials["email"]
    self.netid = credentials["netid"]
    self.password = credentials["password"]
    self.default_timeout = credentials["default_timeout"]
    self.interval = credentials["interval"]


  def read_credentials(self):
    with open("credentials.txt", "r") as f:
      contents = f.read()
      credentials = json.loads(contents)
      return credentials
  

  def is_credential_valid(self):
    return os.path.isfile("./credentials.txt")
  

  def create_credential(self):
    with open('credentials.txt', "w") as f:
      poll_name = input("poll name: ")
      email = input("email: ") 
      netid = input("netid: ")
      password = input("password: ")
      default_timeout = input("default timeout: ")
      interval = input("interval: ")
      credentials = {
        "poll_name": poll_name, 
        "email": email,
        "netid": netid,
        "password": password,
        "default_timeout": default_timeout,
        "interval": interval
      }
      f.write(json.dumps(credentials))
      print("created credentials file")
  

if __name__ == "__main__":
  cred = Credentials()
  bot= Bot(
    poll_name=cred.poll_name, 
    email=cred.email,
    netid=cred.netid,
    password=cred.password,
    default_timeout=int(cred.default_timeout),
    interval=int(cred.interval)
  )

  try:
    bot.login()
    bot.poll_mc()
  except Exception as e:
    print("an error occurred")
    print(e)
    print("hit any key to end program")
  
  bot.end_session()
  

