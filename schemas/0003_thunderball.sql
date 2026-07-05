BEGIN;

CREATE SCHEMA thunderball;

CREATE TABLE thunderball.scores (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username_id     BIGINT NOT NULL REFERENCES usernames(id) ON DELETE CASCADE,
    p_width         INT NOT NULL,
    p_height        INT NOT NULL,
    p_ballno        INT NOT NULL,
    score           BIGINT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT unique_parameters UNIQUE (p_width, p_height, p_ballno, score)
);

CREATE TABLE thunderball.payloads (
    id       BIGINT NOT NULL REFERENCES thunderball.scores(id) ON DELETE CASCADE,
    payload  TEXT NOT NULL
);

INSERT INTO schema_migrations (version)
VALUES ('0003_thunderball.sql');

COMMIT;
