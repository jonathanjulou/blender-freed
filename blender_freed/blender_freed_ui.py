# https://blender.stackexchange.com/questions/57306/how-to-create-a-custom-ui

import bpy

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty,
                       FloatVectorProperty, EnumProperty, PointerProperty, CollectionProperty)
                       
from bpy.types import Panel, Menu, Operator, PropertyGroup
                 
                 
# all classes defined in this file            
CLASSES = []




# ========================================================== Scene Properties


class FreedReceiverProperties(PropertyGroup):
    ip: StringProperty(
        name = "IP",
        description="receiver ip",
        default = "0.0.0.0",
        )
    
    port: StringProperty(
        name = "Port",
        description="receiver port",
        default = "5000",
        )
        
    target: PointerProperty(
        name = "Target",
        description = "object linked to the freed receiver",
        type = bpy.types.Object
        )
CLASSES.append(FreedReceiverProperties)




class SceneProperties(PropertyGroup):
    is_running: BoolProperty(
        name="Is Running",
        description="Are freed receivers already running ?",
        default = False
        )
CLASSES.append(SceneProperties)




# ========================================================== Operators


class StartOp(Operator):
    bl_label = "Start Receiving Operator"
    bl_idname = "eztrack_freed.start_op"
    bl_description = "Start receiving FreeD data"

    def execute(self, context):
        scene = context.scene
        freed = scene.freed

        print("starting freed receiving...")
        
        while not freed.is_running:
            bpy.ops.eztrack_freed.modal_operator('INVOKE_DEFAULT')
        
        return {'FINISHED'}
CLASSES.append(StartOp)


class StopOp(Operator):
    bl_label = "Stop Receiving Operator"
    bl_idname = "eztrack_freed.stop_op"
    bl_description = "Stop receiving FreeD data"

    def execute(self, context):
        scene = context.scene
        freed = scene.freed

        print("stopping freed receiving...")
        
        freed.is_running = False
        
        return {'FINISHED'}
CLASSES.append(StopOp)

    
    
    
# ========================================================== Menus


class BlenderFreedUi(bpy.types.Panel):
    bl_label = "Freed"
    bl_idname = "eztrack_freed.ui"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        
        layout.operator("eztrack_freed.start_op", text="Start")
        layout.operator("eztrack_freed.stop_op", text="Stop")
CLASSES.append(BlenderFreedUi)


class FreedReceiverUi_0(bpy.types.Panel):
    bl_label = "Freed Receiver 0"
    bl_parent_id = "eztrack_freed.ui"
    bl_idname = "eztrack_freed.freed_receiver_ui"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        self.layout.prop(context.scene.freed_receiver_0, "ip")
        self.layout.prop(context.scene.freed_receiver_0, "port")
        self.layout.prop(context.scene.freed_receiver_0, "target")
CLASSES.append(FreedReceiverUi_0)


class FreedReceiverUi_1(bpy.types.Panel):
    bl_label = "Freed Receiver 1"
    bl_parent_id = "eztrack_freed.ui"
    bl_idname = "eztrack_freed.freed_receiver_ui_1"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        self.layout.prop(context.scene.freed_receiver_1, "ip")
        self.layout.prop(context.scene.freed_receiver_1, "port")
        self.layout.prop(context.scene.freed_receiver_1, "target")
CLASSES.append(FreedReceiverUi_1)


class FreedReceiverUi_2(bpy.types.Panel):
    bl_label = "Freed Receiver 2"
    bl_parent_id = "eztrack_freed.ui"
    bl_idname = "eztrack_freed.freed_receiver_ui_2"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        self.layout.prop(context.scene.freed_receiver_2, "ip")
        self.layout.prop(context.scene.freed_receiver_2, "port")
        self.layout.prop(context.scene.freed_receiver_2, "target")
CLASSES.append(FreedReceiverUi_2)


class FreedReceiverUi_3(bpy.types.Panel):
    bl_label = "Freed Receiver 3"
    bl_parent_id = "eztrack_freed.ui"
    bl_idname = "eztrack_freed.freed_receiver_ui_3"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        self.layout.prop(context.scene.freed_receiver_3, "ip")
        self.layout.prop(context.scene.freed_receiver_3, "port")
        self.layout.prop(context.scene.freed_receiver_3, "target")
CLASSES.append(FreedReceiverUi_3)

        
        


# ========================================================== Registration


def register():
    # register all new classes
    for new_class in CLASSES:
        bpy.utils.register_class(new_class)
    
    # instantiate our custom properties in the "freed" scene property
    bpy.types.Scene.freed = PointerProperty(type=SceneProperties)
    bpy.types.Scene.freed_receiver_0 = PointerProperty(type=FreedReceiverProperties)
    bpy.types.Scene.freed_receiver_1 = PointerProperty(type=FreedReceiverProperties)
    bpy.types.Scene.freed_receiver_2 = PointerProperty(type=FreedReceiverProperties)
    bpy.types.Scene.freed_receiver_3 = PointerProperty(type=FreedReceiverProperties)


def unregister():
    # remove all new classes
    for class_to_remove in reversed(CLASSES):
        bpy.utils.unregister_class(class_to_remove)
    
    # throw our custom properties into the darkness of memory freeing oblivion
    del bpy.types.Scene.freed



if __name__ == "__main__":
    register()