import main

def toss():
   isToss = main.shm.get(main.ShmVariable.isToss)
   serveMode = main.shm.get(main.ShmVariable.serveMode)
   if not isToss:
      # main.shm.set(main.ShmVariable.isToss, True)
      if serveMode == 1:
         main.normal.toss()
      elif serveMode == 2:
         main.advanced.toss()
      elif serveMode == 3:
         main.skill.toss()
         
def serve():
   isServe = main.shm.get(main.ShmVariable.isServe)
   serveMode = main.shm.get(main.ShmVariable.serveMode)
   if not isServe:
      main.shm.set(main.ShmVariable.isServe, True)
      if serveMode == 1:
         main.normal.start()
      elif serveMode == 2:
         main.advanced.start()
      elif serveMode == 3:
         main.skill.start()
      main.shm.set(main.ShmVariable.isToss, False)
      main.shm.set(main.ShmVariable.isServe, False)
      main.shm.set(main.ShmVariable.isServing, False)