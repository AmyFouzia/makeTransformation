from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         translate: create a translation matrix,
                    then multiply the transform matrix by the translation matrix -
                    takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge matrix
         display: clear the screen, then
                  draw the lines of the edge matrix to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge matrix to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing

See the file script for an example of the file format
"""
def parse_file( fname, points, transform, screen, color ):
    comm = []
    file = open(fname,'r')
    line = file.readlines()
    file.close()

    for i in range(len(line)):
        line[i] = line[i].rstrip()

    for i in range(len(line)):
        print(i+1)
        if(line[i] == 'line'):
            line2 = line[i+1]
            line2 = line2.split(' ')
            add_edge(points,int(line2[0]),int(line2[1]),int(line2[2]),int(line2[3]),int(line2[4]),int(line2[5]))

        elif(line[i] == 'ident'):
            comm.append('ident')

        elif(line[i] == 'scale'):
            line2 = line[i+1]
            line2 = line2.split(' ')
            track = make_scale(int(line2[0]),int(line2[1]),int(line2[2]))
            comm.append(track)

        elif(line[i] == 'move'):
            line2 = line[i+1]
            line2 = line2.split(' ')
            track = make_translate(int(line2[0]),int(line2[1]),int(line2[2]))
            comm.append(track)

        elif(line[i] == 'rotate'):
            line2 = line[i+1]
            line2 = line2.split(' ')

            if(line2[0] == 'x'):
                comm.append(make_rotX(int(line2[1])))

            elif(line2[0] == 'y'):
                comm.append(make_rotY(int(line2[1])))

            elif(line2[0] == 'z'):
                comm.append(make_rotZ(int(line2[1])))

        elif(line[i] == 'apply'):

            for i in range(len(comm)):
                line2 = comm.pop()

                if(isinstance(line2,str)):
                    ident(transform)

                else:
                    matrix_mult(line2,points)

            for j in range(len(points)):
                for k in range(len(points[j])):
                    points[j][k] = int(round(points[j][k]))

        elif(line[i] == 'display'):
            clear_screen(screen)
            draw_lines(points,screen,color)
            display(screen)

        elif(line[i] == 'save'):
            ppm_name = line[i+1]
            save_ppm_ascii( screen, ppm_name )
            d = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE, shell = True )
            d.communicate()

        elif(line[i] == 'quit'):
            break
