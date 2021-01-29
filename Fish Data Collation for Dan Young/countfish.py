from io import open

in_file = 'c:/tmp/dan/sample.txt'
out_file = 'c:/tmp/dan/output.csv'
fish = {}
in_data_section = False
for line in open(in_file,'r', encoding="utf-8"):
    if in_data_section == False and line.startswith('-----------------'):
        in_data_section = True
        continue
    if in_data_section == True and len(line.strip()) == 0:
        in_data_section = False
    if in_data_section == True:
        date =  line[100:110] + ' ' + line[90:98]
        if date not in fish:
            fish[date] = 0
        fish[date] += 1
f = open(out_file,'w', encoding="utf-8")
f.write('datetime,count\n')
for date,count in sorted(fish.items()):
    f.write(date+ ','+str(count)+'\n')
f.close()
