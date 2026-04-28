import re

with open('/Users/harrygujjar/Documents/IPL-Predicition/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Only remove emoji characters, preserve all whitespace including tabs/newlines
emoji_pattern = re.compile(
    "["
    u"\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF"
    u"\U0001F1E0-\U0001F1FF"
    u"\U00002700-\U000027BF"
    u"\U0001F900-\U0001F9FF"
    u"\U00002600-\U000026FF"
    u"\U0001FA00-\U0001FA6F"
    u"\U0001FA70-\U0001FAFF"
    u"\U0001F700-\U0001F7FF"
    u"\U0001F780-\U0001F7FF"
    u"\U0001F800-\U0001F8FF"
    u"\U0001F004-\U0001F004"
    u"\U0001F0CF-\U0001F0CF"
    u"\U00002B50-\U00002B55"
    u"\U000025AA-\U000025FE"
    u"\U00002614-\U00002615"
    u"\U00002648-\U00002653"
    u"\U000026A1-\U000026A1"
    u"\U000026AA-\U000026AB"
    u"\U000026BD-\U000026BE"
    u"\U000026C4-\U000026C5"
    u"\U000026D4-\U000026D4"
    u"\U000026EA-\U000026EA"
    u"\U000026F2-\U000026F3"
    u"\U000026F5-\U000026F5"
    u"\U000026FA-\U000026FA"
    u"\U000026FD-\U000026FD"
    u"\U00002702-\U00002702"
    u"\U00002705-\U00002705"
    u"\U00002708-\U0000270D"
    u"\U0000270F-\U0000270F"
    u"\U00002712-\U00002712"
    u"\U00002714-\U00002714"
    u"\U00002716-\U00002716"
    u"\U00002728-\U00002728"
    u"\U00002733-\U00002734"
    u"\U00002744-\U00002744"
    u"\U0000274C-\U0000274C"
    u"\U0000274E-\U0000274E"
    u"\U00002753-\U00002757"
    u"\U00002763-\U00002764"
    u"\U00002795-\U00002797"
    u"\U000027A1-\U000027A1"
    u"\U000027B0-\U000027B0"
    u"\U00002934-\U00002935"
    u"\U00002B05-\U00002B07"
    u"\U00002B1B-\U00002B1C"
    u"\U00003030-\U00003030"
    u"\U0000FE0F-\U0000FE0F"  # variation selector — safe to remove
    "]+",
    flags=re.UNICODE
)

cleaned = emoji_pattern.sub('', content)

# Only strip trailing spaces on lines, never touch indentation
lines = cleaned.split('\n')
lines = [line.rstrip(' ') for line in lines]
cleaned = '\n'.join(lines)

with open('/Users/harrygujjar/Documents/IPL-Predicition/app.py', 'w', encoding='utf-8') as f:
    f.write(cleaned)

print("Done")
