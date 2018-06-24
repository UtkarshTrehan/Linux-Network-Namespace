from pyroute2 import NSPopen
from subprocess import PIPE
import xlsxwriter

# Verifying the connection by using ping
pingResult = list()
stats = list()
NUMBER_OF_PACKETS = '5'
numberOfPingIteration = int(input('Enter the number of iteration: '))
for i in range(0,numberOfPingIteration):
    nsp = NSPopen('blue', ['ping', '10.1.1.2', '-c', NUMBER_OF_PACKETS], stdout=PIPE) #Running a subprocess inside namespace
    with nsp.stdout:
        for line in iter(nsp.stdout.readline, b''):
            pingResult.append(line)
    nsp.wait()
    nsp.release()
    ping_stats = pingResult[-1]
    stat = ping_stats[23:-3]
    stats.append(stat.split('/'))

#Creating workbook named UserDatabse to store all ping stats
workbook = xlsxwriter.Workbook('UserDatabse.xlsx')
worksheet = workbook.add_worksheet()
#Assigning headers
worksheet.write('A1', 'S.No')
worksheet.write('B1', 'Min (ms)')
worksheet.write('C1', 'Avg (ms)')
worksheet.write('D1', 'Max (ms)')
#Filling up the ping stats into xls file
row = 1
count=1
for i in stats: # Getting each ping instances
  i.insert(0,count)
  count+=1
  col = 0
  for j in i[:-1]: # Getting interested stats values
      worksheet.write(row, col, j)
      col += 1
  row += 1
workbook.close()
