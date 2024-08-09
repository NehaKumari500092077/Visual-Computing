import sys
import traceback
from sets import Set

uname = sys.argv[1]
pwd = sys.argv[2]
url = sys.argv[3]

for i in range(len(sys.argv)):
    if sys.argv[i] == "-uname":
        uname = sys.argv[i + 1]
    if sys.argv[i] == "-pwd":
        pwd = sys.argv[i + 1]
    if sys.argv[i] == "-url":
        url = sys.argv[i + 1]


def getAttributeValue(objectName, attributeName):
    eachObject = str(objectName)
    attributeList = eachObject.split(',')
    for attribute in attributeList:
        keyValues = attribute.split('=')
        if attributeName in keyValues[0]:
            attributeValue = keyValues[1]
            return attributeValue


try:

    connect(uname, pwd, url)

    domainRuntime()
    objname = ObjectName('*oracle.apps.crmCommon.core.extnUpgrade.mbean:name=CrmExtnUpgradeMBean,*')
    mbset = mbs.queryNames(objname, None)
    mbarray = mbset.toArray()

    applicationSet = Set()
    serversSet = Set()

    for mbean in mbarray:
        readOnly = mbs.getAttribute(mbean, 'ReadOnly')
        # print('ReadOnly: %s' % readOnly)
        if not readOnly:
            print('Additional Logs: MBean is not Read only.....')
            applicationName = getAttributeValue(mbean, 'ApplicationName')
            if (applicationName not in applicationSet) or (applicationName == '') or (applicationName is None):
            	print('Additional Logs: Application getting ready for Upgrade %s .....' % applicationName)
                applicationSet.add(applicationName)

                serverName = getAttributeValue(mbean, 'Location')
                # if (serverName not in serversMap) or (serverName == '') or (serverName is None):
                serversSet.add(serverName)

                print('Upgrading custom metadata for application %s on server %s ...' % (applicationName, serverName))
                mbs.invoke(mbean, 'upgrade', None, None)
            else:
                print('Additional Logs: Set Details..... %s' % ','.join(applicationSet))
                print('Additional Logs: Server Name null or Empty or Visited Name: %s' % applicationName) 
        else:
           print('Additional Logs: Read Only....')

    print('\nFor more detailed information about the upgrade, '
          'please refer to the server diagnostic logs for the following servers: %s' % ','.join(serversSet))

    disconnect()

except:
    print 'A problem occured during execution of MDS auto upgrade:'
    traceback.print_exc()
exit()