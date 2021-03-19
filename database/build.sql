CREATE TABLE IF NOT EXISTS Rank (
    UserID integer NOT NULL,
    ServerID integer NOT NULL,
    UserXP integer DEFAULT 0,
    UserLevel integer DEFAULT 1,
    Warns integer DEFAULT 0,
    BirthDay text DEFAULT NULL,
    OldMessage text DEFAULT NULL,
    PRIMARY KEY (UserID, ServerID)
);