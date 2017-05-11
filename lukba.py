import math
print("kecske")
#create an INET, STREAMing socket
#s = socket.socket(
#   socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
#s.connect(("l", 80))

def importjason():
	print('importjatekbolmegvolt')

def Calculate(sensor1pos,sensor2pos,r1, r2):
	u1=sensor1pos[0]
	v1=sensor1pos[1]
	u2=sensor2pos[0]
	v2=sensor2pos[1]
	if(u1==u2):
		print('u1=u2')
		print(v2-v1)
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
		print(x1,y1)
		print(x2,y2)
		result1=[x1,y1]
		result2=[x2,y2]
		result=[result1,result2]
	else:
		print('u1!=u2')
		p=(math.pow(r1,2)-math.pow(r2,2)-math.pow(u1,2)+math.pow(u2,2)-math.pow(v1,2)+math.pow(v2,2))/(2*u2-2*u1)
		q=(2*v2-2*v1)/(2*u2-2*u1)
		a=math.pow(q,2)+1
		b=-2*q*p+2*q*u1-2*v1
		c=math.pow(p,2)+math.pow(u1,2)+math.pow(v1,2)-math.pow(r1,2)-2*u1*p
		print('determináns: ')
		print(math.pow(b,2)-4*a*c)
		y1=((-b)+math.sqrt(math.pow(b,2)-4*a*c))/(2*a)
		y2=((-b)-math.sqrt(math.pow(b,2)-4*a*c))/(2*a)
		x1=p-q*y1
		x2=p-q*y2
		x1=round(x1,2)
		y1=round(y1,2)
		x2=round(x2,2)
		y2=round(y2,2)
		print(x1,y1)
		print(x2,y2)
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
	#rint(position)
	return(position)
	
def printjason():
	print('jatekboljasonprintelve')

def uploadjason():
	print('jatekboljasonfeltoltve')

def main():
	sensor1pos=[0,0]
	sensor2pos=[198,0]
	sensor3pos=[0,224]
	#sensor4pos=[198,224]
	GlassPos=[]
	#sugáradatok teszteléshez
	r1=math.sqrt(2)*100
	print(r1)
	r2=math.sqrt(math.pow(98,2)+math.pow(100,2))
	print(r2)
	r3=math.sqrt(math.pow(100,2)+math.pow(124,2))
	print(r3)
	r4=math.sqrt(math.pow(98,2)+math.pow(124,2))
	print(r4)

	importjason()
	GlassIntersection1=Calculate(sensor1pos,sensor2pos,r1, r2)
	GlassIntersection2=Calculate(sensor1pos,sensor3pos,r1, r3)
	GlassIntersection3=Calculate(sensor2pos,sensor3pos,r2, r3)
	GlassPos.append(GlassIntersection1[0])
	GlassPos.append(GlassIntersection1[1])
	GlassPos.append(GlassIntersection2[0])
	GlassPos.append(GlassIntersection2[1])
	GlassPos.append(GlassIntersection3[0])
	GlassPos.append(GlassIntersection3[1])
	#print(GlassPos)
	position(GlassPos)


	# PhoneIntersection1=Calculate(sensor1pos,sensor2pos,r1, r2)
	# PhoneIntersection2=Calculate(sensor1pos,sensor3pos,r1, r3)
	# PhoneIntersection3=Calculate(sensor2pos,sensor3pos,r2, r3)

	# KeyIntersection1=Calculate(sensor1pos,sensor2pos,r1, r2)
	# KeyIntersection2=Calculate(sensor1pos,sensor3pos,r1, r3)
	# KeyIntersection3=Calculate(sensor2pos,sensor3pos,r2, r3)

	# StickIntersection1=Calculate(sensor1pos,sensor2pos,r1, r2)
	# StickIntersection2=Calculate(sensor1pos,sensor3pos,r1, r3)
	# StickIntersection3=Calculate(sensor2pos,sensor3pos,r2, r3)
	printjason()
	uploadjason()

	print('\n')
	nb = input('Choose a number')
	
if __name__ == '__main__':
	main()
