import vpython as vp
scene = vp.canvas(title="3 Body System with COM", width=1600, height=700, range=100e6)
#Gravitational constant
G = 6.674e-11

#Define planet properties
Venus = vp.sphere(color=vp.color.yellow, make_trail=True)
Venus.pos = vp.vector(50e6, 0, 0)
Venus.radius = 6.051e6
Venus.mass = 4.8675e24
Venus.F = vp.vector(0, 0, 0)
Venus.F_arrow = vp.arrow(color=vp.color.green, shaftwidth=0.5e6) #net force
Venus.v = vp.vector(1e3, 1e3, -1e3)
Venus.v_arrow = vp.arrow(color=vp.color.red, shaftwidth=0.5e6) #velocity vector
Venus.p = Venus.v * Venus.mass #momentum

Earth = vp.sphere(color=vp.color.blue, make_trail=True)
Earth.pos = vp.vector(-50e6, 0, 0)
Earth.radius = 6.378e6
Earth.mass = 5.9735e24
Earth.F = vp.vector(0, 0, 0)
Earth.F_arrow = vp.arrow(color=vp.color.green, shaftwidth=0.5e6)
Earth.v = vp.vector(1e3, -1e3, 0)
Earth.v_arrow = vp.arrow(color=vp.color.red, shaftwidth=0.5e6)
Earth.p = Earth.v * Earth.mass

Mars = vp.sphere(color=vp.color.red, make_trail=True)
Mars.pos = vp.vector(0, 86e6, 0)
Mars.radius = 1.794e6
Mars.mass = 6.417e24
Mars.F = vp.vector(0, 0, 0)
Mars.F_arrow = vp.arrow(color=vp.color.green, shaftwidth=0.5e6)
Mars.v = vp.vector(-2e3, 1e3, 1e3)
Mars.v_arrow = vp.arrow(color=vp.color.red, shaftwidth=0.5e6)
Mars.p = Mars.v * Mars.mass

#Sphere for center of mass
com = vp.sphere(radius=2e6, color=vp.color.cyan, make_trail=True)

PlanetList = [Earth, Venus, Mars]

dt = 1e3
while len(PlanetList) > 1:

    vp.rate(50)

    for i in PlanetList:

        i.F = vp.vector(0, 0, 0)

        for j in PlanetList:
            if i != j:

                r = i.pos - j.pos

                if vp.mag(r) > i.radius + j.radius:
                    F = -G * i.mass * j.mass * r.hat / vp.mag(r) ** 2
                    i.F += F
                    i.p += F * dt
                    i.v = i.p / i.mass

                # combine masses if collision occurs
                else:
                    j.pos = (i.pos * i.mass + j.pos * j.mass) / (i.mass + j.mass)
                    j.mass = i.mass + j.mass
                    j.p = i.p + j.p
                    j.radius = i.radius + j.radius

                    i.visible = False
                    i.F_arrow.visible = False
                    i.v_arrow.visible = False

                    PlanetList.remove(i)
    for i in PlanetList:

        i.pos = i.pos + i.p / i.mass * dt

        i.F_arrow.pos = i.pos
        i.F_arrow.axis = i.F/5e16 #scaling so that arrow shows up properly

        i.v_arrow.pos = i.pos
        i.v_arrow.axis = i.v * 1e4

    #Define center of mass
    weighted_pos = vp.vector(0, 0, 0)
    total_mass = 0

    for a in PlanetList:
        weighted_pos += a.pos * a.mass
        total_mass += a.mass
    com.pos = weighted_pos / total_mass
    scene.center = com.pos #animation will focus on com

# ####Explicit code for force arrows
# #Direction of forces from Earth onto other planets
# r_Earth_Venus = Earth.pos - Venus.pos
# force_Venus_Earth = -G * Earth.mass * Venus.mass * r_Earth_Venus.hat / vp.mag(r_Earth_Venus)**2
# vp.arrow(pos=Earth.pos, axis=force_Venus_Earth/1e16, color=vp.color.red, shaftwidth=0.5e6)
#
# r_Earth_Mars = Earth.pos - Mars.pos
# force_Mars_Earth = -G * Earth.mass * Mars.mass * r_Earth_Mars.hat / vp.mag(r_Earth_Mars)**2
# vp.arrow(pos=Earth.pos, axis=force_Mars_Earth/1e16, color=vp.color.red, shaftwidth=0.5e6)
#
# #Earth net force
# Earth.F = force_Venus_Earth + force_Mars_Earth
# vp.arrow(pos=Earth.pos, axis=Earth.F/1e16, color=vp.color.green, shaftwidth=0.5e6)
#
# #Direction of forces from Venus onto other planets
# r_Venus_Mars = Venus.pos - Mars.pos
# force_Mars_Venus = -G * Venus.mass * Mars.mass * r_Venus_Mars.hat / vp.mag(r_Venus_Mars)**2
# vp.arrow(pos=Venus.pos, axis=force_Mars_Venus/1e16, color=vp.color.red, shaftwidth=0.5e6)
#
# r_Venus_Earth = Venus.pos - Earth.pos
# force_Earth_Venus = -G * Venus.mass * Earth.mass * r_Venus_Earth.hat / vp.mag(r_Venus_Earth)**2
# vp.arrow(pos=Venus.pos, axis=force_Earth_Venus/1e16, color=vp.color.red, shaftwidth=0.5e6)
#
# #Venus net force
# Venus.F = force_Mars_Venus + force_Earth_Venus
# vp.arrow(pos=Venus.pos, axis=Venus.F/1e16, color=vp.color.green, shaftwidth=0.5e6)
#
# #Direction of forces from Venus onto other planets
# r_Mars_Earth = Mars.pos - Earth.pos
# force_Earth_Mars = -G * Mars.mass * Earth.mass * r_Mars_Earth.hat / vp.mag(r_Mars_Earth)**2
# vp.arrow(pos=Mars.pos, axis=force_Earth_Mars/1e16, color=vp.color.red, shaftwidth=0.5e6)
#
# r_Mars_Venus = Mars.pos - Venus.pos
# force_Venus_Mars = -G * Mars.mass * Venus.mass * r_Mars_Venus.hat / vp.mag(r_Mars_Venus)**2
# vp.arrow(pos=Mars.pos, axis=force_Venus_Mars/1e16, color=vp.color.red, shaftwidth=0.5e6)
#
# #Mars net force
# Mars.F = force_Earth_Mars + force_Venus_Mars
# vp.arrow(pos=Mars.pos, axis=Mars.F/1e16, color=vp.color.green, shaftwidth=0.5e6)


