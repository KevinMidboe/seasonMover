import tvdb_api, hashlib

def main():
	t = tvdb_api.Tvdb()
	show = 'Rick and morty'.lower()
	season = 3
	for ep in range(1,10):
		episode = t[show][season][ep]
		itemConcat = '.'.join([show, str(season), str(ep)])
		hash_object = hashlib.sha1(str.encode(itemConcat))
		hex_dig = hash_object.hexdigest()
		print('%s : %s' % (hex_dig, itemConcat))

if __name__ == '__main__':
	main()