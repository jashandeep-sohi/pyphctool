import os
import glob
import time
import multiprocessing as mp
import subprocess as sp

def findvids(cpuType):
 #Check if root
 if os.getuid() != 0: raise Exception('Need root permission.')
 
 #Create Cpu objects
 cpus = [Cpu(path) for path in glob.glob('/sys/devices/system/cpu/cpu?')]
 if len(cpus) == 0: raise Exception('Something serious is wrong. Someone fix this script now!')
 cpu0 = cpus[0]
 availFreqs = cpu0.getAvailableFreqs()
 currentVids = cpu0.getCurrentVids()
 
 #Check for the userspace scaling governor. If not available load it.
 if 'userspace' not in cpu0.getAvailableGovs(): loadModule('cpufreq_userspace')
 
 #Save settings for each CPU, so that we can restore it later.
 preSettings = [(cpu.getCurrentVids(), cpu.getCurrentFreq(), cpu.getCurrentGov(), cpu.getMinMaxFreq()) for cpu in cpus]
 
 #Load previously tested freqs, if any.
 try: 
  with open('./passedvids.temp', 'r') as f: testedfreqs = [int(freqvid.split(':')[0]) for freqvid in f.read().split()]
 except: testedfreqs = []
 
 #Begin messing with stuff.
 try:
  for n, freq in enumerate(availFreqs):
   if freq in testedfreqs: continue
   print('\nAvailable frequencies:', availFreqs)
   print('Testing frequency:', freq)
   print('Current VIDs:', currentVids)
   
   #Put each CPU in the correct state.
   for cpu in cpus:
    cpu.setCurrentGov('userspace')
    cpu.setMinMaxFreq(availFreqs[-1], availFreqs[0])
    cpu.setCurrentFreq(freq)
   
   #Read previously found freq:vid pairs, if any
   try:
    with open('./passedvids.temp', 'r') as fr: prevFoundVids = fr.read()
    for prevFoundVid in prevFoundVids.split():
     tfreq, tvid = map(int,prevFoundVid.split(':'))
     tfreqIndex = availFreqs.index(tfreq)
     currentVids[tfreqIndex] = tvid
   except: prevFoundVids = str()
   
   #Start stressing
   nStressors = len(cpus) * 10
   stressorPool = mp.Pool(processes=nStressors)
   stressorPool.map_async(stressor, range(nStressors))
   
   try:
    newVids = currentVids[:]
    while(True):
     print('\nStressing with VIDs:',newVids)  
     
     #Change vids
     for cpu in cpus: cpu.setCurrentVids(newVids)
     
     for j in reversed(range(1,31)):
      print('\rWait '+str(j)+' seconds...', end='')
      time.sleep(1)
     
     #Passed stress, so write new vids
     with open('./passedvids.temp', 'w') as fw:
      fw.write(prevFoundVids)
      fw.write(str(freq)+':'+str(newVids[n])+'\n') 
      
     if cpuType == 'amd':
      newVids[n] = newVids[n] + 1
      if newVids[n] > 200: break
     else:
      newVids[n] = newVids[n] - 1
      if newVids[n] < 0: break
      
   except KeyboardInterrupt: continue
   finally:
    stressorPool.terminate()
    testedfreqs.append(freq) 
 finally:
  #Restore Everything
  for cpu, preSetting in zip(cpus, preSettings):
   cpu.setCurrentVids(preSetting[0])
   cpu.setMinMaxFreq(preSetting[3][0], preSetting[3][1])
   cpu.setCurrentFreq(preSetting[1])
   cpu.setCurrentGov(preSetting[2])
 print('\n\nCheck file "passedvids.temp" for safe VIDS.')
 print('Keep in mind that these VIDS are one away from a system crash,')
 print('so for peace of mind adjust these depending on how much of a')
 print('risk taker you are.')

#Set the vids at confFileloc
def setvids(confFileLoc):
 #Create Cpu objects
 cpus = [Cpu(path) for path in glob.glob('/sys/devices/system/cpu/cpu?')]
 if len(cpus) == 0: raise Exception('Something serious is wrong. Someone fix this script now!')
 
 #Load VIDs
 try:
  with open(confFileLoc, 'r') as confFile: vids = list(map(int, confFile.readline().split()))
  if len(vids) != len(cpus[0].getDefaultVids()): raise
 except: raise Exception('Could not load vids. Check the configuration file.')
 
 #Set VIDs
 for cpu in cpus:
  cpu.setCurrentVids(vids)
  print(cpu.name, 'vids set to:',vids)


#A helper class
class Cpu(object):
 def __init__(self, path):
  self.path = path
  self.name = path.split('/')[-1]
  self.number = int(self.name[3:])
 
 def getDefaultVids(self):
  try:
   with open(self.path+'/cpufreq/phc_default_vids', 'r') as f: return list( map(int, f.read().split() ) )
  except: raise Exception('Could not get the default PHC vids for', self.name)
  	
 def getCurrentVids(self):
  try:
   with open(self.path+'/cpufreq/phc_vids', 'r') as f: return list( map(int, f.read().split() ) )
  except: raise Exception('Could not get the current PHC vids for', self.name)
  
 def setCurrentVids(self, vids):
  if len(self.getDefaultVids()) != len(vids): raise Exception('VIDS are not the correct length for', self.name)
  try:
   with open(self.path+'/cpufreq/phc_vids', 'w') as f: return f.write( ' '.join(map(str,vids)) )
  except: raise Exception('Could not set the PHC vids', vids,' for', self.name)
  		
 def getAvailableGovs(self):
  try:
   with open(self.path+'/cpufreq/scaling_available_governors', 'r') as f: return f.read().split()
  except: raise Exception('Could not get the available governors for', self.name)
  
 def getCurrentGov(self):
  try:
   with open(self.path+'/cpufreq/scaling_governor', 'r') as f: return f.read().strip()
  except: raise Exception('Could not get the current governor for', self.name)
  	
 def setCurrentGov(self, gov):
  if gov not in self.getAvailableGovs(): raise Exception('Governor',gov,'is not available')
  try:
   with open(self.path+'/cpufreq/scaling_governor', 'w') as f: return f.write( str(gov) )
  except: raise Exception('Could not set the current governor for', self.name)
  		
 def getAvailableFreqs(self):
  try:
   with open(self.path+'/cpufreq/scaling_available_frequencies', 'r') as f: return list( map(int, f.read().split() ) )
  except: raise Exception('Could not get the available frequencies for', self.name)
  
 def getCurrentFreq(self):
  try:
   with open(self.path+'/cpufreq/scaling_cur_freq', 'r') as f: return int(f.read().strip() )
  except: raise Exception('Could not get the current frequency for', self.name)
  
 def setCurrentFreq(self, freq):
  if freq not in self.getAvailableFreqs(): raise Exception('Frequency',freq,'is not available')
  try:
   with open(self.path+'/cpufreq/scaling_setspeed', 'w') as f: return f.write( str(freq) )
  except: raise Exception('Could not set the current frequency for', self.name)
  	
 def getMaxFreq(self):
  try:
   with open(self.path+'/cpufreq/scaling_max_freq', 'r') as f: return int(f.read().strip() )
  except: raise Exception('Could not get the maximum frequency for', self.name)
  		
 def setMaxFreq(self, freq):
  if freq not in self.getAvailableFreqs(): raise Exception('Frequency',freq,'is not available')
  try:
   with open(self.path+'/cpufreq/scaling_max_freq', 'w') as f: return f.write( str(freq) )
  except: raise Exception('Could not set the maximum frequency for', self.name)
  	
 def getMinFreq(self):
  try:
   with open(self.path+'/cpufreq/scaling_min_freq', 'r') as f: return int(f.read().strip() )
  except: raise Exception('Could not get the minimum frequency for', self.name)
  		
 def setMinFreq(self, freq):
  if freq not in self.getAvailableFreqs(): raise Exception('Frequency',freq,'is not available')
  try:
   with open(self.path+'/cpufreq/scaling_min_freq', 'w') as f: return f.write( str(freq) )
  except: raise Exception('Could not set the minimum frequency for', self.name)
  
 def getMinMaxFreq(self):
  return ( self.getMinFreq(), self.getMaxFreq() )
  	
 def setMinMaxFreq(self, mi, ma):
  return tuple( reversed( (self.setMaxFreq(ma), self.setMinFreq(mi)) ) )

#Load module m
def loadModule(m):
 try: return sp.check_call(['modprobe', '--quiet', str(m)])
 except: raise Exception('Could not load module', m)

#A very basic stressor. Runs for ever.
def stressor(x):
 try:
  while True:
   x = x+1
   y = x * x
   z = y * y * y
   a = z % x
 except KeyboardInterrupt: pass


