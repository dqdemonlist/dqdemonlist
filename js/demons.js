
const demons = [
  {
    "id": 1,
    "name": "Beetle",
    "creator": "Cirtrax",
    "verifier": 1,
    "verifyDate": "2025-10-02",
    "completers": [
      {
        "playerId": 3,
        "date": "2025-11-04"
      }
    ]
  },
  {
    "id": 2,
    "name": "Acropolis",
    "creator": "Zobros",
    "verifier": 1,
    "verifyDate": "2025-09-29",
    "completers": [
      {
        "playerId": 3,
        "date": "2025-07-09"
      }
    ]
  },
  {
    "id": 3,
    "name": "Crazy II",
    "creator": "DavJT",
    "verifier": 2,
    "verifyDate": "2025-10-29",
    "completers": [
      {
        "playerId": 3,
        "date": "2025-05-12"
      },
      {
        "playerId": 6,
        "date": "2026-10-29"
      }
    ]
  },
  {
    "id": 4,
    "name": "Quantum Variations",
    "creator": "Darwin",
    "verifier": 1,
    "verifyDate": "2025-10-28",
    "completers": []
  },
  {
    "id": 5,
    "name": "Psychosis",
    "creator": "Hinds",
    "verifier": 1,
    "verifyDate": "2025-09-29",
    "completers": []
  },
  {
    "id": 6,
    "name": "The Furious",
    "creator": "Knobbelboy",
    "verifier": 1,
    "verifyDate": "2024-07-12",
    "completers": []
  },
  {
    "id": 7,
    "name": "Ruuun",
    "creator": "CherryTeam",
    "verifier": 1,
    "verifyDate": "2025-06-01",
    "completers": [
      {
        "playerId": 2,
        "date": "2025-04-08"
      }
    ]
  },
  {
    "id": 8,
    "name": "Ascent",
    "creator": "JustBasic",
    "verifier": 1,
    "verifyDate": "2025-09-18",
    "completers": []
  },
  {
    "id": 9,
    "name": "Necropolis",
    "creator": "IIINepTuneIII",
    "verifier": 3,
    "verifyDate": "2025-11-10",
    "completers": []
  },
  {
    "id": 10,
    "name": "Acu",
    "creator": "Neigefeu",
    "verifier": 1,
    "verifyDate": "2025-11-10",
    "completers": []
  },
  {
    "id": 11,
    "name": "Windy Landscape",
    "creator": "WOOGI1411",
    "verifier": 3,
    "verifyDate": "2025-11-11",
    "completers": []
  },
  {
    "id": 12,
    "name": "Cataclysm",
    "creator": "GgBoy",
    "verifier": 1,
    "verifyDate": "2025-11-15",
    "completers": []
  },
  {
    "id": 13,
    "name": "Rupture",
    "creator": "Jekko",
    "verifier": 3,
    "verifyDate": "2025-11-15",
    "completers": []
  },
  {
    "id": 14,
    "name": "Poltergeist",
    "creator": "AndromedaGMD",
    "verifier": 6,
    "verifyDate": "2025-11-10",
    "completers": []
  },
  {
    "id": 15,
    "name": "Sweater Weather",
    "creator": "VelYT",
    "verifier": 6,
    "verifyDate": "2026-01-31",
    "completers": []
  },
  {
    "id": 16,
    "name": "Gravity",
    "creator": "KazaGD",
    "verifier": 5,
    "verifyDate": "2026-02-26",
    "completers": []
  },
  {
    "id": 17,
    "name": "Bloodbath",
    "creator": "Riot",
    "verifier": 6,
    "verifyDate": "2026-03-01",
    "completers": []
  },
  {
    "id": 18,
    "name": "Sharp Minor",
    "creator": "Giron",
    "verifier": 7,
    "verifyDate": "2025-12-16",
    "completers": []
  },
  {
    "id": 19,
    "name": "Allegiance",
    "creator": "nikroplays",
    "verifier": 8,
    "verifyDate": "2026-03-28",
    "completers": [
      {
        "playerId": 8,
        "date": "2026-03-28"
      }
    ]
  }
];

// Функция для получения демона по ID
function getDemonById(id) {
    return demons.find(demon => demon.id === id);
}

// Функция для получения всех демонов
function getAllDemons() {
    return demons;
}

