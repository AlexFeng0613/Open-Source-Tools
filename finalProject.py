import datetime
import urllib
import webapp2
import random
from xml.dom.minidom import parseString

from google.appengine.ext import db
from google.appengine.api import users
import jinja2
import os

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Category(db.Model):
	name = db.StringProperty()
	create_by = db.StringProperty()  
class Item(db.Model):
	name = db.StringProperty()
	win = db.IntegerProperty()
	lose = db.IntegerProperty()

class MainPage(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			currentUser=users.get_current_user().nickname()
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			currentUser="DefaultUser"
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		categoryQuery=Category.all()
		categories1=categoryQuery.run()
		categories2=categoryQuery.run()
		editableCategoryQuery=Category.all()
		editableCategoryQuery.filter("create_by =",currentUser)
		editableCategory=editableCategoryQuery.run()
		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'editableCategory': editableCategory,
			'categories1': categories1,
			'categories2': categories2,
			'currentUser': currentUser,
		}
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))
    
class CreateCategory(webapp2.RequestHandler):
	def post(self):
		if users.get_current_user():
			newCategoryName = self.request.get('category_name')
			categoryQuery=Category.all()
			categoryQuery.filter("name =",newCategoryName)
			categoryQueryResult=categoryQuery.get()
			if newCategoryName!="":
					category=Category(name=newCategoryName,create_by=users.get_current_user().nickname())
					category.put()
			self.redirect('/')		
			
class EditCategory(webapp2.RequestHandler):
	def post(self):
		action = self.request.get('action')
		currentCategory = self.request.get('edit')
		categoryQuery=Category.all()
		categoryQuery.filter("name =",currentCategory)
		currentCategoryResults=categoryQuery.get()
		if action == "Edit":
			key = currentCategoryResults.key()
			basicItemQuery=Item.all()
			basicItemQuery.ancestor(key)
			currentItem = basicItemQuery.run()
			currentItem2 = basicItemQuery.run()
			template_values = {
				'currentItem': currentItem,
				'currentItem2': currentItem2,
				'currentCategory': currentCategory,
			}
			template = jinja_environment.get_template('edit.html')
			self.response.out.write(template.render(template_values))  
		else :
			currentCategoryResults.delete()
			self.redirect('/')

class VoteCategory(webapp2.RequestHandler):
	def post(self):
		if users.get_current_user():
			currentCategory = self.request.get('vote')
			categoryQuery=Category.all()
			categoryQuery.filter("name =",currentCategory)
			currentCategoryQuery=categoryQuery.get()
			key = currentCategoryQuery.key()
			basicItemQuery=Item.all()
			basicItemQuery.ancestor(key)
			AllItems=basicItemQuery.fetch(50)
			if len(AllItems)<2:
				status="error"
				template_values = {
					'status': status,
					'currentCategory': currentCategory,
				}
			else :
				status="true"
				item1 = random.choice(AllItems)
				AllItems.remove(item1)
				item2 = random.choice(AllItems)
				AllItems.append(item1)
				template_values = {
					'status': status,
					'item1': item1,
					'item2': item2,
					'currentCategory': currentCategory,
				}
			template = jinja_environment.get_template('vote.html')
			self.response.out.write(template.render(template_values)) 
	
class AddItem(webapp2.RequestHandler): 
	def post(self):
		item_name=self.request.get('item_name')
		category_name=self.request.get('category_name')
		categoryQuery=Category.all()
		categoryQuery.filter("name =",category_name)
		currentCategoryResults=categoryQuery.get()
		key=currentCategoryResults.key()
		if item_name!="":
				item=Item(name=item_name,win=0,lose=0,parent=key)
				item.put()  
		self.redirect('/')

class RenameItem(webapp2.RequestHandler):
	def post(self):
		item_name=self.request.get('rename')
		new_name=self.request.get('new_name')
		itemQuery=Item.all()
		itemQuery.filter("name =",item_name)
		item=itemQuery.get()
		item.name=new_name
		item.put()
		self.redirect('/')
	
class RemoveItem(webapp2.RequestHandler): 
	def post(self):
		item_name=self.request.get('remove')
		itemQuery=Item.all()
		itemQuery.filter("name =",item_name)
		currentItemInstances=itemQuery.run()
		for currentItemInstance in currentItemInstances:
			currentItemInstance.delete()
		self.redirect('/') 

class Update(webapp2.RequestHandler): 
	def post(self):
		currentCategory=self.request.get('category_name')
		action=self.request.get('action')
		result=self.request.get('vote')
		voteItem1=self.request.get('vote1')
		voteItem2=self.request.get('vote2')
		categoryQuery=Category.all()
		categoryQuery.filter("name =",currentCategory)
		length = categoryQuery.fetch(1000000)
		currentCategoryResults=categoryQuery.get()
		key = currentCategoryResults.key()
		basicItemQuery=Item.all()
		basicItemQuery.ancestor(key)
		AllItems=basicItemQuery.fetch(100)
		randomItem1 = random.choice(AllItems)
		AllItems.remove(randomItem1)
		randomItem2 = random.choice(AllItems)
		AllItems.append(randomItem1)
		if result != "":
			if action=="Vote":
				basicItemQuery=Item.all()
				basicItemQuery.filter("name =",voteItem1)
				item1=basicItemQuery.get()
				basicItemQuery=Item.all()
				basicItemQuery.filter("name =",voteItem2)
				item2=basicItemQuery.get()
				if result==voteItem1:
					lastVoted=voteItem1
					lastNotVoted = voteItem2
					item1.win = item1.win + 1
					item2.lose = item2.lose + 1
				else:
					lastVoted=voteItem2
					lastNotVoted = voteItem1
					item1.lose = item1.lose + 1
					item2.win = item2.win + 1	
				item1.put()
				item2.put()
				template_values = {
					'status': "true",
					'votedLastTime':"true",
					'currentCategory':currentCategory,
					'item1': randomItem1,
					'item2': randomItem2,
					'voteItem1':voteItem1,
					'voteItem2':voteItem2,
					'lastVote1Win':item1.win,
					'lastVote2Win':item2.win,
					'lastVoted':lastVoted,
					'lastNotVoted':lastNotVoted,
				}
			else:
				basicItemQuery=Item.all()
				basicItemQuery.filter("name =",voteItem1)
				item1=basicItemQuery.get()
				basicItemQuery=Item.all()
				basicItemQuery.filter("name =",voteItem2)
				item2=basicItemQuery.get()
				template_values = {
					'status': "true",
					'votedLastTime':"false",
					'currentCategory':currentCategory,
					'item1': randomItem1,
					'item2': randomItem2,
					'voteItem1':voteItem1,
					'voteItem2':voteItem2,
					'lastVote1Win':item1.win,
					'lastVote2Win':item2.win,
				}
		else:
			basicItemQuery=Item.all()
			basicItemQuery.filter("name =",voteItem1)
			item1=basicItemQuery.get()
			basicItemQuery=Item.all()
			basicItemQuery.filter("name =",voteItem2)
			item2=basicItemQuery.get()
			template_values = {
				'status': "true",
				'votedLastTime':"false",
				'currentCategory':currentCategory,
				'item1': randomItem1,
				'item2': randomItem2,
				'voteItem1':voteItem1,
				'voteItem2':voteItem2,
				'lastVote1Win':item1.win,
				'lastVote2Win':item2.win,
			}
		template = jinja_environment.get_template('vote.html')
		self.response.out.write(template.render(template_values))
			
class ExportCategory(webapp2.RequestHandler):
	def post(self):
		currentCategory=self.request.get('category_name')
		categoryQuery=Category.all()
		categoryQuery.filter("name =",currentCategory)
		categoryQueryResult=categoryQuery.get()
		if categoryQueryResult:
			key=categoryQueryResult.key()
		else:
			key=""
		basicItemQuery=Item.all()
		basicItemQuery.ancestor(key)
		Items=basicItemQuery.fetch(50)
		template_values = {
			'currentCategory':currentCategory,
			'Items':Items,
		}
		template = jinja_environment.get_template('export.xml')
		self.response.out.write(template.render(template_values)) 

class ImportCategory(webapp2.RequestHandler):
	def post(self):
		items=[]
		key=""
		creator=""
		filename=self.request.get('filename')
		xml=parseString(filename)
		category=xml.getElementsByTagName('NAME')[0].childNodes[0].data
		length=xml.getElementsByTagName('NAME').length
		for i in range(1,length):
			items.append(xml.getElementsByTagName('NAME')[i].childNodes[0].data)
		categoryQuery=Category.all()
		categoryQuery.filter("name =",category)
		queryCategoryResult=categoryQuery.get()
		if queryCategoryResult:
			key=queryCategoryResult.key()
			creator=queryCategoryResult.create_by
		if key != "" :
			if creator ==  users.get_current_user().nickname():
				basicItemQuery=Item.all()
				basicItemQuery.ancestor(key)
				AllItems=basicItemQuery.fetch(limit=1000)
				for item1 in AllItems :
					flag = False
					for item2 in items:
						if item1.name == item2:
							flag = True
					if flag == False:
						item1.delete()
				AllItems=basicItemQuery.fetch(limit=1000)
				for item1 in items :
					flag = False
					for item2 in AllItems:
						if item1 == item2.name:
							flag = True
					if flag == False:
						item=Item(name=item1,win=0,lose=0,parent=key)
						item.put() 
		else :
			if users.get_current_user():
				newCategory=Category(name=category,create_by=users.get_current_user().nickname())
				newCategory.put()
				categoryQuery=Category.all()
				categoryQuery.filter("name =",category)
				categoryQueryResult=categoryQuery.get()
				key=categoryQueryResult.key()
				for item in items:
					item=Item(name=item,win=0,lose=0,parent=key)
					item.put() 
		self.redirect('/')
			
class ViewResults(webapp2.RequestHandler):
	def post(self):
		currentCategory=self.request.get('category')
		categoryQuery=Category.all()
		categoryQuery.filter("name =",currentCategory)
		currentCategorySelected=categoryQuery.get()
		key=currentCategorySelected.key()
		basicItemQuery=Item.all()
		basicItemQuery.ancestor(key)
		Items=basicItemQuery.fetch(limit=100)
		template_values = {
			'items':Items,
			'category':currentCategory,
		}
		template = jinja_environment.get_template('results.html')
		self.response.out.write(template.render(template_values))
			
app = webapp2.WSGIApplication([('/', MainPage),('/create_category', CreateCategory),('/edit_category',EditCategory),('/vote_category',VoteCategory),
                               ('/add_item',AddItem),('/remove_item',RemoveItem),('/update',Update),('/rename_item',RenameItem),
							   ('/export_category',ExportCategory),('/import_category',ImportCategory),('/view_results',ViewResults)],debug=True)          