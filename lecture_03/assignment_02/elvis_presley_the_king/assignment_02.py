"""Assignment 02: Build your own robot model
"""
from copy import deepcopy
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
                       visual_color=(random.gauss(0.5, 0.2), random.gauss(0.2, 0.2), random.gauss(0.5, 0.2)))
joint1 = model.add_joint("joint1", Joint.FIXED, link0, link1, origin=origin, axis=axis)
# 2
mesh2 = Mesh.from_shape(cylinder)
mesh22 = Mesh.from_shape(cylinder2).transformed(Rotation.from_axis_and_angle((0, 0.5, 1), .5, point=[length/2, 0, 0]) *
                                                Scale.from_factors([.7, 1, 1], frame=Frame((length/2, 0, 0), (1, 0, 0), (0, 1, 0))))
origin = Frame((length, 0, 0), xaxis=(1, 0, 0), yaxis=(0, 1, 0))
axis = Vector(0, 0, 1)
link2 = model.add_link("link2", visual_meshes=[mesh2, mesh22],
                       visual_color=(random.gauss(0.5, 0.3), random.gauss(0.5, 0.2), random.gauss(0.5, 0.2)))
joint2 = model.add_joint("joint2", Joint.CONTINUOUS, link1, link2, origin=origin, axis=axis)


# Create a configuration object matching the number of joints in your model
configuration = Configuration.from_revolute_values([1.4, ], joint_names=[joint.name for joint in model.get_configurable_joints()])
print(configuration)

# Update the model using the artist
artist = RobotModelArtist(model, layer="COMPAS::robot")
artist.clear_layer()
artist.update(configuration.joint_dict)

# Render everything
artist.draw_visual()
artist.redraw()
