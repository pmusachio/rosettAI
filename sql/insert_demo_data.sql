-- Demo Data para testes iniciais (RH)
-- 5 cenários: atestado completo via IA, atestado com campo obrigatório
-- complementado manualmente, CIDs/quantidades de dias variados, fluxo 100%
-- automático e um atestado ainda pendente de complementação.

-- Inserir os documentos
INSERT INTO documents (id, file_name, file_url, document_issue_date, processing_status)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'atestado_joao.pdf', 'https://example.com/atestado_joao.pdf', CURRENT_DATE - INTERVAL '1 day', 'completed'),
    ('22222222-2222-2222-2222-222222222222', 'foto_atestado_maria.jpg', 'https://example.com/foto_atestado_maria.jpg', CURRENT_DATE - INTERVAL '5 days', 'completed'),
    ('33333333-3333-3333-3333-333333333333', 'scan_carlos.png', 'https://example.com/scan_carlos.png', CURRENT_DATE - INTERVAL '2 days', 'completed'),
    ('44444444-4444-4444-4444-444444444444', 'atestado_ana.pdf', 'https://example.com/atestado_ana.pdf', CURRENT_DATE - INTERVAL '1 day', 'completed'),
    ('55555555-5555-5555-5555-555555555555', 'atestado_pedro.jpg', 'https://example.com/atestado_pedro.jpg', CURRENT_DATE, 'processing');

-- Inserir os atestados extraídos correspondentes
-- (registro 5 fica com leave_days e cid em aberto: ainda não foi complementado)
INSERT INTO medical_certificates (document_id, employee_name, employee_cpf, doctor_name, crm, health_facility, cid, issue_date, leave_start_date, leave_end_date, leave_days, document_type)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'João Silva', '123.456.789-00', 'Dra. Ana Costa', 'CRM-SP 12345', 'Hospital das Clínicas', 'J01.9', CURRENT_DATE - INTERVAL '1 day', CURRENT_DATE - INTERVAL '1 day', CURRENT_DATE + INTERVAL '1 day', 3, 'Atestado Médico'),
    ('22222222-2222-2222-2222-222222222222', 'Maria Oliveira', '987.654.321-11', 'Dr. Ricardo Alves', 'CRM-RJ 54321', 'UPA Copacabana', 'A09', CURRENT_DATE - INTERVAL '5 days', CURRENT_DATE - INTERVAL '5 days', CURRENT_DATE - INTERVAL '3 days', 3, 'Declaração de Comparecimento'),
    ('33333333-3333-3333-3333-333333333333', 'Carlos Souza', '456.789.123-22', 'Dra. Juliana Lima', 'CRM-MG 98765', 'Clínica Santa Maria', 'M54.5', CURRENT_DATE - INTERVAL '2 days', CURRENT_DATE - INTERVAL '2 days', CURRENT_DATE + INTERVAL '2 days', 5, 'Atestado de Afastamento'),
    ('44444444-4444-4444-4444-444444444444', 'Ana Pereira', '321.654.987-33', 'Dr. Bruno Tavares', 'CRM-PR 11223', 'Clínica Vida Plena', 'R51', CURRENT_DATE - INTERVAL '1 day', CURRENT_DATE - INTERVAL '1 day', CURRENT_DATE - INTERVAL '1 day', 1, 'Atestado Médico'),
    ('55555555-5555-5555-5555-555555555555', 'Pedro Santos', NULL, NULL, NULL, NULL, NULL, CURRENT_DATE, NULL, NULL, NULL, 'Atestado Médico');

-- Inserir eventos de auditoria
INSERT INTO processing_events (document_id, event_type, details)
VALUES
    -- 1. Fluxo completo, extração 100% correta pela IA
    ('11111111-1111-1111-1111-111111111111', 'UPLOAD_RECEIVED', '{"source": "web_ui"}'::jsonb),
    ('11111111-1111-1111-1111-111111111111', 'AI_STARTED', '{}'::jsonb),
    ('11111111-1111-1111-1111-111111111111', 'AI_COMPLETED', '{"confidence_score": 0.95}'::jsonb),
    ('11111111-1111-1111-1111-111111111111', 'FINALIZED', '{}'::jsonb),

    -- 2. IA não extraiu um campo obrigatório (quantidade_dias) -> complementado manualmente
    ('22222222-2222-2222-2222-222222222222', 'UPLOAD_RECEIVED', '{"source": "web_ui"}'::jsonb),
    ('22222222-2222-2222-2222-222222222222', 'AI_STARTED', '{}'::jsonb),
    ('22222222-2222-2222-2222-222222222222', 'AI_COMPLETED', '{"confidence_score": 0.80, "missing_fields": ["quantidade_dias"]}'::jsonb),
    ('22222222-2222-2222-2222-222222222222', 'USER_COMPLEMENTED', '{"fields_updated": ["quantidade_dias"]}'::jsonb),
    ('22222222-2222-2222-2222-222222222222', 'FINALIZED', '{}'::jsonb),

    -- 3. Fluxo completo, extração 100% correta pela IA
    ('33333333-3333-3333-3333-333333333333', 'UPLOAD_RECEIVED', '{"source": "web_ui"}'::jsonb),
    ('33333333-3333-3333-3333-333333333333', 'AI_STARTED', '{}'::jsonb),
    ('33333333-3333-3333-3333-333333333333', 'AI_COMPLETED', '{"confidence_score": 0.92}'::jsonb),
    ('33333333-3333-3333-3333-333333333333', 'FINALIZED', '{}'::jsonb),

    -- 4. Fluxo 100% automático, sem nenhuma intervenção manual
    ('44444444-4444-4444-4444-444444444444', 'UPLOAD_RECEIVED', '{"source": "web_ui"}'::jsonb),
    ('44444444-4444-4444-4444-444444444444', 'AI_STARTED', '{}'::jsonb),
    ('44444444-4444-4444-4444-444444444444', 'AI_COMPLETED', '{"confidence_score": 0.97}'::jsonb),
    ('44444444-4444-4444-4444-444444444444', 'FINALIZED', '{}'::jsonb),

    -- 5. Ainda pendente: IA não encontrou CID nem quantidade de dias, aguardando complementação
    ('55555555-5555-5555-5555-555555555555', 'UPLOAD_RECEIVED', '{"source": "web_ui"}'::jsonb),
    ('55555555-5555-5555-5555-555555555555', 'AI_STARTED', '{}'::jsonb),
    ('55555555-5555-5555-5555-555555555555', 'AI_COMPLETED', '{"confidence_score": 0.40, "missing_fields": ["quantidade_dias", "cid", "nome_medico"]}'::jsonb);
