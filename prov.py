import difflib
words = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'wig', 'tig', 'pig', 'mig', 'vig', 'sig', 'aig', '1ig', '5ig', 'uig', 'big', 'grape', 'honeydew', 'indian gooseberry', 'jackfruit']
input_word = input('Введите слово: ')
matches = difflib.get_close_matches(input_word, words, n=5)
print('Самые похожие слова:')
for match in matches:
    print(match)