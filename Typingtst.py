from tkinter import *
from tkinter import messagebox
import requests
import random

url = "https://api.themoviedb.org/3/search/movie"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9"
                     ".eyJhdWQiOiI0MzYzNTQyNzA3NWJmYWE1NzUwMmJhZjQ5NDVhOTM0ZSIsInN1YiI6IjY1MDQ0MGJlZGI0ZWQ2MTAzM2EzZDVi"
                     "OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.FS_XNmL7TxNQbzIhlMDUi4wOAPU5hucJF-s0Z5Mm2n0"
}
random_text = ''
window = Tk()
window.title('Typing Test', )
window.geometry('1000x800')
window.config(pady=50, padx=100)

count = 60
key_trigger = 0
accuracy_count = 0
movies = ['die hard', 'harry potter','lord of the rings', 'matrix']

def api_caller(name):
    parameters = {
        'query': name,
        'language': 'en-US',
        'page': 1

    }
    response = requests.get(url, params=parameters, headers=headers)

    data = response.json()
    return data['results']


def initiate_movielist():
    global random_text
    movie_list = api_caller(random.choice(movies))
    overview_list = [i['overview'] for i in movie_list if len(i['overview'].split()) > 100]
    random_movie = random.choice(overview_list)
    if random_movie != random_text:
        random_text = random_movie
    else:
        random_text = random.choice(overview_list)
    l2.config(text=random_text)

def click(key):
    global key_trigger
    if key_trigger == 0:
        timer(count)
        key_trigger = 1
def space(e):
    user_in = e1.get('1.0', END).split()
    correct = random_text.split()

    for i, y in zip(user_in, correct):
        word_pos = e1.search(i, '1.0', END)
        offset = '+%dc' % len(i)
        word_end = word_pos + offset
        if i != y:
            e1.tag_add('start', word_pos, word_end)
            e1.tag_config('start', foreground='red')
        else:
            e1.tag_remove('start', word_pos, word_end)


def reset():
    initiate_movielist()
    global count, key_trigger, accuracy_count
    l3.config(text='01:00')
    count = 60
    key_trigger = 0
    accuracy_count = 0
    e1.delete('1.0', END)


def timer(cnt):
    clock = window.after(1000, timer, cnt - 1)
    if cnt < 10:
        l3.config(text=f'00:0{cnt}')
    elif cnt < 60:
        l3.config(text=f'00:{cnt}')
    if cnt == 0:
        window.after_cancel(clock)
        evaluate()
        print(e1.get('1.0', END))


def evaluate():
    global accuracy_count
    random_list = random_text.split()
    user_input = e1.get('1.0', END)
    user_list = user_input.split()
    for i, y in zip(random_list, user_list):
        if i == y:
            accuracy_count += 1
    if len(user_list) < len(random_list):
        word_count = len(user_list)
        speed = word_count
    else:
        word_count = len(random_list)
        speed = user_list
    accuracy = (accuracy_count / word_count) * 100
    messagebox.showinfo(title="Results", message=f'Typing Speed: {speed} WPM\nAccuracy: {round(accuracy)}%\nAccurate '
                                                 f'words:{accuracy_count}/{word_count}')
    reset()

l3 = Label(text='01:00', font=('arial', 30), pady=30)
l3.grid(column=2, row=0)

l2 = Label(text='', wraplength=800, font=('arial', 18), pady=30, justify='left')
l2.grid(row=1, column=0, columnspan=3)

e1 = Text(width=70, height=5,padx=20, pady=20,font=('arial', 15))
e1.focus_set()
e1.bind("<Key>", click)
e1.bind('<space>', space)
e1.grid(row=2, column=0, columnspan=3)
initiate_movielist()
window.mainloop()
