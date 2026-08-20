document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('input[type="date"]').forEach(input => {
    if (!input.min) input.min = new Date().toISOString().split('T')[0];
  });
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      if (alert.classList.contains('show')) bootstrap.Alert.getOrCreateInstance(alert).close();
    }, 6000);
  });
  // One-step live package search on the homepage.
  const searchForm = document.getElementById('heroPackageSearch');
  const searchInput = document.getElementById('heroSearchInput');
  const suggestions = document.getElementById('packageSuggestions');
  const searchHelp = document.getElementById('searchHelp');

  if (searchForm && searchInput && suggestions) {
    let searchTimer = null;
    let activeController = null;

    const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, char => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    }[char]));

    const clearSuggestions = () => {
      suggestions.innerHTML = '';
      suggestions.classList.remove('show');
    };

    const renderSuggestions = (data) => {
      const countLabel = data.count === 1 ? '1 package available' : `${data.count} packages available`;
      suggestions.innerHTML = `
        <div class="suggestion-heading">
          <span><i class="fa-solid fa-location-dot me-1"></i>${escapeHtml(data.query)}</span>
          <strong>${countLabel}</strong>
        </div>
        ${data.packages.map(pkg => `
          <a class="package-suggestion-item" href="${escapeHtml(pkg.url)}" role="option">
            <div class="suggestion-thumb">
              ${pkg.image ? `<img src="${escapeHtml(pkg.image)}" alt="">` : `<i class="fa-solid fa-image"></i>`}
            </div>
            <div class="suggestion-info">
              <strong>${escapeHtml(pkg.name)}</strong>
              <span><i class="fa-solid fa-location-dot"></i> ${escapeHtml(pkg.destination)}</span>
              <small>${escapeHtml(pkg.duration)} · ${escapeHtml(pkg.package_type)}</small>
            </div>
            <div class="suggestion-price">
              <small>From</small>
              <b>₹${escapeHtml(pkg.price)}</b>
              <i class="fa-solid fa-arrow-right"></i>
            </div>
          </a>
        `).join('')}
        <a class="suggestion-all" href="${window.packageListUrl}?q=${encodeURIComponent(data.query)}">
          View all matching packages <i class="fa-solid fa-arrow-right ms-1"></i>
        </a>`;
      suggestions.classList.add('show');
      searchHelp.textContent = `${countLabel} — choose a package to continue.`;
    };

    const showUnavailable = (query) => {
      clearSuggestions();
      searchHelp.textContent = `No package found for "${query}".`;
      const message = document.getElementById('packageUnavailableMessage');
      if (message) message.textContent = `We couldn't find a holiday package for "${query}". Try Goa, Kerala, Bali, Maldives, Dubai or another destination from our catalogue.`;
      const modalEl = document.getElementById('packageUnavailableModal');
      if (modalEl && window.bootstrap) {
        bootstrap.Modal.getOrCreateInstance(modalEl).show();
      } else {
        window.alert(`Package not available for "${query}".`);
      }
    };

    const fetchSuggestions = async (showModalIfEmpty = false) => {
      const query = searchInput.value.trim();
      if (query.length < 2) {
        clearSuggestions();
        searchHelp.textContent = 'Please enter at least 2 characters.';
        return false;
      }
      if (activeController) activeController.abort();
      activeController = new AbortController();
      try {
        const response = await fetch(`${window.packageSearchUrl}?q=${encodeURIComponent(query)}`, {
          headers: {'X-Requested-With': 'XMLHttpRequest'},
          signal: activeController.signal
        });
        if (!response.ok) throw new Error('Search request failed');
        const data = await response.json();
        if (data.packages.length) {
          renderSuggestions(data);
          return true;
        }
        if (showModalIfEmpty) showUnavailable(query);
        else {
          clearSuggestions();
          searchHelp.textContent = `No package found for "${query}".`;
        }
        return false;
      } catch (error) {
        if (error.name !== 'AbortError') {
          clearSuggestions();
          searchHelp.textContent = 'Search is temporarily unavailable. Please try again.';
        }
        return false;
      }
    };

    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(() => fetchSuggestions(false), 220);
    });

    searchForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const query = searchInput.value.trim();
      if (!query) {
        searchInput.focus();
        searchHelp.textContent = 'Please enter a destination or holiday type.';
        return;
      }
      const found = await fetchSuggestions(true);
      if (found) {
        const first = suggestions.querySelector('.package-suggestion-item');
        const count = suggestions.querySelectorAll('.package-suggestion-item').length;
        // One match: take the customer directly to that package. Multiple matches:
        // take them to the package results page so they can choose.
        if (first && count === 1) {
          window.location.href = first.href;
        } else {
          window.location.href = `${window.packageListUrl}?q=${encodeURIComponent(query)}`;
        }
      } else {
        event.stopPropagation();
      }
    });

    document.addEventListener('click', (event) => {
      if (!searchForm.contains(event.target)) clearSuggestions();
    });

    searchInput.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') clearSuggestions();
    });
  }

});

// Global image fallback: broken remote/package images never show a broken-image icon.
document.addEventListener('error', function(event) {
  const img = event.target;
  if (img && img.tagName === 'IMG' && !img.dataset.fallbackApplied) {
    img.dataset.fallbackApplied = '1';
    img.src = '/static/images/travel-placeholder.svg';
    img.classList.add('image-fallback');
  }
}, true);
