const futureDemons = [
  {
    "id": 1,
    "name": "Necropolis",
    "creator": "IIINepTuneIII",
    "difficulty": "Insane Demon",
    "description": "Сложноватый уровень со старым типажом геймплея, строющегося на примитивных таймингах.",
    "beatingPlayers": [
      {
        "playerId": 3,
        "progress": 94,
        "lastUpdate": "2025-11-09"
      }
    ]
  },
  {
    "id": 2,
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
  },
  {
    "id": 3,
    "name": "Acu",
    "creator": "Neigefeu",
    "difficulty": "Extreme Demon",
    "description": "Очень фановый уровень, легкий для своей сложности.",
    "beatingPlayers": [
      {
        "playerId": 2,
        "progress": 72,
        "lastUpdate": "2025-11-05"
      },
      {
        "playerId": 1,
        "progress": 32,
        "lastUpdate": "2025-11-08"
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
