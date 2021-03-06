import bpy
import math
import sys
import json

sys.path.append("src/tools/")

from create2Dgrid import create2Dgrid
from textobj import textobj
from transform import transform
from clearscreen import clearscreen
from creatematerial import creatematerial

def scatterplot3D(x, y, z, cat, grid_material, number_material):
    """
    ==============
    SCATTERPLOT 3D
    ==============
    A scatterplot in three dimenshion is used to display the relationship between three quantitative variables.
    Arguments :
        x               : The array of quantitative values passed by user. It must be of number data type.
        y               : The array of quantitative values passed by user. It must be of number data type.
        z               : The array of quantitative values passed by user. It must be of number data type.
        cat             : The array of categorical values respected to each value in (x, y, z).  
        grid_material    : The material color for grid in plot. Default color is White.
        number_material  : The material color for numbers in plot. Default color is White.
    Imported User Defined Functions :
        clearscreen     : It will delete everything on the Blender Viewport .
        textobj         : It will create a text object and convert into meshes.
        transform       : This will be used as move function for objects.
        creatematerial  : The materials were created and assigned if not exist.
    """
    
    # 8 colors are declared right now for to use, every material is diffuse material in Blender
    scatter_material = [
        ("red",(1,0,0,1)),("yellow",(1,1,0,1)),("blue",(0,0,1,1)),
        ("green",(0,1,0,1)),("cyan",(0,1,1,1)),("purple",(1,0,1,1)),
        ("magenda",(1,0,0.25,1),("orange",(1,0.25,0,1)))
    ]
    
    # Delete everything on the screen.
    clearscreen()
    
    # Variables used in the function.
    x_y_z_cat = []
    x_y_z_cat.extend([list(a) for a in zip(x, y, z, cat)])
    x_max_val = max(x)
    y_max_val = max(y)
    z_max_val = max(z)
    x_scale = math.ceil(x_max_val/10)
    y_scale = math.ceil(y_max_val/10)
    z_scale = math.ceil(z_max_val/10)
    total = len(x)
    categories = list(set(cat))

    # Adding 3D grid by combining 3 2D grids.
    create2Dgrid(
        grid_name="Y_Z",grid_size=10,grid_pos=(0, 0, 0), 
        grid_rot=(math.radians(0), math.radians(-90), math.radians(0)), 
        x_sub=11, y_sub=11, grid_material=grid_material)
    create2Dgrid(
        grid_name="X_Y",grid_size=10,grid_pos=(0, 0, 0), 
        grid_rot=(math.radians(0), math.radians(0), math.radians(0)), 
        x_sub=11, y_sub=11, grid_material=grid_material)
    create2Dgrid(
        grid_name="Z_X",grid_size=10,grid_pos=(0, 0, 0), 
        grid_rot=(math.radians(90), math.radians(0), math.radians(0)), 
        x_sub=11, y_sub=11, grid_material=grid_material)
    
    # Numbering x-axis, y-axis and z-axis.
    for num in range(11):    
        textobj(
            text=int(num*x_scale), text_type="X_plot", text_pos=(num, -1, 0),
            text_rot=(math.radians(0),math.radians(0) ,math.radians(90)),
            text_scale=(0.4,0.4,0.4), number_material=number_material)
        textobj(
            text=int(num*y_scale), text_type="y_plot", text_pos=(0, num, -1), 
            text_rot=(math.radians(90),math.radians(0) ,math.radians(90)),
            text_scale=(0.4,0.4,0.4), number_material=number_material)
        textobj(
            text=int(num*z_scale), text_type="z_plot", text_pos=(0, -1, num),
            text_rot=(math.radians(90),math.radians(0) ,math.radians(90)),
            text_scale=(0.4,0.4,0.4), number_material=number_material)
    
    # Adding a sphere in the corresponding cartesian position.
    for i in range(len(categories)):
        for itr in range(total):
            if categories[i] == x_y_z_cat[itr][-1]:
                # Creating a sphere.
                bpy.ops.mesh.primitive_uv_sphere_add(
                    segments=6, ring_count=6, radius=0.12, enter_editmode=False, 
                    align='WORLD', location=(x[itr]/x_scale,y[itr]/y_scale,z[itr]/z_scale))
                
                # The Name will be in the format : "Scatter Point: (0,0,0), Cat: Male"
                bpy.context.active_object.name = "Scatter No: (" + str(x[itr]) + ", " + str(y[itr]) + ", " + str(z[itr]) + "), Cat :" + str(categories[i]) 
                
                # The material will be created and applied.
                creatematerial(
                    material_name="ScatterMaterial :" + str(categories[i]),diffuse_color=scatter_material[i][1])
                
                mesh = bpy.context.object.data
                for f in mesh.polygons:
                    f.use_smooth = True
        
    bpy.ops.object.select_all(action = 'DESELECT')
    return

if __name__ == "__main__":
    #Json parsing.
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    argv = json.loads(argv[0])

    scatterplot3D(
        x=argv["x"], y=argv["y"], z=argv["z"], cat=argv["cat"],
        grid_material=argv["grid_material"], number_material=argv["number_material"])