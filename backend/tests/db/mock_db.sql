CREATE TYPE status AS ENUM ('not run', 'complete', 'failed');

CREATE TABLE abstract_pipeline (
    contract_id INTEGER PRIMARY KEY,
    download_stage status DEFAULT 'not run',
    split_stage status DEFAULT 'not run',
    clean_stage status DEFAULT 'not run',
    load_stage status DEFAULT 'not run',
);

INSERT INTO 
    abstract_pipeline ( 
        contract_id, 
        download_stage, 
        split_stage, 
        clean_stage, 
        load_stage 
    ) 
VALUES 
    (10, 'complete', 'complete', 'complete', 'complete'),
    (20, 'complete', 'failed', 'not run', 'not run'),
    (30, 'not run', 'not run', 'not run', 'not run')
;