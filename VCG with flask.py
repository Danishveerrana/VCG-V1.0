from flask import Flask, request, jsonify
from turtle import Screen, Turtle
import speech_recognition as sr
import pyttsx3

# Initialize Flask app
app = Flask(__name__)

# Existing TTS and Turtle setup
def initialize_tts_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
    engine.setProperty("rate", 150)
    return engine

def speak(text, engine):
    engine.say(text)
    engine.runAndWait()

engine = initialize_tts_engine()

# Setup Turtle Graphics
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("white")
turtle = Turtle()

def draw_grid(turtle, grid_size, canvas_width, canvas_height):
    turtle.speed(0)
    turtle.penup()
    turtle.color("lightgray")
    for x in range(-canvas_width // 2, canvas_width // 2 + grid_size, grid_size):
        turtle.goto(x, canvas_height // 2)
        turtle.setheading(270)
        turtle.pendown()
        turtle.forward(canvas_height)
        turtle.penup()
    for y in range(-canvas_height // 2, canvas_height // 2 + grid_size, grid_size):
        turtle.goto(-canvas_width // 2, y)
        turtle.setheading(0)
        turtle.pendown()
        turtle.forward(canvas_width)
        turtle.penup()
    turtle.color("black")
    turtle.goto(0, 0)
    turtle.pendown()

draw_grid(turtle, grid_size=10, canvas_width=800, canvas_height=600)

# Flask routes
@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get("command", "").lower()
    value = data.get("value", 0)
    try:
        if "move" in command:
            turtle.forward(int(value))
            speak(f"Moved {value} units.", engine)
        elif "rotate" in command:
            turtle.left(int(value))
            speak(f"Rotated {value} degrees.", engine)
        elif "circle" in command:
            turtle.circle(int(value))
            speak(f"Drew a circle with radius {value}.", engine)
        elif "clear" in command:
            turtle.clear()
            draw_grid(turtle, grid_size=10, canvas_width=800, canvas_height=600)
            speak("Cleared the screen.", engine)
        elif "exit" in command:
            speak("Exiting the application.", engine)
            return jsonify({"status": "exit"})
        else:
            return jsonify({"status": "error", "message": "Unknown command"}), 400
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)