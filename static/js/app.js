// =========================
// Persian Datepicker Init
// =========================
$(function(){
  $('.datepicker').pDatepicker({
    format: 'YYYY/MM/DD',
    autoClose: true,
    toolbox: { calendarSwitch: { enabled: false } }
  });
});

// =========================
// Stats & Progress Bar
// =========================
function updateStats(){
  const tasks = document.querySelectorAll('#tasks-list .task');
  const total = tasks.length;
  const done = document.querySelectorAll('#tasks-list .completed').length;
  document.getElementById('total-count').textContent = total;
  document.getElementById('done-count').textContent = done;
  const percent = total ? Math.round((done/total)*100) : 0;
  document.getElementById('progress-bar').style.width = percent + '%';
}

// =========================
// Filter Tasks
// =========================
function filterBy(mode){
  const tasks = document.querySelectorAll('#tasks-list .task');
  tasks.forEach(t=> t.style.display = 'flex');
  if(mode === 'active'){
    tasks.forEach(t=> { if(t.classList.contains('completed')) t.style.display='none' });
  } else if(mode === 'done'){
    tasks.forEach(t=> { if(!t.classList.contains('completed')) t.style.display='none' });
  }
  document.getElementById('progress-bar').style.transition = 'width .8s cubic-bezier(.2,.9,.3,1)';
}

// =========================
// Animations & Enhancements
// =========================
window.addEventListener('load', ()=>{
  const taskEls = document.querySelectorAll('#tasks-list .task');
  taskEls.forEach((el,i)=> el.style.animationDelay = (i*40)+'ms');
  updateStats();
});

document.addEventListener('click', function(e){
  if(e.target.closest('.delete-btn')){
    const anchor = e.target.closest('a');
    const ok = confirm('آیا از حذف مطمئنی؟');
    if(!ok){
      e.preventDefault();
      const card = anchor.closest('.task');
      if(card){
        card.classList.add('shake');
        setTimeout(()=>card.classList.remove('shake'),500);
      }
    }
  }
});
