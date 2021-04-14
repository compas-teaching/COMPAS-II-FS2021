from compas_fab.robots import Configuration
from compas_rhino.artists import RobotModelArtist

from compas.datastructures import Mesh
from compas.geometry import Circle
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Translation
from compas.robots import Joint
from compas.robots import RobotModel

# create cylinder in yz plane
radius, length = 0.3, 5
cylinder = Cylinder(Circle(Plane([0, 0, 0], [1, 0, 0]), radius), length)
cylinder.transform(Translation.from_vector([length / 2., 0, 0]))

# create robot
model = RobotModel("robot", links=[], joints=[])

# add links and joints to the robot model
# link0 = model.add_link(..)
# link1 = model.add_link(..)
# joint1 = model.add_joint(..)

# Create a configuration object matching the number of joints in your model
# configuration = ....

# Update the model using the artist
artist = RobotModelArtist(model)
# artist.update ...

# Render everything
artist.draw_visual()
artist.redraw()
