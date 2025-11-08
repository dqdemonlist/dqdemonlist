class Router {
    constructor() {
        this.routes = {
            '/': this.renderHome,
            '/demons': this.renderDemons,
            '/players': this.renderPlayers,
            '/future': this.renderFutureDemons,
            '/rules': this.renderRules
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
                <h3>🔥 Demonlist</h3>
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
}


const router = new Router();