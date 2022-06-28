BEGIN TRANSACTION;

CREATE TABLE drivers (
    initials VARCHAR(3) NOT NULL,
    price INT NOT NULL,
    points INT,
    PRIMARY KEY(initials)
);

CREATE TABLE constructors (
    abbreviation VARCHAR(3) NOT NULL,
    price INT NOT NULL,
    points INT,
    PRIMARY KEY(abbreviation)
);

COMMIT;