import midiFunctions as mf

def dancer(musicbox):

    musicbox.add_chords_to_dict('G', ['G_4', 'B_4', 'D_5', 'G_5'])
    musicbox.add_chords_to_dict('C', ['C_4', 'E_4', 'G_4', 'C_5'])
    musicbox.add_chords_to_dict('D', ['D_4', 'Fs_4', 'A_4', 'D_5'])
    musicbox.add_chords_to_dict('F', ['F_4', 'A_4', 'C_5', 'F_5'])
    musicbox.add_chords_to_dict('F7', ['F_4', 'A_4', 'C_5', 'Eb_5'])
    musicbox.add_chords_to_dict('G3', ['G_3', 'B_3', 'D_4', 'G_4'])
    musicbox.add_chords_to_dict('C3', ['C_3', 'E_3', 'G_3', 'C_4'])
    musicbox.add_chords_to_dict('D3', ['D_3', 'Fs_3', 'A_3', 'D_4'])
    musicbox.add_chords_to_dict('F3', ['F_3', 'A_3', 'C_4', 'F_4'])
    musicbox.add_chords_to_dict('F73', ['F_3', 'A_3', 'C_4', 'Eb_4'])

    musicbox.add_to_track(1, 2, [], ['G'], decay=2)
    musicbox.add_to_track(1, 2, [], ['C'], decay=2)
    musicbox.add_to_track(1, 2, [], ['D'], decay=2)
    musicbox.add_to_track(1, 2, [], ['G'], decay=2)
    for i in range(4):
        musicbox.add_to_track(4, 8, ['C_5'], ['C'], decay=4)
        musicbox.add_to_track(4, 8, ['E_5'], ['C'], decay=4)
        musicbox.add_to_track(1, 8, ['G_5'], ['C'], decay=4)
        musicbox.add_to_track(1, 8, ['C_5'], ['C'], decay=4)
        musicbox.add_to_track(1, 8, ['C_6'], ['C'], decay=4)
        musicbox.add_to_track(1, 8, ['G_5'], ['C'], decay=4)
        musicbox.add_to_track(1, 8, ['E_5'], ['C'], decay=4)
        musicbox.add_to_track(1, 8, ['G_5'], ['C'], decay=4)

    for i in range(2):
        musicbox.add_to_track(3, 32, ['C_6'], ['C'])
        musicbox.add_to_track(1, 32, ['C_1'], ['C'])
        musicbox.add_to_track(2, 8, ['C_6'], ['C'])
        musicbox.add_to_track(1, 8, ['E_6'], ['C'])
        musicbox.add_to_track(1, 8, ['C_6'], ['C'])
        musicbox.add_to_track(1, 8, ['E_6'], ['C'])
        musicbox.add_to_track(1, 8, ['G_6'], ['C'])
        musicbox.add_to_track(1, 16, ['E_6'], ['C'])
        musicbox.add_to_track(1, 16, ['G_6'], ['C'])
        musicbox.add_to_track(1, 8, ['C_7'], ['F'])
        musicbox.add_to_track(1, 8, ['B_6'], ['F'])
        musicbox.add_to_track(1, 8, ['A_6'], ['F'])
        musicbox.add_to_track(1, 8, ['G_6'], ['F'])
        musicbox.add_to_track(7, 32, ['G_6'], ['F'])
        musicbox.add_to_track(1, 32, ['G_1'], ['F'])
        musicbox.add_to_track(3, 32, ['G_6'], ['F'])
        musicbox.add_to_track(1, 32, ['G_1'], ['F'])
        musicbox.add_to_track(1, 32, ['G_6'], ['F'])
        musicbox.add_to_track(1, 32, ['G_1'], ['F'])
        musicbox.add_to_track(1, 32, ['G_6'], ['F'])
        musicbox.add_to_track(1, 32, ['G_1'], ['F'])
        musicbox.add_to_track(1, 8, ['G_6'], ['F7'])
        musicbox.add_to_track(1, 8, ['F_6'], ['F7'])
        musicbox.add_to_track(1, 8, ['D_6'], ['F7'])
        musicbox.add_to_track(1, 8, ['B_5'], ['F7'])
        musicbox.add_to_track(1, 8, ['G_5'], ['F7'])
        musicbox.add_to_track(1, 8, ['B_5'], ['F7'])
        musicbox.add_to_track(1, 8, ['D_6'], ['F7'])

        if i == 0:
            musicbox.add_to_track(1, 8, ['F_6'], ['F7'])
            musicbox.add_to_track(1, 8, ['E_6'], ['C'])
            musicbox.add_to_track(1, 8, ['C_6'], ['C'])
            musicbox.add_to_track(1, 8, ['A_6'], ['C'])
            musicbox.add_to_track(5, 8, ['G_6'], ['C'])
        else:
            musicbox.add_to_track(1, 8, ['B_5'], ['F7'])
            musicbox.add_to_track(2, 8, ['C_6'], ['C'])
            musicbox.add_to_track(1, 8, ['D_6'], ['C'])
            musicbox.add_to_track(5, 8, ['C_6'], ['C'])

    for i in range(2):
        musicbox.add_to_track(3, 32, ['C_5'], ['C'])
        musicbox.add_to_track(1, 32, ['C_1'], ['C'])
        musicbox.add_to_track(2, 8, ['C_5'], ['C'])
        musicbox.add_to_track(1, 8, ['E_5'], ['C'])
        musicbox.add_to_track(1, 8, ['C_5'], ['C'])
        musicbox.add_to_track(1, 8, ['E_5'], ['C'])
        musicbox.add_to_track(1, 8, ['G_5'], ['C'])
        musicbox.add_to_track(1, 16, ['E_5'], ['C'])
        musicbox.add_to_track(1, 16, ['G_5'], ['C'])
        musicbox.add_to_track(1, 8, ['C_6'], ['F'])
        musicbox.add_to_track(1, 8, ['B_5'], ['F'])
        musicbox.add_to_track(1, 8, ['A_5'], ['F'])
        musicbox.add_to_track(1, 8, ['G_5'], ['F'])
        musicbox.add_to_track(7, 32, ['G_5'], ['F'])
        musicbox.add_to_track(1, 32, ['G_1'], ['F'])
        musicbox.add_to_track(3, 32, ['G_5'], ['F'])
        musicbox.add_to_track(1, 32, ['G_1'], ['F'])
        musicbox.add_to_track(1, 32, ['G_5'], ['F'])
        musicbox.add_to_track(1, 32, ['G_1'], ['F'])
        musicbox.add_to_track(1, 32, ['G_5'], ['F'])
        musicbox.add_to_track(1, 32, ['G_1'], ['F'])
        musicbox.add_to_track(1, 8, ['G_5'], ['F7'])
        musicbox.add_to_track(1, 8, ['F_5'], ['F7'])
        musicbox.add_to_track(1, 8, ['D_5'], ['F7'])
        musicbox.add_to_track(1, 8, ['B_4'], ['F7'])
        musicbox.add_to_track(1, 8, ['G_4'], ['F7'])
        musicbox.add_to_track(1, 8, ['B_4'], ['F7'])
        musicbox.add_to_track(1, 8, ['D_5'], ['F7'])

        if i == 0:
            musicbox.add_to_track(1, 8, ['F_5'], ['F7'])
            musicbox.add_to_track(1, 8, ['E_5'], ['C'])
            musicbox.add_to_track(1, 8, ['C_5'], ['C'])
            musicbox.add_to_track(1, 8, ['A_5'], ['C'])
            musicbox.add_to_track(5, 8, ['G_5'], ['C'])
        else:
            musicbox.add_to_track(1, 8, ['B_4'], ['F7'])
            musicbox.add_to_track(2, 8, ['C_5'], ['C'])
            musicbox.add_to_track(1, 8, ['D_5'], ['C'])
            musicbox.add_to_track(5, 8, ['C_5'], ['C'])