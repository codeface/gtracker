import glib
import gconf

try:
   import gnomekeyring as gk
   keyring = True
except:
   keyring = False

class Config:
   def __init__(self):
      global keyring
      self.username  = None
      self.password  = None
      self.multiline = False
      self.gconf     = gconf.client_get_default()
      self.appname   = "Gtracker"

      self.username_key   = "/apps/gtracker/username"
      self.password_key   = "/apps/gtracker/password"
      self.interval_key   = "/apps/gtracker/interval"
      self.multi_key      = "/apps/gtracker/multiline"

      self.interval = self.gconf.get_int(self.interval_key)
      if self.interval<1:
         self.interval = 15
         self.gconf.set_int(self.interval_key,self.interval)

      self.multiline = self.gconf.get_bool(self.multi_key)
      if self.multiline==None:
         self.multiline = True
         self.gconf.set_bool(self.multi_key,self.multiline)

      if keyring:
         try:
            glib.set_application_name(self.appname)
         except:
            pass
         if gk.is_available():
            names = gk.list_keyring_names_sync()
            try:
               names.index(self.appname)
            except:
               gk.create_sync(self.appname,"login")

            keys = gk.list_item_ids_sync(self.appname)
            if len(keys)==1:
               info = gk.item_get_info_sync(self.appname,keys[0])
               self.username  = info.get_display_name() 
               self.password  = info.get_secret()
            else:
               self.username  = ""
               self.password  = ""
         else:
            keyring = False

      if not keyring:
         self.username = self.gconf.get_string(self.username_key)
         if self.username==None or len(self.username)<1:
            self.username = ""
            self.gconf.set_string(self.username_key,"")

         self.password = self.gconf.get_string(self.password_key)
         if self.password==None or len(self.password)<1:
            self.password = ""
            self.gconf.set_string(self.password_key,self.password)
      else:
         self.gconf.unset(self.username_key)
         self.gconf.unset(self.password_key)

   def save(self,username,password,interval,multi=True):
      try:
         self.gconf.set_int(self.interval_key,interval)
         self.gconf.set_bool(self.multi_key,multi)
         self.multiline = multi

         if not keyring:
            self.gconf.set_string(self.username_key,username)
            self.gconf.set_string(self.password_key,password)
         else:
            keys = gk.list_item_ids_sync(self.appname)
            if len(keys)>0:
               for key in keys:
                  gk.item_delete_sync(self.appname,2L)
            gk.item_create_sync(self.appname,gk.ITEM_GENERIC_SECRET,username,{"username":username},password,True)
      except Exception as exc:
         return False
      return True
