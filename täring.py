import random
import time

täringud = {
    1: [
        "+-------+",
        "|       |",
        "|   o   |",
        "|       |",
        "+-------+"
    ],
    2: [
        "+-------+",
        "| o     |",
        "|       |",
        "|     o |",
        "+-------+"
    ],
    3: [
        "+-------+",
        "| o     |",
        "|   o   |",
        "|     o |",
        "+-------+"
    ],
    4: [
        "+-------+",
        "| o   o |",
        "|       |",
        "| o   o |",
        "+-------+"
    ],
    5: [
        "+-------+",
        "| o   o |",
        "|   o   |",
        "| o   o |",
        "+-------+"
    ],
    6: [
        "+-------+",
        "| o   o |",
        "| o   o |",
        "| o   o |",
        "+-------+"
    ]
}

print("🎲 TÄRINGU MÄNG 🎲")

while True:
    input("\nVajuta ENTER, et veeretada...")

    tulemus = random.randint(1, 6)

    print("\nVeeretad täringut...\n")
    time.sleep(0.5)

    for rida in täringud[tulemus]:
        print(rida)

    print(f"\nSaid tulemuseks: {tulemus}!")

    if input("\nKas mängime veel? (j/e): ").lower() != "j":
        print("\nAitäh mängimast! 👋")
        break
    