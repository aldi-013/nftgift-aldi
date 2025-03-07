CREATE TABLE offers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gift_link TEXT UNIQUE NOT NULL,
    time_end TEXT NOT NULL,
    highest_bid INTEGER DEFAULT 0,
    winner_id INTEGER DEFAULT NULL
);

CREATE TABLE bids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    offer_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    bid_amount INTEGER NOT NULL,
    FOREIGN KEY (offer_id) REFERENCES offers(id)
);
