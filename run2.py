import os
import re

html_path = r'C:\Users\Amier\Desktop\gymlog\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Agenda View HTML to add a month title and week combo section
new_agenda_html = '''id="viewAgenda" style="display: none;">
      <!-- STREAK BANNER -->
      <div class="streak-container">
        <div class="streak-fire-wrapper">
          <span class="streak-flame-icon streak-flame-gray" id="streakFlameIcon">&#128293;</span>
        </div>
        <div class="streak-count-number" id="streakNumberDisplay">0</div>
      </div>

      <!-- CALENDAR MONTH -->
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; margin-top: 10px;">
        <h3 class="section-title" id="agendaMonthTitle" style="margin: 0; font-size: 18px;">Augustus</h3>
      </div>
      <div class="cal-grid-header" id="calGridHeaderDays">
        <span>Ma</span><span>Di</span><span>Wo</span><span>Do</span><span>Vr</span><span>Za</span><span>Zo</span>
      </div>
      <div class="cal-grid" id="agendaGridContainer"></div>

      <!-- MIJN COMBO / SCHEMA -->
      <h3 class="section-title" style="margin-top: 24px; font-size: 16px;">Mijn Week Schema</h3>
      <div id="agendaWeekComboContainer" style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 24px;"></div>

      <!-- SELECTED DAY DETAIL PREVIEW -->
      <div id="agendaDayDetailContainer"></div>
    </div>'''

content = re.sub(r'id="viewAgenda" style="display: none;">.*?</div>\s*</div>\s*</div>\s*<!-- VIEW 3', new_agenda_html + '\n\n    <!-- VIEW 3', content, flags=re.DOTALL)

# Update renderAgendaView to show a real month calendar and the weekly combo
old_render_agenda = '''function renderAgendaView() {
    updateHomeStreakFlame();
    const streak = calculateCurrentStreak();'''

new_render_agenda_logic = '''function renderAgendaView() {
    updateHomeStreakFlame();
    const streak = calculateCurrentStreak();
    const numEl = document.getElementById('streakNumberDisplay');
    if (numEl) numEl.textContent = streak;

    const today = new Date();
    today.setHours(0,0,0,0);
    
    // Set Month Title
    const monthNames = ['Januari', 'Februari', 'Maart', 'April', 'Mei', 'Juni', 'Juli', 'Augustus', 'September', 'Oktober', 'November', 'December'];
    const monthTitle = document.getElementById('agendaMonthTitle');
    if (monthTitle) monthTitle.textContent = monthNames[today.getMonth()] + ' ' + today.getFullYear();

    const grid = document.getElementById('agendaGridContainer');
    if (grid) grid.innerHTML = '';
    const schema = getActiveRoutineSchema();

    // Generate current month calendar
    const year = today.getFullYear();
    const month = today.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    
    let startDayIdx = firstDay.getDay() - 1;
    if (startDayIdx === -1) startDayIdx = 6; // Sunday is 6
    
    // Pad start
    for (let i = 0; i < startDayIdx; i++) {
      const emptyCell = document.createElement('div');
      emptyCell.className = 'cal-cell locked';
      emptyCell.style.background = 'transparent';
      emptyCell.style.border = 'none';
      if (grid) grid.appendChild(emptyCell);
    }
    
    // Days in month
    for (let i = 1; i <= lastDay.getDate(); i++) {
      const cellDate = new Date(year, month, i);
      const dateStr = formatDateKey(cellDate);
      const dOfWeek = cellDate.getDay();
      const dIdx = (dOfWeek === 0 ? 6 : dOfWeek - 1);

      const isToday = isDateToday(cellDate);
      const isFuture = isDateInFuture(cellDate);
      const isSelected = (formatDateKey(selectedAgendaDate) === dateStr);

      const dayData = schema[dIdx] || { groups: [] };
      const allEx = dayData.groups.flatMap(g => g.exercises);
      const isCompleted = (allEx.length > 0 && allEx.every(ex => loadExerciseDoneState(dateStr, dIdx, ex)));

      const cell = document.createElement('div');
      cell.className = cal-cell;
      
      let statusHtml = '';
      if (isCompleted) statusHtml = '<svg style="width:12px;height:12px;fill:var(--green);" viewBox="0 0 24 24"><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>';
      else if (isFuture) statusHtml = '';
      else if (allEx.length === 0) statusHtml = '-';

      cell.innerHTML = 
        <div class="cal-num"></div>
        <div class="cal-status-icon"></div>
      ;

      cell.onclick = () => {
        selectedAgendaDate = cellDate;
        renderAgendaView();
      };
      if (grid) grid.appendChild(cell);
    }

    // Render Week Combo
    const comboContainer = document.getElementById('agendaWeekComboContainer');
    if (comboContainer) {
      comboContainer.innerHTML = '';
      const dayNames = ['Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag', 'Zaterdag', 'Zondag'];
      for (let i = 0; i < 7; i++) {
        const dData = schema[i] || { groups: [] };
        const groupsList = dData.groups.map(g => g.title).join(', ');
        const isRest = dData.label.includes('RUST') || dData.label.includes('REST');
        const desc = isRest ? 'Rustdag' : (groupsList || 'Vrije training');
        
        const row = document.createElement('div');
        row.style.cssText = 'display: flex; justify-content: space-between; align-items: center; padding: 12px 14px; background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px;';
        row.innerHTML = 
          <div>
            <div style="font-size: 13px; font-weight: 800; color: ;"></div>
            <div style="font-size: 11.5px; color: var(--text-sec); margin-top: 2px;"></div>
          </div>
          <button onclick="switchTab('search')" style="padding: 6px 12px; border-radius: 8px; border: none; background: var(--surface-2); color: var(--text); font-size: 11px; font-weight: 700; cursor: pointer;">
            Bewerk
          </button>
        ;
        comboContainer.appendChild(row);
      }
    }

    renderAgendaDayDetail(selectedAgendaDate);
  }

  // OLD CODE STUB TO PREVENT DUPLICATES
  function renderAgendaView_OLD() {'''

content = re.sub(r'function renderAgendaView\(\) \{[\s\S]*?renderAgendaDayDetail\(selectedAgendaDate\);\s*\}', new_render_agenda_logic, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Phase 2 done")
