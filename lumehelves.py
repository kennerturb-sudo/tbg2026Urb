import turtle

ekraan = turtle.Screen()
ekraan.bgcolor("midnightblue")
ekraan.title("Minu lumehelves")

t = turtle.Turtle()
t.color("lightblue")
t.pensize(3)
t.speed(0)

def haru():
    for i in range(3):
        t.forward(25)

        t.left(45)
        t.forward(20)
        t.backward(20)

        t.right(90)
        t.forward(20)
        t.backward(20)

        t.left(45)

    t.forward(25)
    t.backward(100)

for i in range(7):
    haru()
    t.right(360 / 7)

t.hideturtle()
turtle.done()