from flask import Flask, g
import mysql.connector
from config import username,password,database

def connect_db():
	db = mysql.connector.connect(
		host='localhost',
		username=username,
		password=password,
		database=database
		)
	return db

def get_db():
	if not hasattr(g,'mysql'):
		g.mysql=connect_db()
	return g.mysql

