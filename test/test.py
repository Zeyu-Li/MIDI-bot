from midi2audio import FluidSynth

fs = FluidSynth()
fs.midi_to_audio('test.mid', 'output.wav')