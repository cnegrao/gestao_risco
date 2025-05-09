--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

-- Started on 2025-05-08 10:33:48

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 5090 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 260 (class 1259 OID 172131)
-- Name: tb_area_responsavel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_area_responsavel (
    id_area integer NOT NULL,
    nome_area text NOT NULL
);


ALTER TABLE public.tb_area_responsavel OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 172130)
-- Name: tb_area_responsavel_id_area_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_area_responsavel_id_area_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_area_responsavel_id_area_seq OWNER TO postgres;

--
-- TOC entry 5091 (class 0 OID 0)
-- Dependencies: 259
-- Name: tb_area_responsavel_id_area_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_area_responsavel_id_area_seq OWNED BY public.tb_area_responsavel.id_area;


--
-- TOC entry 223 (class 1259 OID 171617)
-- Name: tb_categorias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_categorias (
    id_categoria integer NOT NULL,
    nome_categoria character varying(255) NOT NULL
);


ALTER TABLE public.tb_categorias OWNER TO postgres;

--
-- TOC entry 5092 (class 0 OID 0)
-- Dependencies: 223
-- Name: TABLE tb_categorias; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tb_categorias IS 'Categorias principais de riscos (ex: Financeiro, Operacional, etc.)';


--
-- TOC entry 5093 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN tb_categorias.id_categoria; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_categorias.id_categoria IS 'Identificador da categoria';


--
-- TOC entry 5094 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN tb_categorias.nome_categoria; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_categorias.nome_categoria IS 'Nome da categoria';


--
-- TOC entry 222 (class 1259 OID 171616)
-- Name: tb_categorias_id_categoria_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_categorias_id_categoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_categorias_id_categoria_seq OWNER TO postgres;

--
-- TOC entry 5095 (class 0 OID 0)
-- Dependencies: 222
-- Name: tb_categorias_id_categoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_categorias_id_categoria_seq OWNED BY public.tb_categorias.id_categoria;


--
-- TOC entry 225 (class 1259 OID 171626)
-- Name: tb_causas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_causas (
    id_causa integer NOT NULL,
    descricao_causa text NOT NULL
);


ALTER TABLE public.tb_causas OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 171625)
-- Name: tb_causas_id_causa_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_causas_id_causa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_causas_id_causa_seq OWNER TO postgres;

--
-- TOC entry 5096 (class 0 OID 0)
-- Dependencies: 224
-- Name: tb_causas_id_causa_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_causas_id_causa_seq OWNED BY public.tb_causas.id_causa;


--
-- TOC entry 227 (class 1259 OID 171637)
-- Name: tb_consequencias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_consequencias (
    id_consequencia integer NOT NULL,
    descricao_consequencia text NOT NULL
);


ALTER TABLE public.tb_consequencias OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 171636)
-- Name: tb_consequencias_id_consequencia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_consequencias_id_consequencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_consequencias_id_consequencia_seq OWNER TO postgres;

--
-- TOC entry 5097 (class 0 OID 0)
-- Dependencies: 226
-- Name: tb_consequencias_id_consequencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_consequencias_id_consequencia_seq OWNED BY public.tb_consequencias.id_consequencia;


--
-- TOC entry 240 (class 1259 OID 171850)
-- Name: tb_controles_existentes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_controles_existentes (
    id_controle integer NOT NULL,
    nome_controle character varying(200) NOT NULL
);


ALTER TABLE public.tb_controles_existentes OWNER TO postgres;

--
-- TOC entry 5098 (class 0 OID 0)
-- Dependencies: 240
-- Name: TABLE tb_controles_existentes; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tb_controles_existentes IS 'Domínio de controles existentes (colunas M e N)';


--
-- TOC entry 5099 (class 0 OID 0)
-- Dependencies: 240
-- Name: COLUMN tb_controles_existentes.nome_controle; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_controles_existentes.nome_controle IS 'Descrição do controle (existência/relevância ou funcionamento)';


--
-- TOC entry 239 (class 1259 OID 171849)
-- Name: tb_controles_existentes_id_controle_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_controles_existentes_id_controle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_controles_existentes_id_controle_seq OWNER TO postgres;

--
-- TOC entry 5100 (class 0 OID 0)
-- Dependencies: 239
-- Name: tb_controles_existentes_id_controle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_controles_existentes_id_controle_seq OWNED BY public.tb_controles_existentes.id_controle;


--
-- TOC entry 217 (class 1259 OID 171590)
-- Name: tb_empresas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_empresas (
    id_empresa integer NOT NULL,
    nome_empresa character varying(255) NOT NULL
);


ALTER TABLE public.tb_empresas OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 171885)
-- Name: tb_execucao_controle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_execucao_controle (
    id_execucao_controle integer NOT NULL,
    descricao text NOT NULL
);


ALTER TABLE public.tb_execucao_controle OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 171884)
-- Name: tb_execucao_controle_id_execucao_controle_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_execucao_controle_id_execucao_controle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_execucao_controle_id_execucao_controle_seq OWNER TO postgres;

--
-- TOC entry 5101 (class 0 OID 0)
-- Dependencies: 243
-- Name: tb_execucao_controle_id_execucao_controle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_execucao_controle_id_execucao_controle_seq OWNED BY public.tb_execucao_controle.id_execucao_controle;


--
-- TOC entry 252 (class 1259 OID 171994)
-- Name: tb_indicador; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_indicador (
    id_indicador integer NOT NULL,
    id_empresa integer NOT NULL,
    id_meta integer NOT NULL,
    descricao text NOT NULL,
    valor_alvo character varying(100),
    data_criacao timestamp without time zone DEFAULT now()
);


ALTER TABLE public.tb_indicador OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 171993)
-- Name: tb_indicador_id_indicador_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_indicador_id_indicador_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_indicador_id_indicador_seq OWNER TO postgres;

--
-- TOC entry 5102 (class 0 OID 0)
-- Dependencies: 251
-- Name: tb_indicador_id_indicador_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_indicador_id_indicador_seq OWNED BY public.tb_indicador.id_indicador;


--
-- TOC entry 250 (class 1259 OID 171974)
-- Name: tb_meta_estrategica; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_meta_estrategica (
    id_meta integer NOT NULL,
    id_empresa integer NOT NULL,
    id_objetivo integer NOT NULL,
    descricao text NOT NULL,
    ano integer NOT NULL,
    data_criacao timestamp without time zone DEFAULT now()
);


ALTER TABLE public.tb_meta_estrategica OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 171973)
-- Name: tb_meta_estrategica_id_meta_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_meta_estrategica_id_meta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_meta_estrategica_id_meta_seq OWNER TO postgres;

--
-- TOC entry 5103 (class 0 OID 0)
-- Dependencies: 249
-- Name: tb_meta_estrategica_id_meta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_meta_estrategica_id_meta_seq OWNED BY public.tb_meta_estrategica.id_meta;


--
-- TOC entry 248 (class 1259 OID 171959)
-- Name: tb_objetivo_estrategico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_objetivo_estrategico (
    id_objetivo integer NOT NULL,
    id_empresa integer NOT NULL,
    descricao text NOT NULL,
    data_criacao timestamp without time zone DEFAULT now()
);


ALTER TABLE public.tb_objetivo_estrategico OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 171958)
-- Name: tb_objetivo_estrategico_id_objetivo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_objetivo_estrategico_id_objetivo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_objetivo_estrategico_id_objetivo_seq OWNER TO postgres;

--
-- TOC entry 5104 (class 0 OID 0)
-- Dependencies: 247
-- Name: tb_objetivo_estrategico_id_objetivo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_objetivo_estrategico_id_objetivo_seq OWNED BY public.tb_objetivo_estrategico.id_objetivo;


--
-- TOC entry 262 (class 1259 OID 172142)
-- Name: tb_plano_tratamento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_plano_tratamento (
    id_plano integer NOT NULL,
    id_risco integer NOT NULL,
    id_tipo_tratamento integer NOT NULL,
    descricao_acao text NOT NULL,
    id_status integer NOT NULL,
    id_area_responsavel integer NOT NULL,
    data_inicio date NOT NULL,
    data_prazo_limite date NOT NULL,
    data_real_termino date,
    comentarios text,
    usuario_criacao character varying(100),
    data_criacao timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tb_plano_tratamento OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 172141)
-- Name: tb_plano_tratamento_id_plano_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_plano_tratamento_id_plano_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_plano_tratamento_id_plano_seq OWNER TO postgres;

--
-- TOC entry 5105 (class 0 OID 0)
-- Dependencies: 261
-- Name: tb_plano_tratamento_id_plano_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_plano_tratamento_id_plano_seq OWNED BY public.tb_plano_tratamento.id_plano;


--
-- TOC entry 219 (class 1259 OID 171596)
-- Name: tb_processos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_processos (
    id_processo integer NOT NULL,
    nome_processo character varying(255) NOT NULL
);


ALTER TABLE public.tb_processos OWNER TO postgres;

--
-- TOC entry 5106 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE tb_processos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tb_processos IS 'Tabela de processos organizacionais';


--
-- TOC entry 5107 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN tb_processos.id_processo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_processos.id_processo IS 'Identificador do processo';


--
-- TOC entry 5108 (class 0 OID 0)
-- Dependencies: 219
-- Name: COLUMN tb_processos.nome_processo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_processos.nome_processo IS 'Nome do processo organizacional';


--
-- TOC entry 218 (class 1259 OID 171595)
-- Name: tb_processos_id_processo_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_processos_id_processo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_processos_id_processo_seq OWNER TO postgres;

--
-- TOC entry 5109 (class 0 OID 0)
-- Dependencies: 218
-- Name: tb_processos_id_processo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_processos_id_processo_seq OWNED BY public.tb_processos.id_processo;


--
-- TOC entry 238 (class 1259 OID 171833)
-- Name: tb_risco_avaliacoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_risco_avaliacoes (
    id_avaliacao integer NOT NULL,
    id_risco integer NOT NULL,
    probabilidade smallint NOT NULL,
    impacto_financeiro smallint NOT NULL,
    impacto_imagem smallint NOT NULL,
    impacto_conformidade smallint NOT NULL,
    impacto_final smallint NOT NULL,
    criticidade character varying(50) NOT NULL,
    data_avaliacao date DEFAULT CURRENT_DATE NOT NULL,
    CONSTRAINT tb_risco_avaliacoes_impacto_conformidade_check CHECK (((impacto_conformidade >= 1) AND (impacto_conformidade <= 5))),
    CONSTRAINT tb_risco_avaliacoes_impacto_financeiro_check CHECK (((impacto_financeiro >= 1) AND (impacto_financeiro <= 5))),
    CONSTRAINT tb_risco_avaliacoes_impacto_imagem_check CHECK (((impacto_imagem >= 1) AND (impacto_imagem <= 5))),
    CONSTRAINT tb_risco_avaliacoes_probabilidade_check CHECK (((probabilidade >= 1) AND (probabilidade <= 5)))
);


ALTER TABLE public.tb_risco_avaliacoes OWNER TO postgres;

--
-- TOC entry 5110 (class 0 OID 0)
-- Dependencies: 238
-- Name: TABLE tb_risco_avaliacoes; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tb_risco_avaliacoes IS 'Avaliações de risco, registrando probabilidade, impactos detalhados e classificação final';


--
-- TOC entry 5111 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN tb_risco_avaliacoes.id_avaliacao; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_avaliacoes.id_avaliacao IS 'Identificador único da avaliação';


--
-- TOC entry 5112 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN tb_risco_avaliacoes.id_risco; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_avaliacoes.id_risco IS 'Chave estrangeira que referencia o risco avaliado';


--
-- TOC entry 5113 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN tb_risco_avaliacoes.probabilidade; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_avaliacoes.probabilidade IS 'Probabilidade de ocorrência do risco (1 a 5)';


--
-- TOC entry 5114 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN tb_risco_avaliacoes.impacto_financeiro; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_avaliacoes.impacto_financeiro IS 'Avaliação do impacto financeiro do risco (1 a 5)';


--
-- TOC entry 5115 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN tb_risco_avaliacoes.impacto_imagem; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_avaliacoes.impacto_imagem IS 'Avaliação do impacto na imagem (1 a 5)';


--
-- TOC entry 5116 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN tb_risco_avaliacoes.impacto_conformidade; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_avaliacoes.impacto_conformidade IS 'Avaliação do impacto na conformidade (1 a 5)';


--
-- TOC entry 5117 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN tb_risco_avaliacoes.impacto_final; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_avaliacoes.impacto_final IS 'Impacto final calculado (ex: máximo dos três impactos)';


--
-- TOC entry 5118 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN tb_risco_avaliacoes.criticidade; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_avaliacoes.criticidade IS 'Classificação do risco (ex: Pequeno, Moderado, Alto, Crítico)';


--
-- TOC entry 5119 (class 0 OID 0)
-- Dependencies: 238
-- Name: COLUMN tb_risco_avaliacoes.data_avaliacao; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_avaliacoes.data_avaliacao IS 'Data da avaliação';


--
-- TOC entry 237 (class 1259 OID 171832)
-- Name: tb_risco_avaliacoes_id_avaliacao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_risco_avaliacoes_id_avaliacao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_risco_avaliacoes_id_avaliacao_seq OWNER TO postgres;

--
-- TOC entry 5120 (class 0 OID 0)
-- Dependencies: 237
-- Name: tb_risco_avaliacoes_id_avaliacao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_risco_avaliacoes_id_avaliacao_seq OWNED BY public.tb_risco_avaliacoes.id_avaliacao;


--
-- TOC entry 229 (class 1259 OID 171674)
-- Name: tb_risco_causa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_risco_causa (
    id_risco integer NOT NULL,
    id_causa integer NOT NULL
);


ALTER TABLE public.tb_risco_causa OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 171689)
-- Name: tb_risco_consequencia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_risco_consequencia (
    id_risco integer NOT NULL,
    id_consequencia integer NOT NULL
);


ALTER TABLE public.tb_risco_consequencia OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 171896)
-- Name: tb_risco_controle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_risco_controle (
    id_controle integer NOT NULL,
    id_risco integer NOT NULL,
    descricao_controle text NOT NULL,
    id_situacao_controle integer NOT NULL,
    id_execucao_controle integer NOT NULL,
    usuario_criacao character varying(100),
    data_criacao timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tb_risco_controle OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 171895)
-- Name: tb_risco_controle_id_controle_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_risco_controle_id_controle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_risco_controle_id_controle_seq OWNER TO postgres;

--
-- TOC entry 5121 (class 0 OID 0)
-- Dependencies: 245
-- Name: tb_risco_controle_id_controle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_risco_controle_id_controle_seq OWNED BY public.tb_risco_controle.id_controle;


--
-- TOC entry 234 (class 1259 OID 171801)
-- Name: tb_risco_eventos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_risco_eventos (
    id_evento integer NOT NULL,
    id_risco integer NOT NULL,
    id_empresa integer NOT NULL,
    tipo_evento character varying(50) NOT NULL,
    descricao_evento text,
    data_evento timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.tb_risco_eventos OWNER TO postgres;

--
-- TOC entry 5122 (class 0 OID 0)
-- Dependencies: 234
-- Name: TABLE tb_risco_eventos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tb_risco_eventos IS 'Histórico de eventos relacionados a alterações, avaliações e respostas aos riscos';


--
-- TOC entry 5123 (class 0 OID 0)
-- Dependencies: 234
-- Name: COLUMN tb_risco_eventos.id_evento; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_eventos.id_evento IS 'Identificador único do evento de risco';


--
-- TOC entry 5124 (class 0 OID 0)
-- Dependencies: 234
-- Name: COLUMN tb_risco_eventos.id_risco; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_eventos.id_risco IS 'Chave estrangeira que referencia o risco associado';


--
-- TOC entry 5125 (class 0 OID 0)
-- Dependencies: 234
-- Name: COLUMN tb_risco_eventos.id_empresa; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_eventos.id_empresa IS 'Identificador da empresa no ambiente multiempresa';


--
-- TOC entry 5126 (class 0 OID 0)
-- Dependencies: 234
-- Name: COLUMN tb_risco_eventos.tipo_evento; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_eventos.tipo_evento IS 'Tipo do evento (ex.: Avaliação, Resposta, Monitoramento)';


--
-- TOC entry 5127 (class 0 OID 0)
-- Dependencies: 234
-- Name: COLUMN tb_risco_eventos.descricao_evento; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_eventos.descricao_evento IS 'Descrição detalhada do evento ocorrido';


--
-- TOC entry 5128 (class 0 OID 0)
-- Dependencies: 234
-- Name: COLUMN tb_risco_eventos.data_evento; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_risco_eventos.data_evento IS 'Data e hora em que o evento foi registrado';


--
-- TOC entry 233 (class 1259 OID 171800)
-- Name: tb_risco_eventos_id_evento_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_risco_eventos_id_evento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_risco_eventos_id_evento_seq OWNER TO postgres;

--
-- TOC entry 5129 (class 0 OID 0)
-- Dependencies: 233
-- Name: tb_risco_eventos_id_evento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_risco_eventos_id_evento_seq OWNED BY public.tb_risco_eventos.id_evento;


--
-- TOC entry 254 (class 1259 OID 172014)
-- Name: tb_risco_meta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_risco_meta (
    id_risco_meta integer NOT NULL,
    id_empresa integer NOT NULL,
    id_risco integer NOT NULL,
    id_meta integer NOT NULL,
    usuario_criacao character varying(100),
    data_criacao timestamp without time zone DEFAULT now()
);


ALTER TABLE public.tb_risco_meta OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 172013)
-- Name: tb_risco_meta_id_risco_meta_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_risco_meta_id_risco_meta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_risco_meta_id_risco_meta_seq OWNER TO postgres;

--
-- TOC entry 5130 (class 0 OID 0)
-- Dependencies: 253
-- Name: tb_risco_meta_id_risco_meta_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_risco_meta_id_risco_meta_seq OWNED BY public.tb_risco_meta.id_risco_meta;


--
-- TOC entry 232 (class 1259 OID 171705)
-- Name: tb_risco_selecionado; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_risco_selecionado (
    id_risco_selecionado integer NOT NULL,
    id_empresa integer,
    id_risco integer,
    data_selecao date DEFAULT CURRENT_DATE NOT NULL,
    usuario character varying(100),
    observacoes text
);


ALTER TABLE public.tb_risco_selecionado OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 171704)
-- Name: tb_risco_selecionado_id_risco_selecionado_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_risco_selecionado_id_risco_selecionado_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_risco_selecionado_id_risco_selecionado_seq OWNER TO postgres;

--
-- TOC entry 5131 (class 0 OID 0)
-- Dependencies: 231
-- Name: tb_risco_selecionado_id_risco_selecionado_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_risco_selecionado_id_risco_selecionado_seq OWNED BY public.tb_risco_selecionado.id_risco_selecionado;


--
-- TOC entry 228 (class 1259 OID 171647)
-- Name: tb_riscos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_riscos (
    id_risco integer NOT NULL,
    id_empresa integer NOT NULL,
    nome_risco character varying(255) NOT NULL,
    descricao text,
    impacto_estimado character varying(50),
    probabilidade character varying(50),
    status character varying(50),
    data_identificacao date,
    criticidade character varying(50),
    id_processo integer,
    id_subprocesso integer,
    id_categoria integer,
    nivel_risco integer,
    impacto_financeiro character varying(50),
    impacto_imagem character varying(50),
    impacto_conformidade character varying(50),
    id_controle_m integer,
    id_controle_n integer
);


ALTER TABLE public.tb_riscos OWNER TO postgres;

--
-- TOC entry 5132 (class 0 OID 0)
-- Dependencies: 228
-- Name: COLUMN tb_riscos.impacto_financeiro; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_riscos.impacto_financeiro IS 'Avaliação do impacto financeiro do risco (1 a 5)';


--
-- TOC entry 5133 (class 0 OID 0)
-- Dependencies: 228
-- Name: COLUMN tb_riscos.impacto_imagem; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_riscos.impacto_imagem IS 'Avaliação do impacto na imagem da organização (1 a 5)';


--
-- TOC entry 5134 (class 0 OID 0)
-- Dependencies: 228
-- Name: COLUMN tb_riscos.impacto_conformidade; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_riscos.impacto_conformidade IS 'Avaliação do impacto na conformidade (1 a 5)';


--
-- TOC entry 5135 (class 0 OID 0)
-- Dependencies: 228
-- Name: COLUMN tb_riscos.id_controle_m; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_riscos.id_controle_m IS 'FK para controle de existência e relevância (coluna M)';


--
-- TOC entry 5136 (class 0 OID 0)
-- Dependencies: 228
-- Name: COLUMN tb_riscos.id_controle_n; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_riscos.id_controle_n IS 'FK para controle de funcionamento (coluna N)';


--
-- TOC entry 242 (class 1259 OID 171874)
-- Name: tb_situacao_controle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_situacao_controle (
    id_situacao_controle integer NOT NULL,
    descricao text NOT NULL
);


ALTER TABLE public.tb_situacao_controle OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 171873)
-- Name: tb_situacao_controle_id_situacao_controle_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_situacao_controle_id_situacao_controle_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_situacao_controle_id_situacao_controle_seq OWNER TO postgres;

--
-- TOC entry 5137 (class 0 OID 0)
-- Dependencies: 241
-- Name: tb_situacao_controle_id_situacao_controle_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_situacao_controle_id_situacao_controle_seq OWNED BY public.tb_situacao_controle.id_situacao_controle;


--
-- TOC entry 258 (class 1259 OID 172120)
-- Name: tb_status_plano; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_status_plano (
    id_status integer NOT NULL,
    descricao text NOT NULL
);


ALTER TABLE public.tb_status_plano OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 172119)
-- Name: tb_status_plano_id_status_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_status_plano_id_status_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_status_plano_id_status_seq OWNER TO postgres;

--
-- TOC entry 5138 (class 0 OID 0)
-- Dependencies: 257
-- Name: tb_status_plano_id_status_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_status_plano_id_status_seq OWNED BY public.tb_status_plano.id_status;


--
-- TOC entry 236 (class 1259 OID 171821)
-- Name: tb_subcategorias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_subcategorias (
    id_subcategoria integer NOT NULL,
    id_categoria integer NOT NULL,
    nome_subcategoria character varying(100) NOT NULL
);


ALTER TABLE public.tb_subcategorias OWNER TO postgres;

--
-- TOC entry 5139 (class 0 OID 0)
-- Dependencies: 236
-- Name: TABLE tb_subcategorias; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tb_subcategorias IS 'Subcategorias de riscos relacionadas a uma categoria principal';


--
-- TOC entry 5140 (class 0 OID 0)
-- Dependencies: 236
-- Name: COLUMN tb_subcategorias.id_subcategoria; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_subcategorias.id_subcategoria IS 'Identificador da subcategoria';


--
-- TOC entry 5141 (class 0 OID 0)
-- Dependencies: 236
-- Name: COLUMN tb_subcategorias.id_categoria; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_subcategorias.id_categoria IS 'Chave estrangeira para a categoria';


--
-- TOC entry 5142 (class 0 OID 0)
-- Dependencies: 236
-- Name: COLUMN tb_subcategorias.nome_subcategoria; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_subcategorias.nome_subcategoria IS 'Nome da subcategoria';


--
-- TOC entry 235 (class 1259 OID 171820)
-- Name: tb_subcategorias_id_subcategoria_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_subcategorias_id_subcategoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_subcategorias_id_subcategoria_seq OWNER TO postgres;

--
-- TOC entry 5143 (class 0 OID 0)
-- Dependencies: 235
-- Name: tb_subcategorias_id_subcategoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_subcategorias_id_subcategoria_seq OWNED BY public.tb_subcategorias.id_subcategoria;


--
-- TOC entry 221 (class 1259 OID 171605)
-- Name: tb_subprocessos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_subprocessos (
    id_subprocesso integer NOT NULL,
    id_processo integer NOT NULL,
    nome_subprocesso character varying(255) NOT NULL
);


ALTER TABLE public.tb_subprocessos OWNER TO postgres;

--
-- TOC entry 5144 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE tb_subprocessos; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tb_subprocessos IS 'Subprocessos vinculados a processos organizacionais';


--
-- TOC entry 5145 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN tb_subprocessos.id_subprocesso; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_subprocessos.id_subprocesso IS 'Identificador do subprocesso';


--
-- TOC entry 5146 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN tb_subprocessos.id_processo; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_subprocessos.id_processo IS 'Chave estrangeira para o processo pai';


--
-- TOC entry 5147 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN tb_subprocessos.nome_subprocesso; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tb_subprocessos.nome_subprocesso IS 'Nome do subprocesso';


--
-- TOC entry 220 (class 1259 OID 171604)
-- Name: tb_subprocessos_id_subprocesso_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_subprocessos_id_subprocesso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_subprocessos_id_subprocesso_seq OWNER TO postgres;

--
-- TOC entry 5148 (class 0 OID 0)
-- Dependencies: 220
-- Name: tb_subprocessos_id_subprocesso_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_subprocessos_id_subprocesso_seq OWNED BY public.tb_subprocessos.id_subprocesso;


--
-- TOC entry 256 (class 1259 OID 172109)
-- Name: tb_tipo_tratamento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_tipo_tratamento (
    id_tipo_tratamento integer NOT NULL,
    codigo character varying(20) NOT NULL,
    descricao text NOT NULL,
    descricao_detalhada text
);


ALTER TABLE public.tb_tipo_tratamento OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 172108)
-- Name: tb_tipo_tratamento_id_tipo_tratamento_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_tipo_tratamento_id_tipo_tratamento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_tipo_tratamento_id_tipo_tratamento_seq OWNER TO postgres;

--
-- TOC entry 5149 (class 0 OID 0)
-- Dependencies: 255
-- Name: tb_tipo_tratamento_id_tipo_tratamento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_tipo_tratamento_id_tipo_tratamento_seq OWNED BY public.tb_tipo_tratamento.id_tipo_tratamento;


--
-- TOC entry 4833 (class 2604 OID 172134)
-- Name: tb_area_responsavel id_area; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_area_responsavel ALTER COLUMN id_area SET DEFAULT nextval('public.tb_area_responsavel_id_area_seq'::regclass);


--
-- TOC entry 4808 (class 2604 OID 171620)
-- Name: tb_categorias id_categoria; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_categorias ALTER COLUMN id_categoria SET DEFAULT nextval('public.tb_categorias_id_categoria_seq'::regclass);


--
-- TOC entry 4809 (class 2604 OID 171629)
-- Name: tb_causas id_causa; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_causas ALTER COLUMN id_causa SET DEFAULT nextval('public.tb_causas_id_causa_seq'::regclass);


--
-- TOC entry 4810 (class 2604 OID 171640)
-- Name: tb_consequencias id_consequencia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consequencias ALTER COLUMN id_consequencia SET DEFAULT nextval('public.tb_consequencias_id_consequencia_seq'::regclass);


--
-- TOC entry 4818 (class 2604 OID 171853)
-- Name: tb_controles_existentes id_controle; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_controles_existentes ALTER COLUMN id_controle SET DEFAULT nextval('public.tb_controles_existentes_id_controle_seq'::regclass);


--
-- TOC entry 4820 (class 2604 OID 171888)
-- Name: tb_execucao_controle id_execucao_controle; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_execucao_controle ALTER COLUMN id_execucao_controle SET DEFAULT nextval('public.tb_execucao_controle_id_execucao_controle_seq'::regclass);


--
-- TOC entry 4827 (class 2604 OID 171997)
-- Name: tb_indicador id_indicador; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_indicador ALTER COLUMN id_indicador SET DEFAULT nextval('public.tb_indicador_id_indicador_seq'::regclass);


--
-- TOC entry 4825 (class 2604 OID 171977)
-- Name: tb_meta_estrategica id_meta; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_meta_estrategica ALTER COLUMN id_meta SET DEFAULT nextval('public.tb_meta_estrategica_id_meta_seq'::regclass);


--
-- TOC entry 4823 (class 2604 OID 171962)
-- Name: tb_objetivo_estrategico id_objetivo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_objetivo_estrategico ALTER COLUMN id_objetivo SET DEFAULT nextval('public.tb_objetivo_estrategico_id_objetivo_seq'::regclass);


--
-- TOC entry 4834 (class 2604 OID 172145)
-- Name: tb_plano_tratamento id_plano; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_plano_tratamento ALTER COLUMN id_plano SET DEFAULT nextval('public.tb_plano_tratamento_id_plano_seq'::regclass);


--
-- TOC entry 4806 (class 2604 OID 171599)
-- Name: tb_processos id_processo; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_processos ALTER COLUMN id_processo SET DEFAULT nextval('public.tb_processos_id_processo_seq'::regclass);


--
-- TOC entry 4816 (class 2604 OID 171836)
-- Name: tb_risco_avaliacoes id_avaliacao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_avaliacoes ALTER COLUMN id_avaliacao SET DEFAULT nextval('public.tb_risco_avaliacoes_id_avaliacao_seq'::regclass);


--
-- TOC entry 4821 (class 2604 OID 171899)
-- Name: tb_risco_controle id_controle; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_controle ALTER COLUMN id_controle SET DEFAULT nextval('public.tb_risco_controle_id_controle_seq'::regclass);


--
-- TOC entry 4813 (class 2604 OID 171804)
-- Name: tb_risco_eventos id_evento; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_eventos ALTER COLUMN id_evento SET DEFAULT nextval('public.tb_risco_eventos_id_evento_seq'::regclass);


--
-- TOC entry 4829 (class 2604 OID 172017)
-- Name: tb_risco_meta id_risco_meta; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_meta ALTER COLUMN id_risco_meta SET DEFAULT nextval('public.tb_risco_meta_id_risco_meta_seq'::regclass);


--
-- TOC entry 4811 (class 2604 OID 171708)
-- Name: tb_risco_selecionado id_risco_selecionado; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_selecionado ALTER COLUMN id_risco_selecionado SET DEFAULT nextval('public.tb_risco_selecionado_id_risco_selecionado_seq'::regclass);


--
-- TOC entry 4819 (class 2604 OID 171877)
-- Name: tb_situacao_controle id_situacao_controle; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_situacao_controle ALTER COLUMN id_situacao_controle SET DEFAULT nextval('public.tb_situacao_controle_id_situacao_controle_seq'::regclass);


--
-- TOC entry 4832 (class 2604 OID 172123)
-- Name: tb_status_plano id_status; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_status_plano ALTER COLUMN id_status SET DEFAULT nextval('public.tb_status_plano_id_status_seq'::regclass);


--
-- TOC entry 4815 (class 2604 OID 171824)
-- Name: tb_subcategorias id_subcategoria; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_subcategorias ALTER COLUMN id_subcategoria SET DEFAULT nextval('public.tb_subcategorias_id_subcategoria_seq'::regclass);


--
-- TOC entry 4807 (class 2604 OID 171608)
-- Name: tb_subprocessos id_subprocesso; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_subprocessos ALTER COLUMN id_subprocesso SET DEFAULT nextval('public.tb_subprocessos_id_subprocesso_seq'::regclass);


--
-- TOC entry 4831 (class 2604 OID 172112)
-- Name: tb_tipo_tratamento id_tipo_tratamento; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_tipo_tratamento ALTER COLUMN id_tipo_tratamento SET DEFAULT nextval('public.tb_tipo_tratamento_id_tipo_tratamento_seq'::regclass);


--
-- TOC entry 4905 (class 2606 OID 172140)
-- Name: tb_area_responsavel tb_area_responsavel_nome_area_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_area_responsavel
    ADD CONSTRAINT tb_area_responsavel_nome_area_key UNIQUE (nome_area);


--
-- TOC entry 4907 (class 2606 OID 172138)
-- Name: tb_area_responsavel tb_area_responsavel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_area_responsavel
    ADD CONSTRAINT tb_area_responsavel_pkey PRIMARY KEY (id_area);


--
-- TOC entry 4849 (class 2606 OID 171624)
-- Name: tb_categorias tb_categorias_nome_categoria_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_categorias
    ADD CONSTRAINT tb_categorias_nome_categoria_key UNIQUE (nome_categoria);


--
-- TOC entry 4851 (class 2606 OID 171622)
-- Name: tb_categorias tb_categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_categorias
    ADD CONSTRAINT tb_categorias_pkey PRIMARY KEY (id_categoria);


--
-- TOC entry 4853 (class 2606 OID 171635)
-- Name: tb_causas tb_causas_descricao_causa_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_causas
    ADD CONSTRAINT tb_causas_descricao_causa_key UNIQUE (descricao_causa);


--
-- TOC entry 4855 (class 2606 OID 171633)
-- Name: tb_causas tb_causas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_causas
    ADD CONSTRAINT tb_causas_pkey PRIMARY KEY (id_causa);


--
-- TOC entry 4857 (class 2606 OID 171646)
-- Name: tb_consequencias tb_consequencias_descricao_consequencia_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consequencias
    ADD CONSTRAINT tb_consequencias_descricao_consequencia_key UNIQUE (descricao_consequencia);


--
-- TOC entry 4859 (class 2606 OID 171644)
-- Name: tb_consequencias tb_consequencias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consequencias
    ADD CONSTRAINT tb_consequencias_pkey PRIMARY KEY (id_consequencia);


--
-- TOC entry 4875 (class 2606 OID 171855)
-- Name: tb_controles_existentes tb_controles_existentes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_controles_existentes
    ADD CONSTRAINT tb_controles_existentes_pkey PRIMARY KEY (id_controle);


--
-- TOC entry 4841 (class 2606 OID 171594)
-- Name: tb_empresas tb_empresas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_empresas
    ADD CONSTRAINT tb_empresas_pkey PRIMARY KEY (id_empresa);


--
-- TOC entry 4881 (class 2606 OID 171894)
-- Name: tb_execucao_controle tb_execucao_controle_descricao_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_execucao_controle
    ADD CONSTRAINT tb_execucao_controle_descricao_key UNIQUE (descricao);


--
-- TOC entry 4883 (class 2606 OID 171892)
-- Name: tb_execucao_controle tb_execucao_controle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_execucao_controle
    ADD CONSTRAINT tb_execucao_controle_pkey PRIMARY KEY (id_execucao_controle);


--
-- TOC entry 4891 (class 2606 OID 172002)
-- Name: tb_indicador tb_indicador_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_indicador
    ADD CONSTRAINT tb_indicador_pkey PRIMARY KEY (id_indicador);


--
-- TOC entry 4889 (class 2606 OID 171982)
-- Name: tb_meta_estrategica tb_meta_estrategica_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_meta_estrategica
    ADD CONSTRAINT tb_meta_estrategica_pkey PRIMARY KEY (id_meta);


--
-- TOC entry 4887 (class 2606 OID 171967)
-- Name: tb_objetivo_estrategico tb_objetivo_estrategico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_objetivo_estrategico
    ADD CONSTRAINT tb_objetivo_estrategico_pkey PRIMARY KEY (id_objetivo);


--
-- TOC entry 4909 (class 2606 OID 172150)
-- Name: tb_plano_tratamento tb_plano_tratamento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_plano_tratamento
    ADD CONSTRAINT tb_plano_tratamento_pkey PRIMARY KEY (id_plano);


--
-- TOC entry 4843 (class 2606 OID 171603)
-- Name: tb_processos tb_processos_nome_processo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_processos
    ADD CONSTRAINT tb_processos_nome_processo_key UNIQUE (nome_processo);


--
-- TOC entry 4845 (class 2606 OID 171601)
-- Name: tb_processos tb_processos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_processos
    ADD CONSTRAINT tb_processos_pkey PRIMARY KEY (id_processo);


--
-- TOC entry 4873 (class 2606 OID 171843)
-- Name: tb_risco_avaliacoes tb_risco_avaliacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_avaliacoes
    ADD CONSTRAINT tb_risco_avaliacoes_pkey PRIMARY KEY (id_avaliacao);


--
-- TOC entry 4863 (class 2606 OID 171678)
-- Name: tb_risco_causa tb_risco_causa_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_causa
    ADD CONSTRAINT tb_risco_causa_pkey PRIMARY KEY (id_risco, id_causa);


--
-- TOC entry 4865 (class 2606 OID 171693)
-- Name: tb_risco_consequencia tb_risco_consequencia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_consequencia
    ADD CONSTRAINT tb_risco_consequencia_pkey PRIMARY KEY (id_risco, id_consequencia);


--
-- TOC entry 4885 (class 2606 OID 171904)
-- Name: tb_risco_controle tb_risco_controle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_controle
    ADD CONSTRAINT tb_risco_controle_pkey PRIMARY KEY (id_controle);


--
-- TOC entry 4869 (class 2606 OID 171809)
-- Name: tb_risco_eventos tb_risco_eventos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_eventos
    ADD CONSTRAINT tb_risco_eventos_pkey PRIMARY KEY (id_evento);


--
-- TOC entry 4893 (class 2606 OID 172022)
-- Name: tb_risco_meta tb_risco_meta_id_empresa_id_risco_id_meta_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_meta
    ADD CONSTRAINT tb_risco_meta_id_empresa_id_risco_id_meta_key UNIQUE (id_empresa, id_risco, id_meta);


--
-- TOC entry 4895 (class 2606 OID 172020)
-- Name: tb_risco_meta tb_risco_meta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_meta
    ADD CONSTRAINT tb_risco_meta_pkey PRIMARY KEY (id_risco_meta);


--
-- TOC entry 4867 (class 2606 OID 171713)
-- Name: tb_risco_selecionado tb_risco_selecionado_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_selecionado
    ADD CONSTRAINT tb_risco_selecionado_pkey PRIMARY KEY (id_risco_selecionado);


--
-- TOC entry 4861 (class 2606 OID 171653)
-- Name: tb_riscos tb_riscos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_riscos
    ADD CONSTRAINT tb_riscos_pkey PRIMARY KEY (id_risco);


--
-- TOC entry 4877 (class 2606 OID 171883)
-- Name: tb_situacao_controle tb_situacao_controle_descricao_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_situacao_controle
    ADD CONSTRAINT tb_situacao_controle_descricao_key UNIQUE (descricao);


--
-- TOC entry 4879 (class 2606 OID 171881)
-- Name: tb_situacao_controle tb_situacao_controle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_situacao_controle
    ADD CONSTRAINT tb_situacao_controle_pkey PRIMARY KEY (id_situacao_controle);


--
-- TOC entry 4901 (class 2606 OID 172129)
-- Name: tb_status_plano tb_status_plano_descricao_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_status_plano
    ADD CONSTRAINT tb_status_plano_descricao_key UNIQUE (descricao);


--
-- TOC entry 4903 (class 2606 OID 172127)
-- Name: tb_status_plano tb_status_plano_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_status_plano
    ADD CONSTRAINT tb_status_plano_pkey PRIMARY KEY (id_status);


--
-- TOC entry 4871 (class 2606 OID 171826)
-- Name: tb_subcategorias tb_subcategorias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_subcategorias
    ADD CONSTRAINT tb_subcategorias_pkey PRIMARY KEY (id_subcategoria);


--
-- TOC entry 4847 (class 2606 OID 171610)
-- Name: tb_subprocessos tb_subprocessos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_subprocessos
    ADD CONSTRAINT tb_subprocessos_pkey PRIMARY KEY (id_subprocesso);


--
-- TOC entry 4897 (class 2606 OID 172118)
-- Name: tb_tipo_tratamento tb_tipo_tratamento_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_tipo_tratamento
    ADD CONSTRAINT tb_tipo_tratamento_codigo_key UNIQUE (codigo);


--
-- TOC entry 4899 (class 2606 OID 172116)
-- Name: tb_tipo_tratamento tb_tipo_tratamento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_tipo_tratamento
    ADD CONSTRAINT tb_tipo_tratamento_pkey PRIMARY KEY (id_tipo_tratamento);


--
-- TOC entry 4911 (class 2606 OID 171669)
-- Name: tb_riscos fk_categoria_risco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_riscos
    ADD CONSTRAINT fk_categoria_risco FOREIGN KEY (id_categoria) REFERENCES public.tb_categorias(id_categoria);


--
-- TOC entry 4925 (class 2606 OID 171827)
-- Name: tb_subcategorias fk_categoria_subcategoria; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_subcategorias
    ADD CONSTRAINT fk_categoria_subcategoria FOREIGN KEY (id_categoria) REFERENCES public.tb_categorias(id_categoria) ON DELETE CASCADE;


--
-- TOC entry 4917 (class 2606 OID 171684)
-- Name: tb_risco_causa fk_causa_rc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_causa
    ADD CONSTRAINT fk_causa_rc FOREIGN KEY (id_causa) REFERENCES public.tb_causas(id_causa);


--
-- TOC entry 4919 (class 2606 OID 171699)
-- Name: tb_risco_consequencia fk_consequencia_rcons; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_consequencia
    ADD CONSTRAINT fk_consequencia_rcons FOREIGN KEY (id_consequencia) REFERENCES public.tb_consequencias(id_consequencia);


--
-- TOC entry 4912 (class 2606 OID 171654)
-- Name: tb_riscos fk_empresa_risco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_riscos
    ADD CONSTRAINT fk_empresa_risco FOREIGN KEY (id_empresa) REFERENCES public.tb_empresas(id_empresa);


--
-- TOC entry 4938 (class 2606 OID 172166)
-- Name: tb_plano_tratamento fk_plano_area; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_plano_tratamento
    ADD CONSTRAINT fk_plano_area FOREIGN KEY (id_area_responsavel) REFERENCES public.tb_area_responsavel(id_area) ON DELETE RESTRICT;


--
-- TOC entry 4939 (class 2606 OID 172151)
-- Name: tb_plano_tratamento fk_plano_risco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_plano_tratamento
    ADD CONSTRAINT fk_plano_risco FOREIGN KEY (id_risco) REFERENCES public.tb_riscos(id_risco) ON DELETE RESTRICT;


--
-- TOC entry 4940 (class 2606 OID 172161)
-- Name: tb_plano_tratamento fk_plano_status; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_plano_tratamento
    ADD CONSTRAINT fk_plano_status FOREIGN KEY (id_status) REFERENCES public.tb_status_plano(id_status) ON DELETE RESTRICT;


--
-- TOC entry 4941 (class 2606 OID 172156)
-- Name: tb_plano_tratamento fk_plano_tipo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_plano_tratamento
    ADD CONSTRAINT fk_plano_tipo FOREIGN KEY (id_tipo_tratamento) REFERENCES public.tb_tipo_tratamento(id_tipo_tratamento) ON DELETE RESTRICT;


--
-- TOC entry 4910 (class 2606 OID 171611)
-- Name: tb_subprocessos fk_processo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_subprocessos
    ADD CONSTRAINT fk_processo FOREIGN KEY (id_processo) REFERENCES public.tb_processos(id_processo);


--
-- TOC entry 4913 (class 2606 OID 171659)
-- Name: tb_riscos fk_processo_risco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_riscos
    ADD CONSTRAINT fk_processo_risco FOREIGN KEY (id_processo) REFERENCES public.tb_processos(id_processo);


--
-- TOC entry 4926 (class 2606 OID 171844)
-- Name: tb_risco_avaliacoes fk_risco_avaliacao; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_avaliacoes
    ADD CONSTRAINT fk_risco_avaliacao FOREIGN KEY (id_risco) REFERENCES public.tb_riscos(id_risco) ON DELETE CASCADE;


--
-- TOC entry 4918 (class 2606 OID 171679)
-- Name: tb_risco_causa fk_risco_rc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_causa
    ADD CONSTRAINT fk_risco_rc FOREIGN KEY (id_risco) REFERENCES public.tb_riscos(id_risco);


--
-- TOC entry 4920 (class 2606 OID 171694)
-- Name: tb_risco_consequencia fk_risco_rcons; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_consequencia
    ADD CONSTRAINT fk_risco_rcons FOREIGN KEY (id_risco) REFERENCES public.tb_riscos(id_risco);


--
-- TOC entry 4914 (class 2606 OID 171856)
-- Name: tb_riscos fk_riscos_controle_m; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_riscos
    ADD CONSTRAINT fk_riscos_controle_m FOREIGN KEY (id_controle_m) REFERENCES public.tb_controles_existentes(id_controle) ON DELETE SET NULL;


--
-- TOC entry 4915 (class 2606 OID 171861)
-- Name: tb_riscos fk_riscos_controle_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_riscos
    ADD CONSTRAINT fk_riscos_controle_n FOREIGN KEY (id_controle_n) REFERENCES public.tb_controles_existentes(id_controle) ON DELETE SET NULL;


--
-- TOC entry 4916 (class 2606 OID 171664)
-- Name: tb_riscos fk_subprocesso_risco; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_riscos
    ADD CONSTRAINT fk_subprocesso_risco FOREIGN KEY (id_subprocesso) REFERENCES public.tb_subprocessos(id_subprocesso);


--
-- TOC entry 4933 (class 2606 OID 172003)
-- Name: tb_indicador tb_indicador_id_empresa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_indicador
    ADD CONSTRAINT tb_indicador_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES public.tb_empresas(id_empresa);


--
-- TOC entry 4934 (class 2606 OID 172008)
-- Name: tb_indicador tb_indicador_id_meta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_indicador
    ADD CONSTRAINT tb_indicador_id_meta_fkey FOREIGN KEY (id_meta) REFERENCES public.tb_meta_estrategica(id_meta);


--
-- TOC entry 4931 (class 2606 OID 171983)
-- Name: tb_meta_estrategica tb_meta_estrategica_id_empresa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_meta_estrategica
    ADD CONSTRAINT tb_meta_estrategica_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES public.tb_empresas(id_empresa);


--
-- TOC entry 4932 (class 2606 OID 171988)
-- Name: tb_meta_estrategica tb_meta_estrategica_id_objetivo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_meta_estrategica
    ADD CONSTRAINT tb_meta_estrategica_id_objetivo_fkey FOREIGN KEY (id_objetivo) REFERENCES public.tb_objetivo_estrategico(id_objetivo);


--
-- TOC entry 4930 (class 2606 OID 171968)
-- Name: tb_objetivo_estrategico tb_objetivo_estrategico_id_empresa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_objetivo_estrategico
    ADD CONSTRAINT tb_objetivo_estrategico_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES public.tb_empresas(id_empresa);


--
-- TOC entry 4927 (class 2606 OID 171915)
-- Name: tb_risco_controle tb_risco_controle_id_execucao_controle_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_controle
    ADD CONSTRAINT tb_risco_controle_id_execucao_controle_fkey FOREIGN KEY (id_execucao_controle) REFERENCES public.tb_execucao_controle(id_execucao_controle);


--
-- TOC entry 4928 (class 2606 OID 171905)
-- Name: tb_risco_controle tb_risco_controle_id_risco_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_controle
    ADD CONSTRAINT tb_risco_controle_id_risco_fkey FOREIGN KEY (id_risco) REFERENCES public.tb_riscos(id_risco);


--
-- TOC entry 4929 (class 2606 OID 171910)
-- Name: tb_risco_controle tb_risco_controle_id_situacao_controle_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_controle
    ADD CONSTRAINT tb_risco_controle_id_situacao_controle_fkey FOREIGN KEY (id_situacao_controle) REFERENCES public.tb_situacao_controle(id_situacao_controle);


--
-- TOC entry 4923 (class 2606 OID 171815)
-- Name: tb_risco_eventos tb_risco_eventos_id_empresa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_eventos
    ADD CONSTRAINT tb_risco_eventos_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES public.tb_empresas(id_empresa) ON DELETE CASCADE;


--
-- TOC entry 4924 (class 2606 OID 171810)
-- Name: tb_risco_eventos tb_risco_eventos_id_risco_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_eventos
    ADD CONSTRAINT tb_risco_eventos_id_risco_fkey FOREIGN KEY (id_risco) REFERENCES public.tb_riscos(id_risco) ON DELETE CASCADE;


--
-- TOC entry 4935 (class 2606 OID 172023)
-- Name: tb_risco_meta tb_risco_meta_id_empresa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_meta
    ADD CONSTRAINT tb_risco_meta_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES public.tb_empresas(id_empresa);


--
-- TOC entry 4936 (class 2606 OID 172033)
-- Name: tb_risco_meta tb_risco_meta_id_meta_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_meta
    ADD CONSTRAINT tb_risco_meta_id_meta_fkey FOREIGN KEY (id_meta) REFERENCES public.tb_meta_estrategica(id_meta);


--
-- TOC entry 4937 (class 2606 OID 172028)
-- Name: tb_risco_meta tb_risco_meta_id_risco_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_meta
    ADD CONSTRAINT tb_risco_meta_id_risco_fkey FOREIGN KEY (id_risco) REFERENCES public.tb_riscos(id_risco);


--
-- TOC entry 4921 (class 2606 OID 171714)
-- Name: tb_risco_selecionado tb_risco_selecionado_id_empresa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_selecionado
    ADD CONSTRAINT tb_risco_selecionado_id_empresa_fkey FOREIGN KEY (id_empresa) REFERENCES public.tb_empresas(id_empresa);


--
-- TOC entry 4922 (class 2606 OID 171719)
-- Name: tb_risco_selecionado tb_risco_selecionado_id_risco_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_risco_selecionado
    ADD CONSTRAINT tb_risco_selecionado_id_risco_fkey FOREIGN KEY (id_risco) REFERENCES public.tb_riscos(id_risco);


-- Completed on 2025-05-08 10:33:48

--
-- PostgreSQL database dump complete
--

