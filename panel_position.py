from Image import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from wx.glcanvas import GLCanvas
import wx



class PositionCanvas(GLCanvas):

	def __init__(self, parent, cartographer):
		GLCanvas.__init__(self, parent, -1, attribList=[wx.glcanvas.WX_GL_DOUBLEBUFFER])
		self.init = False
		glutInit(sys.argv)
		self.cartographer = cartographer
		self.posx = 0
		self.posy = 0
		self.posz = 0
		
		self.earthx = 0
		self.earthy = 0
		self.earthz = 0

		self.size = None
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.x = 0
		self.y = 0
		self.z = 0
		self.lastx = 0
		self.lasty = 0
		self.lastz = 0
		self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
		self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseDown)
		self.Bind(wx.EVT_RIGHT_UP, self.OnMouseUp)
		self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
		self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
		self.view_distance = -10.0
		
		self.earth_size = 2.0



	
	def InitGL(self):
		self.init = True
		self.load_textures()
		glEnable(GL_TEXTURE_2D)
		glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
		glClearDepth(1.0)                   # Enables Clearing Of The Depth Buffer
		glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
		glEnable(GL_DEPTH_TEST)             # Enables Depth Testing
		glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()                    # Reset The Projection Matrix
		width, height = self.GetClientSize()
		gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW)
		glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
		glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
		glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 2.0, 1.0))
		glEnable(GL_LIGHT0)


	def load_textures(self):

		image = open("textures/earth_grid.jpg")
		ix = image.size[0]
		iy = image.size[1]
		image = image.tostring("raw", "RGBX", 0, -1)
		self.earth_texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.earth_texture)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	
		self.earth_quad = gluNewQuadric()
		gluQuadricNormals(self.earth_quad, GLU_SMOOTH)
		gluQuadricTexture(self.earth_quad, GL_TRUE)

		image2 = open("textures/plain_texture.png")
		ix = image2.size[0]
		iy = image2.size[1]
		image2 = image2.tostring("raw", "RGBX", 0, -1)
		self.plain_texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.plain_texture)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image2)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	
		self.plain_quad = gluNewQuadric()
		gluQuadricNormals(self.plain_quad, GLU_SMOOTH)
		gluQuadricTexture(self.plain_quad, GL_TRUE)

	def OnSize(self, event):
		size = self.size = self.GetClientSize()
		glViewport(0, 0, size[0], size[1])
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45.0, float(size[0]) / float(size[1]), 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW)


	def OnPaint(self, event):
		self.SetCurrent()
		if not self.init:
			self.InitGL()

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		glTranslatef(0.0, 0.0, self.view_distance)
		glRotatef(self.posy, 1.0, 0.0, 0.0)
		glRotatef(self.posx, 0.0, 0.0, 1.0)
		glRotatef(self.posz, 0.0, 1.0, 0.0)
		
		glPushMatrix()
		glRotatef(self.earthy, 1.0, 0.0, 0.0)
		glRotatef(self.earthx, 0.0, 0.0, 1.0)
		glRotatef(self.earthz, 0.0, 1.0, 0.0)
		glBindTexture(GL_TEXTURE_2D, self.earth_texture)
		gluSphere(self.earth_quad, self.earth_size, 32, 32)
		glPopMatrix();
		
		if self.cartographer.projection_panel.projection.projection_type == self.cartographer.projection_panel.projection.ProjectionType.Cylindric or self.cartographer.projection_panel.projection.projection_type == self.cartographer.projection_panel.projection.ProjectionType.PseudoCylindric:
			glPushMatrix()
			glTranslatef(0.0, 0.0, -self.earth_size*1.5)
			glEnable(GL_BLEND)
			glBlendFunc(GL_SRC_ALPHA,GL_ONE)			
			glColor4f(1.0, 1.0, 1.0, 0.5)
			glBindTexture(GL_TEXTURE_2D, self.plain_texture)
			gluCylinder(self.plain_quad, self.earth_size*1.01, self.earth_size*1.01, self.earth_size * 3, 32, 64)
			glDisable(GL_BLEND)
			glLineWidth(5.0)
			glColor3f(0.0, 0.8, 0.0)
			glBegin(GL_LINES)
			glVertex3f(0.0, 0.0, self.earth_size)
			glVertex3f(50.0, 50.0, 50.0)
			glEnd()
			glPopMatrix()
		elif self.cartographer.projection_panel.projection.projection_type == self.cartographer.projection_panel.projection.ProjectionType.Conic:
			glPushMatrix()
			glTranslatef(0.0, 0.0, -self.earth_size)
			glEnable(GL_BLEND)
			glBlendFunc(GL_SRC_ALPHA,GL_ONE)
			glColor4f(1.0, 1.0, 1.0, 0.5)
			glBindTexture(GL_TEXTURE_2D, self.plain_texture)
			gluCylinder(self.plain_quad, self.earth_size*2, 0, self.earth_size * 3, 32, 64)
			glDisable(GL_BLEND)
			glPopMatrix()

		elif self.cartographer.projection_panel.projection.projection_type == self.cartographer.projection_panel.projection.ProjectionType.Azimuthal:
			glPushMatrix()
			glTranslatef(0.0, 0.0, -self.earth_size)
			glEnable(GL_BLEND)
			glBlendFunc(GL_SRC_ALPHA,GL_ONE)			# Set The Blending Function For Translucency
			glColor4f(1.0, 1.0, 1.0, 0.5)
			glBindTexture(GL_TEXTURE_2D, self.plain_texture)
			gluDisk(self.plain_quad, 0, self.earth_size * 2, 32, 64)
			glDisable(GL_BLEND)
			glPopMatrix()
			
		self.SwapBuffers()
	
	def set_earth_coordinates(self, x, y, z):
		self.earthx = x
		self.earthy = y
		self.earthz = z

	def OnMouseDown(self, evt):
		self.CaptureMouse()
		self.x, self.y = self.lastx, self.lasty = evt.GetPosition()
		self.z = self.lastz = self.y

	def OnMouseUp(self, evt):
		self.ReleaseMouse()
		
	def OnMouseWheel(self, evt):

		print "vd=" + str(self.view_distance) + " wr=" + str(evt.GetWheelRotation()) 
		if evt.GetWheelRotation() < 0 and self.view_distance > -50:
			self.view_distance += self.view_distance/10
		elif evt.GetWheelRotation() > 0 and self.view_distance < -4:
			self.view_distance -= self.view_distance/10
		
		self.Refresh()

	def OnMouseMotion(self, evt):
		if evt.Dragging() and (evt.LeftIsDown() or evt.RightIsDown()):
			self.x, self.y = evt.GetPosition()
			
			if evt.RightIsDown():
				self.z = self.y
				self.posz += self.z - self.lastz
				self.lastz = self.z
			else:
				self.posx -= self.x - self.lastx
				self.posy += self.y - self.lasty
				self.lastx = self.x
				self.lasty = self.y

			self.Refresh()

	

if __name__ == '__main__':

	app = wx.App()
	frame = wx.Frame(None, -1, 'test', wx.DefaultPosition, wx.Size(400, 400))
	panel = PositionCanvas(frame, None)

	frame.Show()
	app.MainLoop()
