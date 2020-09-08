from flask import Flask, g, request, jsonify
from database import get_db
from functools import wraps

app = Flask(__name__)

def protected(f):
	@wraps(f)
	def decor(*args,**kwargs):
		auth = request.authorization
		db=get_db()
		sql=db.cursor(dictionary=True)
		if auth:
			sql.execute('select * from user where username=%s',[auth.username])
			result=sql.fetchone()
			if auth.password==result['password'] and result['mask_prv'] == True:
				return f(*args,**kwargs)
		return jsonify({'message':'Authentication failed'}),403
	return decor


@app.teardown_appcontext
def close(error):
	if hasattr(g,'mysql'):
		g.mysql.close()


@app.route('/get_data',methods=['GET'])
@protected
def get_data():
	db=get_db()
	sql=db.cursor(dictionary=True)
	sql.execute('select * from issues')
	results=sql.fetchall()
	issues=[]
	for item in results:
		issue_dict={}
		issue_dict['id']=item['id']
		issue_dict['body']=item['body']
		issues.append(issue_dict)

	return jsonify({'issues':issues})

@app.route('/get_data/<int:id>',methods=['GET'])
@protected
def get_data_for(id):
	db=get_db()
	sql=db.cursor(dictionary=True)
	sql.execute('select * from issues where id=%s',[id])
	results=sql.fetchall()

	return jsonify({'id':results['id'],'body':results['body']})

#Masking of plain text only
@app.route('/mask',methods=['PUT'])
@protected
def mask():
	db=get_db()
	sql=db.cursor(dictionary=True)
	data=request.get_json()
	sql.execute('update issues set body= replace(body,%s,"xxxxxx") where id=%s',[data['mask'],data['id']])
	db.commit()

	sql.execute('select * from issues where id=%s',[data['id']])
	result=sql.fetchone()

	return jsonify({'id':result['id'],'body':result['body']})

@app.route('/add_data',methods=['POST'])
@protected
def add_data():
	data=request.get_json()
	db = get_db()
	sql=db.cursor(dictionary=True)
	sql.execute('insert into issues (body) values (%s)',[data['body']])
	db.commit()
	return 'Email content inserted.'

if __name__ == '__main__':
	app.run(debug=True)