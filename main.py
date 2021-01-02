import tkinter as tk
import random
import time
import math
from numpy.core import isfinite, errstate

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
CANVAS_WIDTH = WINDOW_WIDTH / 2
CANVAS_HEIGHT = WINDOW_HEIGHT
POINT_RADIUS = 5
FAILURE_X = 1
FAILURE_Y = 1
RT_XPOINTS =[];
RT_YPOINTS =[];
ART_XPOINTS = [];
ART_YPOINTS = [];
ART_WINS=0;
RT_WINS=0;
not_hit = True





class MainGUI:
    def __init__(self):
        # Create window
        self.window = tk.Tk()
        self.window.title("RT vs ART")
        # Initialise frame
        self.frame = tk.Frame(master=self.window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.frame.pack()
        # Create title
        self.title = tk.Label(self.frame, text="RT and ART Testing", font=("Courier", 20))
        self.title.pack(padx=20, pady=(20, 100))
        # ART title
        self.rt_title = tk.Label(self.frame, text="RT win count: 0", font=("Courier", 15))
        self.rt_title.place(x=60, y=140)
        self.rt_status = tk.Label(self.frame, text="Test Case 0: RT - missed;", font=("Courier", 10))
        self.rt_status.place(x=20, y=120)
        # RT Title
        self.art_title = tk.Label(self.frame, text="ART win count: 0", font=("Courier", 15))
        self.art_title.place(x=700, y=140)
        self.art_status = tk.Label(self.frame, text="ART - missed", font=("Courier", 10))
        self.art_status.place(x=660, y=120)
        # Create canvas for art and rt
        self.art_canvas = self.create_canvas_art(self.frame)
        self.rt_canvas = self.create_canvas_rt(self.frame)
        # Add Button and input
        # Add failure rate
        self.failure_rate = tk.Label(self.frame, text="failure rate", font=("Courier", 10))
        self.failure_rate.place(x=250, y=70)
        self.failure_rate_input = tk.Entry(self.frame) 
        self.failure_rate_input.place(x=350, y=70)
        # Add iterations
        self.iteration = tk.Label(self.frame, text="iterations times", font=("Courier", 10))
        self.iteration.place(x=500, y=70)
        self.iterations_input = tk.Entry(self.frame)
        self.iterations_input.place(x=635, y=70)
        
        self.iteration_count = tk.Label(self.frame, text="iterations count: ", font=("Courier", 10))
        self.iteration_count.place(x=380, y=120)
        #failure_rate_input.create_window(200, 140, window=frame)
        self.run_button = tk.Button(self.frame, text="Run", command=self.run)
        self.run_button.place(x=900, y=70)
        self.window.mainloop()
    def add_random_pointRT(self) -> (int, int):
        # Random with replacement, allows duplicate sampling
        x = random.randint(0, CANVAS_WIDTH)
        y = random.randint(0, CANVAS_WIDTH)
        RT_XPOINTS.append(x)
        RT_YPOINTS.append(y)
        self.rt_canvas.create_oval(x, y, x + POINT_RADIUS, y + POINT_RADIUS, fill="white", outline="black", width=2)
        self.rt_canvas.update()
        return x, y
    def add_random_pointART(self) -> (int, int):
        # Implementing FSCS
        global ART_XPOINTS
        global ART_YPOINTS
        x = 0
        y = 0
        TEST_POINTS_X =[]
        TEST_POINTS_Y =[]
        TEST_DISTANCE = []
        if len(ART_XPOINTS) != 0:
            for i in range(10):
                TEST_POINTS_X.append(random.randint(0, CANVAS_WIDTH))
                TEST_POINTS_Y.append(random.randint(0, CANVAS_WIDTH))
                CALCULATED_DISTANCE = []
                for f in range(len(ART_XPOINTS)):               
                    CALCULATED_DISTANCE.append(math.sqrt(pow(TEST_POINTS_X[i]-ART_XPOINTS[f],2)+pow(TEST_POINTS_Y[i]-ART_YPOINTS[f],2)))
                TEST_DISTANCE.append(min(CALCULATED_DISTANCE))
            x = TEST_POINTS_X[TEST_DISTANCE.index(max(TEST_DISTANCE))]      
            y = TEST_POINTS_Y[TEST_DISTANCE.index(max(TEST_DISTANCE))]    
        else:
            x = random.randint(0, CANVAS_WIDTH)
            y = random.randint(0, CANVAS_WIDTH)            
                  
        ART_XPOINTS.append(x)
        ART_YPOINTS.append(y)        
        self.art_canvas.create_oval(x, y, x + POINT_RADIUS, y + POINT_RADIUS, fill="white", outline="black", width=2)
        self.art_canvas.update()
        return x, y
    def add_failure_point(self, canvasART, canvasRT, failin) -> (int, int):
        # Random with replacement, allows duplicate sampling
        x = random.randint(0, CANVAS_WIDTH)
        y = random.randint(0, CANVAS_WIDTH)
        global FAILURE_X 
        FAILURE_X = x
        global FAILURE_Y 
        FAILURE_Y = y
        if failin == 1:
            canvasART.configure(background='black')
            canvasRT.configure(background='black')
            return x,y
        canvasART.create_rectangle(x, y, x + (failin*POINT_RADIUS*10000), y + (failin*POINT_RADIUS*10000), fill="black", width=2)
        canvasRT.create_rectangle(x, y, x + (failin*POINT_RADIUS*10000), y + (failin*POINT_RADIUS*10000), fill="black", width=2)
        return x, y
    
    def hit(self,x,failin):
        global not_hit
        global ART_WINS
        global RT_WINS     
        self.rt_status['text'] = "Test case " + str(x+1) + " RT - missed"        
        if(RT_XPOINTS[x] in range(FAILURE_X-round(((failin*POINT_RADIUS*1000*5)+3)), FAILURE_X+round(((failin*POINT_RADIUS*1000*5)+3)))  and RT_YPOINTS[x] in range(FAILURE_Y-round(((failin*POINT_RADIUS*1000*5)+3)), FAILURE_Y+round(((failin*POINT_RADIUS*1000*5)+3)))):    
            not_hit = False
            RT_WINS+=1
            self.rt_status['text'] = "Test case " + str(x+1) + " RT - HIT!!!!"
            self.rt_title['text'] =  "RT win count: " + str(RT_WINS)
            print(RT_XPOINTS[x],RT_YPOINTS[x])
            print("RT Wins ")
            self.rt_title.update()
            self.rt_status.update()

        if(ART_XPOINTS[x] in range(FAILURE_X-round(((failin*POINT_RADIUS*1000*5)+3)), FAILURE_X+round(((failin*POINT_RADIUS*1000*5)+3)))  and ART_YPOINTS[x] in range(FAILURE_Y-round(((failin*POINT_RADIUS*1000*5)+3)), FAILURE_Y+round(((failin*POINT_RADIUS*1000*5)+3)))):    
            not_hit = False
            ART_WINS+=1
            self.art_status['text'] = "ART - HIT!!!!"
            self.art_title['text'] =  "ART win count: " + str(ART_WINS)
            print(ART_XPOINTS[x],ART_YPOINTS[x])
            print("ART Wins")
            self.art_title.update()
            self.art_status.update()

    def create_canvas_art(self, frame) -> tk.Canvas:
        art_canvas = tk.Canvas(master=frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white", highlightthickness=1, highlightbackground="black")
        art_canvas.pack(side=tk.RIGHT, anchor=tk.NW, padx=20, pady=20)
        return art_canvas

    def create_canvas_rt(self, frame) -> tk.Canvas:
        rt_canvas = tk.Canvas(master=frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white", highlightthickness=1, highlightbackground="black")
        rt_canvas.pack(side=tk.LEFT, anchor=tk.NW, padx=(20, 0), pady=20)
        return rt_canvas

    def run(self):
        global ART_WINS, RT_WINS
        ART_WINS = 0
        RT_WINS = 0
        # Get the failure rate input and iteration
        failure_rate = float(self.failure_rate_input.get())
        num_of_it = int(self.iterations_input.get())
        print("Number of iteration(s): ", num_of_it)
        self.art_canvas.configure(background='white')
        self.rt_canvas.configure(background='white')
        # Generate failure points
        # Generate random points on art canvas
        if failure_rate == 0 or failure_rate < 0.0001 or failure_rate > 1:
            print("Error please enter proper value")
            return 0,0
        global not_hit
        global RT_XPOINTS
        global RT_YPOINTS
        global ART_XPOINTS
        global ART_YPOINTS
        global art_canvas
        global rt_canvas
        for i in range(1,num_of_it+1):
            self.art_status['text'] = "ART - missed"
            self.iteration_count['text'] = "iterations count: "+ str(i)
            not_hit = True
            RT_XPOINTS.clear()
            RT_YPOINTS.clear()
            ART_XPOINTS.clear()
            ART_YPOINTS.clear()
            points_count = 0 
            self.art_canvas.delete("all")
            self.rt_canvas.delete("all")
            self.add_failure_point(self.art_canvas,self.rt_canvas,failure_rate)
            print("Error point X and Y ", FAILURE_X,FAILURE_Y)    
            print("iteration ", i)
            for i in range(1000):
                if(not_hit == True):
                    self.add_random_pointRT()
                    self.add_random_pointART()
                    self.hit(points_count,failure_rate)
                    points_count+=1
                else:
                    break
            if (not_hit):
                print("Both misses")
            # time.sleep(1)
        print("ART win counts", ART_WINS)
        print("RT win counts", RT_WINS)

           



        

if __name__ == "__main__":
    main_gui = MainGUI()