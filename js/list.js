// Расчет очков для демонов
function calculateDemonPoints(position) {
    const basePoints = 500;
    const decayRate = 0.19; // 19%
    
    if (position === 1) return basePoints;
    
    let points = basePoints;
    for (let i = 2; i <= position; i++) {
        points = points * (1 - decayRate);
    }
    
    return Math.round(points);
}

// ДЛЯ ДОЛОРЕСА (РАССТАВЛЕНИЕ ТОПА)
const demonList = [10, 1, 9, 2, 3, 11, 4, 5, 6, 7, 8];

// Функция для получения топа демонов с рассчитанными очками
function getDemonLeaderboard() {
    return demonList.map((demonId, index) => {
        const demon = getDemonById(demonId);
        const position = index + 1;
        const points = calculateDemonPoints(position);
        
        return {
            ...demon,
            position: position,
            points: points
        };
    });
}

// Функция для получения топа игроков (автоматически по очкам)
function getPlayerLeaderboard() {
    const allPlayers = getAllPlayers();
    
    // Добавляем очки каждому игроку
    const playersWithPoints = allPlayers.map(player => ({
        ...player,
        points: calculatePlayerPoints(player.id)
    }));
    
    // Сортируем игроков по очкам (по убыванию)
    return playersWithPoints
        .sort((a, b) => b.points - a.points)
        .map((player, index) => ({
            ...player,
            position: index + 1
        }));
}