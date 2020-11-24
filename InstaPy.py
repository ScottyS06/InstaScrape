from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import webdriver_path


class InstaPy:

    # creates an InstaPy object which can be used to retrieve info about this
    # Instagram account
    def __init__(self, username: str, password: str):
        self.driver = webdriver.Chrome(executable_path=webdriver_path)
        self.username = username
        self.password = password

    # logins into the Instagram account
    def login(self):
        # open Instagram
        self.driver.get('https://instagram.com')
        sleep(3)

        # get the username and password box
        username_box = self.driver.find_element_by_name('username')
        password_box = self.driver.find_element_by_name('password')

        # send the login information to the username and password box
        username_box.send_keys(self.username)
        password_box.send_keys(self.password)
        password_box.send_keys(Keys.ENTER)
        sleep(3)

    # goes to the profile page on Instagram
    def go_to_profile(self):
        sleep(3)
        profile_pic = self.driver.find_element_by_css_selector('span._2dbep.qNELH img')
        profile_pic.click()
        sleep(3)
        profile_link = self.driver.find_elements_by_class_name('-qQT3')[0]
        profile_link.click()
        sleep(3)

    # goes to the followers link on the profile page
    def go_to_followers_or_following(self, num_arg):
        sleep(3)
        followers_link = self.driver.find_elements_by_class_name('-nal3')[num_arg]
        num_of_followers = followers_link.find_elements_by_css_selector('span')[0].text
        followers_link.click()
        sleep(3)
        return int(num_of_followers)

    # gets a set of all the followers or following of this InstaPy account
    # followers or following depends on the argument passed into the
    # go_to_followers_or_following method
    # pass in the numerical argument associated with the number of followers or
    # following (1 for followers, 2 for following)
    # returns a set of usernames corresponding to either the followers or following
    def get_followers_or_following(self, num):
        sleep(3)
        followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
        followersList.click()
        sleep(2)
        actionChain = webdriver.ActionChains(self.driver)
        while numberOfFollowersInList < num:
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            sleep(.5)
            followersList.click()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)
        follower_boxes = followersList.find_elements_by_css_selector('li')
        followers = set()
        for person in follower_boxes:
            user = person.find_element_by_css_selector('a').get_attribute('href')
            followers.add(user)
        return followers

    # goes to the specified person's instagram account
    # pre: profile_username must be valid
    def go_to_person_profile(self, profile_username):
        sleep(3)
        search_bar = self.driver.find_element_by_css_selector('input.XTCLo.x3qfX')
        sleep(3)
        search_bar.send_keys(profile_username)
        sleep(4)
        search_bar.send_keys(Keys.ENTER)
        search_bar.send_keys(Keys.ENTER)
        sleep(4)

    # goes to the nth post on the current profile page.
    # as of now, the number of posts is limited because the
    # webdriver only loads the first couple images
    # must scroll to see more
    def go_to_nth_post(self, post_num):
        sleep(3)
        posts = self.driver.find_elements_by_css_selector('div._9AhH0')
        post = posts[post_num]
        post.click()
        sleep(4)

    # comments the specified string comment on the current post
    def comment_on_post(self, comment):
        sleep(3)
        comment_box = self.driver.find_element_by_css_selector('textarea.Ypffh')
        sleep(1)
        comment_box.click()
        comment_box = self.driver.find_element_by_css_selector('textarea.Ypffh')
        comment_box.send_keys(comment)
        post_btn = self.driver.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF')
        post_btn.click()
        sleep(4)


def main():
    # example function calls using InstaScraper Object
    # fill in username and password with personal info to initialize
    instaBot = InstaPy('username', 'password')
    instaBot.login()
    instaBot.go_to_profile()
    num = instaBot.go_to_followers_or_following(1)
    following = instaBot.get_followers_or_following(num)


if __name__ == '__main__':
    main()
