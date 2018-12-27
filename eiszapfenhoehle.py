import bpy

import random

import _thread as thread

import time


class Eiszapfen:

    def __init__(self):

        self.x = random.uniform(-4, 4)

        self.y = random.uniform(-4, 4)

        self.drops = 15
        self.drop_counter = self.drops

        self.material = bpy.data.materials.new('eiszapfen_material')
        self.color = (random.uniform(0, .3), random.uniform(0, .3), random.uniform(0.3, 1))

        self.material.diffuse_color = self.color

        self.material.specular_hardness = 200


    def spawn(self):

        self._create_mesh()

        eispickel = Eispickel(self)

        eispickel.spawn()

        Tropfen(self, eispickel).spawn()


    def _create_mesh(self):

        bpy.ops.mesh.primitive_cone_add(location=(self.x, self.y, 4.0))

        bpy.ops.transform.rotate(axis=(0, 0, 0))

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

        bpy.ops.transform.resize(value=(0.7, 0.7, 0.7))

        self.obj = bpy.context.object

        self.obj.name = 'eiszapfen'

        self.obj.data.materials.append(self.material)


    def shrink(self):

        if self.drop_counter <= 0:

            self.obj.hide = True

        else:

            scale_factor = 1 - 1/self.drops

            self.obj.scale[0] *= scale_factor
 
            self.obj.scale[1] *= scale_factor

            self.obj.scale[2] *= scale_factor


class Eispickel:

    def __init__(self, eiszapfen):

        self.eiszapfen = eiszapfen


    def spawn(self):

        self._create_mesh()


    def _create_mesh(self):

        location = (self.eiszapfen.x, self.eiszapfen.y, 1.0)

        bpy.ops.mesh.primitive_cone_add(location=location)

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

        bpy.ops.transform.resize(value=(0.35, 0.35, 0.35))

        self.obj = bpy.context.object

        self.obj.name = 'eispickel'

        self.obj.hide = True

        self.obj.data.materials.append(self.eiszapfen.material)


    def grow(self):

        if self.obj.hide == True:

            self.obj.hide = False

        else:

            #scale_factor = 1.25

            scale_factor = 1 + 1/self.eiszapfen.drops

            self.obj.scale[0] *= scale_factor

            self.obj.scale[1] *= scale_factor

            self.obj.scale[2] *= scale_factor


class Tropfen:

    def __init__(self, eiszapfen, eispickel):

        self.z_initial = 4.3

        self.eiszapfen = eiszapfen

        self.eispickel = eispickel

        self.fall_wait_time = random.uniform(0.025, 0.075)


    def spawn(self):

        self._create_mesh()

        thread.start_new_thread(self._fall, ())


    def _create_mesh(self):

        location = (self.eiszapfen.x, self.eiszapfen.y, self.z_initial)

        bpy.ops.mesh.primitive_ico_sphere_add(location=location)

        bpy.ops.transform.resize(value=(0.2, 0.2, 0.2))

        bpy.ops.object.shade_smooth()

        self.obj = bpy.context.object

        self.obj.name = 'tropfen'

        self.obj.data.materials.append(self.eiszapfen.material)


    def _fall(self):

        if self.eiszapfen.drop_counter <= 0:

            self.obj.hide = True

            return


        self.eiszapfen.drop_counter -= 1

        self.eiszapfen.shrink()


        for i in range(150):

            time.sleep(self.fall_wait_time)

            self.obj.location[2] -= 0.03


        self.obj.location[2] = self.z_initial

        self.eispickel.grow()

        self._fall()



def cleanup():

    for obj in bpy.data.objects:

        obj.hide = False

    bpy.ops.object.select_pattern(pattern="gewoelbe*")

    bpy.ops.object.delete()

    bpy.ops.object.select_pattern(pattern="eiszapfen*")

    bpy.ops.object.delete()

    bpy.ops.object.select_pattern(pattern="tropfen*")

    bpy.ops.object.delete()

    bpy.ops.object.select_pattern(pattern="eispickel*")

    bpy.ops.object.delete()


def create_plane(z, name):

    bpy.ops.mesh.primitive_plane_add(location=(0, 0, z))

    bpy.ops.transform.resize(value=(5, 5, 0))

    obj = bpy.context.object

    obj.name = name

    material = bpy.data.materials.new('gewoelbe_material')

    color = (0.15, 0.20, 0.35)

    material.diffuse_color = color

    material.specular_hardness = 200

    obj.data.materials.append(material)




# main programm

	if bpy.ops.object.mode_set.poll():

   		 bpy.ops.object.mode_set(mode='OBJECT')

		cleanup()

		create_plane(5, 'gewoelbe')

		for i in range(10):

    			Eiszapfen().spawn()
