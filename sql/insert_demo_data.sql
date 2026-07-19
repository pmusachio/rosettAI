-- Demo Data para testes iniciais (Rh)

-- Inserir alguns documentos
INSERT INTO documents (id, file_name, file_url, document_issue_date, processing_status, submission_status)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'atestado_joao.pdf', 'https://example.com/atestado_joao.pdf', CURRENT_DATE - INTERVAL '1 day', 'completed', 'on_time'),
    ('22222222-2222-2222-2222-222222222222', 'foto_atestado_maria.jpg', 'https://example.com/foto_atestado_maria.jpg', CURRENT_DATE - INTERVAL '5 days', 'completed', 'retroactive'),
    ('33333333-3333-3333-3333-333333333333', 'scan_carlos.png', 'https://example.com/scan_carlos.png', CURRENT_DATE - INTERVAL '2 days', 'completed', 'on_time');

-- Inserir os atestados extraídos correspondentes
INSERT INTO medical_certificates (document_id, employee_name, employee_cpf, doctor_name, crm, health_facility, cid, issue_date, leave_start_date, leave_end_date, leave_days, document_type)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'João Silva', '123.456.789-00', 'Dra. Ana Costa', 'CRM-SP 12345', 'Hospital das Clínicas', 'J01.9', CURRENT_DATE - INTERVAL '1 day', CURRENT_DATE - INTERVAL '1 day', CURRENT_DATE + INTERVAL '1 day', 3, 'Atestado Médico'),
    ('22222222-2222-2222-2222-222222222222', 'Maria Oliveira', '987.654.321-11', 'Dr. Pedro Santos', 'CRM-RJ 54321', 'UPA Copacabana', 'A09', CURRENT_DATE - INTERVAL '5 days', CURRENT_DATE - INTERVAL '5 days', CURRENT_DATE - INTERVAL '3 days', 3, 'Declaração de Comparecimento'),
    ('33333333-3333-3333-3333-333333333333', 'Carlos Souza', '456.789.123-22', 'Dra. Juliana Lima', 'CRM-MG 98765', 'Clínica Santa Maria', 'M54.5', CURRENT_DATE - INTERVAL '2 days', CURRENT_DATE - INTERVAL '2 days', CURRENT_DATE + INTERVAL '2 days', 5, 'Atestado de Afastamento');

-- Inserir eventos de auditoria
INSERT INTO processing_events (document_id, event_type, details)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'UPLOAD_RECEIVED', '{"source": "web_ui"}'::jsonb),
    ('11111111-1111-1111-1111-111111111111', 'AI_COMPLETED', '{"confidence_score": 0.95}'::jsonb),
    ('11111111-1111-1111-1111-111111111111', 'FINALIZED', '{}'::jsonb),
    ('22222222-2222-2222-2222-222222222222', 'UPLOAD_RECEIVED', '{"source": "web_ui"}'::jsonb),
    ('22222222-2222-2222-2222-222222222222', 'AI_COMPLETED', '{"confidence_score": 0.80, "missing_fields": ["cid"]}'::jsonb),
    ('22222222-2222-2222-2222-222222222222', 'USER_COMPLEMENTED', '{"fields_updated": ["cid"]}'::jsonb),
    ('22222222-2222-2222-2222-222222222222', 'FINALIZED', '{}'::jsonb);
