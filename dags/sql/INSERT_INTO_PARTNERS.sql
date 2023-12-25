INSERT INTO partners (partner_name, partner_status) 
VALUES 
('A', FALSE),
('B', FALSE),
('C', FALSE)
ON CONFLICT(partner_name) DO NOTHING;