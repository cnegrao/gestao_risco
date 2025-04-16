-- Table: public.tb_categorias

-- DROP TABLE IF EXISTS public.tb_categorias;

CREATE TABLE IF NOT EXISTS public.tb_categorias
(
    id_categoria integer NOT NULL DEFAULT nextval('tb_categorias_id_categoria_seq'::regclass),
    nome_categoria character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT tb_categorias_pkey PRIMARY KEY (id_categoria),
    CONSTRAINT tb_categorias_nome_categoria_key UNIQUE (nome_categoria)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_categorias
    OWNER to postgres;
	
-- Table: public.tb_causas

-- DROP TABLE IF EXISTS public.tb_causas;

CREATE TABLE IF NOT EXISTS public.tb_causas
(
    id_causa integer NOT NULL DEFAULT nextval('tb_causas_id_causa_seq'::regclass),
    descricao_causa text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT tb_causas_pkey PRIMARY KEY (id_causa),
    CONSTRAINT tb_causas_descricao_causa_key UNIQUE (descricao_causa)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_causas
    OWNER to postgres;
	
-- Table: public.tb_consequencias

-- DROP TABLE IF EXISTS public.tb_consequencias;

CREATE TABLE IF NOT EXISTS public.tb_consequencias
(
    id_consequencia integer NOT NULL DEFAULT nextval('tb_consequencias_id_consequencia_seq'::regclass),
    descricao_consequencia text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT tb_consequencias_pkey PRIMARY KEY (id_consequencia),
    CONSTRAINT tb_consequencias_descricao_consequencia_key UNIQUE (descricao_consequencia)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_consequencias
    OWNER to postgres;
	
-- Table: public.tb_empresas

-- DROP TABLE IF EXISTS public.tb_empresas;

CREATE TABLE IF NOT EXISTS public.tb_empresas
(
    id_empresa integer NOT NULL,
    nome_empresa character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT tb_empresas_pkey PRIMARY KEY (id_empresa)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_empresas
    OWNER to postgres;
	
-- Table: public.tb_processos

-- DROP TABLE IF EXISTS public.tb_processos;

CREATE TABLE IF NOT EXISTS public.tb_processos
(
    id_processo integer NOT NULL DEFAULT nextval('tb_processos_id_processo_seq'::regclass),
    nome_processo character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT tb_processos_pkey PRIMARY KEY (id_processo),
    CONSTRAINT tb_processos_nome_processo_key UNIQUE (nome_processo)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_processos
    OWNER to postgres;
	
-- Table: public.tb_risco_causa

-- DROP TABLE IF EXISTS public.tb_risco_causa;

CREATE TABLE IF NOT EXISTS public.tb_risco_causa
(
    id_risco integer NOT NULL,
    id_causa integer NOT NULL,
    CONSTRAINT tb_risco_causa_pkey PRIMARY KEY (id_risco, id_causa),
    CONSTRAINT fk_causa_rc FOREIGN KEY (id_causa)
        REFERENCES public.tb_causas (id_causa) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_risco_rc FOREIGN KEY (id_risco)
        REFERENCES public.tb_riscos (id_risco) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_risco_causa
    OWNER to postgres;
	
-- Table: public.tb_risco_consequencia

-- DROP TABLE IF EXISTS public.tb_risco_consequencia;

CREATE TABLE IF NOT EXISTS public.tb_risco_consequencia
(
    id_risco integer NOT NULL,
    id_consequencia integer NOT NULL,
    CONSTRAINT tb_risco_consequencia_pkey PRIMARY KEY (id_risco, id_consequencia),
    CONSTRAINT fk_consequencia_rcons FOREIGN KEY (id_consequencia)
        REFERENCES public.tb_consequencias (id_consequencia) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_risco_rcons FOREIGN KEY (id_risco)
        REFERENCES public.tb_riscos (id_risco) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_risco_consequencia
    OWNER to postgres;
	
-- Table: public.tb_risco_selecionado

-- DROP TABLE IF EXISTS public.tb_risco_selecionado;

CREATE TABLE IF NOT EXISTS public.tb_risco_selecionado
(
    id_risco_selecionado integer NOT NULL DEFAULT nextval('tb_risco_selecionado_id_risco_selecionado_seq'::regclass),
    id_empresa integer,
    id_risco integer,
    data_selecao date NOT NULL DEFAULT CURRENT_DATE,
    usuario character varying(100) COLLATE pg_catalog."default",
    observacoes text COLLATE pg_catalog."default",
    CONSTRAINT tb_risco_selecionado_pkey PRIMARY KEY (id_risco_selecionado),
    CONSTRAINT tb_risco_selecionado_id_empresa_fkey FOREIGN KEY (id_empresa)
        REFERENCES public.tb_empresas (id_empresa) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT tb_risco_selecionado_id_risco_fkey FOREIGN KEY (id_risco)
        REFERENCES public.tb_riscos (id_risco) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_risco_selecionado
    OWNER to postgres;
	
-- Table: public.tb_riscos

-- DROP TABLE IF EXISTS public.tb_riscos;

CREATE TABLE IF NOT EXISTS public.tb_riscos
(
    id_risco integer NOT NULL,
    id_empresa integer NOT NULL,
    nome_risco character varying(255) COLLATE pg_catalog."default" NOT NULL,
    descricao text COLLATE pg_catalog."default",
    impacto_estimado character varying(50) COLLATE pg_catalog."default",
    probabilidade character varying(50) COLLATE pg_catalog."default",
    status character varying(50) COLLATE pg_catalog."default",
    data_identificacao date,
    criticidade character varying(50) COLLATE pg_catalog."default",
    id_processo integer,
    id_subprocesso integer,
    id_categoria integer,
    CONSTRAINT tb_riscos_pkey PRIMARY KEY (id_risco),
    CONSTRAINT fk_categoria_risco FOREIGN KEY (id_categoria)
        REFERENCES public.tb_categorias (id_categoria) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_empresa_risco FOREIGN KEY (id_empresa)
        REFERENCES public.tb_empresas (id_empresa) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_processo_risco FOREIGN KEY (id_processo)
        REFERENCES public.tb_processos (id_processo) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_subprocesso_risco FOREIGN KEY (id_subprocesso)
        REFERENCES public.tb_subprocessos (id_subprocesso) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_riscos
    OWNER to postgres;
	
-- Table: public.tb_subprocessos

-- DROP TABLE IF EXISTS public.tb_subprocessos;

CREATE TABLE IF NOT EXISTS public.tb_subprocessos
(
    id_subprocesso integer NOT NULL DEFAULT nextval('tb_subprocessos_id_subprocesso_seq'::regclass),
    id_processo integer NOT NULL,
    nome_subprocesso character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT tb_subprocessos_pkey PRIMARY KEY (id_subprocesso),
    CONSTRAINT fk_processo FOREIGN KEY (id_processo)
        REFERENCES public.tb_processos (id_processo) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_subprocessos
    OWNER to postgres;