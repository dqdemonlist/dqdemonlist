const futureDemons = [
  {
    "id": 1,
    "name": "Void Wave",
    "creator": "CherryTeam",
    "difficulty": "Extreme Demon",
    "description": "Длинный и очень атмосферный уровень с сложным геймплеем лоу-экстрима.",
    "beatingPlayers": [
      {
        "playerId": 1,
        "progress": 39,
        "lastUpdate": "2025-09-25"
      }
    ]
  }
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
