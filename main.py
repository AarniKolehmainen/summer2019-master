
def read(date, time):
    fil = open('pickup_times.csv', 'r')
    ids = []
    values = []
    #Value of a is used to skip the first line of the file
    a = 0
    for line in fil:
        #Skip the first line
        if (a == 0):
            a = -1
        else:
            temp = line.split(",")
            filedate = temp[1].split("T")
            filetime = filedate[1].split(":")
            #Check date and time
            if (filedate[0] == date and  int (time[0]) <= int(filetime[0]) < int(time[1]) ):
                i = 0
                
                #Check if id already exists in the list
                while i < len(ids):   
                    if (ids[i] == temp[0]):
                        values[i].append(int (temp[2]))
                        i = -1
                        break
                    i += 1
                
                if (i >= 0 and i <= len(ids)):
                    ids.append(temp[0])
                    values.append([int(temp[2])])
    fil.close()
    return ids, values

def count_medians(values):
    medians = []
    
    for i in range(len(values)):
        values[i].sort()
        length = len(values[i])
        if (length % 2 != 0):
            median = values[i][int ((length-1)/2)]
        else:
            median = (values[i][int (length/2)] + values[i][int ((length/2) -1)]) / 2
        medians.append(median)
    return medians

def sort_by_id(ids, medians, n):
    #Sort by id by using simple insertion sort
    if n > 0:
        sort_by_id(ids, medians, n-1)
        latest_id = ids[n]
        latest_median = medians[n] 
        i = n - 1
        
        while (i >= 0 and int (ids[i]) > int (latest_id)):
            ids[i + 1] = ids[i]
            medians[i + 1] = medians[i]
            i = i - 1
        ids[i + 1] = latest_id
        medians[i + 1] = latest_median
    return

def write(ids, medians, date, hour, name):
    fil = open(name, 'w+')
    fil.write("Median pickup times in {} at hours {}\n".format( date, hour) )
    fil.write("id, median\n")
    for i in range (len(ids)):
        fil.write("{},{}\n".format( ids[i], medians[i]))
    fil.close()
    return

def main():
    status = True
    while (status == True):
        try:
            date = str (input ("Please enter the date in format yyyy-mm-dd\n"))
            hour = str (input ("Please enter start and end hours for example 00-24\n") )
            filename = str (input ("Please enter the name of the file where you want to store the data\n"))
            hours = hour.split("-")
            
            id_list, value_list = read(date, hours)
            median_list = count_medians(value_list)
            sort_by_id(id_list, median_list, len(id_list) - 1)
            write(id_list, median_list, date, hour, filename)
            print ("Medians were saved in file '{}'". format(filename))
            status = False  
        except:
            print ("Something went wrong. Please check your input and try again.\n")
main()