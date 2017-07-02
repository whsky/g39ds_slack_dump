import json
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def get_links(filename):
    """
    INPUT: String of filepath to .json file with parsed output of channel
        activity.
    OUTPUT: List of links to private files, List of public links
    -------------------------------------------------------------------------
    We first need to run the `slack_history.py` script to get a parsed .json
        file of Slack group activity. After we feed in the json file we will
        scrape out the `permalink` and the `permalink_public`. To allow the
        rest of the channel to have access to download the files we will also
        need to run the `create_public_link()` function in this script as well.
    """

    with open(filename) as json_data:
        g39ds = json.load(json_data)
        json_data.close()

    mes = g39ds['messages']
    links = []
    publinks = []
    key1='file'
    key2='permalink'
    key3='permalink_public'
    for m in mes:
        if key1 in m:
            if key3 in m[key1]:
                links.append(m[key1][key2])
                pub = m[key1][key3]
                name = m[key1]["name"]
                name = re.sub(r"\ ", "_", name)
                publinks.append(re.sub(".com/", ".com/files-pri/", pub) \
                                + "/download/" + name)
    return links, publinks


#We need to use selenium to create a public link so downloads will
#   accessable to the whole class
def create_public_link(links, username, password):
    """
    INPUT: list of links to Slack files, String of email address,
        and String of password
    OUTOUT: none
    -------------------------------------------------------------------------
    We will use Selenium to "click" on the Create Public Link option in each
        file's link to enable all channel users to access the download link.
        This takes a while (about 20 seconds per file, or about a hour per
        200 files).
    """
    i=0
    for i,li in reversed(list(enumerate(links))):
        driver = webdriver.Firefox()
        print("File {}/{}".format(i, len(links)))
        driver.get(li)
        elem = driver.find_element_by_id("email")
        elem.send_keys(username)
        elem = driver.find_element_by_id("password")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        sleep(10)
        elem = driver.find_element_by_id("file_action_cog")
        elem.click()

        #In case the file already has a public link, we should use `try/except`:
        try:
            elem = driver.find_element_by_id("create_public_link")
            elem.click()
        except NoSuchElementException:
            pass
        driver.close()

if __name__ == '__main__':
    filename = 'channels/g39ds_platte.json'
    username = "your.slack.email.address@address.com"
    password = "your_slack_password"
    links, publinks = get_links(filename)
    create_public_link(links, username, password)
#F52Q95C9Z/individual.md
