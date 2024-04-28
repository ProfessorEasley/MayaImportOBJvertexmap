'''

Face OBJ Converter

2022 Sasha Volokh

This script is used to import the OBJ output of the 3D Face Reconstruction tool (https://github.com/AaronJackson/vrn),
however it may work with other OBJs with per-vertex coloring. For other OBJs (that do not have per-vertex coloring) you
can use Maya's built-in OBJ importer.

Install the script into your Maya script directory, then from within Maya use the following:

For versions of Maya BEFORE 2022:
import convert_face_obj
reload(convert_face_obj)
convert_face_obj.run()

For versions of Maya 2022 or higher:
import convert_face_obj
import importlib
importlib.reload(convert_face_obj)
convert_face_obj.run()

'''

import maya.cmds as cmds

def run():
    filename = cmds.fileDialog2(fileMode=1, caption="Face OBJ Converter (v1.0)", fileFilter="*.obj")
    #cmds.file( filename[0], i=True );
    print(filename[0])

    import sys


    objIn = filename[0]
    daeOut = objIn+".dae"

    header = '''<?xml version="1.0" encoding="UTF-8"?>
    <COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">
    <asset>
    <up_axis>Y_UP</up_axis>
    </asset>
    <library_geometries>
    <geometry id="shape0-lib" name="shape0">
    <mesh>
    '''

    footer = '''</mesh>
    </geometry>
    </library_geometries>
    <library_visual_scenes>
    <visual_scene id="VisualSceneNode" name="VisualScene">
    <node id="node" name="node">
    <instance_geometry url="#shape0-lib"/>
    </node>
    </visual_scene>
    </library_visual_scenes>
    <scene>
    <instance_visual_scene url="#VisualSceneNode"/>
    </scene>
    </COLLADA>
    '''


    positions = []
    colors = []
    triangles = []

    with open(objIn, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                continue
            parts = line.split(' ')
            if parts[0] == 'g':
                continue
            elif parts[0] == 'v':
                if len(parts) != 7:
                    raise Exception('Per-vertex color information is missing, this script only supports OBJ files with per-vertex coloring')
                x, y, z, r, g, b = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5]), float(parts[6])
                positions.append(x)
                positions.append(y)
                positions.append(z)
                colors.append(r)
                colors.append(g)
                colors.append(b)
                colors.append(1)
            elif parts[0] == 'f':
                a, b, c = parts[1], parts[2], parts[3]
                triangles.append((int(a)-1, int(b)-1, int(c)-1))
            elif parts[0] == 'mtllib':
                raise Exception('OBJ file linked with MTL is not supported (only per-vertex coloring is supported by this script)')
            else:
                raise Exception('unexpected line {}'.format(line))

    with open(daeOut, 'w') as f:
        f.write(header)
        f.write('<source id="shape0-lib-positions" name="position">\n')
        f.write('<float_array id="shape0-lib-positions-array" count="{}">'.format(len(positions)))
        for x in positions[:-1]:
            f.write(str(x))
            f.write(' ')
        f.write(str(positions[-1]))
        f.write('</float_array>\n')
        f.write('''
                            <technique_common>
                            <accessor count="{}" source="#shape0-lib-positions-array" stride="3">
                                <param name="X" type="float"/>
                                <param name="Y" type="float"/>
                                <param name="Z" type="float"/>
                            </accessor>
                        </technique_common>
                '''.format(int(len(positions)/3)))
        f.write('</source>\n')
        f.write('<source id="shape0-lib-vcolor" name="vcolor">\n')
        f.write('<float_array id="shape0-lib-vcolor-array" count="{}">'.format(len(colors)))
        for x in colors[:-1]:
            f.write(str(x))
            f.write(' ')
        f.write(str(colors[-1]))
        f.write('</float_array>')
        f.write('''
                        <technique_common>
                            <accessor count="{}" source="#shape0-lib-vcolor-array" stride="4">
                                <param name="R" type="float"/>
                                <param name="G" type="float"/>
                                <param name="B" type="float"/>
                                <param name="A" type="float"/>
                            </accessor>
                        </technique_common>
        '''.format(int(len(colors)/4)))
        f.write('</source>\n')
        f.write('<vertices id="shape0-lib-vertices">\n')
        f.write('<input semantic="POSITION" source="#shape0-lib-positions"/>\n')
        f.write('</vertices>\n')
        f.write('<triangles count="{}">'.format(len(triangles)))
        f.write('''
            <input offset="0" semantic="VERTEX" source="#shape0-lib-vertices"/>
            <input offset="1" semantic="COLOR" source="#shape0-lib-vcolor"/>''')
        f.write('<p>')
        for a, b, c in triangles[:-1]:
            f.write(str(a))
            f.write(' ')
            f.write(str(a))
            f.write(' ')
            f.write(str(b))
            f.write(' ')
            f.write(str(b))
            f.write(' ')
            f.write(str(c))
            f.write(' ')
            f.write(str(c))
            f.write(' ')
        a, b, c = triangles[-1]
        f.write(str(a))
        f.write(' ')
        f.write(str(a))
        f.write(' ')
        f.write(str(b))
        f.write(' ')
        f.write(str(b))
        f.write(' ')
        f.write(str(c))
        f.write(' ')
        f.write(str(c))
        f.write('</p>')
        f.write('</triangles>')
        f.write(footer)
    cmds.file(daeOut,i=True)
    cmds.select( all=True )
    cmds.polyOptions( colorShadedDisplay=True )
