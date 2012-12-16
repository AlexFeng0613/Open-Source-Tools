How to run this program in GAE environment::
Application is running on this site: http://irisviel-einzbern.appspot.com/.
Get access to this website and click login to the program. After click this link you will be forwarded to login interface.
Having logged in you will see the main page of my program.There are 6 sections and from top to down is welcome information about current account information, View reults with category selection, select a category to vote, create new category, edit current user created category,and import XML file structured categories.
If has no category under current user you have to create one by yourself. Once created these result will be shown at the main page.
View vote results forward to a page showing selected vote result.
Create category will stay at the same page once clicked create button.
Edit current user created category forward to a selected category, in which you have options to add item, remove one selected item, rename selected item and export current category and show in a XML structure file. If you could look into the source code of page it is a perfect XML structured file.
Import  XML file to add the items into the category with erazing ones not in the XML and add new into database while the old one remain unchanged.


The file structure of this final project:
One python program with the name finalProject.py where all of the codes are in. 
One app.yaml file which is the configuration file of the program, which is used by the Google App Engine. Without it and not aware of modifying some arguments may cause this program fail to load by GAE.
Several HTML page templates implemented by the programm files.
One Read Me file.
An export.xml file, serves as the template of xml output page. When exporting current category it works.
An Category.xml file, mainly used when I am developing the importing function for this project. It is in the same form as the example that has 2 level deep structure. Of course it is not must have since I add a xml file selection function and you can choose your preferred categories.

The Basic feature of this project:
It is written in python 2.7, you can see the packages and classes imported at the head of the file.
It is submitted by GIT under Windows 7 system environment. For the convience of typing in and out I choose to work on windows rather than unix or linux machines.
The program implements jinja2 template to render different http pages.
Two google database classes are used in this project: one is the category stores the category name and user who created it, and a Item class with a category as key storing item name, win times and lose times. Data store features and API implement can be seen in the web page rendering and codes.

New feature as required:
This project support multiple users,only a logged in user have access to the categories and items created himself. Also only he can modify his own file, while other logged in users would be unable to see categories and items created not by themselves.
The edit category and item show different items and categories for different users.
For the vote procedure, user would be able to choose among differernt categories, even not created by himself. In addition he can vote on those categories and see results. This results is a summation of many user's voting result as the professor requires.
Importing is supported by my project. User can choose add or delete categories by themselves, or upload a xml file in the correct format consitent with the example, storing item and category names. Imported categories can be either existed or non-existent in the database.

Advanced functions I choose to work:
Due to the busy schedule during the exam weeks and many other arrangements I chose the one which I suit me the best: modify items as like. Items can be added, deleted by the user. Users also have an option that change item names. Manual operation choice can be found in the Edit current user created category page when choose the right category at the main page.
There is also a link at the main page called import category from XML. You can use it to import XML files. Items exists in database but not in the XML file will be removed after import. If XML and database has the same item name its value will be preserved while the new item will be added to the database with its value initialized to be 0.
