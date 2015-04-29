
import random


# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
    
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    self.has_resource = False


  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  approprioate.)
    if(message == 'order'):
        if(type(details) is tuple):
            x, y = details[0], details[1]
            self.body.go_to((x,y))

        if(details == 's'):
            self.body.stop()
            self.state = 'idle'

        if(details == 'a'):
            self.state = 'attack'

        if(details == 'd'):
            self.state = 'build'

        if(details == 'f'):
            self.state = 'harvest'

    if(self.body.amount <= 0.5):
        self.state = 'flee'

    if(self.state == 'attack'):
        if(message != 'collide' or details['what'] != 'Mantis'):
            if(self.target == None):
                self.target = self.body.find_nearest('Mantis')
                self.body.go_to(self.target)
            self.body.set_alarm(0.2)
            self.target = self.body.find_nearest('Mantis')
            self.body.go_to(self.target)

    if(self.state == 'build'):
        if(message != 'collide' or details['what'] != 'Nest'):
            self.target = self.body.find_nearest('Nest')
            self.body.go_to(self.target)

    if(self.state == 'harvest' and self.has_resource == False):
        if(message != 'collide' or details['what'] != 'Resource'):
            self.target = self.body.find_nearest('Resource')
            self.body.go_to(self.target)

    if(self.state == 'harvest' and self.has_resource == True):
        if(message != 'collide' or details['what'] != 'Nest'):
            self.target = self.body.find_nearest('Nest')
            self.body.go_to(self.target)

    if(self.state == 'flee'):
        if(message != 'collide' or details['what'] != 'Nest'):
            self.target = self.body.find_nearest('Nest')
            self.body.go_to(self.target)

    if (message == 'collide' and details['what'] == 'Mantis' and self.state == 'attack'):
        self.body.stop()
        mantis = details['who']
        mantis.amount -= 0.05
        if(mantis.amount == 0.05):
            self.target = None

    if (message == 'collide' and details['what'] == 'Nest' and self.state == 'build'):
        nest = details['who']
        nest.amount += 0.01
        if(nest.amount >= .99):
            self.target = None
            self.state = 'idle'

    if (message == 'collide' and details['what'] == 'Nest' and self.state == 'harvest'):
        self.has_resource = False

    if (message == 'collide' and details['what'] == 'Nest' and self.state == 'flee'):
        self.body.amount = 1
        self.state = 'idle'
        #slug can never escape because he's slow, set slug speed higher or mantis speed lower to show

    if (message == 'collide' and details['what'] == 'Resource' and self.state == 'harvest' and self.has_resource == False):
        resource = details['who']
        resource.amount -= 0.25
        self.has_resource = True

    pass    

world_specification = {
  'worldgen_seed': 3, # comment-out to randomize 13
  'nests': 2,
  'obstacles': 25,
  'resources': 5,
  'slugs': 5,
  'mantises': 5,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
