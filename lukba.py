import math
import socket
import json
#import rethinkdb as r
print("kecske")

def Calculate(sensor1pos,sensor2pos,r1, r2):
	u1=sensor1pos[0]
	v1=sensor1pos[1]
	u2=sensor2pos[0]
	v2=sensor2pos[1]
	if(u1==u2):
		#print('u1=u2')
		#print(v2-v1)
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
		#print(x1,y1)
		#print(x2,y2)
		result1=[x1,y1]
		result2=[x2,y2]
		result=[result1,result2]
	else:
		#print('u1!=u2')
		p=(math.pow(r1,2)-math.pow(r2,2)-math.pow(u1,2)+math.pow(u2,2)-math.pow(v1,2)+math.pow(v2,2))/(2*u2-2*u1)
		q=(2*v2-2*v1)/(2*u2-2*u1)
		a=math.pow(q,2)+1
		b=-2*q*p+2*q*u1-2*v1
		c=math.pow(p,2)+math.pow(u1,2)+math.pow(v1,2)-math.pow(r1,2)-2*u1*p
		#print('determináns: ')
		#print(math.pow(b,2)-4*a*c)
		y1=((-b)+math.sqrt(math.pow(b,2)-4*a*c))/(2*a)
		y2=((-b)-math.sqrt(math.pow(b,2)-4*a*c))/(2*a)
		x1=p-q*y1
		x2=p-q*y2
		x1=round(x1,2)
		y1=round(y1,2)
		x2=round(x2,2)
		y2=round(y2,2)
		#print(x1,y1)
		#print(x2,y2)
		result1=[x1,y1]
		result2=[x2,y2]
		result=[result1,result2]
	return result

def position(coordinates):
	egyez=0
	position=[0,0]
	#print(len(coordinates))
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
	

def main():
	sensor1pos=[0,0]
	sensor2pos=[390,0]
	sensor3pos=[0,440]
	GlassPos=[]
	PhonePos=[]
	KeyPos=[]
	PenPos=[]

	print('Ready to create socket.')
	#socket init
	s=socket.socket()
	print ('Socket created.')
	host = '192.168.0.101' 
	port = 12345
	s.bind((host, port))
	print ('Socket bind complete.')
	# except (socket.error , msg):
		# print 'Bind failed. Error code: ' + str(msg[0]) + 'Error message: ' + msg[1]
		# sys.exit()
	#socekt listening
	s.listen(1)
	while(True):			
		c, addr = s.accept()
		print ('Got connection from: ', addr)
		m = 'Thank you for connecting'
		c.send(m.encode())
		data = c.recv(1024).decode()
		data2=json.loads(data)
		print(data2)
		print('Positions: ')
		
		if('Key' in data2):
			key=data2['Key']
			KeyIntersection1=Calculate(sensor1pos,sensor2pos,key[0], key[1])
			KeyIntersection2=Calculate(sensor1pos,sensor3pos,key[0], key[2])
			KeyIntersection3=Calculate(sensor2pos,sensor3pos,key[1], key[2])
			KeyPos.append(KeyIntersection1[0])
			KeyPos.append(KeyIntersection1[1])
			KeyPos.append(KeyIntersection2[0])
			KeyPos.append(KeyIntersection2[1])
			KeyPos.append(KeyIntersection3[0])
			KeyPos.append(KeyIntersection3[1])
			print('The coordinates of Key: ')
			KeyCoordinates=position(KeyPos)
			KeyPos=[]
		else:
			print('Keys are not in the house! ')
			
		if('Phone'in data2):
			phone=data2['Phone']
			PhoneIntersection1=Calculate(sensor1pos,sensor2pos,phone[0], phone[1])
			PhoneIntersection2=Calculate(sensor1pos,sensor3pos,phone[0], phone[2])
			PhoneIntersection3=Calculate(sensor2pos,sensor3pos,phone[1], phone[2])
			PhonePos.append(PhoneIntersection1[0])
			PhonePos.append(PhoneIntersection1[1])
			PhonePos.append(PhoneIntersection2[0])
			PhonePos.append(PhoneIntersection2[1])
			PhonePos.append(PhoneIntersection3[0])
			PhonePos.append(PhoneIntersection3[1])
			print('The coordinates of Phone: ')
			PhoneCoordinates=position(PhonePos)
			PhonePos=[]
		else:
			print('Phone is not in the house! ')			
		
		if('Glass'in data2):
			glass=data2['Glass']
			GlassIntersection1=Calculate(sensor1pos,sensor2pos,glass[0], glass[1])
			GlassIntersection2=Calculate(sensor1pos,sensor3pos,glass[0], glass[2])
			GlassIntersection3=Calculate(sensor2pos,sensor3pos,glass[1], glass[2])
			GlassPos.append(GlassIntersection1[0])
			GlassPos.append(GlassIntersection1[1])
			GlassPos.append(GlassIntersection2[0])
			GlassPos.append(GlassIntersection2[1])
			GlassPos.append(GlassIntersection3[0])
			GlassPos.append(GlassIntersection3[1])
			print('The coordinates of Glass: ')
			GlassCoordinates=position(GlassPos)
			GlassPos=[]
		else:
			print('Glasses are not in the house! ')	
		
		if('Pen'in data2):
			pen=data2['Pen']
			PenIntersection1=Calculate(sensor1pos,sensor2pos,pen[0], pen[1])
			PenIntersection2=Calculate(sensor1pos,sensor3pos,pen[0], pen[2])
			PenIntersection3=Calculate(sensor2pos,sensor3pos,pen[1], pen[2])
			PenPos.append(PenIntersection1[0])
			PenPos.append(PenIntersection1[1])
			PenPos.append(PenIntersection2[0])
			PenPos.append(PenIntersection2[1])
			PenPos.append(PenIntersection3[0])
			PenPos.append(PenIntersection3[1])
			print('The coordinates of Pen: ')
			PenCoordinates=position(PenPos)
			PenPos=[]
		else:
			print('Pen is not in the house! ')
		c.close() 				
		
		key={}
		glass={}
		phone={}
		pen={}
		
		#rethink init: petiéből
		#tryexception->pass
		#	ha sikerül-->upload	
if __name__ == '__main__':
	main()
