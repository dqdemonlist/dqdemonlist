const players = [
  {
    "id": 1,
    "name": "DoloresKingGMD",
    "completedDemons": [
      15
    ]
  },
  {
    "id": 2,
    "name": "Walen0k",
    "completedDemons": [
      7
    ]
  },
  {
    "id": 3,
    "name": "What",
    "completedDemons": [
      1,
      2
    ]
  },
  {
    "id": 5,
    "name": "kitcat43129",
    "completedDemons": []
  },
  {
    "id": 6,
    "name": "GMDNurka",
    "completedDemons": [
      3
    ]
  },
  {
    "id": 7,
    "name": "KizyakGD",
    "completedDemons": []
  },
  {
    "id": 8,
    "name": "fhfhfh",
    "completedDemons": []
  }
];

// Функция для получения игрока по ID
function getPlayerById(id) {
    return players.find(player => player.id === id);
}

// Функция для получения всех игроков
function getAllPlayers() {
    return players;
}

// Функция для получения демонов игрока (исключая верифицированные)
function getPlayerDemons(playerId) {
    const player = getPlayerById(playerId);
    if (!player) return [];

    // Получаем ID демонов, которые игрок верифицировал
    const verifiedDemonIds = new Set();
    getAllDemons().forEach(demon => {
        if (demon.verifier === playerId) {
            verifiedDemonIds.add(demon.id);
        }
    });

    // Возвращаем только те демоны, которые игрок НЕ верифицировал
    return player.completedDemons
        .filter(demonId => !verifiedDemonIds.has(demonId))
        .map(demonId => {
            const demon = getDemonById(demonId);
            return {
                ...demon,
                completionDate: getCompletionDate(playerId, demonId),
                isVerified: false
            };
        });
}

// Функция для получения верифицированных демонов игрока (включая те, что в completedDemons)
function getPlayerVerifiedDemons(playerId) {
    const player = getPlayerById(playerId);
    if (!player) return [];

    const verifiedDemons = [];
    getAllDemons().forEach(demon => {
        if (demon.verifier === playerId) {
            verifiedDemons.push({
                ...demon,
                verifyDate: demon.verifyDate,
                isVerified: true
            });
        }
    });
    return verifiedDemons;
}

// Функция для получения даты прохождения демона игроком
function getCompletionDate(playerId, demonId) {
    const demon = getDemonById(demonId);
    if (!demon) return null;
    
    const completion = demon.completers.find(comp => comp.playerId === playerId);
    return completion ? completion.date : null;
}

// Функция для расчета очков игрока
function calculatePlayerPoints(playerId) {
    const player = getPlayerById(playerId);
    if (!player) return 0;

    let totalPoints = 0;
    const countedDemons = new Set();

    // Очки за пройденные демоны (из completedDemons)
    player.completedDemons.forEach(demonId => {
        const demonIndex = demonList.indexOf(demonId);
        if (demonIndex !== -1 && !countedDemons.has(demonId)) {
            const position = demonIndex + 1;
            totalPoints += calculateDemonPoints(position);
            countedDemons.add(demonId);
        }
    });

    // Очки за верифицированные демоны (даже если игрок не в completers)
    getAllDemons().forEach(demon => {
        if (demon.verifier === playerId && !countedDemons.has(demon.id)) {
            const demonIndex = demonList.indexOf(demon.id);
            if (demonIndex !== -1) {
                const position = demonIndex + 1;
                totalPoints += calculateDemonPoints(position);
                countedDemons.add(demon.id);
            }
        }
    });

    return totalPoints;
}
