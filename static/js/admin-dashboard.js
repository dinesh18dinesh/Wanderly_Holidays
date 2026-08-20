document.addEventListener('DOMContentLoaded',()=>{
 const sidebar=document.getElementById('adminSidebar'),toggle=document.getElementById('mobileToggle'),close=document.getElementById('sidebarClose'),overlay=document.getElementById('sidebarOverlay');
 const open=()=>{sidebar?.classList.add('open');overlay?.classList.add('show')};
 const shut=()=>{sidebar?.classList.remove('open');overlay?.classList.remove('show')};
 toggle?.addEventListener('click',open);close?.addEventListener('click',shut);overlay?.addEventListener('click',shut);
 document.querySelectorAll('.stat-card,.panel,.welcome-banner').forEach((el,i)=>{el.style.opacity='0';el.style.transform='translateY(10px)';setTimeout(()=>{el.style.transition='opacity .45s ease,transform .45s ease';el.style.opacity='1';el.style.transform='translateY(0)'},45+i*35)});
 document.querySelector('.search-box input')?.addEventListener('keydown',e=>{if(e.key==='Enter' && e.target.value.trim()){e.preventDefault();window.location.href="/django-admin/bookings/booking/?q="+encodeURIComponent(e.target.value.trim())}});
});