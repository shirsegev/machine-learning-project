"""
This program is a survey (questionnaire) containing questions from:
'Analysis and prediction of professional sports consumer
behavior using artificial neural network'
Kyung Hee University
2011.08
Programmer: Joshua Willman
Date: 2019.11.17
"""
from tkinter import (Tk, Label, Button, Radiobutton, Frame, Menu, PhotoImage,
                     messagebox, StringVar, Listbox, BROWSE, END, Toplevel, Entry)
from tkinter import ttk
import time
import svm
import urllib.request

# create empty lists used for questions
answers_list = []


def str_to_int():
    new = []
    for num in answers_list:
        new.append(int(num))
    return new


def dialogBox(title, message):
    """
    Basic function to create and display general dialog boxes.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 225, 125
    positionRight = int(dialog.winfo_screenwidth() / 2 - dialogWidth / 2)
    positionDown = int(dialog.winfo_screenheight() / 2 - dialogHeight / 2)
    dialog.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
    dialog.maxsize(dialogWidth, dialogHeight)
    label = Label(dialog, text=message)
    label.pack(side="top", fill="x", pady=10)
    ok_button = ttk.Button(dialog, text="Yes!!!", command=dialog.destroy)
    ok_button.pack(ipady=3, pady=10)
    dialog.mainloop()


def disable_event():
    pass


class Survey(Tk):
    """
    Main class, define the container which will contain all the frames.
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # call closing protocol to create dialog box to ask
        # if user if they want to quit or not.
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        Tk.wm_title(self, "Survey")

        # get position of window with respect to screen
        windowWidth, windowHeight = 555, 400
        positionRight = int(Tk.winfo_screenwidth(self) / 2 - windowWidth / 2)
        positionDown = int(Tk.winfo_screenheight(self) / 2 - windowHeight / 2)
        Tk.geometry(self, newGeometry="{}x{}+{}+{}".format(
            windowWidth, windowHeight, positionRight, positionDown))
        Tk.maxsize(self, windowWidth, windowHeight)

        # Create container Frame to hold all other classes,
        # which are the different parts of the survey.
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create menu bar
        menubar = Menu(container)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        Tk.config(self, menu=menubar)

        # create empty dictionary for the different frames (the different classes)
        self.frames = {}

        for fr in (StartPage, MainSurvey):
            frame = fr(container, self)
            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def show_frame(self, cont):
        """
        Used to display a frame.
        """
        frame = self.frames[cont]
        frame.tkraise()  # bring a frame to the "top"


class StartPage(Frame):
    """
    First page that user will see.
    Explains the rules and any extra information the user may need
    before beginning the survey.
    User can either click one of the two buttons, Begin Survey or Quit.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        # set up start page window
        self.configure(bg="#EFF3F6")
        start_label = Label(self, text="Marijuana Addiction Predict", font=("Calibri", 30), highlightbackground="green",
                            highlightthickness=5,
                            borderwidth=2)
        start_label.pack(pady=10, padx=10, ipadx=5, ipady=3)

        purpose_text = "Smoking marijuana has become more\ncommon in recent years, and in large\nquantities can cause health and mental damage,\nand even death.\n " \
                       "Answer this survey and find out if you are addicted\nand get tips on how to take care of yourself"
        purpose_text = Label(self, text=purpose_text, font=("Calibri", 16), bg="#B2D3C2",
                             borderwidth=2)
        purpose_text.pack(pady=10, padx=10, ipadx=5, ipady=3)

        start_button = ttk.Button(self, text="Begin Survey",

                                  command=lambda: controller.show_frame(MainSurvey))
        start_button.pack(ipadx=10, ipady=15, pady=15)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.controller.destroy()


class MainSurvey(Frame):
    """
    Class that displays the window for the life style survey questions.
    When the user answers a question, the answer saved to a list.
    """

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        # img = PhotoImage(file=marijuana.png)
        # label_img = ttk.Label(self, image=img)
        # label_img.pack(side=ttk.Top)
        # Create header label
        ttk.Label(self, text="Cannabis Addiction", font=("Calibri", 30),

                  borderwidth=2).pack(padx=10, pady=10)

        self.questions = ["How often do you smoke?", "Have you increased your\nuse of drugs over time ?",
                          "If you decide to quit smoking, you..", "Do you care about the\ntype of cannabis you use?",
                          "How do you feel when you don't\nhave cannabis available immediately?", "Are there any "
                                                                                                  "activities(such "
                                                                                                  "as sex,\nsleeping,"
                                                                                                  "hanging out with "
                                                                                                  "friends, "
                                                                                                  "studying)\nthat you "
                                                                                                  "must do after / "
                                                                                                  "while smoking?",
                          "How would you describe your friends'\ncannabis use?", "What is your level of spending on "
                                                                                 "cannabis?",
                          "Have you been procrastinating or\nunmotivated since you started\nsmoking cannabis?", "Have "
                                                                                                                "you "
                                                                                                                "ever "
                                                                                                                "felt "
                                                                                                                "one of "
                                                                                                                "the "
                                                                                                                "following sensations\nduring or after cannabis use?(Anxiety,memory loss,\nimpact on body skin or other unpleasant\nphysical mental sensations)",
                          "You decided to stop using cannabis for\na while and you succeeded, what was\nthe impact?",
                          "How do you see the use of cannabis?"]

        # set index in questions list
        self.index = 0
        self.length_of_list = len(self.questions)
        print(self.length_of_list)

        # Set up labels and checkboxes
        self.question_label = Label(self, text="{}. {}".format(self.index+1, self.questions[self.index]),
                                    font=('Calibri', 16))
        self.question_label.pack(anchor='w', padx=20, pady=10)
        self.scale_text = [["Once a month,\n I do not want it\n to "
                            "affect my \nstudies / work", "Once a week, it makes\n every meeting with\n friends better",
                            "Every day,\n can not end the\n day without it"],
                           ["No, I use the same amount",
                            "I increased the amount slightly",
                            "I definitely increased\nthe amount, I need a\nlarger amount of\nmarijuana to feel stoned"],
                           ["I will do it without a problem", "I will have a desire,\nbut I will overcome ...",
                            "I will probably find\nmyself smoking again\nin a short time even\nthough I said I would "
                            "stop"],
                           ["I don't care, I smoke what is available",
                            "I prefer a certain type,\nbut it does not really\nmatter to me",
                            "Constantly looking for\nmarijuana strains that\nare considered to have\na stronger effect"],
                           ["Doesn't bother me at all",
                            "I write to myself\nthat I should buy soon",
                            "I'm stressed, nervous\nand anxious"],
                           ["Definitely not", "I don't have to\nbut it does me good",
                            "I must smoke while\ndoing one of the\nactions described"],
                           ["Mose of my friends are not smoking", "50% of my friends smoke",
                            "Most of them smoke"],
                           ["I Usually take from friends",
                            "I purchases with my money,\nbut it is not\na big expense",
                            "I spend a lot on it,\nsometimes beyond what\nI can afford"],
                           ["The use does not\naffect my functioning\nat all",
                            "When I smoke,\nI start procrastinating\non certain issues",
                            "I smoke a lot,\nI tend to procrastinate\nand unmotivated"],
                           ["I didn't feel a\nnegative impact",
                            "I take a break when\nI feel one of the\nsymptoms described",
                            "I felt some of the\nsymptoms described\nand yet I continue"],
                           ["There was no difficulty\nat all",
                            "I missed smoking,\nbut it was not\nterrible",
                            "I felt anxiety,stress\nand even depression. Life has become\nboring, uninteresting and sad."],
                           ["It is nice sometimes",
                            "It's improves my confidence\n I'm feeling more calm",
                            "If I didn't use cannabis\nI would need regular psychiatric\ntreatment. Cannabis is\nless harmful"]]

        scale = [("1", 0), ("2", 1), ("3", 2)]

        self.var = StringVar()
        self.var.set('-1')  # initialize

        # Frame to contain text
        self.checkbox_scale_frame = Frame(self, relief="ridge")
        self.checkbox_scale_frame.pack(pady=2)
        self.b1 = ttk.Label(self.checkbox_scale_frame, text=self.scale_text[self.index][0])
        self.b1.pack(side='left', ipadx=7, ipady=5)
        self.b2 = ttk.Label(self.checkbox_scale_frame, text=self.scale_text[self.index][1])
        self.b2.pack(side='left', ipadx=7, ipady=5)
        self.b3 = ttk.Label(self.checkbox_scale_frame, text=self.scale_text[self.index][2])
        self.b3.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        self.checkbox_frame = Frame(self, relief="ridge",
                                    )
        self.checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(self.checkbox_frame, text=text,
                                variable=self.var, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)

    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '-1':
            dialogBox("No Value Given",
                      "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list-1):


            selected_answer = self.var.get()
            answers_list.append(selected_answer)
            print(answers_list)
            text = "Are you ready to see how\naddicted you are?"
            messagebox.showinfo("Result", text)
            self.clearFrame()
        else:
            selected_answer = self.var.get()
            answers_list.append(selected_answer)
            self.index = (self.index + 1) % self.length_of_list
            print(self.index)

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))

            self.b1.config(text=self.scale_text[self.index][0])
            self.b2.config(text=self.scale_text[self.index][1])
            self.b3.config(text=self.scale_text[self.index][2])

            self.var.set('-1')  # reset value for next question

            time.sleep(.2)  # delay between questions

    def clearFrame(self):
        # destroy all widgets from frame
        for widget in self.winfo_children():
            widget.destroy()

        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        self.pack_forget()

        # set up start page window
        self.configure(bg="#EFF3F6")
        end_label = Label(self, text="Marijuana Addiction Predict", font=("Calibri", 30), highlightbackground="green",
                          highlightthickness=5,
                          borderwidth=2)
        end_label.pack(pady=10, padx=10, ipadx=5, ipady=3)
        # creating the results
        lst = str_to_int()
        predict = svm.prediction(lst)
        info_text = "Your rate is " + str(predict)
        info_label = Label(self, text=info_text, font=("Calibre", 14))

        info_label.pack(pady=10, padx=10, ipadx=20, ipady=3)
        if predict < 3:
            purpose_text = "Congrats!! You are not addicted,\nkeep going ;)"
            purpose_text = Label(self, text=purpose_text, font=("Calibre", 16),
                                 bg="#B2D3C2",
                                 borderwidth=2)
            purpose_text.pack(pady=10, padx=10, ipadx=5, ipady=3)
        elif 2 < predict < 5:
            purpose_text = "I can see you enjoy using marijuana..\nBe careful before it will be too late"
            purpose_text = Label(self, text=purpose_text, font=("Calibre", 14),
                                 bg="#B2D3C2",
                                 borderwidth=2)
            purpose_text.pack(pady=10, padx=10, ipadx=5, ipady=3)
        else:

            purpose_text = "You are probably addicted,\nhere's some tips you can use:\nIsrael: Ica- Israel Center On Addiction, Gmila, Tipulpsichology\nGlobal: Hazelden Betty Ford, Addiction Center"

            purpose_text = Label(self, text=purpose_text, font=("Calibre", 14), bg="#B2D3C2",
                                 borderwidth=2)
            purpose_text.pack(pady=10, padx=10, ipadx=5, ipady=3)

        quit_button = ttk.Button(self, text="Quit", command=self.on_closing)
        quit_button.pack(ipady=3, pady=10)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.controller.destroy()


# Run program
if __name__ == "__main__":
    app = Survey()
    app.mainloop()
