CREATE TYPE status AS ENUM ('not run', 'complete', 'failed');

CREATE TABLE pipeline_status (
    contract_id INTEGER PRIMARY KEY,
    download_stage status DEFAULT 'not run',
    split_stage status DEFAULT 'not run',
    clean_stage status DEFAULT 'not run',
);

INSERT INTO 
    pipeline_status( contract_id, download_stage, split_stage, clean_stage ) 
VALUES 
    (10, 'complete', 'complete', 'complete'),
    (20, 'complete', 'failed', 'not run'),
    (30, 'not run', 'not run', 'not run')
;