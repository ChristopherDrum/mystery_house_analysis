# Python < 3
# see LICENSE file for licensing information

# Uses 64K binary memory dump from emulator as input, grabbed when $5e03 first
# hit in the game, along with Mystery House's MESSAGES file.  See dumpgame.out
# for output.

# In AppleWin, F7 to go to the debugger
# bsave "<filename>.bin", 0, 65536
# will generate a file to... somewhere... (my Mystery House project folder)
# consumable by this script
# at console `python3 dumpgame.py >> output.out`

# logging out additional values to see if we can find object flags
# objects *might* have a "was_moved" flag; butterknife switched from 0 to 1

# typically I do before/after captures and compare them to see what changed with certain events.
FILE = 'before.bin'

def dumpdict(label, addr):
	rv = {}
	print(label)
	n = 0
	while True:
		n += 1
		word = M[addr:addr+8]
		# strip high bit the Apple II so loved for ASCII chars
		word = ''.join([ chr(ch & 0x7f) for ch in word ])
		addr += 8
		print('#%d\t"%s"' % (n, word))
		rv[n] = word.strip()
		
		nsyn = M[addr]
		if nsyn == 0xff:
			# end-of-dictionary sentinela
			break
		addr += 1

		# handle synonyms, if any
		while nsyn > 0:
			word = M[addr:addr+8]
			# strip high bit
			word = ''.join([ chr(ch & 0x7f) for ch in word ])
			addr += 8
			print('\t= "%s"' % word)
			nsyn -= 1
	return rv

def dumpmess():
	# It's just easier to include the full text of MESSAGES in here rather than reading them in each time.
	strings = [
		"IT IS TOO HIGH",
		"OK",
		"IT IS SAM, THE MECHANIC.  HE HAS BEEN HIT IN THE HEAD BY A BLUNT OBJECT",
		"IT IS TOO HEAVY",
		"WINDOWS ARE BOARDED UP EXCEPT THE ATTIC WINDOW",
		"YOU ARE IN THE FENCED BACK YARD.  THE FENCE FOLLOWS THE SIDE OF THE 'HOUSE TO THE NORTH.  THERE IS A DEAD BODY HERE",
		"IT IS GETTING DARK",
		"YOU ARE IN THE SIDE YARD.  YOU CAN FOLLOW THE FENCE TO THE SOUTH",
		"YOU ARE IN THE KITCHEN.  THERE IS A REFRIGERATOR, STOVE AND CABINET",
		"THE WALL IS BRICKED UP BEHIND IT",
		"THE BRICKS BREAK APART LEAVING A LARGE HOLE",
		"YOU HAVE NOTHING STRONG ENOUGH",
		"WATER IS RUNNING INTO THE SINK",
		"YOU HAVE NO CONTAINER",
		"THERE IS NOTHING SPECIAL",
		"THE STOVE EXPLODES, YOU ARE DEAD",
		"THE PITCHER IS EMPTY",
		"YOU CAN'T CLIMB THESE TREES",
		"YOU ARE IN A FOREST",
		"THERE IS A VERY TALL PINE TREE IN FRONT OF YOU",
		"YOU ARE AT THE TOP OF A VERY TALL PINE TREE",
		"YOU ARE LOOKING THROUGH THE ATTIC WINDOW.  YOU SEE A TRAPDOOR IN THE ATTIC CEILING",
		"YOU HAD BETTER CLIMB DOWN FIRST",
		"IT IS FASTENED DOWN",
		"YOU ARE AT THE NORTH END OF A NARROW NORTH/SOUTH PASSAGEWAY",
		"YOU ARE IN A SMALL PANTRY",
		"IT DOES NOT REMOVE",
		"YOU ARE IN A SMALL FENCED CEMETARY.  THERE ARE SIX NEWLY DUG GRAVES",
		"THERE IS A MAN HERE",
		"THERE IS A DEAD BODY HERE",
		"THE WRITING IS WORN DOWN",
		"IT IS JOE, THE GRAVEDIGGER.  HE HAS JUST FINISHED DIGGING THE SIX GRAVES",
		"HE DOESN'T TALK MUCH",
		"WITH WHAT?",
		"YOUR GUN IS EMPTY",
		"IT IS JOE, THE GRAVEDIGGER",
		"I DON'T UNDERSTAND YOU",
		"YOU FALL IN ONE AND JOE BURIES YOU.  YOU ARE DEAD",
		"YOU FALL IN ONE AND CLIMB OUT AGAIN",
		"JOE WON'T LET YOU",
		"YOU ARE IN THE DINING ROOM",
		"IT IS DARK, YOU CAN'T SEE",
		"WOULD YOU LIKE TO PLAY AGAIN?",
		"YOU TRIP OVER RUG AND FALL.  OH,OH, YOU STARTED A FIRE WITH YOUR CANDLE!",
		"THE FIRE IS OUT",
		"THE FIRE IS OUT OF CONTROL.  YOU ARE DEAD",
		"THERE IS NO WICK",
		"WHICH DIRECTION?",
		"YOU ARE IN A MOIST BASEMENT. ALGAE COVERS THE WALLS. THERE IS A DEAD 'BODY HERE.",
		"IT IS TOO HARD",
		"YOU HAVE NOTHING TO WIPE IT WITH",
		"THE WALL IS EXPOSED.  THERE IS A LOOSE BRICK",
		"YOU HAVE FOUND THE JEWELS!",
		"IT IS TOM, THE PLUMBER.  HE SEEMS TO HAVE BEEN STABBED.  THERE IS A 'DAISY IN HIS HAND",
		"THERE IS A SKELETON KEY HERE",
		"IT IS LOOSE",
		"THEY ARE JEWELS, ALL RIGHT!",
		"YOU ARE AT THE SOUTH END OF A NORTH/SOUTH TUNNEL",
		"IT IS VERY LONG",
		"YOU ARE AT THE JUNCTION OF AN EAST/WEST HALLWAY AND A NORTH/SOUTH HALLWAY",
		"WHERE?",
		"THERE IS A DOORWAY HERE",
		"YOU ARE AT A STAIRWAY",
		"YOU ARE IN A BOYS BEDROOM",
		"THERE IS WRITING ON IT",
		"YOU ARE IN AN OLD NURSERY. THERE IS A DEAD BODY HERE.",
		"IT IS DR. GREEN.  IT APPEARS HE HAS BEEN STABBED",
		"YOU ARE IN A LARGE BEDROOM",
		"A DAGGER IS THROWN AT YOU FROM OUTSIDE THE ROOM.  IT MISSES!",
		"YOU ARE IN A SMALL BEDROOM. THERE IS A DEAD BODY HERE.",
		"IT IS SALLY, THE SEAMSTRESS.  SHE HAS A LARGE LUMP ON HER HEAD.  THERE 'IS A BLOND HAIR ON HER DRESS",
		"YOU ARE IN THE STUDY",
		"ITS NICE BUT NOT EXACTLY MY CUP OF TEA. THANX FOR THE LOOK THOUGH.",
		"IT IS FASTENED TO THE WALL WITH FOUR BOLTS",
		"THE PICTURE IS LOOSE",
		"THERE IS A BUTTON ON THE WALL",
		"PART OF THE WALL OPENS",
		"YOU ARE IN THE ATTIC",
		"YOU SEE A FOREST",
		"WHAT TRAPDOOR?",
		"YOU ARE IN A STORAGE ROOM",
		"IT IS LOCKED",
		"YOU HAVE NOTHING TO UNLOCK IT WITH",
		"THERE IS ONE BULLET IN THE GUN",
		"YOU ARE IN THE TOWER",
		"DAISY WON'T LET YOU",
		"SHE IS GOING TO KILL YOU",
		"SHE IS DEAD",
		"YOU KILLED DAISY",
		"DAISY STABBED YOU.  YOU ARE DEAD",
		"YOU ARE IN THE BATHROOM. THERE IS A DEAD BODY HERE.",
		"YOUR PITCHER IS FULL",
		"IT IS BILL, THE BUTCHER. HE HAS BEEN STRANGLED WITH A PAIR OF PANTYHOSE",
		"YOU ARE IN A MUSTY CRAWLSPACE",
		"THE WALL CLOSES BEHIND YOU WITH A BANG",
		"IT WON'T OPEN",
		"YOU ARE ON A STAIRWAY",
		"YOU ARE ON THE PORCH.  STONE STEPS LEAD DOWN TO THE FRONT YARD",
		"YOU ARE IN THE FRONT YARD OF A LARGE ABANDONED VICTORIAN HOUSE.  STONE 'STEPS LEAD UP TO A WIDE PORCH",
		"IT IS VERY HIGH",
		"THERE IS A FOREST",
		"YOU ARE IN AN ENTRY HALL.  DOORWAYS GO EAST, WEST AND SOUTH.  A 'STAIRWAY GOES UP",
		"THE FRONT DOOR TO THE NORTH HAS BEEN CLOSED AND LOCKED",
		"YOU ARE IN THE OLD, DUSTY LIBRARY",
		"THERE ARE NOT MANY BOOKS LEFT",
		"IT IS TOO FAR DOWN",
		"THERE ARE MATCHES HERE",
		"A BUTTERKNIFE",
		"MATCHES",
		"A NOTE",
		"A SKELETON KEY",
		"A SMALL KEY",
		"A SHOVEL",
		"A SLEDGEHAMMER",
		"A LIT CANDLE",
		"AN UNLIT CANDLE",
		"A DAGGER",
		"A GUN",
		"A KNIFE",
		"A PICTURE",
		"A TOWEL",
		"A BRICK",
		"JEWELS",
		"A CABINET",
		"AN EMPTY PITCHER",
		"A PITCHER FULL OF WATER",
		"YOU DONT HAVE IT",
		"THE DOOR IS CLOSED",
		"IT IS OPEN",
		"THE MATCH WENT OUT",
		"I SEE NO WATER",
		"YOU ARE NOT CARRYING IT",
		"IT IS NOT OPEN",
		"IT WONT CLOSE HERE",
		"AN OPEN CABINET",
		"IT IS UNLOCKED",
		"YOU CANT GO IN THAT DIRECTION",
		"IT'S TOO HEAVY TO LIFT",
		"IT WON'T MOVE ANY FARTHER",
		"THANK YOU FOR PLAYING HI-RES ADVENTURE ... GOOD-BYE",
		"TRY GOING IN SOME DIRECTION EX:NORTH,SOUTH,EAST,WEST,UP,DOWN",
		"THE DOOR HAS BEEN CLOSED AND LOCKED",
		"THERE IS A BUTTERKNIFE HERE",
		"THE KITCHEN DOOR IS CLOSED",
		"I DONT KNOW WHAT YOU MEAN",
		"I DONT SEE IT HERE",
		"YOU FALL TO EARTH. LUCKILY YOU HAVE ONLY MINOR INJURIES.",
		"UNFORTUNATELY THE AMBULANCE DRIVER SMASHS INTO A VOLKWAGEN. NO 'SURVIVORS. YOU ARE DEAD.",
		"IF YOU FEEL THAT WAY I REFUSE TO PLAY WITH YOU...",
		"YOU CLIMB UP BUMP YOUR HEAD ON THE CEILING AND FALL, DAZED BUT ALIVE.",
		"IT DOESNT MOVE",
		"I DONT SEE IT HERE",
		"I THINK I SEE A SLEDGEHAMMER HERE.",
		"YOU DON'T HAVE IT",
		"YOU HAVE NOTHING TO LIGHT IT WITH",
		"YOU GO IN THE HOLE BUT CANNOT CONTINUE AND HAVE TO RETURN.",
		"THANX. THAT FEELS EVER SO MUCH BETTER",
		"THANK YOU. I LOVE TO FEEL CLEAN. THATS MUCH BETTER.",
		"I FEEL MUCH MORE RESTED NOW",
		"YOUR GUN IS NOW EMPTY",
		"DAISY IS NOW DEAD",
		"THE KITCHEN DOOR IS OPEN",
		"THE PEOPLE WERE EXPLAINED AT THE BEGINNING OF THE GAME.",
		"CONGRATULATIONS YOU HAVE BEATEN ADVENTURE AND ARE DECLARED A GURU WIZARD",
		"IF ONLY I COULD TELL IF I'D BEEN HERE BEFORE...",
		"DAISY IS ALREADY DEAD"
	]

	messages = {}
	n = 1
	for s in strings:
		messages[n] = s
		n += 1
	return messages

def dumpobjects():
	print('OBJECTS')
	objects = {}

	i = 0x900
	while True:
		objno = M[i]
		if objno == 0xff:
			break
		objnoun = M[i+1]
		objloc = M[i+2]
		objpic = M[i+3]
		objdraw = M[i+4]
		objx = M[i+5]
		objy = M[i+6]
		objtake = M[i+7]
		objmesg = M[i+8]
		objnext = M[i+9]
  
		drawstatus = 'vector'
		if objdraw == 1: drawstatus = 'stamp'
  
		takestatus = 'takeable'
		if objtake == 1: takestatus = 'was moved'
		if objtake == 2: takestatus = 'fixed'
  
		print('%x: #%d\t%s at location %d, (x,y) = (%d,%d), pic #%d\n\t%s, %s(%d)' % (
			i, objno, nouns[objnoun], objloc, objx, objy, objpic, drawstatus, takestatus, objtake
		))
		if objmesg != 0:
			print('\t"%s"' % messages[objmesg])
		objects[objno] = nouns[objnoun]
		i += objnext
	return objects

def dumprooms():
	print('ROOMS')

	n = 0
	i = 0xd00
	while True:
		roommesg = M[i+1]
		if roommesg not in messages:
			print('%x: #%d\t???' % (i, n))
		else:
			print('%x: #%d\t"%s"' % (i, n, messages[roommesg]))
		dirs = ''
		if M[i+2] != 0:	dirs += 'N %d ' % M[i+2]
		if M[i+3] != 0:	dirs += 'S %d ' % M[i+3]
		if M[i+4] != 0:	dirs += 'E %d ' % M[i+4]
		if M[i+5] != 0:	dirs += 'W %d ' % M[i+5]
		if M[i+6] != 0:	dirs += 'U %d ' % M[i+6]
		if M[i+7] != 0:	dirs += 'D %d ' % M[i+7]
		if dirs != '':
			print('\t%s' % dirs)
		print('\troom image = %d, temp room view = %d', (M[i+8], M[i+9]))
		i += 10
		n += 1
		if n == 42:
			# empirically determined
			break

def dumpcode(label, addr):
	print(label)

	while True:
		roomno = M[addr]
		if roomno == 0xff:
			break
		verbno = M[addr+1]
		nounno = M[addr+2]
		next = M[addr+3]
		nconds = M[addr+4]
		ninstrs = M[addr+5]

		L = []
		if roomno != 0xfe:
			L.append( 'ROOM = %d' % roomno )
		if verbno != 0xfe:
			L.append( 'VERB = "%s"' % verbs[verbno] )
		if nounno != 0xfe:
			L.append( 'NOUN = "%s"' % nouns[nounno] )

		pc = addr + 6
		for i in range(nconds):
			op = M[pc]
			nargs = 0
			if op == 3:
				nargs = 2
				objno = M[pc+1]
				loc = M[pc+2]
				s = 'OBJECT "%s" ' % objects[objno]
				if loc == 0xfe:
					s += 'CARRIED'
				else:
					s += 'IN ROOM %d' % loc
			elif op == 5:
				nargs = 1
				s = 'TURN >= %d' % M[pc+1]
			elif op == 6:
				nargs = 2
				varno = M[pc+1]
				const = M[pc+2]
				s = 'VAR %d = %d' % (varno, const)
			elif op == 9:
				nargs = 1
				const = M[pc+1]
				s = 'CURPIC = %d' % const
			elif op == 10:
				nargs = 2
				objno = M[pc+1]
				const = M[pc+2]
				s = 'OBJECT "%s" PICTURE = %d' % (
					objects[objno],
					const
				)
			else:
				assert 0

			L.append(s)
			pc += 1 + nargs

		if len(L) == 0:
			conds = 'true'
		else:
			conds = ' and '.join(L)

		print('%x:' % (addr))
		print('if', conds, 'then')

		INSTRS = {
			1:	( 2, None ),
			2:	( 2, None ),
			3:	( 2, None ),
			4:	( 0, 'inventory' ),
			5:	( 2, None ),
			6:	( 1, None ),
			7:	( 1, None ),
			8:	( 1, None ),
			9:	( 1, None ),
			10:	( 0, 'normal image' ),
			11:	( 0, 'blank image' ),
			12:	( 0, 'brk @ 0x66a8' ),
			13:	( 0, 'exit to BASIC' ),
			14:	( 0, 'brk @ 0x66b1' ),
			15:	( 0, 'save game' ),
			16:	( 0, 'load game' ),
			17:	( 0, 'replay game' ),
			18:	( 4, None ),
			19:	( 2, None ),
			20:	( 0, 'restore room view' ),
			21:	( 0, 'go north' ),
			22:	( 0, 'go south' ),
			23:	( 0, 'go east' ),
			24:	( 0, 'go west' ),
			25:	( 0, 'go up' ),
			26:	( 0, 'go down' ),
			27:	( 0, 'take (NOUN)' ),
			28:	( 0, 'drop (NOUN)' ),
			29:	( 2, None ),
		}
		for i in range(ninstrs):
			op = M[pc]
			if op not in INSTRS:
				print('\tunimp (%d)' % op)
				continue

			nargs = INSTRS[op][0]
			argv = []
			for j in range(nargs):
				argv.append( M[pc+j+1] )

			if type(INSTRS[op][1]) == type(''):
				s = INSTRS[op][1]
			elif op == 1:
				s = 'VAR %d += %d' % (argv[1], argv[0])
			elif op == 2:
				s = 'VAR %d -= %d' % (argv[1], argv[0])
			elif op == 3:
				s = 'VAR %d = %d' % (argv[0], argv[1])
			elif op == 5:
				if argv[1] == 0xfe:
					s = 'carry object %s (%d)' % (
						objects[argv[0]], argv[0]
					)
				else:
					s = 'object %s (%d) location = %d' % (
						objects[argv[0]],
						argv[0], argv[1]
					)
			elif op == 6:
				s = 'goto room %d' % argv[0]
			elif op == 7:
				s = 'set temp room view to %d' % argv[0]
			elif op == 8:
				s = 'set room images to %d' % argv[0]
			elif op == 9:
				s = 'print "%s"' % messages[argv[0]]
			elif op == 18:
				s = 'object %s (%d) location = %d, (x,y) = (%d,%d)' % (
					objects[argv[0]], argv[0],
					argv[1],
					argv[2], argv[3]
				)
			elif op == 19:
				s = 'object %s picture = %d' % (
					objects[argv[1]], argv[0]
				)
			elif op == 29:
				s = 'set room %d images to %d' % (
					argv[0], argv[1]
				)
			else:
				s = 'mystery op %d' % (
					op
				)

			print('\t%s' % s)
			pc += 1 + nargs

		addr += next

f = open(FILE, 'rb')
M = f.read()
f.close

# addresses from reversing
verbs = dumpdict('VERBS', 0x4000)
nouns = dumpdict('NOUNS', 0x1700)

messages = dumpmess()
objects = dumpobjects()
dumprooms()

dumpcode('HIGHPRI', 0x4500)
dumpcode('LOWPRI', 0x4400)
