import bpy
import mathutils

import numpy as np

from .Freed import FreedReceiver


ORI_INTRINSIC = "ZXY" # conventions used here are done to handle blender default camera orientation (toward the ground)
correcrot = np.array([90,180,0])*np.pi/180


def ZYX_to_quat(yaw, pitch, roll):
    yaw*=(np.pi/180)
    pitch*=-(np.pi/180)
    roll*=-(np.pi/180)
    
    cy = np.cos(yaw * 0.5)
    sy = np.sin(yaw * 0.5)
    cp = np.cos(pitch * 0.5)
    sp = np.sin(pitch * 0.5)
    cr = np.cos(roll * 0.5)
    sr = np.sin(roll * 0.5)

    q = np.zeros(4)
    q[0] = cy * cr * cp + sy * sr * sp
    q[1] = sy * cr * cp - cy * sr * sp
    q[2] = cy * sr * cp + sy * cr * sp
    q[3] = cy * cr * sp - sy * sr * cp

    return q


class FreedReferential:
    
    def __init__(self):
        self.position_world = np.zeros(3)
        self.rotation_world = mathutils.Quaternion(np.zeros(4))
        self.zoom  = 0
        self.focus = 0

    def updateCallback(self,data):
        """
            called at each received freed message
        """
        self.position_world[0] = data[0]/1000 # convert to meters
        self.position_world[1] = data[1]/1000
        self.position_world[2] = data[2]/1000
        
        yaw   = -data[3]
        pitch = data[4]
        roll  = data[5]
        
        quat = ZYX_to_quat(yaw, pitch-90, roll)
        quat2 = np.array([quat[3],quat[0],quat[1],quat[2]])
        self.rotation_world = mathutils.Quaternion(quat2)
        
        self.zoom = data[6]
        self.focus = data[7]
        

class ModalOperator(bpy.types.Operator):
    bl_idname = "eztrack_freed.modal_operator"
    bl_label = "Main Loop to Receive FreeD Data"
        
    def initialize(self, context):
        print("Start")
        
        self.n_trackers = 0
        self.tracker_frames = []
        self.receivers = []
        
        self.tracker_ips = []   # add trackers ip here
        self.tracker_ports = [] # add trackers ports here
        self.tracker_objects = [] # add scene objects corresponding to trackers
        
        
        if type(context.scene.freed_receiver_0["target"]) == bpy.types.Object:
            self.tracker_ips.append(context.scene.freed_receiver_0.ip)
            self.tracker_ports.append(int(context.scene.freed_receiver_0.port))
            self.tracker_objects.append(context.scene.freed_receiver_0.target)
            
        if type(context.scene.freed_receiver_1["target"]) == bpy.types.Object:
            self.tracker_ips.append(context.scene.freed_receiver_1.ip)
            self.tracker_ports.append(int(context.scene.freed_receiver_1.port))
            self.tracker_objects.append(context.scene.freed_receiver_1.target)
            
        if type(context.scene.freed_receiver_2["target"]) == bpy.types.Object:
            self.tracker_ips.append(context.scene.freed_receiver_2.ip)
            self.tracker_ports.append(int(context.scene.freed_receiver_2.port))
            self.tracker_objects.append(context.scene.freed_receiver_2.target)
            
        if type(context.scene.freed_receiver_3["target"]) == bpy.types.Object:
            self.tracker_ips.append(context.scene.freed_receiver_3.ip)
            self.tracker_ports.append(int(context.scene.freed_receiver_3.port))
            self.tracker_objects.append(context.scene.freed_receiver_3.target)
            
        
        self.n_trackers = len(self.tracker_ips)
        if self.n_trackers == 0:
            print("no objects targeted, running in the darkness of the void")
        
        for i in range(self.n_trackers):
            self.tracker_frames.append(FreedReferential())
        
            # freed input
            self.receivers.append(FreedReceiver(self.tracker_ips[i], self.tracker_ports[i], self.tracker_frames[i].updateCallback))
            self.receivers[i].start()


    def __del__(self):
        self.stop()
        
        
    def stop(self):
        for i in range(self.n_trackers):
            try:
                self.receivers[i].stop()
            except:
                print("could not close receiver for tracker on port", self.tracker_ports[i])

        print("End")
        

    def execute(self, context):
        # approximately 50 Hz for now. Can go higher if necessary
        
        context.scene.freed.is_running = True
            
        self.initialize(context)
        
        freq = 50 # Hz
        self.timer = context.window_manager.event_timer_add(1/freq, window=context.window)
        return {'FINISHED'}


    def modal(self, context, event): # executed in the event loop, as long as 'RUNNING_MODAL' or 'PASS_THROUGH' has been issued
        
        if event.type == 'ESC' or not context.scene.freed.is_running: # press escape to end 
            self.stop()
            context.scene.freed.is_running = False
            return {'FINISHED'}
        
        elif event.type == 'TIMER': # press escape to end 
            for i in range(self.n_trackers):
                self.tracker_objects[i].location = self.tracker_frames[i].position_world
                
                #quat = CAMERA_POINT_FORWARD_CORRECTION @ self.tracker_frames[i].rotation_world
                quat = self.tracker_frames[i].rotation_world
                self.tracker_objects[i].rotation_mode = 'QUATERNION'
                self.tracker_objects[i].rotation_quaternion = quat
                
                self.tracker_objects[i].keyframe_insert(data_path="rotation_quaternion", frame=context.scene.frame_current)
                self.tracker_objects[i].keyframe_insert(data_path="location", frame=context.scene.frame_current)
            
                
                # try:
                #     bpy.data.cameras[TRACKER_OBJS[i]].angle = np.pi/180 *  self.tracker_frames[i].zoom
                #     bpy.data.cameras[TRACKER_OBJS[i]].dof.focus_distance = self.tracker_frames[i].focus
                # except Exception as e:
                #     print("bound object not a camera : ", e)
                
            
            return {'PASS_THROUGH'}
        
        return {'PASS_THROUGH'}


    def invoke(self, context, event):
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}



def register():
    bpy.utils.register_class(ModalOperator)


def unregister():
    bpy.utils.unregister_class(ModalOperator)
    