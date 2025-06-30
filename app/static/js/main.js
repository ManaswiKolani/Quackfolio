document.addEventListener('DOMContentLoaded', () => {
    const popup = document.getElementById('stock-popup');
    const body = document.getElementById('popup-body');
    const closeBtn = document.getElementById('popup-close');

    document.querySelectorAll('.duck-img').forEach(duck => {
        const status = duck.getAttribute('data-status');

        duck.addEventListener('mouseenter', () => {
            duck.src = `/static/images/${status === 'good' ? 'good_duck2' : 'bad_duck2'}.png`;
        });

        duck.addEventListener('mouseleave', () => {
            duck.src = `/static/images/${status === 'good' ? 'good_duck' : 'bad_duck'}.png`;
        });

        duck.addEventListener('click', () => {
            const ticker = duck.getAttribute('data-ticker');
            const price = duck.getAttribute('data-price');
            const change = duck.getAttribute('data-change');
            const percent = duck.getAttribute('data-percent');
            const volume = duck.getAttribute('data-volume');
            const avgVolume = duck.getAttribute('data-avg-volume');
            const marketCap = duck.getAttribute('data-market-cap');
            const pe = duck.getAttribute('data-pe') || "--";
            const change52wk = duck.getAttribute('data-change52wk') || "--";
            const graphPath = duck.getAttribute('data-graph');
            

            body.innerHTML = `
                <strong>${ticker}</strong><br>
                Price: ${price}<br>
                Change: ${change} (${percent})<br>
                Volume: ${volume}<br>
                Avg Volume: ${avgVolume}<br>
                Market Cap: ${marketCap}<br>
                P/E Ratio (TTM): ${pe}<br>
                52 Week Change: ${change52wk}<br><br>
                ${graphPath ? `<img src="${graphPath}" alt="Graph for ${ticker}" style="width: 100%; border-radius: 8px; border: 1px solid #999;" onerror="console.error('Failed to load graph:', '${graphPath}')">` : '<p>No graph available</p>'}
            `;

            popup.classList.remove('hidden');
        });
    });

    closeBtn.addEventListener('click', () => {
        popup.classList.add('hidden');
    });

    popup.addEventListener('click', (e) => {
        if (e.target === popup) {
            popup.classList.add('hidden');
        }
    });
});