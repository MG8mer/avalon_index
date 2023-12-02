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