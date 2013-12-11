import json, urllib
import cybercom_urllib2
from sites import sites

#login to cybercommons
username = raw_input('Please enter Cybercommons Username: ')
prompt ="%s Password: " % (username)
password = raw_input(prompt)
urllib2 = cybercom_urllib2.login(username,password).get()
#url = 'http://apps.cybercommons.org/accounts/userdata/'
#temp = json.loads(urllib2.urlopen(url).read())
#uid = temp['user']['id']
#cybercommons user id which uploaded data
uid = '1' # Need to fix, Make data public and not tied to userid. This would allow others to not have to know my id

#siteparam
siteparam="{'spinup_years':'1450','Lat':'35.9','Co2ca':'3.70E-04','a1':'7.0','Ds0':'2000','Vcmx0':'0.65E-04','extku':'0.5','xfang':'0','alpha':'0.385','stom_n':'2','Wsmax':'35','Wsmin':'6','rdepth':'70.0','SLA':'1.2E-2','LAIMAX':'4.0','LAIMIN':'0.1','nsc':'40.74','Storage':'57.6','Q_leaf':'3.3334','Q_wood':'0.9981','Q_root1':'62.41','Q_root2':'35.1517','Q_root3':'11.0793','Q_coarse':'0.0','Q_fine':'369.9881','Q_soil1':'4869.856','Q_soil2':'2304.713','Q_soil3':'1397.098','rfibre':'0.7','output':'2','Rootmax':'1000.0','Stemmax':'1000.0','SenS':'0.0005','SenR':'0.0005'}"
model="grassland"
forc='[]'
dda_freq=1
tags_template="TECO - Grassland,%s,%s,%s"
MW_template="{'tair':[('add',%d)]}"
task_submission = "http://apps.cybercommons.org/queue/run/cybercomq.model.teco.task.runTECOworkflow/?"
output =[]
project = "Zheng_Grassland"

for site in sites:
    #Get base years by access database
    url = "http://apps.cybercommons.org/mongo/distinct/teco/uploaded_grass/year/{'spec':{'Site':'" + site + "'}}/"
    base =json.loads(urllib2.urlopen(url).read())
    base_yrs='(%d,%d)' % (base[0],base[-1])
    #Modify Weather add tair by parameter sweep
    for tempinc in range(0,1): # Adjust end sweep number to increase tair 
        tags = tags_template % (site,project, "Weather:tair plus %d degrees" % (tempinc))
        mod_weather=MW_template % (tempinc)
        #status
        print tags
        #Load Params can add Modification of Weather use template 
        Params = {'site':site,'base_yrs':base_yrs,'forecast':forc,'siteparam':siteparam,'model':model,'dda_freq':dda_freq,'upload':uid,'tags':tags,'mod_weather':mod_weather}
        Params = urllib.urlencode(Params)
        #Run Task
        url = task_submission + Params 
        temp= json.loads(urllib2.urlopen(url).read())
        temp['Site']=site
        temp['Task_Result']="http://apps.cybercommons.org/queue/report/" + temp['task_id']
        temp['Download']="http://static.cybercommons.org/queue/model/teco/" + temp['task_id'] + "/model_run_archive.zip"
        temp['Plot']="http://static.cybercommons.org/apptest/teco_plot/?task_id=" + temp['task_id'] + "Cdaily&model=TECO_Grassland_Cdaily"
        output.append(temp)

#Generate Task Report
report = open( project + ".txt", 'w')
report.write("Project: %s\n\n" % (project))
for out in output:
    report.write("TASK ID: %s Site: %s\n" % (out['task_id'],out['Site']))
    report.write("\tResult: %s\n" % (out['Task_Result']))
    report.write("\tDownload: %s\n" % (out['Download']))
    report.write("\tPlot: %s\n\n" % (out['Plot']))
