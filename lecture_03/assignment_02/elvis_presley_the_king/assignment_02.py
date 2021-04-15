"""Assignment 02: Build your own robot model
"""
from copy import deepcopy
import math
import random

# Rhino
from compas_fab.robots import Configuration
from compas_rhino.artists import RobotModelArtist

from compas.datastructures.mesh import Mesh
from compas.geometry.primitives import Circle
from compas.geometry.shapes import Cylinder
from compas.geometry.primitives import Frame, Vector
from compas.geometry.primitives import Plane
from compas.geometry.transformations import Translation, Rotation, Scale
from compas.robots.model import Joint
from compas.robots.model import RobotModel

# create cylinder in yz plane
radius, length = 0.3, 5
cylinder = Cylinder(Circle(Plane([0, 0, 0], [1, 0, 0]), radius), length)
cylinder.transform(Translation.from_vector([length / 2., 0, 0]))
cylinder2 = deepcopy(cylinder)


def get_color_value():
    col_val = abs(random.gauss(0.5, 0.05))
    return col_val if col_val < 1.0 else 1.0


def model():
    # create robot
    model = RobotModel("robot", links=[], joints=[])

    # add links and joints to the robot model
    # 0
    link0 = model.add_link("world")
    # 1
    mesh1 = Mesh.from_shape(cylinder)
    origin = Frame.worldXY()
    axis = Vector(0, 0, 1)
    link1 = model.add_link("link1", visual_mesh=mesh1,
                           visual_color=(get_color_value(), get_color_value(), get_color_value()))
    joint1 = model.add_joint("joint1", Joint.FIXED, link0, link1, origin=origin, axis=axis)
    # 2
    mesh2 = Mesh.from_shape(cylinder)
    mesh22 = Mesh.from_shape(cylinder2).transformed(Rotation.from_axis_and_angle((0, 0.5, 1), .5, point=[length/2, 0, 0]) *
                                                    Scale.from_factors([.7, 1, 1], frame=Frame((length/2, 0, 0), (1, 0, 0), (0, 1, 0))))
    origin = Frame((length, 0, 0), xaxis=(1, 0, 0), yaxis=(0, 1, 0))
    axis = Vector(0, 0, 1)
    link2 = model.add_link("link2", visual_meshes=[mesh2, mesh22],
                           visual_color=(abs(get_color_value()), get_color_value(), get_color_value()))
    joint2 = model.add_joint("joint2", Joint.CONTINUOUS, link1, link2, origin=origin, axis=axis)

    # Create a configuration object matching the number of joints in your model
    configuration = Configuration.from_revolute_values([1.4], joint_names=[joint.name for joint in model.get_configurable_joints()])

    # iterative link and joint creation
    previous_link = link2
    for i in range(10):
        new_mesh = Mesh.from_shape(cylinder)
        new_mesh2 = Mesh.from_shape(cylinder2).transformed(Rotation.from_axis_and_angle((0, 0.5*i*(i%2), 1), .5, point=[length/2, 0, 0]) *
                                                           Scale.from_factors([.7+(i/2)%3, 1, 1], frame=Frame((length/2, 0, 0), (1, 0, 0), (0, 1, 0))))
        origin = Frame((length, 0, 0), xaxis=(1, 0, 0), yaxis=(0, 1, 0))
        axis = Vector(0, .1*i, 1)
        new_link_name = "link{}".format(3+i)
        new_joint_name = "joint{}".format(3+i)
        link3 = model.add_link(new_link_name, visual_meshes=[new_mesh, new_mesh2],
                               visual_color=(get_color_value(), get_color_value(), get_color_value()))
        joint3 = model.add_joint(new_joint_name, Joint.CONTINUOUS, previous_link, link3, origin=origin, axis=axis)
        configuration.joint_names.append(new_joint_name)
        configuration.values.append((i % 3)/(i+0.1))
        previous_link = link3
    return model, configuration


model1, conf1 = model()

# Update the model using the artist
artist = RobotModelArtist(model1, layer="COMPAS::robot")
artist.clear_layer()
artist.update(conf1.joint_dict)

# Render everything once
artist.draw_visual()
artist.redraw()

artists = []
for i in range(1, 9):
    model2, conf2 = model()
    artist2 = RobotModelArtist(model2, layer="COMPAS::robot2")
    artist2.layer = "COMPAS::robot2"
    artist2.clear_layer()
    conf2.values[conf2.joint_names.index("joint2")] = 1+math.degrees(i)
    artist2.update(conf2.joint_dict)

    artists.append(artist2)

# Render everything else
for arti in artists:
    arti.draw_visual()
    arti.redraw()
