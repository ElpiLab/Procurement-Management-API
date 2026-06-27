CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(50)
);

INSERT INTO suppliers (name, country) 
VALUES
('ABB', 'Switzerland'),
('Siemens', 'Germany');