create table chengyugushi
(
    id      VARCHAR(32) PRIMARY KEY,
    name    VARCHAR(255) UNIQUE,
    pinyin  VARCHAR(255),
    `explain` TEXT,
    content TEXT
);