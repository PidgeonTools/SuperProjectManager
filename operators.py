import bpy
import os

from .functions.main_functions import (
    sn_handle_script_line_exception,
    build_folder
)


class BLENDER_PROJECT_STARTER_OT_Build_Project(bpy.types.Operator):
    bl_idname = "blender_project_starter.build_project"
    bl_label = "Build Project"
    bl_description = "Build Project Operator "
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            if "Automatic Setup" == bpy.context.scene.project_setup:
                prefs = context.preferences.addons[__package__].preferences

                build_folder(context, prefs.folder_save1)

                if prefs.folder_save2:
                    build_folder(context, prefs.folder_save2)

                if prefs.folder_save3:
                    build_folder(context, prefs.folder_save3)

                if prefs.folder_save4:
                    build_folder(context, prefs.folder_save4)

                if prefs.folder_save5:
                    build_folder(context, prefs.folder_save5)



            else:
                scene = bpy.context.scene

                build_folder(context, scene.folder_1)

                if scene.folder_2:
                    build_folder(context, scene.folder_2)

                if scene.folder_3:
                    build_folder(context, scene.folder_3)

                if scene.folder_4:
                    build_folder(context, scene.folder_4)

                if scene.folder_5:
                    build_folder(context, scene.folder_5)


            if bpy.context.scene.save_blender_file:
                bpy.ops.wm.save_as_mainfile(filepath=(os.path.join(bpy.path.abspath(os.path.join(bpy.context.scene.project_location,bpy.context.scene.project_name)), bpy.context.scene.save_file_name) + "_v001.blend"), filter_btx=True, compress=bpy.context.scene.compress_save, relative_remap= bpy.context.scene.remap_relative)

            if bpy.context.scene.open_directory:
                try:
                    OpenLocation =  bpy.path.abspath(os.path.join(bpy.context.scene.project_location,bpy.context.scene.project_name))
                except Exception as exc:
                    sn_handle_script_line_exception(exc, ("OpenLocation =  '" + bpy.path.abspath(os.path.join(bpy.context.scene.project_location,bpy.context.scene.project_name))))

                try: 
                    OpenLocation = os.path.realpath(OpenLocation)

                except Exception as exc:
                    sn_handle_script_line_exception(exc, "OpenLocation = os.path.realpath(OpenLocation)")

                try:
                    os.startfile(OpenLocation)
                except Exception as exc:
                    sn_handle_script_line_exception(exc, "os.startfile(OpenLocation)")


        except Exception as exc:
            print(str(exc) + " | Error in execute function of Build Project")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Build Project")
        return self.execute(context)

def register():
    bpy.utils.register_class(BLENDER_PROJECT_STARTER_OT_Build_Project)


def unregister():
    bpy.utils.unregister_class(BLENDER_PROJECT_STARTER_OT_Build_Project)
