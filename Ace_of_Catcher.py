import time
import random

class Pitcher:
    def __init__(self, name, control, confidence, proficiency, best_position):
        self.name = name
        self.control = control
        self.confidence = confidence
        self.proficiency = proficiency
        self.best_position = best_position
        self.pitches_thrown = 0
        self.strike_count = 0
        self.ball_count = 0
        self.hits_allowed = 0
        self.runs_allowed = 0
        self.walks = 0
        self.hit_by_pitch = 0
        self.strikeouts = 0
        self.outs_recorded = 0

    def improve_proficiency(self, pitch_type):
        if pitch_type in self.proficiency:
            self.proficiency[pitch_type] = min(100, self.proficiency[pitch_type] + 3)

    def decrease_confidence(self, reason="default"):
        if reason == "hit_by_pitch":
            self.confidence = max(0, self.confidence - 30)
        elif reason == "home_run":
            self.confidence = max(0, self.confidence - 40)
        elif reason == "hit":
            self.confidence = max(0, self.confidence - 5)
        else:
            self.confidence = max(0, self.confidence - 5)

    def get_pitch_accuracy(self, pitch_type, location, perf_mod):
        control = self.control
        confidence = self.confidence
        proficiency = self.proficiency[pitch_type]
        best_bonus = 0
        if location == self.best_position:
            best_bonus = 10
        return (0.4 * control + 0.4 * proficiency + 0.2 * confidence + best_bonus) * perf_mod

    def display_attributes(self):      
        print(f"🎖 {self.name} Attributes:")
        print(f"Control: {self.control}, Confidence: {self.confidence}, Best Position: {self.best_position}")
        print(f'Proficiency: Fastball: {self.proficiency["fastball"]}, Slider: {self.proficiency["slider"]}, Changeup: {self.proficiency["changeup"]}')

    def display_records(self):
        print(f"Thrown Pitches: {self.pitches_thrown}, Count of Ball: {self.ball_count}, Count of Strikes: {self.strike_count}")

def generate_pitcher(style="balanced"):
    descriptions = {
        "power": ("Kiyomine", "Power pitcher with explosive fastballs and intimidating presence."),
        "crafty": ("Narumiya", "Crafty ace known for his precise control and wicked off-speed pitches."),
        "balanced": ("Toudou", "Balanced pitcher with excellent control and well-rounded pitch arsenal.")
    }
    if style == "power":
        name, desc = descriptions["power"]
        print(f"🛡️ Pitcher Selected: {name} - {desc}")
        return Pitcher(
            name,
            control = random.randint(70, 80),
            confidence = 100,
            proficiency = {
                "fastball": random.randint(80, 95), 
                "slider": random.randint(50, 70), 
                "changeup": random.randint(55, 75)
                },
            best_position = "high_inside"
        )
    elif style == "crafty":
        name, desc = descriptions["crafty"]
        print(f"🛡️ Pitcher Selected: {name} - {desc}")
        return Pitcher(
            name,
            control = random.randint(85, 95),
            confidence = 90,
            proficiency = {
                "fastball": random.randint(65, 80),
                "slider": random.randint(70, 90), 
                "changeup": random.randint(75, 95)
                },
            best_position = "low_outside"
        )
    else: 
        name, desc = descriptions["balanced"]
        print(f"🛡️ Pitcher Selected: {name} - {desc}")
        return Pitcher(
            name,
            control = random.randint(75, 85),
            confidence = 95,
            proficiency = {
                "fastball": random.randint(75, 90),
                "slider": random.randint(65, 80),
                "changeup": random.randint(70, 85)
            },
            best_position = random.choice(["high_inside", "low_inside", "high_outside", "low_outside"])
        )

class Batter:
    def __init__(self, name, reaction, contact, power, discipline, speed):
        self.name = name
        self.reaction = reaction
        self.contact = contact
        self.power = power
        self.discipline = discipline
        self.speed = speed
        self.memory = []
        self.strikes = 0
        self.balls = 0
        self.on_base = False

    def should_swing(self, pitch_zone, pitch_type):
        base_score = 0.6 * self.discipline + 0.4 * self.reaction
        if pitch_zone == "middle":
            zone_mod = 1.1
        elif pitch_zone == "corner":
            zone_mod = 1.0 + (self.reaction - 70) / 200
        elif pitch_zone == "ball":
            zone_mod = 0.6 + (100 - self.discipline) / 250
        else:
            zone_mod = 1.0

        if pitch_type == "fastball":
            pitch_mod = 1.0
        elif pitch_type == "slider":
            pitch_mod = 1.1
        elif pitch_type == "changeup":
            pitch_mod = 0.9
        else:
            pitch_mod = 1.0

        memory_bias = 0
        for past_type, outcome in self.memory:
            if past_type == pitch_type:
                if outcome == "no_swing":
                    memory_bias += 5
                elif outcome == "contact":
                    memory_bias += 15
                elif outcome == "miss":
                    memory_bias -= 5

        final_score = base_score * zone_mod * pitch_mod + memory_bias
        return final_score >= 70

    def contact_score(self, pitch_type, contact_difficulty):
        base = 0.4 * self.contact + 0.3 * self.reaction + 0.3 * self.power
        memory_bias = 0
        for past_type, outcome in self.memory:
            if past_type == pitch_type:
                if outcome == "no_swing":
                    memory_bias += 5
                elif outcome == "contact":
                    memory_bias += 15
                elif outcome == "miss":
                    memory_bias -= 5
        adjusted_score = (base + memory_bias) / contact_difficulty
        return adjusted_score

    def display_attributes(self):
        print(f"🗒️ {self.name} Attributes:")
        print(f"Reaction: {self.reaction}, Contact: {self.contact}, Power: {self.power}")
        print(f"Discipline: {self.discipline}, Speed: {self.speed}")

def generate_batter(order):
    if order == 1:
        return Batter("Kuramochi", random.randint(70, 85), random.randint(65, 75),  random.randint(50, 65), random.randint(60, 75), random.randint(90, 100))
    elif order == 2:
        return Batter("Kominato", random.randint(85, 95), random.randint(85, 95),  random.randint(45, 60), random.randint(85, 95), random.randint(70, 85))
    elif order == 3:
        return Batter("Isashiki", random.randint(70, 85), random.randint(80, 90),  random.randint(75, 90), random.randint(65, 80), random.randint(70, 80))
    elif order == 4:
        return Batter("Yuki", random.randint(75, 90), random.randint(85, 95),  random.randint(85, 100), random.randint(75, 90), random.randint(60, 75))
    elif order == 5:
        return Batter("Masuko", random.randint(60, 75), random.randint(70, 80),  random.randint(85, 95), random.randint(55, 70), random.randint(55, 70))
    elif order == 6:
        return Batter("Miyuki", random.randint(90, 100), random.randint(90, 100),  random.randint(70, 85), random.randint(90, 100), random.randint(65, 80))
    elif order == 7:
        return Batter("Furuya", random.randint(55, 70), random.randint(60, 75),  random.randint(90, 100), random.randint(50, 65), random.randint(65, 75))
    elif order == 8:
        return Batter("Shirasu", random.randint(70, 80), random.randint(75, 85),  random.randint(55, 70), random.randint(70, 80), random.randint(70, 80))
    elif order == 9:
        return Batter("Sawamura", random.randint(50, 65), random.randint(55, 65),  random.randint(45, 60), random.randint(50, 65), random.randint(65, 80))

class GameEngine:
    def __init__(self):
        self.bases = [None, None, None]
        self.score = 0  # first, second, third base
        style = self.choose_pitcher_style()
        self.pitcher = generate_pitcher(style)
        self.pitcher.display_attributes()
        self.batters = [generate_batter(i + 1) for i in range(9)]
        self.current_batter_index = 0
        self.pitch_difficulty_table = {
            "fastball": {
                "high_inside": 1.1, "low_inside": 0.9,
                "high_outside": 0.8, "low_outside": 1.0
            },
            "slider": {
                "high_inside": 0.8, "low_inside": 1.1,
                "high_outside": 1.1, "low_outside": 1.2
            },
            "changeup": {
                "high_inside": 0.7, "low_inside": 1.1,
                "high_outside": 0.9, "low_outside": 1.3
            }
        }
        self.contact_difficulty_table = {
            "fastball": {
                "high_inside": 0.9, "low_inside": 1.0,
                "high_outside": 0.95, "low_outside": 1.0
            },
            "slider": {
                "high_inside": 1.1, "low_inside": 1.0,
                "high_outside": 1.2, "low_outside": 1.1
            },
            "changeup": {
                "high_inside": 1.3, "low_inside": 1.0,
                "high_outside": 1.2, "low_outside": 1.1
            }
        }

    def choose_pitcher_style(self):
        print("Choose your pitcher style:")
        print("1 - Power")
        print("2 - Crafty")
        print("3 - Balanced")
        while True:
            choice = input("Enter choice (1/2/3): ")
            if choice == "1":
                return "power"
            elif choice == "2":
                return "crafty"
            elif choice == "3":
                return "balanced"
            else:
                print("Invalid. Please choose 1, 2, or 3.")
  
    def pitch_sequence(self, pitch_type, location, batter):
        self.pitcher.pitches_thrown += 1
        control = self.pitcher.control
        proficiency = self.pitcher.proficiency[pitch_type]
        confidence = self.pitcher.confidence
        best_bonus = 0 
        if location == self.pitcher.best_position:
            best_bonus = 10
        perf_mod = self.pitch_difficulty_table[pitch_type][location]

        accuracy_score = (0.4 * control + 0.4 * proficiency + 0.2 * confidence + best_bonus) * perf_mod

        if accuracy_score >= 85 and location == self.pitcher.best_position:
            pitch_result = "perfect"
        elif accuracy_score >= 65:
            pitch_result = "middle"
        else:
            pitch_result = "ball"
            if accuracy_score < 30:
                print("Hit by pitch!")
                self.pitcher.ball_count += 1
                self.pitcher.hit_by_pitch += 1
                self.pitcher.decrease_confidence("hit_by_pitch")
                batter.memory.append((pitch_type, "contact"))
                batter.on_base = True
                return "on_base"

        print(f"🎯 Pitch result: {pitch_result.upper()}!")

        if pitch_result == "perfect":
            zone = "corner"
        elif pitch_result == "middle":
            zone = "middle"
        else:
            zone = "ball"

        swing = batter.should_swing(zone, pitch_type)
        if not swing:
            print("Batter does not swing.")
            if pitch_result == "ball":
                batter.balls += 1
                self.pitcher.ball_count += 1
            else:
                batter.strikes += 1
                self.pitcher.strike_count += 1
            batter.memory.append((pitch_type, "no_swing"))
            return

        print("Batter swings!")

        contact_difficulty = self.contact_difficulty_table[pitch_type][location]
        final_contact = batter.contact_score(pitch_type, contact_difficulty)

        if final_contact < 70:
            print("Swing and miss!")
            batter.strikes += 1
            self.pitcher.strike_count += 1
            print("Result: MISS")
            batter.memory.append((pitch_type, "miss"))
            return

        if final_contact >= 95:
            hit_type = "home_run"
            self.pitcher.runs_allowed += 1
            batter.on_base = True
            self.pitcher.decrease_confidence("home_run")
            print("HOME RUN!")
            return "on_base"
        elif final_contact >= 85:
            hit_type = "line_drive"
            self.pitcher.hits_allowed += 1
            batter.on_base = True
            self.pitcher.decrease_confidence("hit")
            print("HIT: Outfield Single!")
            return "on_base"
        elif final_contact >= 75:
            hit_type = "ground_ball"
            batter.on_base = batter.speed >= 80
            print("The ball is HIT INTO THE INFIELD!")
            if batter.on_base:
                self.pitcher.hits_allowed += 1
                self.pitcher.decrease_confidence("hit")
                print("HIT: Infield Single!")
                return "on_base"
            else:
                print("On base FAILED.")
                return "out"
        else:
            hit_type = "foul"
            print("FOUL BALL!")
            if batter.strikes < 2:
                batter.strikes += 1
            self.pitcher.strike_count += 1
            batter.memory.append((pitch_type, "contact"))
            return

        batter.strikes = 0
        batter.balls = 0
        batter.memory.append((pitch_type, "contact"))
        return "on_base"

    def check_steal(self):
        steal_failed = False
        for i in [2, 1, 0]:
            runner = self.bases[i]
            if runner and runner.speed > 80 and i < 2 and self.bases[i + 1] is None:
                next_base = ['SECOND', 'THIRD', 'HOME'][i]
                print(f"{runner.name} attempts to STEAL {next_base} base!")
                input("⚠️ Catcher, press ENTER to prepare...")
                start = time.time()
                input("NOW! Press ENTER again quickly!")
                end = time.time()
                reaction = end - start
                if reaction <= 0.5:
                    print(f"Caught stealing! {runner.name} is OUT.")
                    self.bases[i] = None
                    steal_failed = True
                else:
                    print(f"{runner.name} SUCCESSFULLY STEALS {next_base} base!")
                    runner.speed = max(0, runner.speed - 10)
                    self.bases[i + 1] = runner
                    self.bases[i] = None
        if steal_failed:
            return "fail"
        else:
            return "success"

    def update_bases(self, batter):
        if self.bases[2]:
            print(f"RUN SCORES from third! ({self.bases[2].name})")
            self.score += 1
            if self.score >= 3:
                print("💥 3 RUNS ALLOWED! YOU LOSE! THE INNING ENDS EARLY.")
        self.bases[2] = self.bases[1]
        self.bases[1] = self.bases[0]
        self.bases[0] = batter

    def display_bases(self):
        labels = ['1st', '2nd', '3rd']
        for i, base in enumerate(self.bases):
            if base:
                print(f"{labels[i]} base: {base.name}")
            else:
                print(f"{labels[i]} base: Empty")

    def play_inning(self):
        outs = 0
        on_base = 0
        batter_descriptions = {
            "Kuramochi": "Speedster leadoff, always a base-stealing threat.",
            "Kominato": "Consistent contact hitter, patient and sharp-eyed.",
            "Isashiki": "Aggressive swinger with solid mid-range power.",
            "Yuki": "Clean-up slugger with power and leadership.",
            "Masuko": "Power bat, capable of driving in runs with long balls.",
            "Miyuki": "Star catcher, master of reading pitchers.",
            "Furuya": "Pitcher-turned-batter with raw power.",
            "Shirasu": "Reliable utility hitter, consistent and smart.",
            "Sawamura": "Pitcher batting ninth, unpredictable but enthusiastic."
        }
        batter_count = 0
        while outs < 3 and self.score < 3:
            batter = self.batters[self.current_batter_index % 9]
            print(f"\n🧢 NOW BATTING: {batter.name} (#{self.current_batter_index % 9 + 1})")
            print(f"{batter_descriptions[batter.name]}")
            batter.display_attributes()
            while True:
                show_stats = input("Show pitcher stats before pitching? (y/n): ").lower()
                if show_stats == "y":
                    self.pitcher.display_attributes()
                    self.pitcher.display_records()
                    break
                else:
                    break
            
            while batter.balls < 4 and batter.strikes < 3 and not batter.on_base:
                print("\n⚾ Choose pitch type:")
                print("1 - Fastball")
                print("2 - Slider")
                print("3 - Changeup")
                pitch_type = None
                while True:
                    pitch_choice = input("Enter choice (1/2/3 or Q to quit): ").lower()
                    if pitch_choice == "q":
                        print("Game exited by player.")
                        exit()
                    if pitch_choice == "1":
                        pitch_type = "fastball"
                    elif pitch_choice == "2":
                        pitch_type = "slider"
                    elif pitch_choice == "3":
                        pitch_type = "changeup"
                    else:
                        print("Invalid. Please choose 1, 2, or 3.")
                    if pitch_type in ["fastball", "slider", "changeup"]:
                        break

                print("🎯 Choose pitch location:")
                print("1 - High Inside")
                print("2 - Low Inside")
                print("3 - High Outside")
                print("4 - Low Outside")
                location = None
                while True:
                    loc_choice = input("Enter choice (1/2/3/4 or Q to quit): ").lower()
                    if loc_choice == "q":
                        print("Game exited by user.")
                        exit()
                    if loc_choice == "1":
                        location = "high_inside"
                    elif loc_choice == "2":
                        location = "low_inside"
                    elif loc_choice == "3":
                        location = "high_outside"
                    elif loc_choice == "4":
                        location = "low_outside"
                    else:
                        print("Invalid. Please choose 1, 2, 3, or 4.")
                    if location in ["high_inside", "low_inside", "high_outside", "low_outside"]:
                        break

                result = self.pitch_sequence(pitch_type, location, batter)
                print(f"📊 Count: {batter.strikes} Strikes, {batter.balls} Balls")
                if result == "out":
                    outs += 1
                    break
                elif result == "on_base":
                    self.update_bases(batter)                    
                    on_base += 1
                    steal_result = self.check_steal()
                    if steal_result == "fail":
                        outs += 1
                        on_base -= 1
                    # self.display_bases()
                    break

            if batter.balls >= 4:
                print("WALK! The batter takes first base.")
                batter.on_base = True
                on_base += 1
                self.update_bases(batter)
                steal_result = self.check_steal()
                if steal_result == "fail":
                    outs += 1
                    on_base -= 1
                if self.score >= 3:
                    break
            elif batter.strikes >= 3:
                print("STRIKEOUT!")
                outs += 1     
                if outs >= 3:
                    break       

            print("--- Current base situation ---")
            self.display_bases()
            base_runners = 0
            for runner in self.bases:
                if runner != None:
                    base_runners += 1            
            print(f"Runners on base: {base_runners}, Outs: {outs}, Runs Allowed: {self.score}")
            self.current_batter_index += 1

        print(f"\n⚾ Inning complete. Total Runs Allowed: {self.score}, Outs: {outs}")
        print("\nPitcher Final Stats:")
        print(f"🎯 Strikes Thrown: {self.pitcher.strike_count}")
        print(f"🎯 Balls Thrown:   {self.pitcher.ball_count}")
        print(f"💥 Hits Allowed:   {self.pitcher.hits_allowed}")
        print(f"💣 Runs Allowed:   {self.pitcher.runs_allowed}")
        print(f"🤕 Hit By Pitch:   {self.pitcher.hit_by_pitch}")

        if self.score == 0:
            print("🧤 Congratulation! Flawless battery work! You and the pitcher shut Seido down completely!")
        elif self.score == 1:
            print("🎯 Sharp calling and calm nerves — you guided your pitcher to a tight win!")
        elif self.score == 2:
            print("🛡️ A bit shaky, but your game sense as catcher saved the inning!")
        else:
            print("⚠️ Too many runs slipped by. Review your calls and protect the zone better next time!")

print("🎉 Welcome to *Ace of Catcher*! Let's defeat the team from Seido together!💪")

if __name__ == "__main__":
    game = GameEngine()
    input("🌟 Press ENTER to start the game!")
    print("🎬 The game begins now! Focus behind the plate!")
    game.play_inning()
