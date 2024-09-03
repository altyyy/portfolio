import re

def extract_numbers(text):
    pattern = r'\d+(?:\.\d+)?'
    return re.findall(pattern, text)

# テスト文字列
text = "今日は3.14と42と0.5が見つかりました。"
numbers = extract_numbers(text)
print(numbers)