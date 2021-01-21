import discord
import random
import os
# from keep_alive import keep_alive
from Midi import Midi
from midi2audio import FluidSynth

client = discord.Client()

@client.event
async def on_mount():
    # on ready
    print(f'Logged in {client.user}')

@client.event
async def on_message(message):
    # if message is sent by self, do nothing
    if message.author == client.user:
        return

    msg = message.content
    channel = message.channel

    # debug
    # print(message.content)
    if not msg.startswith('!midi'):
        return
    try:
        # midi bot stuff
        # notes
        notes = []
        temp = msg.split(' ')
        for note in temp:
            if note != '' and note != ' ':
                notes.append(note)
        if len(notes) % 2 != 0:
            await channel.send('Incorrect use of !midi, to use !midi, follow with a space then the bpm and then note duration pairs all separate by spaces')
            return
        # sets 1 track and tempo as 115 bpm
        mid = Midi(1, int(notes[1]))
        
        # sets instrument as piano (TODO: change in the future)
        mid.set_instrument(1)

        parts = []
        dur_parts = []
        flag = True
        print(notes, len(notes))

        for index, item in enumerate(notes):
            if index <= 1:
                continue
            if flag:
                parts.append(item)
            else:
                dur_parts.append(float(item))
            flag = not flag

        # parts = ["B4", "C#5", "D5", "D5", "E5", "c#5", "b4", "a4", "r"] + ["B4", "B4", "C#5", "D5", "a4" , "d5", "a5", "a5", "E5"]
        # dur_parts = [.5, .5, .5, .5, .5, .5, .25, 1, .5] + [.5, .5, .5, .5, 1, .5, 1, .5, 2]

        # translate notes
        notes = mid.notes_to_midi(parts)

        # push notes and duration to stack
        mid.push_notes(notes, dur_parts)

        # output to file named test
        mid.output_mid("test")
        # midi to wav
        fs = FluidSynth()
        fs.midi_to_audio('test.mid', 'output.wav')
        await channel.send('Calling Terry Gannon 📞...')
    except:
        await channel.send('Incorrect use of !midi, to use !midi, follow with a space then the bpm and then note duration pairs all separate by spaces')

# keep_alive()
client.run(os.getenv('TOKEN'))
