from math import pi

import matrix

def reload_bones_imports():
    reload(matrix)
    
class Joint:
    origin = matrix.Vector(0, 0)
    # Joints hold position and transformation relative to the root
    # This is considered ABSOLUTE
    def __init__(self, bone_in):
        self.bone_in = bone_in
        self.bones_out = []
        self.transform = matrix.Identity()
        self.position = matrix.Vector(0, 0)        

    def __repr__(self):
        return "Joint:\n\tPos: " + str(self.position) + \
            "\n\tTransform:\n" + str(self.transform) + \
            "\n----------------------------"

    def calc_position(self):
        # You probably want to call calc_transform first!
        self.position = self.origin * self.transform

    def calc_skeleton(self):
        self.calc_position()
        for bone in self.bones_out:
            bone.calc_transform()
            bone.end.transform = bone.transform * self.transform
            bone.end.calc_skeleton()

class Root(Joint):
    def __init__(self):
        Joint.__init__(self, None)
        
class Bone:
    # Bones hold transformation information from start to end
    # This is considered RELATIVE
    def __init__(self, start_joint):
        self.start = start_joint
        self.start.bones_out.append(self)
        self.end = Joint(self)
        self.end.bone_in = self
        self.rotation = 0
        self.length = 1
        self.transform = matrix.Identity()
        
    def __repr__(self):
        return "Bone:\nlength: %f\nrotation: %f\n"%(self.length, 
                                                    self.rotation) + \
                                                    str(self.transform)
    def calc_transform(self):
        self.transform = \
                       matrix.Translation(matrix.Vector(0, self.length)) * \
                       matrix.Rotation(self.rotation)

    def set_absolute_rotation(self, rot):
        """Sets rotation in the origin/root reference frame"""
        self.rotation = rot
        bone = self.start.bone_in
        while bone:
            self.rotation -= bone.rotation
            bone = bone.start.bone_in

    def delete(self):
        self.end.bone_in = None
        for bone in self.end.bones_out:
            bone.delete()
        self.end.bones_out = []
        self.start.bones_out.remove(self)
        
def print_skeleton(root):
    print root
    for bone in root.bones_out:
        print bone
        print_skeleton(bone.end)

def test():
    root = Root()
    b1 = Bone(root)
    b1.length = 50
    b1.rotation = pi / 2
    
    b2 = Bone(b1.end)
    b2.length = 100
    b2.rotation = 0

    print_skeleton(root)
    root.calc_skeleton()
    print "---"
    print_skeleton(root)

    
        
