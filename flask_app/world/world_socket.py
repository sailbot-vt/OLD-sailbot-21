from flask_socketio import Namespace, emit


class WorldSocket(Namespace):

    def __init__(self, world, Namespace=None):
        super().__init__(Namespace)
        self.world = world

    def true_wind_speed(self):
        return self.world.wind.true_wind().distance()

    def true_wind_angle(self):
        return self.world.wind.true_wind().angle()

    def apparent_wind_speed(self):
        return self.world.wind.apparent_wind().distance()
        
    def apparent_wind_angle(self):
        return self.world.wind.apparent_wind().angle()
    