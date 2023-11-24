def confirm(question):
	res = input(question)
	if len(res) == 0:
		return False
	return res.lower()[0] == 'y'