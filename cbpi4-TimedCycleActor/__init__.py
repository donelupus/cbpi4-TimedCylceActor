import importlib

timed_cycle_actor = importlib.import_module("cbpi4-TimedCycleActor.timed_cycle_actor")

def setup(cbpi):
    '''
    This method is called by the server during startup
    Here you need to register your plugins at the server
    :param cbpi: the cbpi core
    '''
    cbpi.plugin.register("Timed Cycle Actor", timed_cycle_actor.TimedCycleActor)
    pass