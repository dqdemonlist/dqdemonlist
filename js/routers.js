class Router {
    constructor() {
        this.routes = {
            '/': this.renderHome,
            '/demons': this.renderDemons,
            '/players': this.renderPlayers,
            '/future': this.renderFutureDemons,
            '/rules': this.renderRules,
            '/stats': this.renderStats,
            '/send-record': this.renderSendRecord,
            '/skill-ranking': this.renderSkillRanking
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
        const navLinks = document.querySelectorAll('.nav-link, .dropdown-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentRoute}`) {
                link.classList.add('active');
            }
        });
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
                        <div class="stat-label">Avg beatings per demon</div>
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
                        <span class="player-points">${calculatePlayerPoints(topPlayer.id)} pts</span>
                    </div>
                    <div class="player-stats">${topPlayer.completedDemons.length} demons beated</div>
                </div>
                ` : ''}
                ${topDemon ? `
                <div class="top-demon-card">
                    <h3>🔥 Top 1 Demon</h3>
                    <div class="demon-info">
                        <span class="demon-name">${topDemon.name}</span>
                        <span class="demon-points">${topDemon.points} pts</span>
                    </div>
                    <div class="demon-stats">${topDemon.completers.length} players beated</div>
                </div>
                ` : ''}
                ${mostCompletedDemon ? `
                <div class="popular-demon-card">
                    <h3>🎯 Most Popular</h3>
                    <div class="demon-info">
                        <span class="demon-name">${mostCompletedDemon.name}</span>
                        <span class="completion-count">${mostCompletedDemon.completers.length}</span>
                    </div>
                </div>
                ` : ''}
            </div>
        `;
        const recentCompletionsHTML = recentCompletions.length ? `
            <div class="recent-completions">
                <h3>🕐 Recent completions</h3>
                <div class="completions-list">
                    ${recentCompletions.map(c => `
                        <div class="completion-item">
                            <span class="player">${c.playerName}</span>
                            <span class="demon">${c.demonName}</span>
                            <span class="date">${formatDate(c.date)}</span>
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
                    Demonlist, Top Players, Future Demons List of Dolores Squad's Community.<br>
                    Follow other players' progress, browse the top rankings, and join Dolores Squad!
                </p>
                <div class="home-buttons">
                    <a href="#/demons" class="home-btn btn-demons">Demonlist</a>
                    <a href="#/players" class="home-btn btn-players">Players list</a>
                    <a href="#/future" class="home-btn btn-future">Future Demons</a>
                    <a href="#/rules" class="home-btn btn-rules">Rules</a>
                    <a href="#/stats" class="home-btn" style="background: var(--accent-future); color: white;">📊 Statistics</a>
                    <a href="#/skill-ranking" class="home-btn" style="background: var(--accent-secondary); color: white;">🧠 Skill Ranking</a>
                    <a href="#/send-record" class="home-btn" style="background: var(--accent-primary); color: white;">📤 Send Record</a>
                </div>
                ${statsHTML}
                ${detailedStatsHTML}
                ${recentCompletionsHTML}
            </div>
        `;
    }

    renderDemons() {
        const leaderboard = getDemonLeaderboard();
        const demonsHTML = leaderboard.map(d => `
            <div class="demon-item" data-demon-id="${d.id}">
                <div class="demon-rank">#${d.position}</div>
                <div class="demon-info">
                    <div class="demon-name">${d.name}</div>
                    <div class="demon-creator">by ${d.creator}</div>
                </div>
                <div class="demon-points">${d.points} pts</div>
            </div>
        `).join('');
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="demons-container">
                <h1 class="page-title">Demonlist</h1>
                <div class="demons-list">${demonsHTML}</div>
            </div>
        `;
        document.querySelectorAll('.demon-item').forEach(item => {
            item.addEventListener('click', () => {
                openDemonModal(parseInt(item.dataset.demonId));
            });
        });
    }

    renderPlayers() {
        const leaderboard = getPlayerLeaderboard();
        const playersHTML = leaderboard.map(p => {
            const points = calculatePlayerPoints(p.id);
            const relSkill = calculateRelativeSkill(p.id).toFixed(1);
            return `
                <div class="player-item" data-player-id="${p.id}">
                    <div class="player-rank">#${p.position}</div>
                    <div class="player-info">
                        <div class="player-name">${p.name}</div>
                        <div class="player-stats">${p.completedDemons.length} demons • ${relSkill}%</div>
                    </div>
                    <div class="player-points">${points} pts</div>
                </div>
            `;
        }).join('');
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="players-container">
                <h1 class="page-title">Players List</h1>
                <div class="subtitle">💡 Относительный скилл — % от лучшего игрока</div>
                <div class="players-list">${playersHTML}</div>
            </div>
        `;
        document.querySelectorAll('.player-item').forEach(item => {
            item.addEventListener('click', () => {
                openPlayerModal(parseInt(item.dataset.playerId));
            });
        });
    }

    renderFutureDemons() {
        const futureDemons = getAllFutureDemons();
        const futureDemonsHTML = futureDemons.map(d => {
            const beatingPlayers = getBeatingPlayers(d.id);
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
                <div class="future-demon-item" data-future-demon-id="${d.id}">
                    <div class="future-demon-header">
                        <div class="future-demon-info">
                            <div class="future-demon-name">${d.name}</div>
                            <div class="future-demon-creator">by ${d.creator}</div>
                        </div>
                        <div class="future-demon-difficulty">${d.difficulty}</div>
                    </div>
                    <div class="beating-players">${playersHTML}</div>
                </div>
            `;
        }).join('');
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="future-demons-container">
                <h1 class="page-title">Future Demons</h1>
                <h3>Levels that can reach the top!</h3>
                <div class="future-demons-list">${futureDemonsHTML}</div>
            </div>
        `;
        document.querySelectorAll('.future-demon-item').forEach(item => {
            item.addEventListener('click', () => {
                openFutureDemonModal(parseInt(item.dataset.futureDemonId));
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
                            <li>Подтверждение рекордов через сырое, нередактированное видео (Google Disk / Yandex Disk)</li>
                            <li>FPS: Разрешено прохождение на любом FPS, но без FPS Bypass</li>
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
                            <li>Видео должно показывать весь геймплей</li>
                            <li>Должны быть слышны клики, показаны индикаторы FPS, CPS</li>
                            <li>Видео должно быть в качестве 720p или выше</li>
                        </ul>
                    </div>
                    <div class="rules-section">
                        <h2>Контакты модераторов для помощи в Discord</h2>
                        <ul class="rules-list">
                            <li>Dolores - king5356</li>
                            <li>angyedz - angyedz</li>
                            <li>Wlen0k - looloolloolol</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    renderStats() {
        const totalPlayers = getTotalPlayers();
        const totalDemons = getTotalDemons();
        const totalFutureDemons = getTotalFutureDemons();
        const totalCompletions = getTotalCompletions();
        const avgCompletions = totalDemons ? (totalCompletions / totalDemons).toFixed(2) : 0;
        const totalPoints = getTotalPointsDistributed();

        const topPlayer = getPlayerWithMostPoints();
        const topDemon = getMostCompletedDemon();
        const demons = getAllDemons();
        const newestDemon = demons.reduce((a, b) => new Date(a.verifyDate) > new Date(b.verifyDate) ? a : b, demons[0]);
        const oldestDemon = demons.reduce((a, b) => new Date(a.verifyDate) < new Date(b.verifyDate) ? a : b, demons[0]);
        const playerMostBeats = getAllPlayers().reduce((a, b) => a.completedDemons.length > b.completedDemons.length ? a : { completedDemons: [] });

        // Скилл-статистика
        const allPlayers = getAllPlayers();
        const topSkillPlayer = allPlayers.reduce((a, b) => calculateAbsoluteSkill(a.id) > calculateAbsoluteSkill(b.id) ? a : { id: 0 });
        const avgSkill = allPlayers.reduce((sum, p) => sum + calculateAbsoluteSkill(p.id), 0) / (allPlayers.length || 1);

        const formatDateStat = (d) => d ? d.toLocaleDateString('ru-RU') : '—';

        const allCompletions = [];
        demons.forEach(d => {
            d.completers.forEach(c => {
                allCompletions.push({
                    player: getPlayerById(c.playerId)?.name || 'Unknown',
                    demon: d.name,
                    date: c.date
                });
            });
        });
        const recent10 = allCompletions.sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0, 10);
        const dates = allCompletions.map(c => new Date(c.date));
        const firstCompletion = dates.length ? new Date(Math.min(...dates)) : null;
        const lastCompletion = dates.length ? new Date(Math.max(...dates)) : null;

        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
        const recentCompletions = allCompletions.filter(c => new Date(c.date) >= thirtyDaysAgo);
        const activePlayersMap = {};
        recentCompletions.forEach(c => {
            activePlayersMap[c.player] = (activePlayersMap[c.player] || 0) + 1;
        });
        const activePlayers = Object.entries(activePlayersMap).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count).slice(0, 5);

        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="stats-full-container">
                <h1 class="page-title">📊 Полная статистика</h1>

                <div class="stats-section">
                    <h2>🧠 Скилл игроков</h2>
                    <div class="stats-grid">
                        <div class="stat-box">
                            <div class="stat-value">${Math.round(avgSkill)}</div>
                            <div class="stat-label">Средний абсолютный скилл</div>
                        </div>
                        <div class="stat-box leader">
                            <div class="stat-label">Лидер по скиллу</div>
                            <div class="stat-value">${topSkillPlayer.name || '—'}</div>
                            <div class="stat-sub">${topSkillPlayer.name ? calculateAbsoluteSkill(topSkillPlayer.id) + ' очков' : ''}</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${allPlayers.length}</div>
                            <div class="stat-label">Игроков с активным скиллом</div>
                        </div>
                    </div>
                </div>

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
                            <div class="stat-value">${playerMostBeats.name || '—'}</div>
                            <div class="stat-sub">${playerMostBeats.completedDemons.length} демонов</div>
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
                            <span class="value">${firstCompletion && lastCompletion ? Math.round((lastCompletion - firstCompletion) / (1000 * 60 * 60 * 24)) + ' дней' : '—'}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderSkillRanking() {
        const allPlayers = getAllPlayers();
        const skillLeaderboard = allPlayers
            .map(p => ({ ...p, absSkill: calculateAbsoluteSkill(p.id), relSkill: calculateRelativeSkill(p.id) }))
            .sort((a, b) => b.absSkill - a.absSkill)
            .map((p, i) => ({ ...p, position: i + 1 }));

        const playersHTML = skillLeaderboard.map(p => `
            <div class="player-item" data-player-id="${p.id}">
                <div class="player-rank">#${p.position}</div>
                <div class="player-info">
                    <div class="player-name">${p.name}</div>
                    <div class="player-stats">${p.completedDemons.length} demons</div>
                </div>
                <div class="player-skill">${p.absSkill} • <span style="color:var(--accent-neon)">${p.relSkill.toFixed(1)}%</span></div>
            </div>
        `).join('');

        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="players-container">
                <h1 class="page-title">🧠 Skill Ranking</h1>
                <div class="subtitle">Абсолютный скилл • Относительный скилл (%)</div>
                <div class="players-list">${playersHTML}</div>
            </div>
        `;
        document.querySelectorAll('.player-item').forEach(item => {
            item.addEventListener('click', () => {
                openPlayerModal(parseInt(item.dataset.playerId));
            });
        });
    }

    renderSendRecord() {
        const app = document.getElementById('app');
        const demons = getAllDemons();
        const players = getAllPlayers();
        const topSize = demonList.length;

        const demonOptions = demons.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
        const playerOptions = players.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
        const positionOptions = Array.from({ length: topSize }, (_, i) => i + 1).map(pos => `<option value="${pos}">#${pos}</option>`).join('');

        app.innerHTML = `
            <div class="send-record-container">
                <h1 class="page-title">📤 Send Your Record</h1>
                <form id="recordForm" class="record-form">
                    <div class="form-group">
                        <label>1. Сложность:</label>
                        <div class="radio-group">
                            <label><input type="radio" name="difficulty" value="Extreme Demon" required> Extreme</label>
                            <label><input type="radio" name="difficulty" value="Insane Demon" required> Insane</label>
                            <label><input type="radio" name="difficulty" value="Hard Demon" required> Hard</label>
                            <label><input type="radio" name="difficulty" value="Medium Demon" required> Medium</label>
                            <label><input type="radio" name="difficulty" value="Easy Demon" required> Easy</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>2. Демон:</label>
                        <select id="demonSelect" class="form-select" required>
                            <option value="">— Из списка —</option>
                            ${demonOptions}
                        </select>
                        <input type="text" id="customDemon" class="form-input" placeholder="Или вручную...">
                    </div>
                    <div class="form-group">
                        <label>Ваш ник:</label>
                        <select id="playerSelect" class="form-select" required>
                            <option value="">— Из топа —</option>
                            ${playerOptions}
                        </select>
                        <input type="text" id="customPlayer" class="form-input" placeholder="Или вручную...">
                    </div>
                    <div class="form-group">
                        <label>3. YouTube:</label>
                        <input type="url" id="youtubeLink" class="form-input" placeholder="https://youtu.be/..." required>
                    </div>
                    <div class="form-group">
                        <label>4. Облако:</label>
                        <input type="url" id="cloudLink" class="form-input" placeholder="Yandex/Google Drive..." required>
                    </div>
                    <div class="form-group">
                        <label>5. Позиция в топе:</label>
                        <select id="positionSelect" class="form-select" required>
                            <option value="">— Выберите —</option>
                            ${positionOptions}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>6. Контакт:</label>
                        <input type="text" id="contactInfo" class="form-input" placeholder="@yourname" required>
                    </div>
                    <button type="submit" id="submitBtn" class="submit-btn" disabled>📤 Отправить</button>
                </form>
            </div>
        `;
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
            const hasDifficulty = document.querySelector('input[name="difficulty"]:checked') !== null;
            const demon = demonSelect.value || customDemon.value.trim();
            const player = playerSelect.value || customPlayer.value.trim();
            const youtubeValid = this.isValidUrl(youtubeLink.value);
            const cloudValid = this.isValidUrl(cloudLink.value);
            const position = positionSelect.value;
            const contact = contactInfo.value.trim();

            submitBtn.disabled = !(hasDifficulty && demon && player && youtubeValid && cloudValid && position && contact);
        };

        [demonSelect, customDemon, playerSelect, customPlayer, youtubeLink, cloudLink, positionSelect, contactInfo].forEach(el => {
            el.addEventListener('input', updateSubmitButton);
        });
        document.querySelectorAll('input[name="difficulty"]').forEach(r => {
            r.addEventListener('change', updateSubmitButton);
        });

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const difficulty = document.querySelector('input[name="difficulty"]:checked').value;
            const demonName = demonSelect.value ? getDemonById(parseInt(demonSelect.value))?.name || '' : customDemon.value.trim();
            const playerName = playerSelect.value ? getPlayerById(parseInt(playerSelect.value))?.name || '' : customPlayer.value.trim();
            const payload = {
                difficulty,
                demonName,
                playerName,
                position: positionSelect.value,
                youtube: youtubeLink.value.trim(),
                cloud: cloudLink.value.trim(),
                contact: contactInfo.value.trim()
            };
            try {
                const res = await fetch('https://dolores-telegram.hdigdi89.workers.dev', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (res.ok) {
                    alert('✅ Рекорд отправлен!');
                    form.reset(); submitBtn.disabled = true;
                } else {
                    alert('❌ Ошибка отправки');
                }
            } catch (err) {
                alert('📡 Не удалось подключиться к серверу (Worker не запущен?)');
            }
        });
    }

    isValidUrl(string) {
        try { new URL(string); return string.trim() !== ''; } catch (_) { return false; }
    }

    render404() {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="home-container">
                <h1 class="home-title">404 - Страница не найдена</h1>
                <p class="home-subtitle">Запрошенная страница не существует.</p>
                <div class="home-buttons">
                    <a href="#/" class="home-btn btn-demons">На главную</a>
                </div>
            </div>
        `;
    }
}

const router = new Router();