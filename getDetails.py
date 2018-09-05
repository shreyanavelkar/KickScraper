import time
from PIL import Image
import pytesseract
import io
import requests


def get_updates(browser):
    try:
        updates = int(browser.find_element_by_xpath("//div[@class='row']//a[@data-content='updates']//span").text)
    except:
        updates = 0
    return updates


def get_comments(browser):
    try:
        comments = int(
            browser.find_element_by_xpath("//div[@class='row']//a[@data-content='comments']//span//data").text)
    except:
        comments = 0
    return comments


def get_creator_info(creator_url,browser):
    try:
        browser.get(creator_url)
        time.sleep(20)
        created_projects = browser.find_element_by_xpath(
            "//ul[contains(@class,'nav--subnav__list')]//li//a//span[@class='count']").text
        creator_url_about = creator_url + "/about"
        browser.get(creator_url_about)
        creator_bio_elem = browser.find_elements_by_xpath("//p")
        creator_bio = []
        for elem in creator_bio_elem:
            creator_bio.append(elem.text)
        creator_socia_media_list = browser.find_elements_by_xpath("//ul[@class='menu-submenu mb6']//li//a")
        creator_socia_media = []
        for elem in creator_socia_media_list:
            smurl = elem.get_attribute('href')
            creator_socia_media.append(smurl)

    except:
        created_projects = 'NA'
        creator_bio = 'NA'
        creator_socia_media = 'NA'

    return created_projects, creator_bio, creator_socia_media


def get_pledge_goals(browser):
    try:
        # strech goals
        proj_urls = browser.find_elements_by_xpath("//div[@class='project-nav__links']//a")
        links = []
        for each_link in proj_urls:
            link = each_link.get_attribute('href')
            links.append(link)

        reward_link = links[0]
        project_description_link = links[1]
        updates_link = links[3]
        community_link = links[4]

        browser.get(reward_link)
        goal_list = browser.find_elements_by_xpath(
            "//div[@class='NS_projects__rewards_list js-project-rewards']//ol//li[@class!='list-disc']")
        number_of_goals = len(goal_list)
        pledge_list = browser.find_elements_by_xpath(
            "//div[@class='NS_projects__rewards_list js-project-rewards']//ol//li//h2//span[@class='money']")
        reward_list = browser.find_elements_by_xpath(
            "//div[@class='NS_projects__rewards_list js-project-rewards']//ol//li//div[@class='pledge__reward-description pledge__reward-description--expanded']//p")
        backer_list = browser.find_elements_by_xpath(
            "//div[@class='NS_projects__rewards_list js-project-rewards']//ol//li//div[@class='pledge__backer-stats']//span")
        pledge = []
        for each_pledge in pledge_list:
            pledge.append(each_pledge.text)
        reward = []
        for each_reward in reward_list:
            reward.append(each_reward.text)
        backer = []
        for each_backer in backer_list:
            backer.append(each_backer.text)
        goals = []
        for i in range(number_of_goals):
            gamification_text = [
                "Pledge  " + str(i) + " : " + "Pledge" + pledge[i] + " or more  Reward Given : " + reward[
                    i] + " Supported by Backers : " + backer[i]]
            goals.append(gamification_text)

        browser.get(project_description_link)
        text_list = browser.find_elements_by_xpath("//div[@class='row']//p")
        i = 0
        desc = ''
        for each_item in text_list:
            try:
                text = each_item.text
            except:
                bold_list = each_item.find_elements_by_xpath('//b')
                if isinstance(bold_list, types.list):
                    text = bold_list[i]
                    i = i + 1
                else:
                    text = bold_list

            desc = desc + ' ' + text
    except:
        goals = ['Info not available']
        number_of_goals = 0
        desc = 'NA'
    return number_of_goals, goals, desc


def get_image_text(browser):
    try:
        image_list = browser.find_elements_by_xpath("//div[@class='row']//figure//img")
        image_url_list = []
        for each_image in image_list:
            image_url = each_image.get_attribute('src')
            image_url_list.append(image_url)

        img_text_list = []
        for i in range(len(image_url_list)):
            response = requests.get(image_url_list[i])
            try:
                img = Image.open(io.BytesIO(response.content))
                img_text = pytesseract.image_to_string(img)
            except:
                card = Image.new("RGBA", (220, 220), (255, 255, 255))
                img = Image.open(io.BytesIO(response.content)).convert("RGBA")
                x, y = img.size
                card.paste(img, (0, 0, x, y), img)
                card.save("test.png", format="png")
                newImg = Image.open("test.png")
                img_text = pytesseract.image_to_string(newImg)
            img_text_list.append(img_text)
    except:
        img_text_list = ['Images cannot be read']
    return img_text_list