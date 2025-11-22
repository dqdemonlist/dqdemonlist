class Router {
    constructor() {
        this.routes = {
            '/': this.renderHome,
            '/demons': this.renderDemons,
            '/players': this.renderPlayers,
            '/future': this.renderFutureDemons,
            '/rules': this.renderRules,
            '/send-record': this.renderSendRecord,
            '/stats': this.renderStats
        };
        
        this.init();
    }
    
    init() {
        window.addEventListener('hashchange', () => this.handleRoute());
        window.addEventListener('load', () => this.handleRoute());
    }
    
    handleRoute() {
        const hash = window.location.hash.slice(1) || '/';
        const renderFunction = this.routes[hash];
        
        if (renderFunction) {
            renderFunction.call(this);
            this.updateActiveLink(hash);
        } else {
            this.render404();
        }
    }
    
    updateActiveLink(currentRoute) {
        // Обновляем активные ссылки в dropdown
        const dropdownLinks = document.querySelectorAll('.dropdown-link');
        dropdownLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentRoute}`) {
                link.classList.add('active');
            }
        });
    }
    
    renderHome() {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="home-container">
                <h1 class="home-title">Dolores Squad's Lists</h1>
                <p class="home-subtitle">
                Demonlist, Top Players, Future Demons List of Dolores Squad's Community.
                Follow other players' progress, browse the top rankings, and join Dolores Squad!
                </p>
                <div class="home-buttons">
                    <a href="#/demons" class="home-btn btn-demons">Demonlist</a>
                    <a href="#/players" class="home-btn btn-players">Players List</a>
                    <a href="#/future" class="home-btn btn-future">Future Demons</a>
                    <a href="#/rules" class="home-btn btn-rules">Rules</a>
                </div>
                <div class="stats-container">
                    <div class="stat-card">
                        <div>${getAllDemons().length}</div>
                        <div>Demons in ranking</div>
                    </div>
                    <div class="stat-card">
                        <div>${getAllPlayers().length}</div>
                        <div>Players in ranking</div>
                    </div>
                    <div class="stat-card">
                        <div>${getAllFutureDemons().length}</div>
                        <div>Future Demons</div>
                    </div>
                </div>
            </div>
        `;
    }
    
renderDemons() {
    const leaderboard = getDemonLeaderboard();
    const demonsHTML = leaderboard.map(demon => `
        <div class="demon-item" data-demon-id="${demon.id}">
            <div class="demon-rank">#${demon.position}</div>
            <div class="demon-info">
                <div class="demon-name">${demon.name}</div>
                <div class="demon-creator">by ${demon.creator}</div>
            </div>
            <div class="demon-points">${demon.points} pts</div>
        </div>
    `).join('');
    
    const app = document.getElementById('app');
    app.innerHTML = `
        <div class="demons-container">
            <h1 class="page-title">Demonlist</h1>
            <div class="demons-list">
                ${demonsHTML}
            </div>
        </div>
    `;
    
    document.querySelectorAll('.demon-item').forEach(item => {
        item.addEventListener('click', () => {
            const demonId = parseInt(item.getAttribute('data-demon-id'));
            openDemonModal(demonId);
        });
    });
}

renderPlayers() {
    const leaderboard = getPlayerLeaderboard();
    const playersHTML = leaderboard.map(player => {
        const playerPoints = calculatePlayerPoints(player.id);
        return `
            <div class="player-item" data-player-id="${player.id}">
                <div class="player-rank">#${player.position}</div>
                <div class="player-info">
                    <div class="player-name">${player.name}</div>
                    <div class="player-stats">${player.completedDemons.length} Completed demons</div>
                </div>
                <div class="player-points">${playerPoints} pts</div>
            </div>
        `;
    }).join('');
    
    const app = document.getElementById('app');
    app.innerHTML = `
        <div class="players-container">
            <h1 class="page-title">Players List</h1>
            <div class="players-list">
                ${playersHTML}
            </div>
        </div>
    `;
    
    document.querySelectorAll('.player-item').forEach(item => {
        item.addEventListener('click', () => {
            const playerId = parseInt(item.getAttribute('data-player-id'));
            openPlayerModal(playerId);
        });
    });
}
    
    renderFutureDemons() {
        const futureDemons = getAllFutureDemons();
        const futureDemonsHTML = futureDemons.map(demon => {
            const beatingPlayers = getBeatingPlayers(demon.id);
            const playersHTML = beatingPlayers.map(bp => `
                <div class="beating-player">
                    <div class="player-progress-info">
                        <span class="player-name">${bp.playerName}</span>
                        <span class="progress-percent">${bp.progress}%</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: ${bp.progress}%"></div>
                    </div>
                </div>
            `).join('');
            
            return `
                <div class="future-demon-item" data-future-demon-id="${demon.id}">
                    <div class="future-demon-header">
                        <div class="future-demon-info">
                            <div class="future-demon-name">${demon.name}</div>
                            <div class="future-demon-creator">by ${demon.creator}</div>
                        </div>
                        <div class="future-demon-difficulty">${demon.difficulty}</div>
                    </div>
                    <div class="beating-players">
                        ${playersHTML}
                    </div>
                </div>
            `;
        }).join('');
        
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="future-demons-container">
                <h1 class="page-title">Future Demons</h1>
                <h3>
                    Levels that can reach the top!
                </h3>
                <div class="future-demons-list">
                    ${futureDemonsHTML}
                </div>
            </div>
        `;
        
        document.querySelectorAll('.future-demon-item').forEach(item => {
            item.addEventListener('click', () => {
                const demonId = parseInt(item.getAttribute('data-future-demon-id'));
                openFutureDemonModal(demonId);
            });
        });
    }
    
    renderRules() {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="rules-container">
                <h1 class="page-title">Правила Демонлиста</h1>
                <div class="rules-content">
                    <div class="rules-section">
                        <h2>📋 Требования к демонам</h2>
                        <ul class="rules-list">
                            <li>Уровень должен быть верифицирован</li>
                            <li>Минимальный порог входа в лист начинается от Easy Demon</li>
                            <li>Уровень должен быть рейтнут</li>
                        </ul>
                    </div>
                    
                    <div class="rules-section">
                        <h2>🎮 Требования к игрокам</h2>
                        <ul class="rules-list">
                            <li>Читерство: Любое использование читов ведет к бану из топа</li>
                            <li>Подтверждение рекордов через сырое, нередактированное видео (Google Disk - Yandex Disk)</li>
                            <li>FPS: Разрешено прохождение на любом FPS, но без FPS Bypass (использование физики 2.1 в моде Click Between Frames также запрещено)</li>
                        </ul>
                    </div>
                    
                    <div class="rules-section">
                        <h2>⭐ Система очков</h2>
                        <ul class="rules-list">
                            <li>Базовые очки: Топ 1 демон дает 500 очков</li>
                            <li>Уменьшение: Каждая следующая позиция теряет 19% очков</li>
                            <li>Обновление: Очки пересчитываются при изменении топа</li>
                        </ul>
                    </div>
                    <div class="rules-section">
                        <h2>📹 Требования к доказательствам</h2>
                        <ul class="rules-list">
                            <li>Видео загруженное на Yandex Disk или Doogle Drive должно показывать весь геймплей</li>
                            <li>Должны быть слышны клики, показаны индикаторы FPS, CPS</li>
                            <li>Видео должно быть в качестве 720p или выше</li>
                        </ul>
                    </div>
                </div>
            </div>
                </div>
            </div>
            <div class="rules-container2">
            <div class="rules-content">
                    <div class="rules-section">
                        <h2>Контакты модераторов для помощи в Discord</h2>
                        <ul class="rules-list">
                            <li>Dolores - king5356</li>
                            <li>angyedz - angyedz</li>
                            <li>Wlen0k - looloolloolol</li>
                        </ul>
                    </div>
            
            
            
            
            
            </div>
        `;
    }
    
    render404() {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="home-container">
                <h1 class="home-title">404 - Страница не найдена</h1>
                <p class="home-subtitle">
                    Запрошенная страница не существует. Вернитесь на главную страницу.
                </p>
                <div class="home-buttons">
                    <a href="#/" class="home-btn btn-demons">На главную</a>
                </div>
            </div>
        `;
    }
renderHome() {
    const totalPlayers = getTotalPlayers();
    const totalDemons = getTotalDemons();
    const totalFutureDemons = getTotalFutureDemons();
    const totalCompletions = getTotalCompletions();
    const averageCompletions = getAverageCompletionsPerDemon();
    const mostCompletedDemon = getMostCompletedDemon();
    const topPlayer = getPlayerWithMostPoints();
    const topDemon = getDemonWithHighestPoints();
    const totalPoints = getTotalPointsDistributed();
    const recentCompletions = getRecentCompletions();

    const statsHTML = `
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number">${totalDemons}</div>
                <div class="stat-label">Demons in ranking</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${totalPlayers}</div>
                <div class="stat-label">Players in ranking</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${totalFutureDemons}</div>
                <div class="stat-label">Future Demons</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${totalCompletions}</div>
                <div class="stat-label">All completions</div>
            </div>
        </div>
    `;

    const detailedStatsHTML = `
        <div class="detailed-stats">
            <div class="stats-grid">
                <div class="stat-item-large">
                    <div class="stat-value">${averageCompletions}</div>
                    <div class="stat-label">Average number of beatings per demon</div>
                </div>
                <div class="stat-item-large">
                    <div class="stat-value">${totalPoints}</div>
                    <div class="stat-label">All Points</div>
                </div>
            </div>
            
            ${topPlayer ? `
            <div class="top-player-card">
                <h3>👑 Best Player</h3>
                <div class="player-info">
                    <span class="player-name">${topPlayer.name}</span>
                    <span class="player-points">${calculatePlayerPoints(topPlayer.id)} points</span>
                </div>
                <div class="player-stats">
                    ${topPlayer.completedDemons.length} demons beated
                </div>
            </div>
            ` : ''}
            
            ${topDemon ? `
            <div class="top-demon-card">
                <h3>🔥 Top 1 Demon</h3>
                <div class="demon-info">
                    <span class="demon-name">${topDemon.name}</span>
                    <span class="demon-points">${topDemon.points} points</span>
                </div>
                <div class="demon-stats">
                    ${topDemon.completers.length} players beated
                </div>
            </div>
            ` : ''}
            
            ${mostCompletedDemon ? `
            <div class="popular-demon-card">
                <h3>🎯 Most Popular</h3>
                <div class="demon-info">
                    <span class="demon-name">${mostCompletedDemon.name}</span>
                    <span class="completion-count">${mostCompletedDemon.completers.length} completions</span>
                </div>
            </div>
            ` : ''}
        </div>
    `;

    const recentCompletionsHTML = recentCompletions.length > 0 ? `
        <div class="recent-completions">
            <h3>🕐 Recent completions</h3>
            <div class="completions-list">
                ${recentCompletions.map(completion => `
                    <div class="completion-item">
                        <span class="player">${completion.playerName}</span>
                        <span class="demon">${completion.demonName}</span>
                        <span class="date">${formatDate(completion.date)}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    ` : '';

    const app = document.getElementById('app');
    app.innerHTML = `
        <div class="home-container">
            <h1 class="home-title">Dolores Squad's Lists</h1>
            <p class="home-subtitle">
            Demonlist, Top Players, Future Demons List of Dolores Squad's Community.
            Follow other players' progress, browse the top rankings, and join Dolores Squad!
            </p>
            <div class="home-buttons">
                <a href="#/demons" class="home-btn btn-demons">Demonlist</a>
                <a href="#/players" class="home-btn btn-players">Players list</a>
                <a href="#/future" class="home-btn btn-future">Future Demons</a>
                <a href="#/rules" class="home-btn btn-rules">Rules</a>
            </div>
            
            ${statsHTML}
            ${detailedStatsHTML}
            ${recentCompletionsHTML}
        </div>
    `;
}
// ===== НОВАЯ ВКЛАДКА: СТАТИСТИКА =====
renderStats() {
    const app = document.getElementById('app');

    // --- Общая статистика ---
    const totalPlayers = getTotalPlayers();
    const totalDemons = getTotalDemons();
    const totalFutureDemons = getTotalFutureDemons();
    const totalCompletions = getTotalCompletions();
    const avgCompletions = totalDemons ? (totalCompletions / totalDemons).toFixed(2) : 0;
    const totalPoints = getTotalPointsDistributed();

    // --- Лидеры ---
    const topPlayer = getPlayerWithMostPoints();
    const topDemon = getMostCompletedDemon();
    const demons = getAllDemons();
    const newestDemon = demons.reduce((a, b) => new Date(a.verifyDate) > new Date(b.verifyDate) ? a : b);
    const oldestDemon = demons.reduce((a, b) => new Date(a.verifyDate) < new Date(b.verifyDate) ? a : b);

    const playerMostBeats = getAllPlayers().reduce((a, b) => a.completedDemons.length > b.completedDemons.length ? a : b);

    // --- Активность (последние 10 прохождений) ---
    const allCompletions = [];
    demons.forEach(demon => {
        demon.completers.forEach(c => {
            allCompletions.push({
                player: getPlayerById(c.playerId)?.name || 'Unknown',
                demon: demon.name,
                date: c.date
            });
        });
    });
    const recent10 = allCompletions
        .sort((a, b) => new Date(b.date) - new Date(a.date))
        .slice(0, 10);

    // --- Временные показатели ---
    const dates = allCompletions.map(c => new Date(c.date));
    const firstCompletion = dates.length ? new Date(Math.min(...dates)) : null;
    const lastCompletion = dates.length ? new Date(Math.max(...dates)) : null;

    // --- Активность за последние 30 дней ---
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    const recentCompletions = allCompletions.filter(c => new Date(c.date) >= thirtyDaysAgo);
    const activePlayersMap = {};
    recentCompletions.forEach(c => {
        activePlayersMap[c.player] = (activePlayersMap[c.player] || 0) + 1;
    });
    const activePlayers = Object.entries(activePlayersMap)
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 5);

    // --- Форматирование дат ---
    const formatDateStat = (d) => d ? d.toLocaleDateString('ru-RU') : '—';

    // --- Генерация HTML ---
    const html = `
        <div class="stats-full-container">
            <h1 class="page-title">📊 Полная статистика</h1>

            <!-- Общая статистика -->
            <div class="stats-section">
                <h2>📈 Общая статистика</h2>
                <div class="stats-grid">
                    <div class="stat-box"><div class="stat-value">${totalDemons}</div><div class="stat-label">Демонов в топе</div></div>
                    <div class="stat-box"><div class="stat-value">${totalPlayers}</div><div class="stat-label">Игроков</div></div>
                    <div class="stat-box"><div class="stat-value">${totalFutureDemons}</div><div class="stat-label">Будущих демонов</div></div>
                    <div class="stat-box"><div class="stat-value">${totalCompletions}</div><div class="stat-label">Всего прохождений</div></div>
                    <div class="stat-box"><div class="stat-value">${avgCompletions}</div><div class="stat-label">Среднее на демон</div></div>
                    <div class="stat-box"><div class="stat-value">${totalPoints}</div><div class="stat-label">Всего очков</div></div>
                </div>
            </div>

            <!-- Лидеры -->
            <div class="stats-section">
                <h2>🏆 Лидеры</h2>
                <div class="stats-grid">
                    <div class="stat-box leader">
                        <div class="stat-label">Лучший игрок</div>
                        <div class="stat-value">${topPlayer ? topPlayer.name : '—'}</div>
                        <div class="stat-sub">${topPlayer ? calculatePlayerPoints(topPlayer.id) + ' очков' : ''}</div>
                    </div>
                    <div class="stat-box leader">
                        <div class="stat-label">Самый активный</div>
                        <div class="stat-value">${playerMostBeats ? playerMostBeats.name : '—'}</div>
                        <div class="stat-sub">${playerMostBeats ? playerMostBeats.completedDemons.length + ' демонов' : ''}</div>
                    </div>
                    <div class="stat-box leader">
                        <div class="stat-label">Самый популярный демон</div>
                        <div class="stat-value">${topDemon ? topDemon.name : '—'}</div>
                        <div class="stat-sub">${topDemon ? topDemon.completers.length + ' прохождений' : ''}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Самый новый</div>
                        <div class="stat-value">${newestDemon?.name || '—'}</div>
                        <div class="stat-sub">${newestDemon ? formatDateStat(new Date(newestDemon.verifyDate)) : ''}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Самый старый</div>
                        <div class="stat-value">${oldestDemon?.name || '—'}</div>
                        <div class="stat-sub">${oldestDemon ? formatDateStat(new Date(oldestDemon.verifyDate)) : ''}</div>
                    </div>
                </div>
            </div>

            <!-- Активность -->
            <div class="stats-section">
                <h2>🔥 Активность (последние 30 дней)</h2>
                <div class="active-players-list">
                    ${activePlayers.length ? activePlayers.map(p => `
                        <div class="active-player-item">
                            <span class="player-name">${p.name}</span>
                            <span class="completion-count">${p.count} прохождений</span>
                        </div>
                    `).join('') : '<p>Нет активности за последние 30 дней</p>'}
                </div>
            </div>

            <!-- Последние прохождения -->
            <div class="stats-section">
                <h2>🕐 Последние 10 прохождений</h2>
                <div class="recent-completions-list">
                    ${recent10.length ? recent10.map(c => `
                        <div class="recent-item">
                            <span class="player">${c.player}</span> →
                            <span class="demon">${c.demon}</span>
                            <span class="date">${formatDate(c.date)}</span>
                        </div>
                    `).join('') : '<p>Прохождений пока нет</p>'}
                </div>
            </div>

            <!-- Временные рамки -->
            <div class="stats-section">
                <h2>⏳ Хронология</h2>
                <div class="timeline-stats">
                    <div class="timeline-item">
                        <span class="label">Первое прохождение:</span>
                        <span class="value">${formatDateStat(firstCompletion)}</span>
                    </div>
                    <div class="timeline-item">
                        <span class="label">Последнее прохождение:</span>
                        <span class="value">${formatDateStat(lastCompletion)}</span>
                    </div>
                    <div class="timeline-item">
                        <span class="label">Охват времени:</span>
                        <span class="value">${firstCompletion && lastCompletion ? 
                            Math.round((lastCompletion - firstCompletion) / (1000 * 60 * 60 * 24)) + ' дней' 
                            : '—'}</span>
                    </div>
                </div>
            </div>
        </div>
    `;

    app.innerHTML = html;
}
    // === НОВАЯ ВКЛАДКА: SEND RECORD ===
    renderSendRecord() {
        const app = document.getElementById('app');

        // Подготовка данных
        const demons = getAllDemons();
        const players = getAllPlayers();
        const topSize = demonList.length;

        const demonOptions = demons.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
        const playerOptions = players.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
        const positionOptions = Array.from({ length: topSize }, (_, i) => i + 1)
            .map(pos => `<option value="${pos}">#${pos}</option>`).join('');

        app.innerHTML = `
            <div class="send-record-container">
                <h1 class="page-title">📤 Send Your Record</h1>
                <form id="recordForm" class="record-form">
                    <!-- Сложность -->
                    <div class="form-group">
                        <label>1. Какой сложности демон вы прошли?</label>
                        <div class="radio-group">
                            <label><input type="radio" name="difficulty" value="Extreme Demon" required> Extreme Demon</label>
                            <label><input type="radio" name="difficulty" value="Insane Demon" required> Insane Demon</label>
                            <label><input type="radio" name="difficulty" value="Hard Demon" required> Hard Demon</label>
                            <label><input type="radio" name="difficulty" value="Medium Demon" required> Medium Demon</label>
                            <label><input type="radio" name="difficulty" value="Easy Demon" required> Easy Demon</label>
                        </div>
                    </div>

                    <!-- Демон -->
                    <div class="form-group">
                        <label>2. Какой демон вы прошли?</label>
                        <select id="demonSelect" class="form-select" required>
                            <option value="">— Выберите из списка —</option>
                            ${demonOptions}
                        </select>
                        <input type="text" id="customDemon" class="form-input" placeholder="Или введите название вручную...">
                    </div>

                    <!-- Игрок -->
                    <div class="form-group">
                        <label>Ваш ник?</label>
                        <select id="playerSelect" class="form-select" required>
                            <option value="">— Выберите из топа —</option>
                            ${playerOptions}
                        </select>
                        <input type="text" id="customPlayer" class="form-input" placeholder="Или введите ник вручную...">
                    </div>

                    <!-- YouTube -->
                    <div class="form-group">
                        <label>3. Видео на YouTube</label>
                        <input type="url" id="youtubeLink" class="form-input" placeholder="https://youtu.be/..." required>
                    </div>

                    <!-- Облако -->
                    <div class="form-group">
                        <label>4. Видео на Yandex Disk / Google Drive</label>
                        <input type="url" id="cloudLink" class="form-input" placeholder="Ссылка на облако..." required>
                    </div>

                    <!-- Позиция -->
                    <div class="form-group">
                        <label>5. Какой по топу, уровень который вы прошли по вашему мнению?</label>
                        <select id="positionSelect" class="form-select" required>
                            <option value="">— Выберите позицию —</option>
                            ${positionOptions}
                        </select>
                    </div>

                    <!-- Контакт -->
                    <div class="form-group">
                        <label>6. Ваш Discord / Telegram для связи</label>
                        <input type="text" id="contactInfo" class="form-input" placeholder="@yourname or your#1234" required>
                    </div>

                    <!-- Кнопка -->
                    <button type="submit" id="submitBtn" class="submit-btn" disabled>
                        📤 Отправить рекорд
                    </button>
                </form>
            </div>
        `;

        // Добавляем обработчики
        this.initSendRecordForm();
    }

    initSendRecordForm() {
        const form = document.getElementById('recordForm');
        const demonSelect = document.getElementById('demonSelect');
        const customDemon = document.getElementById('customDemon');
        const playerSelect = document.getElementById('playerSelect');
        const customPlayer = document.getElementById('customPlayer');
        const youtubeLink = document.getElementById('youtubeLink');
        const cloudLink = document.getElementById('cloudLink');
        const positionSelect = document.getElementById('positionSelect');
        const contactInfo = document.getElementById('contactInfo');
        const submitBtn = document.getElementById('submitBtn');

        const updateSubmitButton = () => {
            const difficultySelected = document.querySelector('input[name="difficulty"]:checked') !== null;
            const demonChosen = demonSelect.value || customDemon.value.trim();
            const playerChosen = playerSelect.value || customPlayer.value.trim();
            const youtubeValid = this.isValidUrl(youtubeLink.value);
            const cloudValid = this.isValidUrl(cloudLink.value);
            const positionValid = positionSelect.value;
            const contactValid = contactInfo.value.trim();

            submitBtn.disabled = !(
                difficultySelected &&
                demonChosen &&
                playerChosen &&
                youtubeValid &&
                cloudValid &&
                positionValid &&
                contactValid
            );
        };

        [demonSelect, customDemon, playerSelect, customPlayer, youtubeLink, cloudLink, positionSelect, contactInfo]
            .forEach(el => el.addEventListener('input', updateSubmitButton));

        document.querySelectorAll('input[name="difficulty"]').forEach(radio => {
            radio.addEventListener('change', updateSubmitButton);
        });

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const difficulty = document.querySelector('input[name="difficulty"]:checked').value;
            const demonName = demonSelect.value
                ? getDemonById(parseInt(demonSelect.value))?.name || ''
                : customDemon.value.trim();
            const playerName = playerSelect.value
                ? getPlayerById(parseInt(playerSelect.value))?.name || ''
                : customPlayer.value.trim();
            const position = positionSelect.value;
            const youtube = youtubeLink.value.trim();
            const cloud = cloudLink.value.trim();
            const contact = contactInfo.value.trim();


            const WORKER_URL = 'https://dolores-telegram.hdigdi89.workers.dev';

            const payload = {
                difficulty,
                demonName,
                playerName,
                position,
                youtube,
                cloud,
                contact
            };

            try {
                const res = await fetch(WORKER_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (res.ok) {
                    alert('✅ Ваш рекорд успешно отправлен! Модераторы скоро проверят.');
                    form.reset();
                    submitBtn.disabled = true;
                } else {
                    const err = await res.json();
                    alert('❌ Ошибка: ' + (err.error || 'Неизвестная ошибка'));
                }
            } catch (err) {
                alert('📡 Не удалось подключиться к серверу.');
            }
        });
    }

    isValidUrl(string) {
        try {
            new URL(string);
            return string.trim() !== '';
        } catch (_) {
            return false;
        }
    }
}




const router = new Router();