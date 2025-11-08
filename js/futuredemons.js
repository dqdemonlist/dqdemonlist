const futureDemons = [

];

// Функция для получения будущего демона по ID
function getFutureDemonById(id) {
    return futureDemons.find(demon => demon.id === id);
}

// Функция для получения всех будущих демонов
function getAllFutureDemons() {
    return futureDemons;
}

// Функция для получения игроков, проходящих демон
function getBeatingPlayers(demonId) {
    const demon = getFutureDemonById(demonId);
    if (!demon) return [];
    
    return demon.beatingPlayers.map(bp => {
        const player = getPlayerById(bp.playerId);
        return {
            ...bp,
            playerName: player ? player.name : 'Unknown'
        };
    }).sort((a, b) => b.progress - a.progress);
}
