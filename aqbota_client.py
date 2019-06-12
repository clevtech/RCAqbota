import socket
import sys
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

host = '0.0.0.0'
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


moveBindings = {
        'i':(1,0,0,0),
        'o':(1,0,0,-1),
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
        'u':(1,0,0,1),
        ',':(-1,0,0,0),
        '.':(-1,0,0,1),
        'm':(-1,0,0,-1),
        'O':(1,-1,0,0),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'U':(1,1,0,0),
        '<':(-1,0,0,0),
        '>':(-1,-1,0,0),
        'M':(-1,1,0,0),
        't':(0,0,1,0),
        'b':(0,0,-1,0),
    }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }


pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
rospy.init_node('tcp_operational_node')

speed = rospy.get_param("~speed", 0.5)
turn = rospy.get_param("~turn", 1.0)
x = 0
y = 0
z = 0
th = 0
status = 0


connected = False
print("Connecting")

while True:
    if not connected:
        try:
            s.connect((host, port))
            print("Server connected")
            connected = True
        except:
            pass
    else:
        while 1:
            try:
                key = s.recv(1024)
                key = str(key.decode('utf-8'))[0]
                if key in moveBindings.keys():
                    x = moveBindings[key][0]
                    y = moveBindings[key][1]
                    z = moveBindings[key][2]
                    th = moveBindings[key][3]
                else:
                    x = 0
                    y = 0
                    z = 0
                    th = 0
                twist = Twist()
                twist.linear.x = x * speed
                twist.linear.y = y * speed
                twist.linear.z = z * speed
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = th * turn
                pub.publish(twist)
            except:
                x = 0
                y = 0
                z = 0
                th = 0
                twist = Twist()
                twist.linear.x = x * speed
                twist.linear.y = y * speed
                twist.linear.z = z * speed
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = th * turn
                pub.publish(twist)
                print("Server not connected")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connected = False
                break


s.close()
