from transitions import Machine
# from transitions.extensions import GraphMachine as Machine
class Matter:
    def hiss(self):
        print("Ssssss!")

    def vanish(self):
        print("It disappeared!")

stuff = Matter()

states = ['solid', 'liquid', 'gas', 'plasma']
transitions = [
    {'trigger': 'melt', 'source': 'solid', 'dest': 'liquid', 'before': 'hiss'},
    {'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas', 'after': 'vanish'},
    {'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas'},
    {'trigger': 'freeze', 'source': 'liquid', 'dest': 'solid'},
    {'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma'}]

machine = Machine(stuff, states=states, transitions=transitions,
                  initial='liquid', auto_transitions=False)

# stuff.graph.draw('graph.png', prog='dot')
