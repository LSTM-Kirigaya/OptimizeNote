from re import X
from manimlib import *

def quadratic(u, v, c2p = None):
    x = np.array([[u], [v]])
    Q = np.array([
        [0.5, 0],
        [0, 0.5]
    ])
    triple = [u, v, x.T @ Q @ x]
    return triple

def c2p_quadratic(axe : ThreeDAxes):
    def func(u, v):
        return axe.c2p(*quadratic(u, v))
    return func

class CG1(Scene):
    CONFIG = {
        "camera_class" : ThreeDCamera
    }
    def construct(self):
        frame : CameraFrame = self.camera.frame
        frame.set_euler_angles(
            theta=70 * DEGREES,
            phi=30 * DEGREES,
        )

        self.axes = ThreeDAxes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            z_range=(-4, 4),
            height=6,
            width=6,
            depth=6
        )
        
        init_points = np.array([2,2,0])
        title = TexText("$f(x)=x^TQx, x\in\mathbb R^2$(GD as optimizer)", font_size=30)

        title.fix_in_frame()
        title.move_to(UP * 3.2)
        

        surface = ParametricSurface(
            u_range=(-2.5, 2.5),
            v_range=(-2.5, 2.5),
            uv_func=c2p_quadratic(self.axes),
            color=BLUE_C,
            opacity=0.5
        )

        dot_on_plane = Sphere(color=RED,  radius=DEFAULT_DOT_RADIUS)
        dot_on_surface = Sphere(color=YELLOW, radius=DEFAULT_DOT_RADIUS)
        dot_on_plane.move_to(self.c2p(init_points))
        dot_on_surface.move_to(self.c2p(quadratic(init_points[0], init_points[1])))
        
        # use update to bind
        t = ValueTracker(value=2)

        dot_on_plane.add_updater(self.plane_update(t))
        dot_on_surface.add_updater(self.surface_update(t))

        # create tracepath
        trace_on_plane = TracedPath(
            traced_point_func=dot_on_plane.get_center,
            stroke_color=RED,
            stroke_width=2
        )
        trace_on_surface = TracedPath(
            traced_point_func=dot_on_surface.get_center,
            stroke_color=YELLOW,
            stroke_width=2
        )


        for mob in self.get_mobjects():
            mob.scale(1.5)

        self.play(ShowCreation(trace_on_plane), ShowCreation(trace_on_surface))
        self.play(Write(self.axes))
        self.play(FadeIn(surface))

        self.play(ShowCreation(dot_on_surface), ShowCreation(dot_on_plane))
        self.play(Write(title))
        self.play(t.animate.set_value(0), run_time=3)
    
    def c2p(self, point):
        if isinstance(point, list):
            return self.axes.c2p(*point)
        elif isinstance(point, np.ndarray):
            return self.axes.c2p(*point.tolist())
    
    def plane_update(self, t : ValueTracker):
        def func(dot : Sphere):
            y = x = t.get_value()
            z = 0
            dot.move_to(self.c2p([x, y, z]))
            return dot 
        return func 
    
    def surface_update(self, t : ValueTracker):
        def func(dot : Sphere):
            y = x = t.get_value()
            z = quadratic(x, y)[-1]
            dot.move_to(self.c2p([x, y, z]))
            return dot 
        return func 


class CG2(Scene):
    CONFIG = {
        "camera_class" : ThreeDCamera
    }
    def construct(self):
        frame : CameraFrame = self.camera.frame
        frame.set_euler_angles(
            theta=70 * DEGREES,
            phi=30 * DEGREES,
        )

        self.axes = ThreeDAxes(
            x_range=(-5, 5),
            y_range=(-5, 5),
            z_range=(-4, 4),
            height=6,
            width=6,
            depth=6
        )
        
        init_points = np.array([2,2,0])
        title = TexText("$f(x)=x^TQx, x\in\mathbb R^2$(CG as optimizer)", font_size=30)
        tex1 = Tex("(2,2,f(2,2))")

        title.fix_in_frame()
        title.move_to(UP * 3.2)
        

        surface = ParametricSurface(
            u_range=(-2.5, 2.5),
            v_range=(-2.5, 2.5),
            uv_func=c2p_quadratic(self.axes),
            color=BLUE_C,
            opacity=0.5
        )

        dot_on_plane = Sphere(color=RED,  radius=DEFAULT_DOT_RADIUS)
        dot_on_surface = Sphere(color=YELLOW, radius=DEFAULT_DOT_RADIUS)
        dot_on_plane.move_to(self.c2p(init_points))
        dot_on_surface.move_to(self.c2p(quadratic(init_points[0], init_points[1])))
        
        # use update to bind
        t = ValueTracker(value=2)

        dot_on_plane.add_updater(self.plane_update(t))
        dot_on_surface.add_updater(self.surface_update(t))

        # create tracepath
        trace_on_plane = TracedPath(
            traced_point_func=dot_on_plane.get_center,
            stroke_color=RED,
            stroke_width=2
        )
        trace_on_surface = TracedPath(
            traced_point_func=dot_on_surface.get_center,
            stroke_color=YELLOW,
            stroke_width=2
        )


        for mob in self.get_mobjects():
            mob.scale(1.5)

        self.play(ShowCreation(trace_on_plane), ShowCreation(trace_on_surface))
        self.play(Write(self.axes))
        self.play(FadeIn(surface))

        self.play(ShowCreation(dot_on_surface), ShowCreation(dot_on_plane))
        self.play(Write(title))
        self.play(t.animate.set_value(0), run_time=3)
    
    def c2p(self, point):
        if isinstance(point, list):
            return self.axes.c2p(*point)
        elif isinstance(point, np.ndarray):
            return self.axes.c2p(*point.tolist())
    
    def plane_update(self, t : ValueTracker):
        def func(dot : Sphere):
            tv = t.get_value()
            if tv >= 1:
                x = 2 * (tv - 1)
                y = 2
            else:
                x = 0
                y = 2 * tv  

            z = 0
            dot.move_to(self.c2p([x, y, z]))
            return dot 
        return func 
    
    def surface_update(self, t : ValueTracker):
        def func(dot : Sphere):
            tv = t.get_value()
            if tv >= 1:
                x = 2 * (tv - 1)
                y = 2
            else:
                x = 0
                y = 2 * tv  
            z = quadratic(x, y)[-1]
            dot.move_to(self.c2p([x, y, z]))
            return dot 
        return func 

if __name__ == "__main__":
    from os import system
    system("manimgl {} CG2 -c black -w --hd".format(__file__))