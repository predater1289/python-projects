import tkinter as tk
import random

# -------------------- GLOBAL VARIABLES --------------------
team1_name = ""
team2_name = ""

team1_players = []
team2_players = []

team1_player_scores = [0]*5
team2_player_scores = [0]*5

team1_wickets = 0
team2_wickets = 0

current_team = 1
current_player_index = 0

team1_score = 0
team2_score = 0

balls = 0
total_balls = 0

running = False
current_result = None

outcomes = [1, 2, 3, 4, 5, 6, "OUT", "CATCH OUT", "LBW"]

# -------------------- FUNCTIONS --------------------

def get_valid_overs(value):
    options = [1, 2, 5, 10, 15, 20]
    value = int(value)
    return min(options, key=lambda x: abs(x - value))


def start_match():
    global team1_name, team2_name, team1_players, team2_players
    global total_balls, team1_player_scores, team2_player_scores
    global team1_score, team2_score, balls, current_team, current_player_index
    global team1_wickets, team2_wickets

    team1_name = team1_entry.get()
    team2_name = team2_entry.get()

    team1_players = [p.get() for p in team1_entries]
    team2_players = [p.get() for p in team2_entries]

    team1_player_scores = [0]*5
    team2_player_scores = [0]*5

    team1_score = 0
    team2_score = 0

    team1_wickets = 0
    team2_wickets = 0

    balls = 0
    current_team = 1
    current_player_index = 0

    overs = get_valid_overs(overs_scale.get())
    total_balls = overs * 6

    setup_frame.pack_forget()
    game_frame.pack()

    update_display()


def update_display():
    if current_team == 1:
        team_label.config(text=f"{team1_name} Batting")
        player_label.config(text=f"Batsman: {team1_players[current_player_index]}")
        score_label.config(text=f"{team1_score}/{team1_wickets}")
        target_label.config(text="")
    else:
        team_label.config(text=f"{team2_name} Batting")
        player_label.config(text=f"Batsman: {team2_players[current_player_index]}")
        score_label.config(text=f"{team2_score}/{team2_wickets}")

        target = team1_score + 1
        balls_left = total_balls - balls
        runs_needed = target - team2_score

        target_label.config(
            text=f"🎯 Target: {target} | Need {runs_needed} in {balls_left} balls"
        )

    overs_label.config(text=f"Balls: {balls}/{total_balls}")


def start_game():
    global running
    running = True
    apply_btn.config(state="disabled")
    change_result()


def stop_game():
    global running
    running = False
    apply_btn.config(state="normal")


def change_result():
    global running, current_result
    if running:
        current_result = random.choice(outcomes)
        result_label.config(text=str(current_result))
        root.after(100, change_result)


def apply_result():
    global balls, current_player_index, current_team
    global team1_score, team2_score, current_result, running
    global team1_wickets, team2_wickets

    if running or current_result is None:
        return

    if balls >= total_balls:
        switch_innings()
        return

    balls += 1

    if isinstance(current_result, int):
        if current_team == 1:
            team1_score += current_result
            team1_player_scores[current_player_index] += current_result
        else:
            team2_score += current_result
            team2_player_scores[current_player_index] += current_result

            if team2_score >= team1_score:
                show_result()
                return
    else:
        if current_team == 1:
            team1_wickets += 1
        else:
            team2_wickets += 1

        current_player_index += 1

        if current_player_index >= 5:
            switch_innings()
            current_result = None
            return

    update_display()

    current_result = None
    result_label.config(text="▶ Press Start")
    apply_btn.config(state="disabled")


def switch_innings():
    global current_team, current_player_index, balls

    if current_team == 1:
        current_team = 2
        current_player_index = 0
        balls = 0
        result_label.config(text="2nd Innings 🏏")
    else:
        show_result()

    update_display()


def show_result():
    game_frame.pack_forget()
    result_frame.pack()

    if team1_score > team2_score:
        winner = team1_name
    elif team2_score > team1_score:
        winner = team2_name
    else:
        winner = "Match Draw"

    text = f"{team1_name}: {team1_score}/{team1_wickets}\n"
    for i in range(5):
        text += f"{team1_players[i]} - {team1_player_scores[i]} runs\n"

    text += "\n"

    text += f"{team2_name}: {team2_score}/{team2_wickets}\n"
    for i in range(5):
        text += f"{team2_players[i]} - {team2_player_scores[i]} runs\n"

    text += f"\n🏆 Winner: {winner}"

    result_text.config(text=text)

# -------------------- UI --------------------

root = tk.Tk()
root.title("🏏 Cricket Game")
root.geometry("520x650")
root.configure(bg="#1e7f3f")  # green ground

# ----------- SETUP FRAME -----------
setup_frame = tk.Frame(root, bg="#1e7f3f")
setup_frame.pack()

def label(text):
    return tk.Label(setup_frame, text=text, bg="#1e7f3f", fg="white", font=("Arial", 12, "bold"))

label("Team 1 Name").pack()
team1_entry = tk.Entry(setup_frame)
team1_entry.pack()

team1_entries = []
for i in range(5):
    e = tk.Entry(setup_frame)
    e.insert(0, f"T1_Player{i+1}")
    e.pack()
    team1_entries.append(e)

label("Team 2 Name").pack()
team2_entry = tk.Entry(setup_frame)
team2_entry.pack()

team2_entries = []
for i in range(5):
    e = tk.Entry(setup_frame)
    e.insert(0, f"T2_Player{i+1}")
    e.pack()
    team2_entries.append(e)

label("Select Overs").pack()

overs_scale = tk.Scale(setup_frame, from_=1, to=20, orient="horizontal", length=300)
overs_scale.pack()
overs_scale.set(1)

overs_display = tk.Label(setup_frame, text="Overs: 1", bg="#1e7f3f", fg="yellow")
overs_display.pack()

def update_overs_label(val):
    overs_display.config(text=f"Overs: {get_valid_overs(val)}")

overs_scale.config(command=update_overs_label)

tk.Button(setup_frame, text="Start Match 🏏", bg="orange", command=start_match).pack(pady=10)

# ----------- GAME FRAME -----------
game_frame = tk.Frame(root, bg="#1e7f3f")

team_label = tk.Label(game_frame, font=("Arial", 16, "bold"), bg="#1e7f3f", fg="white")
team_label.pack()

target_label = tk.Label(game_frame, font=("Arial", 13), bg="#1e7f3f", fg="yellow")
target_label.pack()

player_label = tk.Label(game_frame, font=("Arial", 14), bg="#1e7f3f", fg="white")
player_label.pack()

score_label = tk.Label(game_frame, font=("Arial", 28, "bold"), bg="#1e7f3f", fg="cyan")
score_label.pack()

overs_label = tk.Label(game_frame, font=("Arial", 12), bg="#1e7f3f", fg="white")
overs_label.pack()

result_label = tk.Label(game_frame, text="▶ Press Start", font=("Arial", 22, "bold"), bg="#1e7f3f", fg="white")
result_label.pack(pady=20)

tk.Button(game_frame, text="Start ▶", bg="green", fg="white", command=start_game).pack(side="left", padx=10)
tk.Button(game_frame, text="Stop ⏹", bg="red", fg="white", command=stop_game).pack(side="left", padx=10)

apply_btn = tk.Button(game_frame, text="Apply ✔", bg="blue", fg="white", command=apply_result, state="disabled")
apply_btn.pack(side="left", padx=10)

# ----------- RESULT FRAME -----------
result_frame = tk.Frame(root, bg="#1e7f3f")

result_text = tk.Label(result_frame, font=("Arial", 14), bg="#1e7f3f", fg="white", justify="left")
result_text.pack()

# -------------------- RUN --------------------
root.mainloop()