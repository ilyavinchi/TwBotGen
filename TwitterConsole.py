while True:
	with open("t.cmds", 'w') as f:
		wr = input("Введите код: ", )
		f.write(wr)