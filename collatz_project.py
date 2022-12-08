import xlrd

from PIL import Image, ImageDraw, ImageFont 
import math

#font for numbers

fontPath = "C:/Users/zoegriffiths/Library/Fonts/Cooper Black Regular.ttf"
font_to_use  =  ImageFont.truetype (fontPath, 100)

#draw grid back ground for map

img = Image.new("RGB",(20500,22000),'white')
dr = ImageDraw.Draw(img)

#colours
    
red = (227,41,46)
green = (88,255,133)
black = (0,0,0)
blue = (0,0,255)

#get data from spreadsheet

book = xlrd.open_workbook("submissions.xls")
sh = book.sheet_by_index(0)
number_of_cols = sh.ncols
number_of_rows = sh.nrows

#three coloumns in the sheet being used are for: school number, student/art work number and starting number for each piece of work

schools = []
students = []
start_nos = []

for i in range(1,number_of_rows):
    start_nos.append(sh.cell_value(rowx=i,colx=3))
    schools.append(sh.cell_value(rowx=i,colx=1))
    students.append(sh.cell_value(rowx=i,colx=2))
    
    schools_no_repeat = []
    for i in schools:
        if i not in schools_no_repeat: 
            schools_no_repeat.append(i)
            
twos = list(range(10,100))
threes = list(range(100,1000))

#Find numbers en route to 1 from particular starting numbers

def collatz(start_number): 
    list = []
    next_number = start_number 
    list.append(start_number)
    start = True
    while start:
        if next_number % 2 == 0: 
            next_number = int(next_number / 2)
            list.append(next_number)
            if next_number == 1: 
                start = False       
        else: 
            next_number = 3*next_number + 1
            list.append(next_number)
            if next_number == 1: 
                start = False
    return list

#I'm interested in the map we can draw with what we've got, what we can draw 

#find out which numbers we have pics of

def what_got():

    nos_no_repeat = []
    for i in start_nos:
        if i not in nos_no_repeat: 
            nos_no_repeat.append(i)
    
    count = [0]*len(nos_no_repeat)
    
    for i in start_nos: 
        count[nos_no_repeat.index(i)] += 1
    
    paths = []
    path_lengths = []
    for i in nos_no_repeat:
        path = collatz(i)
        paths += path
    
    got_no_repeat = []
    for i in paths:
        if i not in got_no_repeat: 
            got_no_repeat.append(i)
            
    return got_no_repeat


#shows all the numbers in the minimal map from all two digit numbers to 1

def twos_map():

    paths = []
    path_lengths = []
    for i in twos:
        path = collatz(i)
        paths += path
    
    need = []
    for i in paths:
        if i not in need: 
            need.append(i)
            
    return need

#shows all the numbers in the minimal map from all three digit numbers to 1

def threes_map():

    paths = []
    path_lengths = []
    for i in threes:
        path = collatz(i)
        paths += path
    
    need = []
    for i in paths:
        if i not in need: 
            need.append(i)
            
    return need

#renaming each section of map

display = twos_map()
got = what_got()
extra = threes_map()

#which three digit numbers I'm missing for the minimal map from three-digits (to suggest schools to use these as start numbers for additional maps)

def threes_missing():
    
    done = [0]*len(threes)
    not_done = []
    
    for m in got: 
        if m in threes: 
            done[threes.index(m)]+=1

    for i in range(len(threes)): 
        if done[i] == 0:
            not_done.append(threes[i])
            
    print(len(not_done))
    print(not_done)
    
    return not_done

# what colours to show each dot in map 

def colours(number_name): 
    if number_name in got:
        if number_name in display:
            col = green
        else:
            col = blue
    elif number_name not in display: 
        col = red
    else: 
        col = black
    return col


# Draw the map showing numbers we either have or need for a map 

def draw_map(): 
    orbits = [1]
    
    #draws dot for number 1
    
    dr.ellipse((5000,21830,5100,21930), fill=green, outline='black', width=1)
    x_1 = [5000]
    x_2 = [5100] 
    y_1 = [21830]
    y_2 = [21930]
    total = 1
    divide = 1
   
    #stuff for student allocation
    student_tally = [0]*len(students)
    school_tally = [0]*len(schools_no_repeat)
    
    s_c = [0]*len(schools_no_repeat)
    lists = [1,200]
    
    draw_list = []
    student_allocate = []
    school_allocate = []
    
    
    for number in orbits:
        
        #vertical spacing between dots
        
        gap = 120
    
        #if the number has two routes into it 
        
        if number % 2 == 0 and number % 3 == 1 and not (number==4): 
            
            #then we need to decide how far apart to make the 'fork,  the later the fork the closer together
            
            divide += 1
            
            if divide == 2:
                dif = float(1/2)*4500
            elif divide == 3 or divide == 4: 
                dif = float(1/3)*4500
            elif divide == 5 or divide == 6:
                dif = float(1/4)*4500
            elif divide == 7 or divide == 8 or divide == 9 or divide == 10 or divide == 11 or divide == 12 or divide == 13:
                dif = float(1/(divide-2))*4500
            else:
                dif = float(1/20)*4500
            if number == 40: 
                diff = 2*dif
            else:
                diff = dif 
            
            #make the odd number that leads to 'number'
            
            number_1 = (number - 1)/3
            
            #make the even number that leads to 'number' 
            
            number_2 = number*2
            
            #only drawing in our map if it is in the minimal map from three digit numbers (we're not going out further than this)
            
            if number_1 in extra:
                
                orbits.append(number_1)
                
                #position of new number 
                
                new_x_1 = x_1[orbits.index(number)] + diff
                new_x_2 = x_2[orbits.index(number)] + diff
                new_y_1 = y_1[orbits.index(number)] - gap
                new_y_2 = y_2[orbits.index(number)] - gap
                x_coord = (new_x_1 + new_x_2)/2
                y_coord =(new_y_1 + new_y_2)/2
                coords = (x_coord,y_coord)
                x_1.append(new_x_1)
                x_2.append(new_x_2)
                y_1.append(new_y_1)
                y_2.append(new_y_2)
                
                #deciding colours based on if we have number, and if it's in the minimal two digit map 
                
                col = colours(number_1)
                
                #drawing dot for this number
                dr.ellipse((new_x_1,new_y_1,new_x_2,new_y_2), fill=col, outline='black', width=1)
                
                #drawing line coming 'number' to number_1
                
                new_line_x = (new_x_1 + new_x_2)/2
                new_line_y = new_y_2
                line_x = (x_1[orbits.index(number)] + x_2[orbits.index(number)])/2
                line_y = y_1[orbits.index(number)]
                dr.line([(line_x,line_y),(new_line_x,new_line_y)], fill='black', width=4, joint=None)
            
                #print number on dot
            
                dr.text(coords, "{0}".format(int(number_1)), fill = (0,0,0), font=font_to_use, anchor="mm")
                
            
            # same for doubling route, #only drawing in our map if it is in the minimal map from three digit numbers (we're not going out further than this)
           
            if number_2 in extra:
                
                orbits.append(number_2)
                
                #due to the shape of the map some forks were longer than others to make space for things
                
                if number_2 == 104 or number_2 == 140 or number_2 == 368: 
                    diff = 2*dif
                elif number_2 == 68 or number_2 == 44: 
                    diff = 3*dif
                
                #position of new number 
                new2_x_1 = x_1[orbits.index(number)] - diff
                new2_x_2 = x_2[orbits.index(number)] - diff
                new2_y_1 = y_1[orbits.index(number)] - gap
                new2_y_2 = y_2[orbits.index(number)] - gap
                x_1.append(new2_x_1)
                x_2.append(new2_x_2)
                y_1.append(new2_y_1)
                y_2.append(new2_y_2)
                x_coord = (new2_x_1 + new2_x_2)/2
                y_coord =(new2_y_1 + new2_y_2)/2
                coords = (x_coord,y_coord)
                 
                #deciding colours based on if we have number, and if it's in the minimal two digit map 
                
                col = colours(number_2)
                
                #drawing dot for this number
                
                dr.ellipse((new2_x_1,new2_y_1,new2_x_2,new2_y_2), fill=col, outline='black', width=1)
                
                #drawing line coming 'number' to number_2
                
                new_line_x = (new2_x_1 + new2_x_2)/2
                new_line_y = new2_y_2
                line_x = (x_1[orbits.index(number)] + x_2[orbits.index(number)])/2
                line_y = y_1[orbits.index(number)]
                dr.line([(line_x,line_y),(new_line_x,new_line_y)], fill='black', width=4, joint=None)
            
                #print number on dot
                
                dr.text(coords, "{0}".format(int(number_2)), fill = (0,0,0), font=font_to_use, anchor="mm")
           
        
        #if the number has one route into it 
        
        else:
            
            #make the even number that leads to 'number' 
            number_2 = number*2
            
            #only drawing in our map if it is in the minimal map from three digit numbers (we're not going out further than this)
            if number_2 in extra:
                
                orbits.append(number_2)
                
                #position of new number
                new2_x_1 = x_1[orbits.index(number)]
                new2_x_2 = x_2[orbits.index(number)] 
                new2_y_1 = y_1[orbits.index(number)] - gap
                new2_y_2 = y_2[orbits.index(number)] - gap
                x_1.append(new2_x_1)
                x_2.append(new2_x_2)
                y_1.append(new2_y_1)
                y_2.append(new2_y_2)
                x_coord = (new2_x_1 + new2_x_2)/2
                y_coord =(new2_y_1 + new2_y_2)/2
                coords = (x_coord,y_coord)
                
                #deciding colours based on if we have number, and if it's in the minimal two digit map 
                
                col = colours(number_2)
                
                #drawing dot for this number
                
                dr.ellipse((new2_x_1,new2_y_1,new2_x_2,new2_y_2), fill=col, outline='black', width=1)
                    
                #drawing line coming 'number' to number_1
                
                new_line_x = (new2_x_1 + new2_x_2)/2
                new_line_y = new2_y_2
                line_x = (x_1[orbits.index(number)] + x_2[orbits.index(number)])/2
                line_y = y_1[orbits.index(number)]
                dr.line([(line_x,line_y),(new_line_x,new_line_y)], fill='black', width=4, joint=None)
            
                #print number on dot
                
                dr.text(coords, "{0}".format(int(number_2)), fill = (0,0,0), font=font_to_use, anchor="mm")    
                
    return orbits 
                 
    

#work out which piece of work contributes to each number in the map
    
def allocate_pieces(map_numbers):
    
    student_tally = [0]*len(students)
    school_tally = [0]*len(schools_no_repeat)
    
    lists = [1,200]
    
    draw_list = []
    
    student_allocate = []
    number_allocate = []
    school_allocate = []
    
    reverse_map = []

    for point in range(len(map_numbers)-1,-1,-1): 
        reverse_map.append(map_numbers[point])
    
    #numbers are allocated from the top of the map down (because there is fewer pieces of work that can contribute to each number higher up the map)
    
    for thing in reverse_map:
        print(thing)
                    
        if thing in display and thing in got: 
                        
            allocated = 0
                    
            for s_limit in lists:
                if allocated >0:
                    #this implies this number has already been allocated 
                    break
                else:
                    if s_limit == 1: 
                        
                        #this bit of code ensures the student chosen is from a school that haven't been featured yet, unless that's not possible in which case we run the section underneath 
                        
                        for i in range(len(start_nos)): 
                            if thing in collatz(start_nos[i]):
                                if school_tally[schools_no_repeat.index(schools[i])] < s_limit:
                                    student_allocate.append(students[i])
                                    school_allocate.append(schools[i])
                                    number_allocate.append(thing)
                                    school_tally[schools_no_repeat.index(schools[i])]+=1
                                    student_tally[i] += 1
                                    print ("{0} has been allocated".format(thing))
                                    allocated += 1
                                    break 
                    else: 
                        for limit in range(150):
                            if allocated >0:
                                break
                            else: 
                                
                                #in this section s_limit is 200, so if it's not possible to find a school that's been used zero times we then don't care how many times the school we choose has been used. But we do then choose a student who has been used as little as possible.
                                
                                for i in range(len(start_nos)): 
                                    if thing in collatz(start_nos[i]):
                                        if school_tally[schools_no_repeat.index(schools[i])] < s_limit:
                                            if student_tally[i] == limit:
                                                student_allocate.append(students[i])
                                                school_allocate.append(schools[i])
                                                number_allocate.append(thing)
                                                school_tally[schools_no_repeat.index(schools[i])]+=1
                                                student_tally[i] += 1
                                                print ("{0} has been allocated".format(thing))
                                                allocated += 1
                                                break                         
    
    #printing allocation instructions
    for l in range(len(number_allocate)):
        print(("{0} is drawn by {1} of school {2}").format(number_allocate[l],student_allocate[l],school_allocate[l]))
    
    #checking no school has not been featured
    for p in range(len(schools_no_repeat)):
        print("school {0} was used {1} times".format(schools_no_repeat[p],school_tally[p]))
        if school_tally[p] == 0:
            print("UHOH")

#You can see in the code above that pieces of work featured early on in the 'submissions' spreadsheet are given a higher priority than those later. But it's worth noting that the data in the sheet was sorted such that work with a better 'score' (from 1 to 4) was higher up the spreadsheet (and would therefore get priority). And then within those four categories the pieces of work were listed in a random order so no preference is given to any particular school. 

map_numbers = draw_map()

allocate_pieces(map_numbers)
    
        
img.save("map_project.png")

