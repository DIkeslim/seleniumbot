import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask
from selenium.webdriver.common.keys import Keys

from flask_mysqldb import MySQL


print(datetime.datetime.now())
time.sleep(5)

app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'crawler'
#
# mysql = MySQL(app)


@app.route("/")
def index():
    PATH = "C:\Program Files\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://staging.financialfitness.center/classroom/trove-uni/")

  # cur = mysql.connection.cursor()

    # Image links
    imgs = driver.find_elements_by_xpath("//img")
    img_list = [img.get_attribute("src") for img in imgs]

    elements = driver.find_elements_by_css_selector('a.course-collection-card')
    link_list = [el.get_attribute("href") for el in elements]
    cat_list = [el.text for el in elements]
    cat_slug = [el.text.lower().replace(' ', '-') for el in elements]

    data = list()


    for i, cat in enumerate(cat_list):

        link = link_list[i]

        driver.get(link)
        element = WebDriverWait(driver, 10).until(
                     EC.presence_of_element_located((By.LINK_TEXT, cat)))

        # Image links
        imgs = driver.find_elements_by_xpath("//img")
        lessons_img_list = [img.get_attribute("src") for img in imgs]

        elements = driver.find_elements_by_css_selector('a.course-card-name')
        lessons_link_list = [el.get_attribute("href") for el in elements]
        lessons_list = [el.text for el in elements]

        print('lessons', lessons_list, lessons_link_list, lessons_img_list)
        lessons = list()
        for j, lesson in enumerate(lessons_list):
            lessons.append({
                'title': lesson,
                'image_link': lessons_img_list[j],
                'link': lessons_link_list[j],
                'slug': lesson.lower().replace(' ', '-')
            })




            second_link = lessons_link_list[j]
            driver.get(second_link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, lesson)))

            content = driver.find_elements_by_xpath('//div[@class="article-content"]')
            cont_list = [con.text for con in content]
            print(cont_list)
            div_content = list()

            for k, content in enumerate(cont_list):
                div_content.append({
                    'content': cont_list[k]
                })

            quiz = driver.find_elements_by_css_selector('a.btn')
           # driver.find_element_by_xpath('//div[@class="btn"]/a').get_attribute('href')
            quiz_list = [qu.get_attribute("href") for qu in quiz]
            #driver.find_elements_by_css_selector('a.btn')

            print(quiz_list)

            quiz_link = list()

            for l, quiz in enumerate(quiz_list):
                quiz_link.append({
                    'quiz': quiz_list[l]
                })

        data.append({
            'category': cat,
            'image_link': img_list[i],
            'link': link_list[i],
            'slug': cat.lower().replace(' ', '-'),
            'lessons': lessons,
            'content': cont_list[k]
        })

   

       #cur.execute(f"INSERT INTO robot (categories,image,slug) VALUES ('{category}', '{image_link}', '{slug}')")
       #mysql.connection.commit()
       #cur.close()
        return ("done")

        print('Final', data)

    driver.quit()



if __name__ == '__main__':
    app.run(debug=True)









