
def read(date, time):
    fil = open('pickup_times.csv', 'r')
    # Store id valuelist pairs in a two dimensional list.
    # So we have list of id's in index 0 and list of pickup time lists in index 1
    id_value_list = [[], []]
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
                while i < len(id_value_list[0]):   
                    if (id_value_list[0][i] == temp[0]):
                        id_value_list[1][i].append(int (temp[2]))
                        i = -1
                        break
                    i += 1
                
                #if id did not exist, add new
                if (i >= 0 and i <= len(id_value_list[0])):
                    id_value_list[0].append(temp[0])
                    id_value_list[1].append([int(temp[2])])
    fil.close()
    return id_value_list

def count_medians(id_value_list):
    medians = []
    
    for i in range(len(id_value_list[0])):
        id_value_list[1][i].sort()
        length = len(id_value_list[1][i])
        if (length % 2 != 0):
            median = id_value_list[1][i][int ((length-1)/2)]
        else:
            median = (id_value_list[1][i][int (length/2)] + id_value_list[1][i][int ((length/2) -1)]) / 2
        #Store the id-median pairs as tuples to a list
        #That means a change in indexing
        #For example id of n:th pair can be found from medians[n][0] and median from medians[n][1]
        medians.append( (id_value_list[0][i], median) )
    return medians

def sort_by_id(medians, n):
    #Sort by id by using simple insertion sort
    
    if n > 0:
        sort_by_id(medians, n-1)
        latest_pair = medians[n] 
        #i is he next index to compare
        i = n - 1
        
        while (i >= 0 and int (medians[i][0]) > int (latest_pair[0])):
            medians[i + 1] = medians[i]
            i = i - 1
        medians[i + 1] = latest_pair
    return

def write(medians, date, hour, filename):
    fil = open(filename, 'w+')
    fil.write("Median pickup times in {} at hours {}\n".format( date, hour) )
    fil.write("id, median\n")
    for i in range (len(medians)):
        fil.write("{},{}\n".format( medians[i][0], medians[i][1]))
    fil.close()
    return

def main():
    status = True
    #A loop for the script to not crash on invalid input or restricted file
    while (status == True):
        try:
            date = str (input ("Please enter the date in format yyyy-mm-dd\n"))
            hour = str (input ("Please enter start and end hours for example 00-24\n") )
            filename = str (input ("Please enter the name of the file where you want to store the data\n"))
            hours = hour.split("-")
            id_value_list = read(date, hours)
            medians = count_medians(id_value_list)
            sort_by_id(medians, len(medians) - 1)
            write(medians, date, hour, filename)
            print ("Medians were saved in file '{}'". format(filename))
            status = False
        except:
            print ("Something went wrong. Please check your input and try again.\n")
main()