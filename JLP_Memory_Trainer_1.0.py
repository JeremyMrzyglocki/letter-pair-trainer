import random, math
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
#USE FULLSCREEN-MODE to see full GUI

#Code by Jeremy Mrzyglocki
#Version v10 in personal version-track-metric

'''
STRUCTURE OF CODE:
1) VARIABLES
2) FUNCTIONS
3) TKINTER WIGDETS
4) EXTRA: commented DEBUGGING-WIDGETS

What I am going to implement in the future:
-A way to track more time splits
-Error-Analyzer (Frequenty mistaken letter pair statistics)
-Leaderboard
-js implementation on my website with online-leaderboard
-increase the 16-cube-limit (implement a functional scrollbar)
'''
#########################################  Variables  #################################################

font = ("Monaco", 15) #using a monospace font so that the letters are below eachother
fontsmall = ("Monaco", 12)
my_letter_sceme = 'ABCDEFGHIJKLMNOPQRSTUVWZ'

timer_running = False # timer for memorization
elapsed_time_s = 0
elapsed_time_m = 0 
timer2_running = False # timer for recall
elapsed_time_s2 = 0 
elapsed_time_m2 = 0 

attempt_number = 0
letter_scheme = []

number_of_cubes = 16
initial_cube_number = 16
max_letters_edges = 16
max_letters_corners = 12
max_letters = max_letters_edges + max_letters_corners

number_of_wrong_cubes_in_attempt = 0 # increases by one for each incorrect cube
number_of_wrong_letters_in_attempt = 0 # increases by one for each incorrectly recalled letter
number_of_letters_in_attempt = 0

# probabilities based on my calculations provided in README
p_edges_8, p_edges_9, p_edges_10, p_edges_11, p_edges_12, p_edges_13, p_edges_14, p_edges_15, p_edges_16 = 0.00618, 0.03204, 0.10363, 0.21045, 0.26784, 0.21219, 0.10557, 0.03316, 0.00694
prob_edges = [p_edges_8, p_edges_9, p_edges_10, p_edges_11, p_edges_12, p_edges_13, p_edges_14, p_edges_15, p_edges_16]
values_edges = [8, 9, 10, 11, 12, 13, 14, 15, 16] # sum of probabilites is 1 

# These are just my approximations based on experience
p_corners_5, p_corners_6, p_corners_7, p_corners_8, p_corners_9, p_corners_10, p_corners_11 = 0.005, 0.1, 0.245, 0.30, 0.245, 0.1, 0.005
prob_corners = [p_corners_5, p_corners_6, p_corners_7, p_corners_8, p_corners_9, p_corners_10, p_corners_11]
values_corners = [5, 6, 7, 8, 9, 10, 11] # sum of probabilites is 1 

######################################### empty Array-Variables  #################################################
# I use the word "master" to indicate that this is an array that holds information about the full set of Letters generated

master_array =       [[' '] * (max_letters + 1) for _ in range(number_of_cubes)]
master_array_input = [[' '] * (max_letters + 1) for _ in range(number_of_cubes)]  # Initialize characters array
master_array_string = [' '] * int(max_letters + max_letters)
master_farben =      [[' '] * (max_letters + 1) for _ in range(number_of_cubes)]

stats = [[0]*2]*10 #For now only 10 attempts are able to be saved per session, currently not using this variable yet

#########################################  Widget-Variables  #################################################

letterstring_tasks_total_array = []

colorbarframe_for_one_cube_edges = [0]*30
colorbarframe_for_one_cube_edges_array = []
colorbarframe_for_one_cube_corners = [0]*30
colorbarframe_for_one_cube_corners_array = []

colorbar_piece_for_one_cube_array_edges = [[0] * number_of_cubes for _ in range(number_of_cubes)]
colorbar_piece_for_one_cube_array_corners = [[0] * number_of_cubes for _ in range(number_of_cubes)]

entry_boxes_edges_array = []
entry_boxes_corners_array = []

#########################################  FUNCTIONS  #################################################

def select_value_with_probability():
    selected_index_edges = random.choices(range(len(values_edges)), prob_edges)[0]
    selected_index_corners = random.choices(range(len(values_corners)), prob_corners)[0]
    selected_value_edges = values_edges[selected_index_edges]
    selected_value_corners = values_corners[selected_index_corners]
    #recursive Parity-Check: (for explanation of what Parity means here, see README)
    if ( (selected_value_edges%2 == 1) and (selected_value_corners%2 == 1) or (selected_value_edges%2 == 0) and (selected_value_corners%2 == 0)):
        #line for debugging:
        #print('selected_value_edges=', str(selected_value_edges)+ ' selected_value_corners=', str(selected_value_corners))
        return selected_value_edges, selected_value_corners
    else: 
        return select_value_with_probability()


def gen_lps():  # lps stands for letter pairs
    global number_of_cubes, letter_scheme, letterstring_tasks_total_array, master_array
    number_of_cubes = int(textbox_n.get("1.0", tk.END).strip())
    letter_scheme = list(textbox.get("1.0", tk.END).strip())
    checkbox_n.select()
    checkbox.select()

    master_array = [[' '] * (max_letters + 1) for _ in range(number_of_cubes)] #clears the master_array

    # fills the master array
    for row in range(number_of_cubes):
        for position in range(max_letters):
            master_array[row][position] = random.choice(letter_scheme)
            while ((position % 2 == 1) and (master_array[row][position] == master_array[row][position-1])): #This recursive loop checks for duplicates
                master_array[row][position] = random.choice(letter_scheme) #...and swaps the letter out

    # deleting objects in master_array so that there are different lenghts of letters strings for edges and corners
    for row in range(number_of_cubes):
        selected_value_edges, selected_value_corners = select_value_with_probability()
        for i in range(max_letters_edges - (selected_value_edges)):
            master_array[row][(max_letters_edges-1) - i] = ' ' 
        for i in range(max_letters_corners - selected_value_corners):
            master_array[row][(max_letters-1) - i] = ' '

    for clear in range(number_of_cubes):
        letterstring_tasks_total_array[clear].config(text=' ')  # clears the rows from the generation before

    for row in range(number_of_cubes):  # previously I had a ton of cases here. Not fixing that would have led to more than 200 extra
        # lines of code. The master_array was the solution for this
        master_array_string[row] = '{}{} {}{} {}{} {}{} {}{} {}{} {}{} {}{}.{}{} {}{} {}{} {}{} {}{} {}{}'.format(
            master_array[row][0], master_array[row][1], master_array[row][2], master_array[row][3],
            master_array[row][4], master_array[row][5], master_array[row][6], master_array[row][7],
            master_array[row][8], master_array[row][9], master_array[row][10], master_array[row][11],
            master_array[row][12], master_array[row][13], master_array[row][14], master_array[row][15],
            master_array[row][16], master_array[row][17], master_array[row][18], master_array[row][19],
            master_array[row][20], master_array[row][21], master_array[row][22], master_array[row][23],
            master_array[row][24], master_array[row][25], master_array[row][26], master_array[row][27],
        )
        displayed_row_number = str("  {:2d}".format(row + 1))
        letterstring_tasks_total_array[row].config(text=(displayed_row_number + ') ' + master_array_string[row]))
    for row in range(number_of_cubes):
        entry_boxes_corners_array[row].config(state="disabled")  # Disables the textboxes before end of memorization
        entry_boxes_edges_array[row].config(state="disabled")
    

def configure_letters():
    global letter_scheme
    input_text = textbox.get("1.0", tk.END).strip()
    letter_scheme = list(input_text)
    checkbox.select()

def on_text_change(event):
    checkbox.deselect()
    textbox.unbind("<<Modified>>")
    textbox.edit_modified(False)
    textbox.bind("<<Modified>>", on_text_change)

def configure_number_of_cubes():
    global number_of_cubes
    number_of_cubes = int(textbox_n.get("1.0", tk.END).strip())
    checkbox_n.select()

def store_characters():
    for row in range(number_of_cubes):
        for j in range(max_letters_edges):
            master_array_input[row][j] = entry_boxes_edges_array[row].get("1." + str(j))
            if ((entry_boxes_edges_array[row].get("1." + str(j))) == "\n"): #filters out the \n that are saved for empty input
                master_array_input[row][j] = ' '

        for j in range(max_letters_corners):
            master_array_input[row][j+max_letters_edges] = entry_boxes_corners_array[row].get("1." + str(j))
            if ((entry_boxes_corners_array[row].get("1." + str(j))) == "\n"): #filters out the \n that are saved for empty input
                master_array_input[row][j+max_letters_edges] = ' '          
    for row in range(number_of_cubes):
        entry_boxes_edges_array[row].config(state="disabled")
        entry_boxes_corners_array[row].config(state="disabled")

def compare_arrays():
    global master_farben, master_array_input, master_array, counter
    for rows in range(number_of_cubes):
        for j in range(max_letters_edges):
            if (master_array_input[rows][j] == master_array[rows][j] and master_array_input[rows][j] != ' ' and master_array[rows][j] != ' '):
                master_farben[rows][j] = 1
            elif (master_array_input[rows][j] == ' ' and master_array[rows][j] == ' '):
                master_farben[rows][j] = 2
            else:
                master_farben[rows][j] = 0
        for k in range(max_letters_corners):
            j_shifted = k+max_letters_edges
            if (master_array_input[rows][j_shifted] == master_array[rows][j_shifted] and master_array_input[rows][j_shifted] != ' ' and master_array[rows][j_shifted] != ' '):
                master_farben[rows][j_shifted] = 1
            elif (master_array_input[rows][j_shifted] == ' ' and master_array[rows][j_shifted] == ' '):
                master_farben[rows][j_shifted] = 2
            else:
                master_farben[rows][j_shifted] = 0
        counter = 0
    for remember_widget in letterstring_tasks_total_array:
        remember_widget.grid() #reveals the letters

def check():
    #Debugging lines:
    '''
    print('colorbar_piece_for_one_cube_array_edges:')
    print(colorbar_piece_for_one_cube_array_edges)
    print('colorbar_piece_for_one_cube_array_corners:')
    print(colorbar_piece_for_one_cube_array_corners)
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print(master_array)
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print(master_array_input)
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print(master_array_string)
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print(master_farben)
    '''
    #Debugging lines end
    
    #The following two for-loops I could pack into one function for fewer lines of codes, but I won't for the sake of code readability
    for j in range(int(number_of_cubes)):
        for n in range(max_letters_edges):
            if (master_farben[j][n] == 1):
                colorbar_piece_for_one_cube_array_edges[j][n].configure(bg="green")
            if (master_farben[j][n] == 0):
                colorbar_piece_for_one_cube_array_edges[j][n].configure(bg="red")
            if (master_farben[j][n] == 2):
                colorbar_piece_for_one_cube_array_edges[j][n].configure(bg="white")

    for j in range(int(number_of_cubes)):
        for n in range(max_letters_corners):
            if (master_farben[j][n+max_letters_edges] == 1):
                colorbar_piece_for_one_cube_array_corners[j][n].configure(bg="green")
            if (master_farben[j][n+max_letters_edges] == 0):
                colorbar_piece_for_one_cube_array_corners[j][n].configure(bg="red")
            if (master_farben[j][n+max_letters_edges] == 2):
                colorbar_piece_for_one_cube_array_corners[j][n].configure(bg="white")


def check_accuracy():
    global number_of_wrong_cubes_in_attempt, number_of_wrong_letters_in_attempt, number_of_letters_in_attempt
    inputcorrect = True

    for i in range(number_of_cubes):
        for j in range(max_letters):
            if master_farben[i][j]==0: # checks every element of the master_farben array containing the data about correctly, incorrectly and not-needed letters, 0=mistake
                inputcorrect = False
                number_of_wrong_letters_in_attempt = number_of_wrong_letters_in_attempt+1
            if master_farben[i][j]!=2: # 2 means that this position in the array is skipped as it is an empty letter
                number_of_letters_in_attempt = number_of_letters_in_attempt+1
        if inputcorrect == False:
            number_of_wrong_cubes_in_attempt = number_of_wrong_cubes_in_attempt+1
    inputcorrect = True # after one line/cube, this boolean is reset

def compare_and_check(): # the order of these functions in crucial for correct calculations
    store_characters()
    compare_arrays()
    check()
    stop_timer2()
    check_accuracy()
    generate_results_text()

def generate_and_start():
    gen_lps()
    start_timer()

def generate_results_text():
    total_elapsed_time_m = elapsed_time_m+elapsed_time_m2
    total_elapsed_time_s = elapsed_time_s+elapsed_time_s2
    
    avg_memo_time_per_cube_m = math.floor((elapsed_time_m*60+elapsed_time_s)/60)
    avg_memo_time_per_cube_s = (elapsed_time_m*60+elapsed_time_s)%60

    if (total_elapsed_time_s>59):
        total_elapsed_time_s = total_elapsed_time_s-60
        total_elapsed_time_m += 1
    results_string = (
        f"--------------------------------------------\n" # string formatting fun incoming
        f"Result of this attempt:\n"
        f" {str(elapsed_time_m).zfill(2)}:{str(elapsed_time_s).zfill(2)} min for memo\n"
        f"+{str(elapsed_time_m2).zfill(2)}:{str(elapsed_time_s2).zfill(2)} min for recall\n"
        f"={str(total_elapsed_time_m).zfill(2)}:{str(total_elapsed_time_s).zfill(2)} min in total\n"
        f"Average memo-time per cube: {str(avg_memo_time_per_cube_m).zfill(2)}:{str(avg_memo_time_per_cube_s).zfill(2)}\n"
        f"Mistakes: {number_of_wrong_letters_in_attempt}\n"
        f"Accuracy(letters): {(number_of_letters_in_attempt-number_of_wrong_letters_in_attempt)/number_of_letters_in_attempt}% \n\n"
        f"Accuracy(cubes):{number_of_cubes-number_of_wrong_cubes_in_attempt}/{number_of_cubes} ({(number_of_cubes-number_of_wrong_cubes_in_attempt)/number_of_cubes}%) \n"
        f"Points: {number_of_cubes-2*number_of_wrong_cubes_in_attempt}\n"
        f"_exported-from-Jeremy's-Letter-Pair-Trainer_\n"
        f"--------------------------------------------\n"
)    
    results_textbox.insert("end", results_string + "\n")

def copy_to_clipboard():
    text = results_textbox.get("1.0", "end-1c")  # gets text from the textbox
    root.clipboard_clear()  # clears the clipboard
    root.clipboard_append(text)  # saves the text to the clipboard
    messagebox.showinfo("Copied", "Results copied to clipboard!")

#########################################  FUNCTIONS FOR TIMER  #################################################

def start_timer():
    attempt_number =+ 1
    global timer_running
    if not timer_running:
        timer_running = True
        update_timer()

def start_timer2():
    global timer2_running
    if not timer2_running:
        timer2_running = True
        update_timer2()

def stop_timer():
    global timer_running
    timer_running = False
    stats[attempt_number][0] = elapsed_time_s + elapsed_time_m*60
    #print('The attempt took you '+str(stats[attempt_number])+' seconds.') # debugging line
    time_result_label.config(text=f"The memorization took you {elapsed_time_s + elapsed_time_m*60} seconds.")
    for row in range(number_of_cubes):
        entry_boxes_corners_array[row].config(state="normal")  # enables the textboxes after submittion
        entry_boxes_edges_array[row].config(state="normal") 
    timer_label.config(fg="black")
    for hide_widget in letterstring_tasks_total_array: # comment this line for debugging
        hide_widget.grid_forget() # hides the Letters; comment this line for debugging
    start_timer2()

def stop_timer2():
    global timer2_running
    timer2_running = False
    stats[attempt_number][1] = elapsed_time_s2 + elapsed_time_m2*60
    time2_result_label.config(text=f"The recall took you {elapsed_time_s2 + elapsed_time_m2*60} seconds.")
    timer2_label.config(fg="black")

def update_timer():
    global elapsed_time_s
    global elapsed_time_m
    if timer_running:
        elapsed_time_s += 1
        if elapsed_time_s == 60:
            elapsed_time_s = 0
            elapsed_time_m += 1
        timer_label.config(text=f"Elapsed Time (memo): {elapsed_time_m}:{elapsed_time_s:02d} minutes", fg="red")
        root.after(1000, update_timer)

def update_timer2():
    global elapsed_time_s2
    global elapsed_time_m2
    if timer2_running:
        elapsed_time_s2 += 1
        if elapsed_time_s2 == 60:
            elapsed_time_s2 = 0
            elapsed_time_m2 += 1
        timer2_label.config(text=f"Elapsed Time (recall): {elapsed_time_m2}:{elapsed_time_s2:02d} minutes", fg="red")
        root.after(1000, update_timer2)

#########################################  WIDGETS  #################################################

root = tk.Tk()
root.title("Letter Pair Generator by Jeremy M v10")

column0 = tk.Frame(root, bd=2, relief=tk.SOLID)
column0.grid(row=0, column=0, sticky="nsew")

column1 = tk.Frame(root, bd=2, relief=tk.SOLID)
column1.grid(row=0, column=1, sticky="nsew")

column2 = tk.Frame(root, bd=2, relief=tk.SOLID)
column2.grid(row=0, column=2, sticky="nsew")

column3 = tk.Frame(root, bd=2, relief=tk.SOLID)
column3.grid(row=0, column=3, sticky="nsew")

# The following code creates the widgets in column0 to column3

#########################################  column0 beginning  #################################################

for j in range(int(number_of_cubes)):
    letterstring_task_for_one_cube = tk.Label(column0, text='###################################', font=font, height=1, width=45)
    letterstring_task_for_one_cube.grid(row=j, column=0)
    letterstring_tasks_total_array.append(letterstring_task_for_one_cube)

#########################################  column0 end  #################################################
#########################################  column1 beginning #################################################
'''
How column 1's grid is structurally built: 
16 cube_frames, all alligned horizontally; each frame consists of:
    the Textlabel for the "n)"-numbering (at 0,0)
    the text_input_line at (at 0,1)
    the colorbar_frame at (at 1,1); consisting of: 
        16 one colored frames (for letter of edges each)
'''

for j in range(int(number_of_cubes)): # creates the 16 cube_frames
    
    cube_frame_col1 = tk.Frame(column1, height=10, width=20)
    cube_frame_col1.grid(row=j, column=0)

    cube_frame_col1_description_1 = tk.Label(cube_frame_col1, text=f'{j+1})', font=font, height=1, width=2) # displays row number
    cube_frame_col1_description_1.grid(row=0, column=0)

    entry_boxes_edges = tk.Text(cube_frame_col1, font=font, height=1, width=25)
    entry_boxes_edges.grid(row=0, column=1)
    entry_boxes_edges.config(state="disabled")
    entry_boxes_edges_array.append(entry_boxes_edges)

    colorbarframe_for_one_cube_edges = tk.Frame(cube_frame_col1, height=1, width=20)
    colorbarframe_for_one_cube_edges.grid(row=1, column=1)
    colorbarframe_for_one_cube_edges_array.append(colorbarframe_for_one_cube_edges)

    for n in range(max_letters_edges):
        colorbar_piece_for_one_letter_edges = tk.Label(colorbarframe_for_one_cube_edges, font=font, height=1, width=1, bg="gray")
        colorbar_piece_for_one_letter_edges.grid(row=0, column=n)
        colorbar_piece_for_one_cube_array_edges[j][n] = colorbar_piece_for_one_letter_edges

#########################################  column1 end  #################################################
#########################################  column2 beginning #################################################
'''
How column 2's grid is structurally built: 
16 cube_frames, all alligned horizontally; each frame consists of:
    the Textlabel for the "n)"-numbering (at 0,0)
    the text_input_line at (at 0,1)
    the colorbar_frame at (at 1,1); consisting of: 
        12 one colored frames (for letter of corners each)
'''

for j in range(int(number_of_cubes)): # creates the 16 cube_frames
    cube_frame_col2 = tk.Frame(column2, height=10, width=20)
    cube_frame_col2.grid(row=j, column=0)

    entry_boxes_corners = tk.Text(cube_frame_col2, font=font, height=1, width=19)
    entry_boxes_corners.grid(row=0, column=0)
    entry_boxes_corners.config(state="disabled")
    entry_boxes_corners_array.append(entry_boxes_corners)

    colorbarframe_for_one_cube_corners = tk.Frame(cube_frame_col2, height=1, width=20)
    colorbarframe_for_one_cube_corners.grid(row=1, column=0)
    colorbarframe_for_one_cube_corners_array.append(colorbarframe_for_one_cube_corners)

    for n in range(max_letters_corners):
        colorbar_piece_for_one_letter_corners = tk.Label(colorbarframe_for_one_cube_corners, font=font, height=1, width=1, bg="gray")
        colorbar_piece_for_one_letter_corners.grid(row=0, column=n)
        colorbar_piece_for_one_cube_array_corners[j][n] = colorbar_piece_for_one_letter_corners

#########################################  column2 end  #################################################
#########################################  column3 beginning #################################################

generate_button = tk.Button(column3, text="Generate Letter Pairs & start memo-timer", command=generate_and_start)
generate_button.grid(row=1, column=0)

timer_label = tk.Label(column3, text="Elapsed Time (memo): 0:00 minutes")
timer_label.grid(row=2, column=0)

time_result_label = tk.Label(column3, text="#Result#")
time_result_label.grid(row=3, column=0)

stop_button = tk.Button(column3, text="Stop memorization and start recall-timer", command=stop_timer)
stop_button.grid(row=4, column=0)

timer2_label = tk.Label(column3, text="Elapsed Time (recall): 0:00 minutes")
timer2_label.grid(row=5, column=0)

time2_result_label = tk.Label(column3, text="#Result#")
time2_result_label.grid(row=6, column=0)

store_button = tk.Button(column3, text="Check & stop recall-timer", command=compare_and_check)
store_button.grid(row=7, column=0)

heading_results = tk.Label(column3, text="Total result:")
heading_results.grid(row=8, column=0)

results_textbox = tk.Text(column3, height=14, width=45)
results_textbox.insert("1.0", "")
results_textbox.grid(row=9, column=0)

button = ttk.Button(column3, text="Copy results to Clipboard", command=copy_to_clipboard)
button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

spacing = tk.Label(column3, text='\n\n\n\n\n\n\n\n\nSettings:\n')
spacing.grid(row=11, column=0)


# Settings
textbox_heading = tk.Label(column3, text='Input the 24 letters of your memo-system:')
textbox_heading.grid(row=30, column=0)

textbox = tk.Text(column3, height=1, width=max_letters)
textbox.insert("1.0", my_letter_sceme)
textbox.grid(row=31, column=0)

button = tk.Button(column3, text="show characters", command=store_characters)
button.grid(row=32, column=0)

checkbox = tk.Checkbutton(column3, state=tk.DISABLED)
checkbox.grid(row=33, column=1)

textbox_heading_n = tk.Label(column3, text='Input number of cubes that you want to memorize:')
textbox_heading_n.grid(row=34, column=0)

textbox_n = tk.Text(column3, height=1, width=3)
textbox_n.insert("1.0", initial_cube_number)
textbox_n.grid(row=35, column=0)

button_n = tk.Button(column3, text="Save Number of Cubes", command=configure_number_of_cubes)
button_n.grid(row=36, column=0)

checkbox_n = tk.Checkbutton(column3, state=tk.DISABLED)
checkbox_n.grid(row=37, column=1)

#########################################  column3 end #################################################
#########################################  END WIDGETS #################################################

column0.grid(row=0, column=0)
column1.grid(row=0, column=1)
column2.grid(row=0, column=2)
column3.grid(row=0, column=3)

root.mainloop()



'''
# developer settings (de-comment to get access to debugging buttons) and add before root-mainloop()

def print_array():
    output_text = ', '.join(letter_scheme) 
    output_label.config(text=output_text)

spacing = tk.Label(column3, text='Developer Settings: (Debugging)')
spacing.grid(row=30, column=0)

print_button = tk.Button(column3, text="Show saved letter sceme", command=print_array)
print_button.grid(row=31, column=0)

output_label = tk.Label(column3, text="")
output_label.grid(row=32, column=0)

random_button = tk.Button(column3, text="Print # of edge-/corner-letters", command=select_value_with_probability)
random_button.grid(row=33, column=0)

compare_button = tk.Button(column3, text="Compare and check", command=compare_arrays)
compare_button.grid(row=34, column=0)

compare_button = tk.Button(column3, text="Check result", command=check)
compare_button.grid(row=35, column=0)

# developer settings end
'''





