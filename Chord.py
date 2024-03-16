class ChordEncoder:
    
    scaleDegreesMap = {} #Map of all scales and their degrees

    keySigPrefs = {
        'C': 'flat', 'G': 'sharp', 'D': 'sharp', 'A': 'sharp', 'E': 'sharp', 'B': 'sharp', 'F#': 'sharp', 'C#': 'sharp',
        'F': 'flat', 'Bb': 'flat', 'Eb': 'flat', 'Ab': 'flat', 'Db': 'flat', 'Gb': 'flat', 'Cb': 'flat',
        'Am': 'sharp', 'Em': 'sharp', 'Bm': 'sharp', 'F#m': 'sharp', 'C#m': 'sharp', 'G#m': 'sharp', 'D#m': 'sharp', 'A#m': 'flat',
        'Dm': 'flat', 'Gm': 'flat', 'Cm': 'flat', 'Fm': 'flat', 'Bbm': 'flat', 'Ebm': 'flat', 'Abm': 'flat'
    }
    chromaticScaleSharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    chromaticScaleFlats = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

    @classmethod
    def genAllScaleDegrees(cls):
        '''
        Generates and stores scale degrees for all major and minor keys
        '''

        majorKeys = ['C', 'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb', 
                     'G', 'D', 'A', 'E', 'B', 'F#', 'C#']

        minorKeys = ['A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 
                      'D', 'G', 'C', 'F', 'Bb', 'Eb', 'Ab']
        
        for key in majorKeys:
            cls.scaleDegreesMap[(key, 'M')] = cls._genScaleDegrees(key, 'M')
        for key in minorKeys:
            cls.scaleDegreesMap[(key, 'm')] = cls._genScaleDegrees(key, 'm')
        
    @staticmethod
    def _genScaleDegrees(key, mode):
        '''
        Generates scale degrees for a given key and mode.
        :param key: String, the key of the scale.
        :param mode: String, the mode of the scale ('M' for major, 'm' for minor).
        '''

        chromaticScaleSharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        chromaticScaleFlats = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

        if key == 'Cb' and mode == 'M':
            return ['Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb']
        elif key == 'A#' and mode == 'm':
            return ['A#', 'C', 'D', 'D#', 'F', 'G', 'A']
        elif key == 'Ab' and mode == 'm':
            return ['Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'Gb']
        
        if key not in chromaticScaleSharps and key not in chromaticScaleFlats:
            raise ValueError("Key does not exist.")
        
        #Use sharps or flats based on key
        useFlats = ChordEncoder.keySigPrefs.get(key + ('m' if mode == 'm' else ''), 'sharp') == 'flat' #Default to sharp if key not found
        chromaticScale = chromaticScaleFlats if useFlats else chromaticScaleSharps
        startIndex = chromaticScale.index(key)
        
        majorScaleIntervals = ['W', 'W', 'H', 'W', 'W', 'W', 'H']
        minorScaleIntervals = ['W', 'H', 'W', 'W', 'H', 'W', 'W']
        
        intervals = majorScaleIntervals if mode == 'M' else minorScaleIntervals
        scale = [key]
        cur = startIndex

        for interval in intervals:
            if interval == 'W':
                cur = (cur + 2) % 12 #Mod 12, or the length of the chromatic scale
            elif interval == 'H':
                cur = (cur + 1) % 12 
            scale.append(chromaticScale[cur])
        return scale[:-1] #Exclude last note since it's the octave

    def __init__(self, key='C', mode = 'M'):
        if not ChordEncoder.scaleDegreesMap:
            ChordEncoder.genAllScaleDegrees()
        self.key = key
        self.mode = mode
        self.scaleDegrees = ChordEncoder.scaleDegreesMap[(key, mode)]
        self.useFlats = self.keySigPrefs.get(key, 'sharp') == 'flat'

    def _getChromaticIndex(self, note, chromaticScale):
        """Find the index of a note in the chromatic scale."""
        try:
            return chromaticScale.index(note)
        except ValueError:
            return None
    
    def _convertToPreferredNotation(self, note):
        """
        Converts sharp notes to flats if the key signature preference is flats.
        """
        if self.useFlats:
            conversionMap = {'A#': 'Bb', 'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab'}
            return conversionMap.get(note, note)
        return note

    def getRomanNumeral(self, roman_numeral):
        """
        Encodes a Roman numeral to its corresponding note and chord quality. Supports major and minor keys, and flat modification.

        :param roman_numeral: String, the Roman numeral to encode.

        :return: Tuple, the note and quality of the chord.
        """
        base_numeral = roman_numeral.upper()
        is_flat = 'B' in base_numeral
        base_numeral = base_numeral.replace('B', '')

        quality_mapping = {
            'M': {'I': 'M', 'II': 'm', 'III': 'm', 'IV': 'M', 'V': 'M', 'VI': 'm', 'VII': 'd'},
            'm': {'I': 'm', 'II': 'd', 'III': 'M', 'IV': 'm', 'V': 'm', 'VI': 'M', 'VII': 'M'}
        }

        chord_quality = quality_mapping[self.mode][base_numeral] if base_numeral in quality_mapping[self.mode] else 'M'

        # Adjusting for the scale degree
        scale_degrees = 'I II III IV V VI VII'.split()
        if base_numeral in scale_degrees:
            degree_index = scale_degrees.index(base_numeral)
        else:
            raise ValueError("Invalid Roman numeral")

        # Get the note from scale degrees
        degree_note = self.scaleDegrees[degree_index]

        # Apply flat modifier if needed
        if is_flat:
            if self.useFlats:
                # Move one note back in the flats scale for flat modifier
                flat_index = self.chromaticScaleFlats.index(degree_note)
                degree_note = self.chromaticScaleFlats[(flat_index - 1) % 12]
            else:
                # Move one note back in the sharps scale for flat modifier
                sharp_index = self.chromaticScaleSharps.index(degree_note)
                degree_note = self.chromaticScaleSharps[(sharp_index - 1) % 12]

            # 'bVII' chord in major keys is typically major
            if self.mode == 'M':
                chord_quality = 'M'

        # Ensure the note is in the correct notation for the key
        if self.useFlats and degree_note in self.chromaticScaleSharps:
            # Find equivalent in flats if necessary
            sharp_index = self.chromaticScaleSharps.index(degree_note)
            degree_note = self.chromaticScaleFlats[sharp_index % 12]
        elif not self.useFlats and degree_note in self.chromaticScaleFlats:
            # Or find equivalent in sharps
            flat_index = self.chromaticScaleFlats.index(degree_note)
            degree_note = self.chromaticScaleSharps[flat_index % 12]

        return degree_note, chord_quality
    
# # Example Usage
# root = ChordEncoder('C', 'M')  # For C Major key
# note, quality = root.getRomanNumeral('VI')
# print(note + quality) 
