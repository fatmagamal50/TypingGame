import random
import sys
from math import cos, sin
from OpenGL.GL import *
from OpenGL.GLUT import *

# Game variables
words = []
line_position = 50
game_over = False
score = 0
buffer = ""
speed=0.2
cu=0
speed_cu=speed
longest_streak = 0
words_dropped = 0
correct_words = 0 
is_paused = False

# Word class
class Word:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.width = len(text) * 10  # Adjust the width based on the word's length
        self.height = 40
        self.rotation_angle = 0  # Initialize rotation angle to 0

    def draw(self):
        glColor3f(1.0, 1.0, 1.0)  # Set color to white
        glPushMatrix()  # Push the current matrix onto the stack
        glTranslatef(self.x, self.y, 0)  # Translate to the word's position
        glRotatef(self.rotation_angle, 0, 0, 1)  # Rotate around the z-axis
        glRasterPos2f(-self.width / 2, 0)  # Set position for drawing
        for character in self.text:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))  # Draw each character
        glPopMatrix()  # Pop the previous matrix from the stack

    def update(self):
        global speed
        self.y -= speed  # Update word's position (move it downwards)
        if score >= 60:
            self.rotation_angle += 2  # Increase rotation angle by 2 degrees

# Create new word at a random position
def create_word():
    words.append(Word("example", 100, 400))
    words.append(Word("dina", 150, 440))
    words.append(Word("fatma", 200, 500))
    words.append(Word("soha", 250, 570))
    words.append(Word("ahmed", 300, 650))
    words.append(Word("menna", 350, 700))
    words.append(Word("rana", 400, 750))
    words.append(Word("samar", 420, 780))
    

# Check collision between word and line
def check_collision(word):
    global game_over, longest_streak, words_dropped
    
    if (
        word.x < line_position + 400 +50 and
        word.x + word.width > line_position-50 and
        word.y < 100 and
        word.y + word.height > 100
    ):
        game_over = True
        longest_streak = score // 10  # Each correct word adds 10 to the score
        return True
    
    return False

# Display callback function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    if not is_paused:
        if not game_over:
            global speed,cu,speed_cu
            if speed==0:
                speed=speed_cu
        
            # Draw words
            for word in words:
                word.draw()
            
            # Draw line
            glColor3f(0.0, 0.0, 0.0)  # Set color to green
            glBegin(GL_LINES)
            glVertex2f(line_position-50, 100)
            glVertex2f(line_position + 400+50, 100)
            glEnd()

            # draw rocket
            glColor3f(0.0,1.0,0.0)
            glBegin(GL_POLYGON)
            glVertex2f(250,110)
            glVertex2f(275,90)
            glVertex2f(275,10)
            glVertex2f(300,20)
            glVertex2f(200,20)
            glVertex2f(225,10)
            glVertex2f(225,90)
            glEnd()
            
            # Draw score
            glColor3f(1.0, 1.0, 1.0)  # Set color to white
            glRasterPos2f(10, 10)  # Set position for drawing score
            score_text = "Score: {}".format(score)
            for character in score_text:
                glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))  # Draw each character
            
            # Draw buffer
            glRasterPos2f(10, 30)  # Set position for drawing buffer
            buffer_text = "Buffer: {}".format(buffer)
            for character in buffer_text:
                glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))  # Draw each character
            
            # Draw white dots moving up
            glColor3f(1.0, 1.0, 1.0)  # Set color to white
            glPointSize(3.0)  # Set point size
            glBegin(GL_POINTS)
            for i in range(30):
                x = random.randint(0, 500)
                y = random.randint(0, 500)
                glVertex2f(x, y)
            glEnd()
            if cu==60:
                speed+=0.2
                speed_cu=speed
                cu=0
                create_word()
        # print(cu)        


        else:
            display_game_over()
    else:
        glClear(GL_COLOR_BUFFER_BIT)
        # Display a "Paused" message
        
        speed=0
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(500 / 2 - 60, 500 / 2)
        glutBitmapString(GLUT_BITMAP_HELVETICA_18, b"Paused")
    
    glutSwapBuffers()

# Update callback function
def update(value):
    global game_over, score, buffer, words_dropped,cu
    
    if not game_over:
        for word in words:
            word.update()
            
            if check_collision(word):
                words.remove(word)
                score += 0
                cu+=10
                words_dropped += 1
                break
        
        glutPostRedisplay()
        glutTimerFunc(10, update, 0)
    else:
        display_game_over()


# Keyboard callback function
def keyboard(key, x, y):
    global buffer,is_paused
    
    if key == b"q":
        sys.exit()
    elif key == b'\r':
        process_buffer()
    elif key == b'\b':
        buffer = buffer[:-1]
    elif key.isalpha():
        buffer += key.decode()
    elif key== b' ':
        is_paused = not is_paused
    

# Process entered buffer
def process_buffer():
    global buffer, words, score, correct_words,cu

    for word in reversed(words):
        if word.text == buffer:
            words.remove(word)
            score += 10
            cu+=10
            # correct_words += 1
            break

    buffer = ""


# Display game-over message and statistics
def display_game_over():
    glClear(GL_COLOR_BUFFER_BIT)
    
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    
    # Draw game-over message
    game_over_text = "Game Over"
    glRasterPos2f(250 - len(game_over_text) * 5, 250)
    for character in game_over_text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))
    
    # Draw score
    score_text = "Score: {}".format(score)
    glRasterPos2f(250 - len(score_text) * 5, 220)
    for character in score_text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))
    
    # Draw longest streak
    streak_text = "Longest Streak: {}".format(longest_streak)
    glRasterPos2f(250 - len(streak_text) * 5, 160)
    for character in streak_text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(character))
    
    glutSwapBuffers()

# Initialize OpenGL
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutCreateWindow(b"ZType")
glutDisplayFunc(display)
glutTimerFunc(10, update, 0)
glutKeyboardFunc(keyboard)
glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color to black
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, 500, 0, 500, -1, 1)  # Update the width to match the screen width
create_word()

glutMainLoop()