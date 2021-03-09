"""Assignment 01: Project box to xy-plane
"""
from compas.geometry import Point
from compas.geometry import Plane
from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Projection
from compas_rhino.artists import BoxArtist
from compas_rhino.artists import MeshArtist
from compas.datastructures import Mesh

# tilted frame
frame = Frame([1, 0, 3], [-0.45, 0, 0.3], [1, -0.45, 0])

# Box Creation
width, length, height = 1, 1, 1
box = Box(frame, width, length, height)

# perspective Projection
camera_point = Point(1,1,1.5)
plane = Plane([0, 0, 0], [0, 0, 1])
P_persp = Projection.from_plane_and_point(plane, camera_point)

# parallel Projection
direction = [3, 1, 3]
P_paral = Projection.from_plane_and_direction(plane, direction)

# orthogonal Projection
P_ortho = Projection.from_plane(plane)

# Create a Mesh from the Box
mesh = Mesh.from_shape(box)

# Apply the Projection onto the mesh
mesh_paral = mesh.transformed(P_paral)
mesh_ortho = mesh.transformed(P_ortho )
mesh_persp = mesh.transformed(P_persp)a

# Create artists
artist1 = BoxArtist(box)
artist2 = MeshArtist(mesh_paral)
artist3 = MeshArtist(mesh_ortho)
artist4 = MeshArtist(mesh_persp)

# Draw
artist1.draw()
artist2.draw_edges(color="#FF0000")
artist3.draw_edges(color="#FFFF00")
artist4.draw_edges(color="033AD9")
