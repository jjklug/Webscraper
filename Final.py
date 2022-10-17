#CS021 - Jack Klug
#Web Scraper project

#This scraper will go through a website that I created for my CS008 class an

import requests

def main():
    original_filename = "website-data.txt"
    scraper(original_filename)
    #dictionary does not end up getting used
    planner_dictionary, planner_list = read_site_data(original_filename)
    #Tells the user what the program does and allows them to choose what to do with the program
    print("Welcome to Jack's webscraper. My webscraper scrapes my very own website at https://jjklug.w3.uvm.edu/cs008/final/display.php and extracts the html from the website. This python tool can be used to analyze the data - specifically the data from the dynamic table that is located on the website. My webscraper tool allows you to do several different things with the data that has been scraped.")
    choice = 0
    while(choice != 3):
        print("What would you like to do with the data?")
        print("1 - Display the data in python")
        print("2 - Put the clean data in a file")
        print("3 - Exit the tool")
        choice = int(input("Enter your choice here: "))
        while(choice < 0 and choice >= 3):
            choice = input("Please enter a valid option: ")

        if (choice == 1):
            display_table(planner_list)
        elif (choice == 2):
            filename = input("What would you like to name the file that the data will be entered in: ")
            new_file(filename, planner_list)
        elif (choice == 3):
            print("Thanks for using Jack's webscraper!")


#This function uses the requests library to extract the html data from a website
def scraper(filename):
    infile = open(filename, "w")
    url = "https://jjklug.w3.uvm.edu/cs008/final/display.php"
    page = requests.get(url)
    infile.write(page.text)
    infile.close()

#This function takes the file that was scraped off the website and it sorts through the data cleaning it up and sorting it into lists
#These lists are used to create a dictionary and a 2d list that is returned by this function
def read_site_data(original_filename):
    outfile = open(original_filename, "r")
    #variable that sets a value for the length of a th and td elements to avoid any confusion from magic numbers
    tdth_element_length = 4
    #intial checker variable used to extract the data from the table on the site
    check = 0
    #secondary checker variable used to find the headers from the table and insert them into a list
    header_checker = 0
    #third checker variable used to tell the program when to stop adding to the header list after the first time 
    header_list_ender = 0
    #list that contains the headers for the table
    header_list = []
    #lists that will contain the data
    netID_list = []
    assignment_title_list = []
    class_list = []
    assignment_length_list =[]
    due_date_list =[]
    assignment_desc_list =[]
    #massive for loop that iterates through the file extracting the data from it
    for line in outfile:
        line = line.rstrip("\n")
        line = line.strip()
        if (line.find("<table>") != -1):
            check = 1
        elif (line.find("</table>") != -1):
            check = 0
        #Use a checker variable to clear away all the other unnecessary data from the loop
        #only looks at the data inside the table rather than the entire webpage's html
        if (check == 1):
            if (line.find("</tr>") == 0):
                header_list_ender = 1
            #this section creates the header list specifically because that part is separate from the rest of the table data
            if (header_list_ender == 0):
                if (line.find("<th>") != -1):
                    header_checker = 1
                if (header_checker == 1):
                    header_list.append(line[(line.find("<th>")+tdth_element_length):(line.find("</th>"))])
                if (line.find("</th>") != -1):
                    header_checker = 0
            #this part of the loop looks into the rest of the data in the table
            #the data that goes underneath the headers
            if (header_list_ender == 1):
                if (line.find("<tr>") != -1):
                    if (line.find("<td>") != -1):
                        #assigning all the lists values in a seperate function
                        netID_list,assignment_title_list,class_list,assignment_length_list,due_date_list,assignment_desc_list = list_creation(tdth_element_length,line, netID_list,assignment_title_list,class_list,assignment_length_list, due_date_list, assignment_desc_list)
    #list creation is complete and now I am adding these lists into one dictionary that is easily accessible
    #dictionary that will contain the lists
    homework_planner_data = {}
    for x in range(len(header_list)):
        if (x==0):
            homework_planner_data[header_list[x]] = netID_list
        if (x==1):
            homework_planner_data[header_list[x]] = assignment_title_list
        if (x==2):
            homework_planner_data[header_list[x]] = class_list
        if (x==3):
            homework_planner_data[header_list[x]] = assignment_length_list
        if (x==4):
            homework_planner_data[header_list[x]] = due_date_list
        if (x==5):
            homework_planner_data[header_list[x]] = assignment_desc_list
    
    #create a 2d list with all the table data inside of it
    planner_list = []
    planner_list.extend([netID_list, assignment_title_list, class_list, assignment_length_list, due_date_list, assignment_desc_list])

    outfile.close()
    return homework_planner_data, planner_list

#function that creates the lists for each section of the table by accessing the date from the file
def list_creation(tdth_element_length, line, list1, list2, list3, list4, list5, list6):
    starting_index = line.index("<td>")+tdth_element_length
    ending_index = line.index("</td>")
    list1.append(line[starting_index:ending_index])

    starting_index = line.index("<td>", ending_index)+tdth_element_length
    ending_index = line.index("</td>", starting_index)
    list2.append(line[starting_index:ending_index])

    starting_index = line.index("<td>", ending_index)+tdth_element_length
    ending_index = line.index("</td>", starting_index)
    list3.append(line[starting_index:ending_index])

    starting_index = line.index("<td>", ending_index)+tdth_element_length
    ending_index = line.index("</td>", starting_index)
    list4.append(line[starting_index:ending_index])

    starting_index = line.index("<td>", ending_index)+tdth_element_length
    ending_index = line.index("</td>", starting_index)
    list5.append(line[starting_index:ending_index])

    starting_index = line.index("<td>", ending_index)+tdth_element_length
    ending_index = line.index("</td>", starting_index)
    list6.append(line[starting_index:ending_index])

    return list1,list2,list3,list4,list5,list6

#this function displays all the data that has been gathered from the website and displays it in a neat table
def display_table(planner_list):
    longest_list = 0
    #find out the length of the longest list to determine how many dashes to use
    for y in range(len(planner_list[0])):
        curr_list_length = 0
        for x in range(len(planner_list)):
            curr_list_length += len(planner_list[x][y])
        if (curr_list_length > longest_list):
            longest_list = curr_list_length

    print('')
    print('')
    #header row
    for z in range(longest_list):
        print("-", end='')
    print('')
    print("| NetID | Assignment Title | Class | Assignment Length | Due Date | Assignment Description |")
    #this loop goes through the lists and prints out the data in a neat table form
    for y in range(len(planner_list[0])):
        for z in range(longest_list):
                print("-", end='')
        print('')
        print('| ', end='')
        for x in range(len(planner_list)):
            print(f"{planner_list[x][y]}", end=' | ')
        print('')
    for z in range(longest_list):
        print("-", end='')
    print('')

#function that takes the table data and writes it to a file
def new_file(filename, planner_list):
    infile = open(filename, "w")
    longest_list = 0
    #find out the length of the longest list to determine how many dashes to use
    for y in range(len(planner_list[0])):
        curr_list_length = 0
        for x in range(len(planner_list)):
            curr_list_length += len(planner_list[x][y])
        if (curr_list_length > longest_list):
            longest_list = curr_list_length

    #header row
    for z in range(longest_list):
        infile.write("-")
    infile.write('\n')
    infile.write("| NetID | Assignment Title | Class | Assignment Length | Due Date | Assignment Description |\n")
    #this loop goes through the lists and prints out the data in a neat table form
    for y in range(len(planner_list[0])):
        for z in range(longest_list):
                infile.write("-")
        infile.write('\n')
        infile.write('| ')
        for x in range(len(planner_list)):
            infile.write(f"{planner_list[x][y]} | ")
        infile.write('\n')
    for z in range(longest_list):
        infile.write("-")

main()

