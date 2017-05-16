import math
import socket
import json
import rethinkdb as r
#print("kecske") this is just a commonly used initialization by group members, commented, because we are serious now

#Function for calculating the two possible (x;y) positions for an object based on it's distance from two positions (simulated sensors)
def Calculate(sensor1pos,sensor2pos,r1, r2):
	u1=sensor1pos[0]
	v1=sensor1pos[1]
	u2=sensor2pos[0]
	v2=sensor2pos[1]
	if(u1==u2):
		y=(r1*r1-r2*r2-v1*v1+v2*v2)/(-2*v1+2*v2)
		a=1
		b=-2*u1
		c=u1*u1+y*y+-2*v1*y+v1*v1-r1*r1
		x1=((-b)+math.sqrt(math.pow(b,2)-4*a*c))/(2*a)
		x2=((-b)-math.sqrt(math.pow(b,2)-4*a*c))/(2*a)
		x1=round(x1,2)
		x2=round(x2,2)
		y=round(y,2)
		y1=y
		y2=y

		result1=[x1,y1]
		result2=[x2,y2]
		result=[result1,result2]
	else:
		p=(math.pow(r1,2)-math.pow(r2,2)-math.pow(u1,2)+math.pow(u2,2)-math.pow(v1,2)+math.pow(v2,2))/(2*u2-2*u1)
		q=(2*v2-2*v1)/(2*u2-2*u1)
		a=math.pow(q,2)+1
		b=-2*q*p+2*q*u1-2*v1
		c=math.pow(p,2)+math.pow(u1,2)+math.pow(v1,2)-math.pow(r1,2)-2*u1*p
		y1=((-b)+math.sqrt(math.pow(b,2)-4*a*c))/(2*a)
		y2=((-b)-math.sqrt(math.pow(b,2)-4*a*c))/(2*a)
		x1=p-q*y1
		x2=p-q*y2
		x1=round(x1,2)
		y1=round(y1,2)
		x2=round(x2,2)
		y2=round(y2,2)
		result1=[x1,y1]
		result2=[x2,y2]
		result=[result1,result2]
	return result

#function for extraxting the correct coordinates of a simulated object, given all the possibe positions calculated
def position(coordinates):
	egyez=0
	position=[0,0]
	for i in range(0,4):
		for j in range(0,6):
			if (coordinates[i]==coordinates[j]):
				egyez+=1
		if (egyez==3):
			position=coordinates[i]
		else:
			egyez=0
	print(position)
	return(position)
	
#main function
def main():
	sensor1pos=[0,0]
	sensor2pos=[390,0]
	sensor3pos=[0,440]
	IPos = []
	Coordinates = {}
	
	#server implementation:
	#socket initialization
	print('Ready to create socket.')
	s=socket.socket()
	print ('Socket created.')
	host = 'localhost' 
	port = 12345
	s.bind((host, port))
	print ('Socket bind complete.')
	#socekt listening
	s.listen(1)
	while(True):	#this part of the main function is constantly running, it is  calculating and uploading the object-positions to a database if new data is recieved	
		#accepting data and communicating with client
		c, addr = s.accept()
		print ('Got connection from: ', addr)
		m = 'Thank you for connecting'
		c.send(m.encode())
		data = c.recv(1024).decode()
		data2=json.loads(data)
		types = list(data2.keys())
		print(data2)
		print('Positions: ')
		
		#Calculating positions for the recieved objects
		for i in range(0,len(types)):
			if(types[i] in data2):
				pos=data2[types[i]]
				Intersection1=Calculate(sensor1pos,sensor2pos,pos[0], pos[1])
				Intersection2=Calculate(sensor1pos,sensor3pos,pos[0], pos[2])
				Intersection3=Calculate(sensor2pos,sensor3pos,pos[1], pos[2])
				IPos.append(Intersection1[0])
				IPos.append(Intersection1[1])
				IPos.append(Intersection2[0])
				IPos.append(Intersection2[1])
				IPos.append(Intersection3[0])
				IPos.append(Intersection3[1])
				print('The coordinates of ' + types[i] + ":")
				Coordinates[types[i]] = position(IPos)
				IPos=[]
			else:
				print(types[i] + ' are not in the house! ')		
		
		c.close() 				
		
		pos={}

		#Uploading the names and calculated positions of the recieved objects to a rethink database server in json format
		json_data = []

		for i in range(0,len(types)):
			if(types[i] in data2) : json_data.append({'coordinates' : {'x' : int(Coordinates[types[i]][0]), 'y' : int(Coordinates[types[i]][1])}, 'type' : types[i]})

		print(json_data)
		print(json.dumps(json_data))
		try:
			db = r.connect( "localhost", 28015).repl()
			print('Connected to DB')
			r.db('IoT').table('objects').delete().run()
			print(r.db('IoT').table('objects').insert(json_data).run())
			db.close()
		except r.ReqlDriverError as e:
			print('Unable to connect to the database')

if __name__ == '__main__':
	main()