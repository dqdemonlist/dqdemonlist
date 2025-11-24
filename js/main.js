// Управление темами
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    const themeToggle = document.querySelector('.theme-toggle');
    themeToggle.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
    themeToggle.title = 'Переключить тему';
    
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        themeToggle.innerHTML = newTheme === 'dark' ? '☀️' : '🌙';
        localStorage.setItem('theme', newTheme);
    });
}

// Инициализация кнопки Discord
function initDiscordButton() {
    const discordBtn = document.querySelector('.discord-btn');
    
    discordBtn.addEventListener('click', () => {
        // Замени на свою Discord ссылку
        window.open('https://discord.gg/v8aZ5HYXCC', '_blank');
    });
}

// Инициализация модальных окон
function initModals() {
    const demonModal = document.getElementById('demonModal');
    const playerModal = document.getElementById('playerModal');
    const futureDemonModal = document.getElementById('futureDemonModal');
    const closeButtons = document.querySelectorAll('.close');
    
    const closeModal = () => {
        demonModal.style.display = 'none';
        playerModal.style.display = 'none';
        futureDemonModal.style.display = 'none';
        document.body.style.overflow = 'auto';
        document.body.style.paddingRight = '0';
    };
    
    // Закрытие модальных окон при клике на крестик
    closeButtons.forEach(button => {
        button.addEventListener('click', closeModal);
    });
    
    // Закрытие модальных окон при клике вне контента
    window.addEventListener('click', (event) => {
        if (event.target === demonModal || event.target === playerModal || event.target === futureDemonModal) {
            closeModal();
        }
    });
    
    // Закрытие по Escape
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
}

// Функция для открытия модального окна демона
function openDemonModal(demonId) {
    const demon = getDemonById(demonId);
    if (!demon) return;
    
    const demonPosition = demonList.indexOf(demonId) + 1;
    const demonPoints = calculateDemonPoints(demonPosition);
    
    const verifierPlayer = getPlayerById(demon.verifier);
    const verifierName = verifierPlayer ? verifierPlayer.name : 'Unknown';
    
    const completersHTML = demon.completers.map(completer => {
        const player = getPlayerById(completer.playerId);
        return player ? `
            <div class="completer-item">
                <span class="completer-name">${player.name}</span>
                <span class="completer-date">${formatDate(completer.date)}</span>
            </div>
        ` : '';
    }).join('');
    
    const modalContent = document.getElementById('demonModalContent');
    modalContent.innerHTML = `
        <div class="demon-modal-header">
            <h2 class="demon-modal-name">${demon.name}</h2>
            <div class="demon-modal-creator">Creator: ${demon.creator}</div>
        </div>
        
        <div class="demon-modal-stats">
            <div class="stat-item">
                <div class="stat-label">Placement</div>
                <div class="stat-value">#${demonPosition}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Points</div>
                <div class="stat-value">${demonPoints}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Victors</div>
                <div class="stat-value">${demon.completers.length} игроков</div>
            </div>
        </div>
        
        <div class="verifier-info">
            <div class="verifier-label">Verifier</div>
            <div class="verifier-name">${verifierName}</div>
            <div class="verifier-date">${formatDate(demon.verifyDate)}</div>
        </div>
        
        <div class="completers-section">
            <h3 class="completers-title">All victors</h3>
            <div class="completers-list-container">
                <div class="completers-list">
                    ${completersHTML}
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('demonModal').style.display = 'block';
}

// Функция для открытия модального окна игрока
function openPlayerModal(playerId) {
    const player = getPlayerById(playerId);
    if (!player) return;
    
    const playerPoints = calculatePlayerPoints(playerId);
    const playerDemons = getPlayerDemons(playerId);
    
    const demonsHTML = playerDemons.map(demon => {
        const demonPosition = demonList.indexOf(demon.id) + 1;
        const demonPoints = calculateDemonPoints(demonPosition);
        return `
            <div class="demon-card" data-demon-id="${demon.id}">
                <div class="demon-card-name">${demon.name}</div>
                <div class="demon-card-rank">#${demonPosition} • ${demonPoints} points</div>
            </div>
        `;
    }).join('');
    
    const modalContent = document.getElementById('playerModalContent');
    modalContent.innerHTML = `
        <div class="player-modal-header">
            <h2 class="player-modal-name">${player.name}</h2>
        </div>
        
        <div class="player-modal-stats">
            <div class="stat-item">
                <div class="stat-label">All points</div>
                <div class="stat-value">${playerPoints}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Demons beated</div>
                <div class="stat-value">${player.completedDemons.length}</div>
            </div>
        </div>
        
        <div class="demons-completed-section">
            <h3 class="demons-completed-title">Demons beated</h3>
            <div class="demons-grid-container">
                <div class="demons-grid">
                    ${demonsHTML}
                </div>
            </div>
        </div>
    `;
    
    // Добавляем обработчики для карточек демонов
    setTimeout(() => {
        document.querySelectorAll('#playerModalContent .demon-card').forEach(card => {
            card.addEventListener('click', () => {
                const demonId = parseInt(card.getAttribute('data-demon-id'));
                document.getElementById('playerModal').style.display = 'none';
                openDemonModal(demonId);
            });
        });
    }, 0);
    
    document.getElementById('playerModal').style.display = 'block';
}

// Функция для открытия модального окна будущего демона
function openFutureDemonModal(demonId) {
    const demon = getFutureDemonById(demonId);
    if (!demon) return;
    
    const beatingPlayers = getBeatingPlayers(demonId);
    
    const playersHTML = beatingPlayers.map(bp => `
        <div class="beating-player-modal">
            <div class="player-progress-modal">
                <div class="progress-info-modal">
                    <span class="player-name">${bp.playerName}</span>
                    <span class="progress-percent">${bp.progress}%</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar" style="width: ${bp.progress}%"></div>
                </div>
            </div>
            <div class="last-update">${formatDate(bp.lastUpdate)}</div>
        </div>
    `).join('');
    
    const modalContent = document.getElementById('futureDemonModalContent');
    modalContent.innerHTML = `
        <div class="demon-modal-header">
            <h2 class="demon-modal-name">${demon.name}</h2>
            <div class="demon-modal-creator">Создатель: ${demon.creator}</div>
            <div style="margin-top: 10px;">
                <span class="difficulty-badge">${demon.difficulty}</span>
            </div>
        </div>
        
        <div class="future-demon-modal-stats">
            <div class="stat-item">
                <div class="stat-label">Players beating</div>
                <div class="stat-value">${demon.beatingPlayers.length}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Highest run</div>
                <div class="stat-value">${Math.max(...demon.beatingPlayers.map(bp => bp.progress))}%</div>
            </div>
        </div>
        
        <div class="demon-description">
            <div class="description-label">Description</div>
            <div class="description-text">${demon.description}</div>
        </div>
        
        <div class="beating-players-section">
            <h3 class="beating-players-title">Players who would be the victor</h3>
            <div class="beating-players-container">
                <div class="beating-players-list">
                    ${playersHTML}
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('futureDemonModal').style.display = 'block';
}

// Функция для форматирования даты
function formatDate(dateString) {
    if (!dateString) return 'Неизвестно';
    
    try {
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('ru-RU', options);
    } catch (error) {
        return 'Неизвестно';
    }
}
// Функции для статистики
function getTotalPlayers() {
    return getAllPlayers().length;
}

function getTotalDemons() {
    return getAllDemons().length;
}

function getTotalFutureDemons() {
    return getAllFutureDemons().length;
}

function getTotalCompletions() {
    let total = 0;
    getAllDemons().forEach(demon => {
        total += demon.completers.length;
    });
    return total;
}

function getAverageCompletionsPerDemon() {
    const demons = getAllDemons();
    if (demons.length === 0) return 0;
    
    const totalCompletions = getTotalCompletions();
    return Math.round(totalCompletions / demons.length);
}

function getMostCompletedDemon() {
    const demons = getAllDemons();
    if (demons.length === 0) return null;
    
    return demons.reduce((max, demon) => {
        return demon.completers.length > max.completers.length ? demon : max;
    });
}

function getPlayerWithMostPoints() {
    const players = getAllPlayers();
    if (players.length === 0) return null;
    
    return players.reduce((max, player) => {
        const playerPoints = calculatePlayerPoints(player.id);
        const maxPoints = calculatePlayerPoints(max.id);
        return playerPoints > maxPoints ? player : max;
    });
}

function getRecentCompletions() {
    let allCompletions = [];
    
    getAllDemons().forEach(demon => {
        demon.completers.forEach(completer => {
            allCompletions.push({
                playerName: getPlayerById(completer.playerId)?.name || 'Unknown',
                demonName: demon.name,
                date: completer.date
            });
        });
    });
    
    // Сортируем по дате (новые сначала)
    return allCompletions.sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0, 5);
}

function getDemonWithHighestPoints() {
    const leaderboard = getDemonLeaderboard();
    return leaderboard[0]; // Первый демон в топе
}

function getTotalPointsDistributed() {
    let total = 0;
    getAllPlayers().forEach(player => {
        total += calculatePlayerPoints(player.id);
    });
    return total;
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initModals();
    initDiscordButton();

    // === ПОКАЗ МОДАЛЬНОГО ОКНА С ЛИЦЕНЗИЕЙ ===
    const licenseModal = document.getElementById('licenseModal');
    const closeBtn = document.getElementById('closeLicenseModal');
    const hasAccepted = localStorage.getItem('licenseAccepted') === 'true';

    if (!hasAccepted) {
        licenseModal.style.display = 'flex';
    }

    closeBtn?.addEventListener('click', () => {
        licenseModal.style.display = 'none';
        localStorage.setItem('licenseAccepted', 'true');
    });

    // Закрытие по клику вне контента
    licenseModal?.addEventListener('click', (e) => {
        if (e.target === licenseModal) {
            licenseModal.style.display = 'none';
            localStorage.setItem('licenseAccepted', 'true');
        }
    });

    console.log('GD Demonlist initialized successfully!');
});
// ——— СКИЛЛ-МЕТРИКИ ———
const SKILL_ALPHA = 5;

function calculateAbsoluteSkill(playerId) {
    const player = getPlayerById(playerId);
    if (!player) return 0;
    const points = calculatePlayerPoints(playerId);
    const beaten = player.completedDemons.length;
    return points + SKILL_ALPHA * beaten;
}

function calculateRelativeSkill(playerId) {
    const allPlayers = getAllPlayers();
    if (!allPlayers.length) return 0;
    let topSkill = 0;
    for (const p of allPlayers) {
        const s = calculateAbsoluteSkill(p.id);
        if (s > topSkill) topSkill = s;
    }
    const skill = calculateAbsoluteSkill(playerId);
    return topSkill > 0 ? (100 * skill / topSkill) : 0;
}