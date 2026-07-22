-- Consultas Analíticas

-- 1. Total de atestados por período (mês)
SELECT 
    DATE_TRUNC('month', created_at) AS mes,
    COUNT(*) AS total_atestados
FROM documents
WHERE processing_status = 'completed'
GROUP BY mes
ORDER BY mes DESC;

-- 2. Ranking de CIDs mais frequentes
SELECT 
    cid,
    COUNT(*) AS frequencia
FROM medical_certificates
WHERE cid IS NOT NULL
GROUP BY cid
ORDER BY frequencia DESC
LIMIT 10;

-- 3. Média de dias de afastamento por CID
SELECT 
    cid,
    ROUND(AVG(leave_days), 1) AS media_dias
FROM medical_certificates
WHERE cid IS NOT NULL AND leave_days IS NOT NULL
GROUP BY cid
ORDER BY media_dias DESC;

-- 4. Colaboradores com mais atestados no período
SELECT 
    employee_name,
    COUNT(*) AS total_atestados,
    SUM(leave_days) AS total_dias_afastamento
FROM medical_certificates
WHERE employee_name IS NOT NULL
GROUP BY employee_name
ORDER BY total_atestados DESC
LIMIT 10;

-- 5. Total de dias de absenteísmo por mês (baseado na data de início do afastamento)
SELECT 
    DATE_TRUNC('month', leave_start_date) AS mes_afastamento,
    SUM(leave_days) AS total_dias
FROM medical_certificates
WHERE leave_start_date IS NOT NULL AND leave_days IS NOT NULL
GROUP BY mes_afastamento
ORDER BY mes_afastamento DESC;

-- 6. Taxa de complementação manual (Auditoria)
SELECT
    event_type,
    COUNT(*) as total
FROM processing_events
WHERE event_type IN ('AI_COMPLETED', 'USER_COMPLEMENTED', 'FINALIZED')
GROUP BY event_type;
