-- 1. Tabela de Controle de Documentos
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    accepted_at TIMESTAMP WITH TIME ZONE,
    document_issue_date DATE,
    processing_status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, error
    submission_status VARCHAR(50), -- on_time, retroactive
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Tabela de Dados Extraídos (Atestados)
CREATE TABLE IF NOT EXISTS medical_certificates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    employee_name VARCHAR(255),
    employee_cpf VARCHAR(20),
    doctor_name VARCHAR(255),
    crm VARCHAR(50),
    health_facility VARCHAR(255),
    cid VARCHAR(10),
    issue_date DATE,
    leave_start_date DATE,
    leave_end_date DATE,
    leave_days INTEGER,
    document_type VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(document_id)
);

-- 3. Tabela de Eventos (Auditoria)
CREATE TABLE IF NOT EXISTS processing_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL, -- UPLOAD_RECEIVED, AI_STARTED, AI_COMPLETED, USER_COMPLEMENTED, FINALIZED
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    details JSONB DEFAULT '{}'::jsonb
);

-- Function to update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_documents_updated_at
BEFORE UPDATE ON documents
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_medical_certificates_updated_at
BEFORE UPDATE ON medical_certificates
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
