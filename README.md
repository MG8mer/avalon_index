# Avalon_Index (Version No. 1) Documentation

## Video
[Video of our `code` running](https://drive.google.com/file/d/1C7DjG1G48Ax7haQWrtKugGJpwkQQn6zK/view?usp=sharing)

## Breakthough Moment 
I would say our development team's breakthrough moment (Me, Avash, and Po) is when we figured out the `aiosqlite` portion of our version #1.
> In other words, when we figured out how to implement tables.

The first part of this breakthrough is when we actually made the table when we ran the bot *if no table existed already*, and we implemented it as follows:

```Python
@client.event
async def on_ready(): # from https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
  print("Bot is up") # from https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
  # Table creation from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER, guild_id INTEGER, class INTEGER, start INTEGER)')
    await db.commit()
  print(f"{len(client.guilds)}")
  print(f"{client.guilds[0].id}")
```
In the code above, when the bot runs and is ready, it prints `Bot is up`, then if not already created, a table in a file named `main.db` is created called "users". Then, we print the amount of guilds (*servers*) the bot is in and id of the 0th guild.

Then, we struggled to implement the table for the rest of our functions. However, the main roadblock to overcome to implement it for the `start` command, as after it is implemented it gives us the ability to check if the user has used that command in order to let them use other commands properly. Initially, it was difficult as I had a lack of SQL knowledge, but after some skimming through w3schools, stack overflow, and youtube videos, we were able to utilize a table for the start function.

__Let's break it down:__

> *We will not worry about the other parts of the code which mainly consist of sending an embed for the user when `/start` is used.*

1. To start, similar to in the `on_ready` function, we connect to the database in `main.db` with the following code:

   ```Python
   @client.slash_command(name = "start", description = "Starts the game!") 
   async def start(interaction: Interaction): #/start command, to start the game users must type this first
     async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        pass
      await db.commit()
   ```

   `Pass` is to be substituted with our code.

    We will look at each code segment individually then put it all together.

2. Next, we create a row for the user, where insert values for the columns `user_id`, which is the discord id of the user, `guild_id`, which the id of the server the user used `/start` in, and `start`, which is set to one, meaning the user has used the `/start` command. This is implemented as follows:

   ```Python
   await cursor.execute('INSERT INTO users (user_id, guild_id, start) VALUES (?, ?, ?)', (interaction.user.id,client.guilds[0].id, 1))
   ```

   Although there is another column created in the `on_ready` function called `class`, we don't insert a value for it as that is implemented in the `pick` command, which we will nto worry about for now.

3. Although the implementation for this `/start` command can be complete in step 2, we must ensure there are now duplicate rows by making it so that `/start` can only be used once. This requires a conditional, but before that we must fetch the value of start in the row for that user. This is done as follows:

   ```Python
   await cursor.execute('SELECT start FROM users WHERE user_id = ?', (interaction.user.id,))
   ```
   Let's now store that query in a variable:
   ```Python
   start_value = await cursor.fetchone()
   ```

   Great! We can now implement a conditional: `if start_value is equal to one, or if the user has already used start, simply respond to that interaction with the message "You have 
   already used start! If you would like to reset your stats, please use the /reset command."`:

   ```Python
   if start_value == (1,):
       await interaction.response.send_message("You have already used start! If you would like to reset your stats, please use the /reset command.")
   ```

  > Notice how it's start_value == (1,) and not start_value == 1? That is because in testing, when printing the variable start_value after a user used `/start`, it printed (1,) rather than 1, so we compensated accordingly.

  `Else if start_value is NOT one, or in other words if the user hasn't used start, making the value of start_value None, create a row for the user and insert the applicable values like normal:`

  ```Python
   else:
      await cursor.execute('INSERT INTO users (user_id, guild_id, start) VALUES (?, ?, ?)', (interaction.user.id,client.guilds[0].id, 1))
  ```
  > Notice how the INSERT query from step two was moved to the else part of the conditional.

4. Then, we put it all together!

   ```Python
   @client.slash_command(name = "start", description = "Starts the game!")
   async def start(interaction: Interaction):  #/start command, to start the game users must type this first
   async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT start FROM users WHERE user_id = ?', (interaction.user.id,))
      start_value = await cursor.fetchone()
      if start_value == (1,):
         await interaction.response.send_message("You have already used start! If you would like to reset your stats, please use the /reset command.")
      else:
        await cursor.execute('INSERT INTO users (user_id, guild_id, start) VALUES (?, ?, ?)', (interaction.user.id,client.guilds[0].id, 1))
    await db.commit()
   ```
   > Notice how pass has been replaced by the code written in the steps prior.

  And that is our breakthrough.

  ## Development Process
  > ### **Tasks**

  - Inspired by the quote "Many hands make light work," we allowed everyone to contribute whever they were free as some of us were busy with other work and tests. Moreover, we made sure everyone had a role in the **V1** of __*Avalon Index*__.  We also set deadlines for each other on whatever task we were doing at that moment depending on how important that task is for the entire project to move on. Here is a table representing the tasks each of us has done and future tasks that we will contribute to...
  >
  |                |Tasks Done                        | Future Tasks |
  |----------------|-------------------------------|---------------|
  |**Po**            |`Embeds (Help Pages, Start Page, About Pages), Slash Commands, {TENOR} API Related Aspects, Debugging Code, Keeping the Bot Alive Using Uptime, Initially Planned to Work on Database (The task was put upon Hamzeus as Po had SATs)`|`Battle Command,  Leveling System, Activity System, Skill Points System, Touch-ups for Embeds`|
  |**Hamzeus**          |`Setting up Database, Slash Commands, Debugging Code, Creating the Base Stats and Values for Classes, Creating Game Idea`         |`Battle Command, Activity System, Leveling System, Skill Points System`|
  |**Avash**            |`Creating Game Idea, Creating the Base Stats and Values, Creating Custom Assets for Each Class, Debugging Code (On Hamzeus's Laptop), Slash Commands (was not able to get it to run successfully)`                                           |`Battle Command, Activity System, Leveling System, Skill Points System`|

  ### Milestones
  >For Milestones and Features that have a **``✘``** will be worked on after **V1** as we needed the basics setup such as the **DATABASE**

  |**`Milestones and Features`**| **`Finished`** |  
  |------------|----------------|
  |<div align="center">Creating our 3 Classes|<div align="center">✓|
  |<div align="center">Custom Assets For Three Classes|<div align="center">✓|
  |<div align="center">User can enter ``/start`` in order to start|<div align="center">✓|
  |<div align="center">User can enter ``/help`` in order to select 1 out of 2 pages of wise words|<div align="center">✓|
  |<div align="center">User can enter ``/about`` in order to view info on the 1 out of 3 classes|<div align="center">✓|
  |<div align="center">User can enter ``/pick`` in order to pick1 out of 3 classes|<div align="center">✓|
  |<div align="center">User can enter ``/stats`` in order to view 1 out of 3 classes|<div align="center">✓|
  |<div align="center">User can enter ``.gif <search_term>`` in order to receive a random gif related to the search term|<div align="center">✓|
  |<div align="center">Embed Pages **`(Help Pages, About Pages, etc.)`**|<div align="center">✔|
  |<div align="center">Database|<div align="center">✓|
  |<div align="center">Small tutorial to show how mechanics work with a visual to show weaknesses **`(Tutorial Idea was scratched since we replaced it with /help)`**|<div align="center">✗|
  |<div align="center">Show skill tree and evolutions of each class in order to let user truly select their preference **`(Skill Tree System was not acheivable till we had the database setup)`**|<div align="center">✗|
  |<div align="center">Basic Mechanics **`(Gameplay was not acheivable till we had the database setup)`**|<div align="center">✗|
  |||