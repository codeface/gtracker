from state import *
import gettext

_ = gettext.gettext

class Story:
   def __init__(self,proj_id,id,name,state,owner,points=0,menu_item=None):
      self.proj_id   = proj_id
      self.id        = id
      self.name      = name
      self.state     = state
      self.owner     = owner
      self.points    = points
      self.tasks     = []
      self.menu_item = menu_item

   def __str__(self):
      state_info  = States.get_state(self.state)
      next_state  = States.get_state(state_info.next_states[0])
      points      = _("Unestimated") if int(self.points)<0 else ("%s points" % self.points)
      if len(self.tasks)>0:
         return _("%s: %s (%s) (%s) (%d tasks)") % (next_state.verb,self.name,points,self.owner,len(self.tasks))
      else:
         return _("%s: %s (%s) (%s)") % (next_state.verb,self.name,points,self.owner)

   def remove_task(self,task):
      found = None
      for t in self.tasks:
         if task.id==t.id:
            found = t
            break
      if found==None:
         return False
      self.tasks.remove(t)
      return True
