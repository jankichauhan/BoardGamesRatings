import xml.etree.ElementTree as ET
import os

import mysql.connector
import unicodedata


config = {
  'user': '',
  'password': '',
  'host': '127.0.0.1',
  'database': 'Capstone_project',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
mycursor = cnx.cursor()
class Parser():
    def __init__(self):
        print("in init")
        self.id = ''
        self.name = ''
        self.yearpublished = ''
        self.minplayers = 0
        self.maxplayers = 0
        self.playingtime = 0
        self.averagerating = 0
        self.designer = list([])
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
            self.yearpublished = child.find('yearpublished').text if child.find('yearpublished') is not None else 0
            self.minplayers = child.find('minplayers').text if child.find('minplayers') is not None else 0
            self.maxplayers = child.find('maxplayers').text if child.find('maxplayers') is not None else 0
            self.playingtime = child.find('playingtime').text if child.find('playingtime') is not None else 0
            self.age = child.find('age').text if child.find('age') is not None else ''
            self.averagerating = child.find('statistics').find('ratings').find('average').text if child.find('statistics') is not None else ''
            ranks = child.find('statistics').find('ratings').find('ranks') if child.find('statistics') is not None else ''
            for rank in ranks:
                if rank.get('friendlyname') == 'Board Game Rank':
                    self.rank = rank.get('value')
            for grandChild in child:
                if grandChild.tag == 'boardgamedesigner':
                    self.designer.append(grandChild.text)
                if grandChild.tag == 'boardgamecategory':
                    self.category.append(grandChild.text)
                if grandChild.tag == 'boardgamepublisher':
                    self.publisher.append(grandChild.text)
                if grandChild.tag == 'boardgamemechanic':
                    self.mechanics.append(grandChild.text)
                if grandChild.tag == 'name':
                    if grandChild.get('primary') == 'true':
                        self.name = self.remove_accents(grandChild.text)
        self.print_values()
        self.insert_into_table()

    def print_values(self):
        print("id = " + str(self.id))
        print(self.name)
        print(self.yearpublished)
        print(self.minplayers)
        print(self.maxplayers)
        print(self.playingtime)
        print(self.averagerating)
        print(self.designer)
        print(self.publisher)
        print(self.category)
        print(self.mechanics)
        print(self.age)
        print(self.rank)
        print(self.counter)

    def remove_accents(self, input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii.decode()

    def insert_into_table(self):


        # Clear all table content before inserting

        designer = ''
        publisher = ''
        mechanic = ''
        category = ''

        if self.id != '' and self.name != '':
            if self.designer:
                designer = ':'.join(self.designer[:3])
                designer = self.remove_accents(designer)
                print(designer)
            if self.publisher:
                publisher = ':'.join(self.publisher[:3])
                publisher = self.remove_accents(publisher)
                print(publisher)
            if self.mechanics:
                mechanic = ':'.join(self.mechanics[:3])
            if self.category:
                category = ':'.join(self.category[:3])
                print(category)
            if self.rank == '' or self.rank == 'Not Ranked':
                self.rank = 0
            sql_insert = "INSERT INTO board_game VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (self.id, self.name, self.yearpublished, self.minplayers, self.maxplayers, self.playingtime, self.averagerating, designer, category, mechanic, publisher, self.age, self.rank)
            print(sql_insert, val)
            mycursor.execute(sql_insert, val)
            cnx.commit()

            print("1 record inserted, ID:", mycursor.lastrowid)
        else:
            print("Game is missing name")




files = os.listdir('../data/')
counter = 0
sql_delete = "delete from board_game where board_game_id > 0"
mycursor.execute(sql_delete)
cnx.commit()
for file in files:
    print(file)
    counter += 1
    Parser().getelements(file)
print(counter)
# Parser().getelements('game161936.xml')
