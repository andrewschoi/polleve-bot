from selenium import webdriver
from selenium.webdriver.common.by import By

class Bot():
  def __init__(self, poll_name=None):
    self.driver =  webdriver.Firefox()
    self.poll_name = poll_name
  
  def login(self):
    print("logging in...")
    self.driver.get(f'https://pollev.com/home')
    login = self.driver.find_element(By.XPATH, "/html/body/pe-application/div/nav-wrapper/pe-navigation/nav/div[1]/pe-navigation-item[4]/div")
    login.click()
    print("click login")

  def end_session(self):
    print("closing...")
    self.driver.close()
    print("successfully closed")
    


if __name__ == "__main__":
  bot= Bot(poll_name="4820sp")
  bot.login()
  input()
  bot.end_session()
  

