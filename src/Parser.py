import xml.etree.ElementTree as ET
import os

import mysql.connector

config = {
  'user': 'root',
  'password': 'Janki149!',
  'host': '127.0.0.1',
  'database': 'Capstone_project',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

class Parser():
    def __init__(self):
        print("in init")
        self.id = ''
        self.name = ''
        self.yearpublished = ''
        self.minplayer = 0
        self.maxplayer = 0
        self.playingtime = 0
        self.averagerating = 0.0
        self.desinger = list([])
        self.publisher = list([])
        self.category = list([])
        self.mechanics = list([])
        self.age = ''
        self.rank = ''
        self.counter = 0;

    def getelements(self, filename):
        tree = ET.parse("../data/" + filename)
        root = tree.getroot()

        for child in root:
            self.id = child.get('objectid')
            self.yearpublished = child.find('yearpublished').text if child.find('yearpublished') is not None else ''
            self.minplayers = child.find('minplayers').text if child.find('yearpublished') is not None else ''
            self.maxplayers = child.find('maxplayers').text if child.find('yearpublished') is not None else ''
            self.playingtime = child.find('playingtime').text if child.find('yearpublished') is not None else ''
            self.age = child.find('age').text if child.find('yearpublished') is not None else ''
            if(child.find('boardgamedesigner') !=  None):
                self.desinger.append(child.find('boardgamedesigner').text)
            if (child.find('boardgamecategory') !=  None):
                self.category.append(child.find('boardgamecategory').text)
            if (child.find('boardgamepublisher') != None):
                self.publisher.append(child.find('boardgamepublisher').text)
            if (child.find('boardgamemechanic') != None):
                self.mechanics.append(child.find('boardgamemechanic').text)
            name = child.find('name') if child.find('yearpublished') is not None else ''
            if name != '' and name.get('primary') == 'true':
                self.name = name.text
            self.averagerating = child.find('statistics').find('ratings').find('average').text if child.find('statistics') is not None else ''
            ranks = child.find('statistics').find('ratings').find('ranks') if child.find('statistics') is not None else ''
            for rank in ranks:
                if rank.get('friendlyname') == 'Board Game Rank':
                    self.rank = rank.get('value')
        self.print_values()
        self.insert_into_table()

    def print_values(self):
        print("id = " + str(self.id))
        print(self.name)
        print(self.yearpublished)
        print(self.minplayer)
        print(self.maxplayer)
        print(self.playingtime)
        print(self.averagerating)
        print(self.desinger)
        print(self.publisher)
        print(self.category)
        print(self.mechanics)
        print(self.age)
        print(self.rank)
        print(self.counter)

    def insert_into_table(self):
        mycursor = cnx.cursor()
        desinger = ''
        publisher = ''
        mechanic = ''
        category = ''

        if self.id != '' and self.name != '':
            if self.desinger:
                desinger = self.desinger[0]
            if self.publisher:
                publisher = self.publisher[0]
            if self.mechanics:
                mechanic = self.mechanics[0]
            if self.category:
                category = self.category[0]
            sql = "INSERT INTO board_game VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (self.id, self.name, self.yearpublished, self.minplayer, self.maxplayer, self.playingtime, self.averagerating, desinger, category, mechanic, publisher, self.age, self.rank)
            mycursor.execute(sql, val)


            print("1 record inserted, ID:", mycursor.lastrowid)
        else:
            print("Game is missing name")




files = os.listdir('../data/')
counter = 0
for file in files:
    print(file)
    counter += 1
    Parser().getelements(file)
    print(counter)

cnx.commit()