
  function toggleLike(btn) {
    btn.classList.toggle('liked');
    const countEl = btn.querySelector('span');
    const n = parseInt(countEl.textContent);
    if (btn.classList.contains('liked')) {
      countEl.textContent = n + 1;
      const svg = btn.querySelector('svg');
      svg.setAttribute('fill', 'currentColor');
      svg.setAttribute('stroke', 'none');
    } else {
      countEl.textContent = n - 1;
      const svg = btn.querySelector('svg');
      svg.setAttribute('fill', 'none');
      svg.setAttribute('stroke', 'currentColor');
    }
  }

  function toggleFollow(btn) {
    btn.classList.toggle('following');
    btn.textContent = btn.classList.contains('following') ? 'Following' : 'Follow';
  }

  // Nav active state
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
      item.classList.add('active');
    });
  });


