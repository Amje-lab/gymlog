import os

html_path = r'C:\Users\Amier\Desktop\gymlog\index.html'
ws_path = r'C:\Users\Amier\.gemini\antigravity\scratch\workout-tracker\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken emojis
bad_func = '''    function getFlameEmoji(s) {
      if (s >= 5000) return '??';
      if (s >= 2000) return '??';
      if (s >= 1000) return '??';
      if (s >= 500) return '??';
      if (s >= 300) return '??';
      if (s >= 100) return '?';
      if (s >= 30) return '??';
      if (s >= 10) return '??';
      return '??';
    }'''

good_func = '''    function getFlameEmoji(s) {
      if (s >= 5000) return '♾️';
      if (s >= 2000) return '🌌';
      if (s >= 1000) return '💎';
      if (s >= 500) return '👑';
      if (s >= 300) return '🌟';
      if (s >= 100) return '⚡';
      if (s >= 30) return '💥';
      if (s >= 10) return '☄️';
      return '🔥';
    }'''

content = content.replace(bad_func, good_func)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
with open(ws_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Emojis fixed via Python!")