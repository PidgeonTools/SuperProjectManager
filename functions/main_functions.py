import bpy
from bpy.utils import previews
import os
import math


def build_folder(context, prop):
    try:
        path = os.path.join(bpy.path.abspath(bpy.context.scene.project_location), bpy.context.scene.project_name, prop)

    except Exception as exc:
        sn_handle_script_line_exception(exc, ("path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location, bpy.context.scene.project_name), prop))))

    try:
        os.makedirs(path)
    except Exception as exc:
        sn_handle_script_line_exception(exc, "os.makedirs(path)")


def sn_print(tree_name, *args):
    if tree_name in bpy.data.node_groups:
        item = bpy.data.node_groups[tree_name].sn_graphs[0].prints.add()
        for arg in args:
            item.value += str(arg) + ";;;"
        for area in bpy.context.screen.areas:
            area.tag_redraw()
    print(*args)


def sn_handle_script_line_exception(exc, line):
    print("# # # # # # # # SCRIPT LINE ERROR # # # # # # # #")
    print("Line:", line)
    raise exc
