import os
import re

html_path = r'C:\Users\Amier\Desktop\gymlog\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Header padding for mobile (top spacing)
content = content.replace('.app-header {', '.app-header {\n      padding-top: max(env(safe-area-inset-top), 24px);')
content = content.replace('.app-header {', '.app-header {\n      margin-top: 15px;') # additional spacing just in case

# 2. Blue buttons -> Grey
content = content.replace('linear-gradient(135deg, #0a84ff 0%, #00d2ff 100%)', 'linear-gradient(135deg, #4b5563 0%, #9ca3af 100%)')
content = content.replace('rgba(0, 210, 255, 0.35)', 'rgba(156, 163, 175, 0.35)')
# Replace active cyan text with grey/white
content = content.replace('color: #00d2ff', 'color: #9ca3af')
content = content.replace('border: 1px solid rgba(0,210,255,0.3)', 'border: 1px solid rgba(156,163,175,0.3)')
content = content.replace('box-shadow: 0 4px 16px rgba(0, 210, 255, 0.35)', 'box-shadow: 0 4px 16px rgba(156,163,175, 0.35)')

# 3. Theme Grid Swiping
content = content.replace('id="themeColorGrid" style="display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:10px;"', 'id="themeColorGrid" style="display:flex; overflow-x:auto; gap:16px; margin-top:10px; padding-bottom:12px; scroll-snap-type: x mandatory;"')
# Add flex-shrink to the swatches in JS
content = content.replace("swatch.className = 'theme-swatch';", "swatch.className = 'theme-swatch';\n      swatch.style.flexShrink = '0';\n      swatch.style.scrollSnapAlign = 'center';")

# 4. Profile Picture
profile_pic_html = '''
      <div style="display: flex; justify-content: center; margin-bottom: 24px;">
        <label for="profileImageInput" style="cursor: pointer; position: relative; display: block;">
          <div id="profileAvatarPreview" style="width: 100px; height: 100px; border-radius: 50%; background: var(--surface-2); border: 2px solid var(--border); display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 800; color: var(--text-sec); overflow: hidden; background-size: cover; background-position: center;">A</div>
          <div style="position: absolute; bottom: 0; right: 0; background: #4b5563; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border: 2px solid var(--bg-top); box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
            <svg style="width:16px;height:16px;fill:#fff" viewBox="0 0 24 24"><path d="M4 4h3l2-2h6l2 2h3a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm8 3a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 2a3 3 0 1 1 0 6 3 3 0 0 1 0-6z"/></svg>
          </div>
        </label>
        <input type="file" id="profileImageInput" accept="image/*" style="display:none;" onchange="handleProfileImageUpload(event)" />
      </div>
'''
content = content.replace('<!-- PERSOONLIJKE GEGEVENS -->\n      <div class="profile-card">', f'<!-- PERSOONLIJKE GEGEVENS -->\n{profile_pic_html}\n      <div class="profile-card">')

js_avatar = '''
  function handleProfileImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
      const dataUrl = e.target.result;
      localStorage.setItem('gymlog_avatar', dataUrl);
      updateAvatarDisplays();
      triggerToast('Profielfoto geüpdatet!');
    };
    reader.readAsDataURL(file);
  }

  function updateAvatarDisplays() {
    const saved = localStorage.getItem('gymlog_avatar');
    const headerBtn = document.getElementById('headerAvatarBtn');
    const profilePrev = document.getElementById('profileAvatarPreview');
    const name = (document.getElementById('profileNameInput') || {}).value || 'A';
    const initial = name.charAt(0).toUpperCase();

    if (saved) {
      if (headerBtn) { headerBtn.style.backgroundImage = url(); headerBtn.style.backgroundSize = 'cover'; headerBtn.style.backgroundPosition = 'center'; headerBtn.textContent = ''; }
      if (profilePrev) { profilePrev.style.backgroundImage = url(); profilePrev.textContent = ''; }
    } else {
      if (headerBtn) { headerBtn.style.backgroundImage = 'none'; headerBtn.textContent = initial; }
      if (profilePrev) { profilePrev.style.backgroundImage = 'none'; profilePrev.textContent = initial; }
    }
  }
'''
content = content.replace('function loadProfileSettings() {', f'{js_avatar}\n  function loadProfileSettings() {{')
content = content.replace('loadProfileSettings();\n  renderHomeView();', 'loadProfileSettings();\n  updateAvatarDisplays();\n  renderHomeView();')


# 5. Streak Flame Logic & Styling
# We need to replace the streak card HTML in viewHome so it has proper IDs
old_streak_html = '<div style="background: linear-gradient(180deg, rgba(255, 149, 0, 0.12) 0%, rgba(20, 22, 28, 0.95) 100%); border: 1.5px solid rgba(255, 149, 0, 0.35); border-radius: 16px; padding: 14px 18px; margin-bottom: 14px; display: flex; align-items: center; gap: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">'
new_streak_html = '<div id="homeStreakCard" style="background: linear-gradient(180deg, rgba(136, 136, 136, 0.12) 0%, rgba(20, 22, 28, 0.95) 100%); border: 1.5px solid rgba(136, 136, 136, 0.35); border-radius: 16px; padding: 14px 18px; margin-bottom: 14px; display: flex; align-items: center; gap: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); transition: all 0.3s;">'
content = content.replace(old_streak_html, new_streak_html)
content = content.replace('<span style="color: #ff9500; letter-spacing: 0.04em;"> DAGEN STREAK</span>', '<span id="homeStreakLabel" style="color: #888; letter-spacing: 0.04em; transition: all 0.3s;"> DAGEN STREAK</span>')

# Update updateHomeStreakFlame function
old_flame_logic = '''    // Home flame icon color: grey unless trained today
    const homeFlame = document.getElementById('homeStreakFlame');
    if (homeFlame) {
      if (trainedToday || streak > 0) {
        homeFlame.style.filter = 'none';
        homeFlame.style.opacity = '1';
        homeFlame.style.color = '#ff9500';
      } else {
        homeFlame.style.filter = 'grayscale(1)';
        homeFlame.style.opacity = '0.4';
        homeFlame.style.color = '#888';
      }
    }'''

new_flame_logic = '''
    function getFlameEmoji(s) {
      if (s >= 5000) return '♾️';
      if (s >= 2000) return '🌌';
      if (s >= 1000) return '💎';
      if (s >= 500) return '👑';
      if (s >= 300) return '🌟';
      if (s >= 100) return '⚡';
      if (s >= 30) return '💥';
      if (s >= 10) return '☄️';
      return '🔥';
    }

    const homeFlame = document.getElementById('homeStreakFlame');
    const homeCard = document.getElementById('homeStreakCard');
    const homeLabel = document.getElementById('homeStreakLabel');
    
    if (homeFlame) {
      homeFlame.textContent = getFlameEmoji(streak);
      if (trainedToday || streak > 0) {
        homeFlame.style.filter = 'none';
        homeFlame.style.opacity = '1';
        homeFlame.style.color = '#ff9500';
        if (homeCard) {
          homeCard.style.border = '1.5px solid rgba(255, 149, 0, 0.4)';
          homeCard.style.background = 'linear-gradient(180deg, rgba(255, 149, 0, 0.15) 0%, rgba(20, 22, 28, 0.95) 100%)';
        }
        if (homeLabel) homeLabel.style.color = '#ff9500';
      } else {
        homeFlame.style.filter = 'grayscale(1)';
        homeFlame.style.opacity = '0.6';
        homeFlame.style.color = '#888';
        if (homeCard) {
          homeCard.style.border = '1.5px solid rgba(136, 136, 136, 0.3)';
          homeCard.style.background = 'linear-gradient(180deg, rgba(136, 136, 136, 0.1) 0%, rgba(20, 22, 28, 0.95) 100%)';
        }
        if (homeLabel) homeLabel.style.color = '#888';
      }
    }
'''
content = content.replace(old_flame_logic, new_flame_logic)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Phase 1 done')
