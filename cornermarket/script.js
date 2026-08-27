const nav = document.getElementById('nav');
if (nav) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 10);
  });
}

const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

document.querySelectorAll('.stat').forEach((el,i)=> el.style.transitionDelay = (i*0.08)+'s');
document.querySelectorAll('.menu-card').forEach((el,i)=> el.style.transitionDelay = (i*0.06)+'s');

/* ---- Order modal state ---- */
let mode = 'pickup';
let timing = 'now';

function openModal(){ const o=document.getElementById('modalOverlay'); if(o) o.classList.add('open'); }
function closeModal(){ const o=document.getElementById('modalOverlay'); if(o) o.classList.remove('open'); }

function setMode(m){
  mode = m;
  const sp=document.getElementById('segPickup'), sd=document.getElementById('segDelivery');
  if(sp) sp.classList.toggle('active', m==='pickup');
  if(sd) sd.classList.toggle('active', m==='delivery');
  updateNote();
}
function setTiming(t){
  timing = t;
  const cn=document.getElementById('cardNow'), cl=document.getElementById('cardLater');
  if(cn) cn.classList.toggle('active', t==='now');
  if(cl) cl.classList.toggle('active', t==='later');
  const sb=document.getElementById('scheduleBox');
  if(sb) sb.style.display = t==='later' ? 'block' : 'none';
  updateNote();
}
function setDate(el){
  document.querySelectorAll('.date-chip').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');
}
function updateNote(){
  const n = document.getElementById('confirmNote');
  if(!n) return;
  if(timing==='now'){
    n.textContent = 'Ready in ~15 mins · No payment until pickup';
  } else {
    n.textContent = (mode==='delivery' ? 'Delivery scheduled' : 'Pickup scheduled') + ' · We\'ll have it ready';
  }
}
function confirmOrder(){
  closeModal();
  // TODO: wire to menu/cart — for now just acknowledge.
}
