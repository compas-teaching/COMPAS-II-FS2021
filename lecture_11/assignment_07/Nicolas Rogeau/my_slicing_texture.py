from compas_slicer.geometry import Path
from compas_slicer.utilities.utils import get_normal_of_path_on_xy_plane
from compas.geometry import Point
from compas.geometry import scale_vector, add_vectors

def create_dovetail_texture(slicer, dovetail_distance):
    """Creates an amazingly cool overhang texture"""

    print("Creating amazingly cool texture")

    #for every path in every layer
    for i, layer in enumerate(slicer.layers):
        if i % 2 == 0 and i > 0:
            # for every 2nd layer, except for the first layer
            for j, path in enumerate(layer.paths):
                # create an empty layer in which we can store our modified points
                new_path = []
                points = path.points
                for k in range(len(points)): 
                    # Take the third point in each group of five points (quintuplet)
                    if k % 5 == 2 and k < len(points)-3:
                        # get the normal of the first and last point of the quintuplet in relation to the mesh
                        normal_pt1 = get_normal_of_path_on_xy_plane(k-2, points[k-2], path, mesh=None)
                        normal_pt5 = get_normal_of_path_on_xy_plane(k+2, points[k+2], path, mesh=None)
                        # scale both vectors in function of the layer to move the point
                        normal_pt1_scaled = scale_vector(normal_pt1, -dovetail_distance/((i%5)+1))
                        normal_pt5_scaled = scale_vector(normal_pt5, -dovetail_distance/((i%5)+1))
                        # create two new points by adding points and normal vectors
                        new_pt_3A = add_vectors(points[k-2], normal_pt1_scaled)
                        new_pt_3B = add_vectors(points[k+2], normal_pt5_scaled)
                        # recreate the new_pt values as compas_points
                        pt_3A = Point(new_pt_3A[0], new_pt_3A[1], new_pt_3A[2])
                        pt_3B = Point(new_pt_3B[0], new_pt_3B[1], new_pt_3B[2])
                        # append both points to the new path
                        new_path.append(pt_3A)
                        new_path.append(pt_3B)
                    # the other points stay the same
                    else:
                        new_path.append(points[k])
                # replace the current path with the new path that we just created
                layer.paths[j] = Path(new_path, is_closed=path.is_closed)
