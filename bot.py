import discord
import os
import random

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!moves'):
    answer = """Enter your command + total power. So **Change the Game** with power of 3 would be: !ctg 3.
    !ctg = **Change the Game**
    !con = **Convince**
    !face = **Face Danger**
    !go = **Go Toe to Toe**
    !hit = **Hit With All You've Got**
    !inv = **Investigate**
    !sneak = **Sneak Around**
    !risk = **Take the Risk**
    !shbs = **Stop. Holding. Back. A Significant Sacrifice**
    !shbn = **Stop. Holding. Back. No Return**
    !shbu = **Stop. Holding. Back. The Ultimate Sacrifice**"""


    await message.channel.send(answer)


  moves_list = ["!ctg", "!con", "!face", "!go", "!hit", "!inv", "!sneak", "!risk", "!shbs", "!shbn", "!shbu"]
  move_dict = {"!ctg": "**Change the Game**", "!con": "**Convince**", "!face": "**Face Danger**", "!go": "**Go Toe to Toe**", "!hit": "**Hit with All You've Got**", "!inv": "**Investigate**", "!sneak": "**Sneak Around**", "!risk": "**Take the Risk**", "!shbs": "**Stop. Holding. Back. A Significant Sacrifice**", "!shbn": "**Stop. Holding. Back. No Return**", "!shbu": "**Stop. Holding. Back. The Ultimate Sacrifice**"}
  valid_move = False
  valid_pwr = True

  for move in moves_list:
    if message.content.startswith(move):
      valid_move = True
      prefix = move_dict[move] + " \n"
      break






  if valid_move == True:
    store = message.content.split()
    if len(store) > 2:
      await message.channel.send("Nah, you messed up the roll. It's \"!command power\".")
      valid_pwr = False

    elif len(store) > 1:
      pwr = store[1]

      if pwr.find('+') > -1:
        pwr = pwr[pwr.find('+') + 1:]
      try:
        pwr = int(pwr)
      except:
        valid_pwr = False
        word = ""
        i = 0
        for char in pwr:
          if i % 2:
            if type(char) == str:
              word += char.upper()
          else:
            word += char
          i += 1

        await message.channel.send("I rOlL wItH a PoWeR oF " + word + ". \n Really?")
    else:
      pwr = 0

    if valid_pwr == True:
      # roll logic
      first_die = random.randint(1, 6)
      second_die = random.randint(1, 6)
      result = first_die + second_die + pwr
      dynamite = False

      if pwr > 0:
        dice_holder =  "[{}][{}] + {} = {}:".format(first_die, second_die, pwr, result)
      elif pwr == 0:
        dice_holder = "[{}][{}] = {}:".format(first_die, second_die, result)
      else:
        pwr = str(pwr)
        pwr = pwr[pwr.find('-') + 1:]
        dice_holder = "[{}][{}] - {} = {}:".format(first_die, second_die, pwr, result)

      if result >= 10:
        lvl = "Strong Hit"
        if result >= 12:
          dynamite = True
      elif result > 6:
        lvl = "Weak Hit"
      else:
        lvl = "Miss"

      if not message.content.startswith("!face") and not message.content.startswith("!shbs") and not message.content.startswith("!shbn") and not message.content.startswith("!shbu") and lvl == "Miss":
        # Miss
        effects = """The MC chooses one of the following:
        - **Complicate Things, Bigtime:** Problematic story development, typically a new dannger.
        - **Deny Them Something They Want:** Adversaries get away. Objective becomes out of reach. Witnesses stop talking.
        - **Make Something Horrible Happen:** Beloved character dies. The personal lives of PCs are threatened. Allies turn to enemies.
        - **Turn Their Move Against Them:** Action succeeds "too well" or affects an unintended target. Unexpected side-effect or reaction on action.
        - **Give a Status**
        - **Burn a Tag**
        - **Force Them to Choose:** Select two or three outcomes, all bad, linked to a separate Hard Move. The PC can pick their poison.""".format(first_die, second_die, pwr, result)

      # Hit with All You've Got
      elif message.content.startswith("!hit"):
        if lvl == "Strong Hit":
          # Strong Hit
          if pwr == 0:
            pwr = 1
          effects = """Give the target an appropriate tier-{} status. Choose two:
          - You take cover or secure a superior position. If you don't choose this, your target can impose a status on you. If the target is a PC, the tier = their Power.
          - You get them good or get many of them (+1 tier).
          - You control the collateral damage.
          - You hold the target's attention, if possible.
          - You gain the upper hand. Take 1 Juice.
            - Create a story tag.
            - Burn a power tag or a story tag.
            - Give or reduce a status (one tier per point of Juice)""".format(pwr)

          # Dynamite
          if dynamite:
            effects += """\n \n**Dynamite!**: Choose one option from the list below:
            - Outstanding hit: Choose three options from the standard list.
            - Defend another: The target of your attack cannot attack a chosen ally on the target's next move.
            - Hit them hard: Increase the tier of the status you give by two or hitting two more targets with the same status.
            - Extreme collateral damage: Everyone and everything (including allies) takes a status similar to the main status with tier = Power.
            - Control the conflict: Take 2 Juice and you can use it to choose effect improvements from **Change the Game**.
              - Scale up the effect (greater area or more targets).
              - Prolong the effect (make it ongoing)
              - Hide the effect"""

        # Weak Hit
        elif lvl == "Weak Hit":
          if pwr == 0:
            pwr = 1
          effects = """Give the target an appropriate tier-{} status. Choose two:
          - You take cover or secure a superior position If you don't choose this, your target can impose a status on you. If the target is a PC, the tier = their Power.
          - You get them good or get many of them (+1 tier).
          - You control the collateral damage.
          - You hold the target's attention, if possible.
          - You gain the upper hand Take 1 Juice.
            - Create a story tag.
            - Burn a power tag or a story tag.
            - Give or reduce a status (one tier per point of Juice)""".format(pwr)

      # Change the Game
      elif message.content.startswith("!ctg"):
        juice = 0
        if lvl == "Strong Hit":
          if pwr < 2:
            juice = 2
          else:
            juice = pwr

          effects = """You generated {} Juice. Choose from the options below:
            - Create a story tag.
            - Burn a power tag or a story tag.
            - Give or reduce a status (one tier per point of Juice)
            - Scale up the effect (greater area or more targets).
            - Prolong the effect (make it ongoing)
            - Hide the effect""".format(juice)

          # dynamite
          if dynamite:
            effects += """\n \n**Dynamite!**: You generate a minimum of 3 Juice and gain access to these additional options.
            - Large-scale effect
            - Permanent effect
            - Mist-hidden effect: the mist conspires to hide this effect even from Rifts."""

        # Weak Hit
        elif lvl == "Weak Hit":
          if pwr > 0:
            juice = pwr
          else:
            juice = 1

          effects = """You generated {} Juice. Choose from the options below:
            - Create a story tag.
            - Burn a power tag or a story tag.
            - Give or reduce a status (one tier per point of Juice)""".format(juice)

      # Face Danger
      elif message.content.startswith('!face'):

        # Strong Hit
        if lvl == "Strong Hit":
          effects = "You fend off the effect and take no status at all."

          # dynamite
          if dynamite:
            effects += """\n \n **Dynamite!**: Choose one:
            - You reflect the status at your attacker or otherwise use it against them. Attacker gets a status with tier = tier of original attack.
            - You bolster your defenses. Ongoing tier-1 status of your choice describing improved dfenses."""
        # Weak Hit
        elif lvl == "Weak Hit":
          effects = "Take the status at one tier lower."

        # miss
        else:
          effects = "Take the full status effect."

      # Convince
      elif message.content.startswith('!con'):
        if pwr < 1:
            pwr = 1
        # Strong Hit
        if lvl == "Strong Hit":
          effects = "Your target takes a tier-{} status or changes their agenda to include yours, at least for the time being.".format(pwr)

          # dynamite
          if dynamite:
            mod_pwr = pwr + 2
            effects += """\n \n **Dynamite!**: The target takes a tier-{} status instead. Even if the target chooses to avoid this, they must still take a tier-2 temporary status represening your influence. If this is against a PC, option to trade tiers for hurt points.""".format(mod_pwr)

        # Weak Hit
        elif lvl == "Weak Hit":
          effects = "Your target takes a tier-{} status or gives in a little while protecting their own agenda.".format(pwr)


      # Go Toe to Toe
      elif message.content.startswith('!go'):
        if pwr < 1:
          pwr = 1
        # Strong Hit
        if lvl == "Strong Hit":
          effects = """Choose 2:
          - You managage to achieve your goal, e.g., take something they hold, blocking their path, create an opening.
          - You get them good, giving your opponent a tier-{} status.
          - You block, dodge, or counter their best attempts. If you don't choose this, your opponent can impose a status on you. If PC, tier = Power.
          """.format(pwr)

          # dynamite
          if dynamite:
            effects += "\n \n **Dynamite!**: Instead of choosing, take all three options from above."

        # Weak Hit
        elif lvl == "Weak Hit":
          effects = """Choose 1:
          - You managage to achieve your goal, e.g., take something they hold, blocking their path, create an opening.
          - You get them good, giving your opponent a tier-{} status.
          - You block, dodge, or counter their best attempts. If you don't choose this, your opponent can impose a status on you. If PC, tier = Power.
          """.format(pwr)

      # investigate
      elif message.content.startswith('!inv'):
        if pwr < 1:
          pwr = 1

        # Strong Hit
        if lvl == "Strong Hit":
          if pwr == 1:
            effects = "You get 1 clue."
          else:
            effects = "You get {} clues.".format(pwr)
          # dynamite
          if dynamite:
            effects += "\n \n **Dynamite!**: The MC reveals the most valuable detail in the scene that your investigation could reveal."

        # Weak Hit
        elif lvl == "Weak Hit":
          if pwr == 1:
            effects = "You get 1 clue."
          else:
            effects = "You get {} clues.".format(pwr)
          effects += """ The MC also chooses one from the following:
          - Your investigation exposes you to danger.
          - The clues you get are fuzzy, incomplete, or part-true part-false.
          - Whoever or whatever you are asking the question(s) can ask you one question as well. You answer on the same terms.
          """

      # Sneak Around
      elif message.content.startswith('!sneak'):
        # Strong Hit
        if lvl == "Strong Hit":
          effects = "Everyone who should fall for your deception or subterfudge falls for it."

          # dynamite
          if dynamite:
            effects += "\n \n **Dynamite!**: Your may move or act unnoticed by your target for the rest of the scene. You must move or act in the same way as you did while making this roll to keep this effect."

        # Weak Hit
        elif lvl == "Weak Hit":
          effects = """There's a complication. The MC chooses one of the following:
            - Someone unimportant noticed you, but that just made them important, right?
            - You are precieved only by a secondary sense.
            - You must leave something important behind - or be discovered."""

      # Take the Risk
      elif message.content.startswith('!risk'):

        # Strong Hit
        if lvl == "Strong Hit":
          effects = "You do it, somehow."

          # dynamite
          if dynamite:
            effects += """\n \n **Dynamite!**: You pull it off spectacularly and even turn the situation to your advantage. Generate 2 Juice to spend on the options below:
            - Create a story tag.
            - Burn a power tag or a story tag.
            - Give or reduce a status (one tier per point of Juice)
            - Scale up the effect (greater area or more targets).
            - Prolong the effect (make it ongoing)
            - Hide the effect"""

        # Weak Hit
        elif lvl == "Weak Hit":
          effects = """You have a hard bargain or an ugly choice. Two or three negative outcomes are presented that you may choose:
          - **Complicate Things, Bigtime:** Problematic story development, typically a new dannger.
          - **Deny Them Something They Want:** Adversaries get away. Objective becomes out of reach. Witnesses stop talking.
          - **Make Something Horrible Happen:** Beloved character dies. The personal lives of PCs are threatened. Allies turn to enemies.
          - **Turn Their Move Against Them:** Action succeeds "too well" or affects an unintended target. Unexpected side-effect or reaction on action.
          - **Give a Status**
          - **Burn a Tag**"""

      # Stop. Holding. Back. Significant Sacrifice.
      elif message.content.startswith('!shbs'):

        # Strong Hit
        if lvl == "Strong Hit":
          effects = "You achieve what you want. Mark Fade/Crack on one theme."

        # Weak Hit
        elif lvl == "Weak Hit":
          effects = "You achieve what you want. Mark Fade/Crack and burn all the power tags on one theme."

        # Miss
        else:
          effects = """Mark Fade/Crack and burn all the power tags on one theme. You also lose control over your powers or fail to use them as planned.
          - **Complicate Things, Bigtime:** Problematic story development, typically a new dannger.
          - **Deny Them Something They Want:** Adversaries get away. Objective becomes out of reach. Witnesses stop talking.
          - **Make Something Horrible Happen:** Beloved character dies. The personal lives of PCs are threatened. Allies turn to enemies.
          - **Turn Their Move Against Them:** Action succeeds "too well" or affects an unintended target. Unexpected side-effect or reaction on action.
          - **Give a Status**
          - **Burn a Tag**
          - **Force Them to Choose:** Select two or three outcomes, all bad, linked to a separate Hard Move. The PC can pick their poison."""


      # Stop. Holding. Back. No Return
      elif message.content.startswith('!shbn'):

        # Strong Hit
        if lvl == "Strong Hit":
          effects = "You achieve what you want. Mark Fade/Crack and burn all the power tags on one theme."

        # Weak Hit
        elif lvl == "Weak Hit":
          effects = "You achieve what you want. Replace one theme."

        # Miss
        else:
          effects = """Replace one theme. You also lose control over your powers or fail to use them as planned.
      - **Complicate Things, Bigtime:** Problematic story development, typically a new dannger.
      - **Deny Them Something They Want:** Adversaries get away. Objective becomes out of reach. Witnesses stop talking.
      - **Make Something Horrible Happen:** Beloved character dies. The personal lives of PCs are threatened. Allies turn to enemies.
      - **Turn Their Move Against Them:** Action succeeds "too well" or affects an unintended target. Unexpected side-effect or reaction on action.
      - **Give a Status**
      - **Burn a Tag**
      - **Force Them to Choose:** Select two or three outcomes, all bad, linked to a separate Hard Move. The PC can pick their poison."""

           # Stop. Holding. Back. Ultimate
      elif message.content.startswith('!shbu'):

        # Strong Hit
        if lvl == "Strong Hit":
          effects = "You achieve what you want. Replace one theme."

        # Weak Hit
        elif lvl == "Weak Hit":
          effects = "You achieve what you want, but are killed, destoryed, or transformed forever in the process. Take a tier-6 status. You cannot **Face Danger**."

        # Miss
        else:
          effects = """You are killed, destoryed, or transformed forever. Take a tier-6 status. You cannot **Face Danger**. You also lose control over your powers or fail to use them as planned.
      - **Complicate Things, Bigtime:** Problematic story development, typically a new dannger.
      - **Deny Them Something They Want:** Adversaries get away. Objective becomes out of reach. Witnesses stop talking.
      - **Make Something Horrible Happen:** Beloved character dies. The personal lives of PCs are threatened. Allies turn to enemies.
      - **Turn Their Move Against Them:** Action succeeds "too well" or affects an unintended target. Unexpected side-effect or reaction on action.
      - **Give a Status**
      - **Burn a Tag**
      - **Force Them to Choose:** Select two or three outcomes, all bad, linked to a separate Hard Move. The PC can pick their poison."""

      if type(pwr) == str:
        pwr = int(pwr)
      if pwr > 6:
        disclaimer = "So you rolled with a power of " + str(pwr) + "!?! \nAlright, I'm just a bot. What do I know? Here's your totally legitmate result with a power of " + str(pwr) + ". \n\n"
      else:
        disclaimer = ""
      answer = disclaimer + prefix + dice_holder + " " + lvl + "\n" + effects
      await message.channel.send(answer)

client.run(os.getenv('TOKEN'))
