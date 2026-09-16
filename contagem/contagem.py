words = ["python", "java", "python"]

count = {}

for word in words:
    count[word] = count.get(word, 0) + 1

sorted_words = sorted(
    count.items(),
    key=lambda x: (-x[1], x[0])
)

result = [word for word, freq in sorted_words[:3]]

print(result)