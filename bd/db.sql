--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.4

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: user_admin
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO user_admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: clientes; Type: TABLE; Schema: public; Owner: user_admin
--

CREATE TABLE public.clientes (
    cliente_id integer NOT NULL,
    cliente_nacionalidad character varying NOT NULL,
    cliente_cedula integer NOT NULL,
    cliente_nombre text NOT NULL,
    cliente_apellido text NOT NULL,
    cliente_telefono text,
    cliente_direccion text
);


ALTER TABLE public.clientes OWNER TO user_admin;

--
-- Name: clientes_cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: user_admin
--

CREATE SEQUENCE public.clientes_cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clientes_cliente_id_seq OWNER TO user_admin;

--
-- Name: clientes_cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_admin
--

ALTER SEQUENCE public.clientes_cliente_id_seq OWNED BY public.clientes.cliente_id;


--
-- Name: detalles_ordenes_divisas; Type: TABLE; Schema: public; Owner: user_admin
--

CREATE TABLE public.detalles_ordenes_divisas (
    detalle_orden_divisa integer NOT NULL,
    orden_id integer NOT NULL,
    divisa_id integer NOT NULL,
    detalle_orden_divisa_cantidad double precision NOT NULL
);


ALTER TABLE public.detalles_ordenes_divisas OWNER TO user_admin;

--
-- Name: detalles_ordenes_divisas_detalle_orden_divisa_seq; Type: SEQUENCE; Schema: public; Owner: user_admin
--

CREATE SEQUENCE public.detalles_ordenes_divisas_detalle_orden_divisa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.detalles_ordenes_divisas_detalle_orden_divisa_seq OWNER TO user_admin;

--
-- Name: detalles_ordenes_divisas_detalle_orden_divisa_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_admin
--

ALTER SEQUENCE public.detalles_ordenes_divisas_detalle_orden_divisa_seq OWNED BY public.detalles_ordenes_divisas.detalle_orden_divisa;


--
-- Name: detalles_ordenes_platos; Type: TABLE; Schema: public; Owner: user_admin
--

CREATE TABLE public.detalles_ordenes_platos (
    detalle_orden_plato_id integer NOT NULL,
    orden_id integer NOT NULL,
    plato_id integer NOT NULL,
    detalle_orden_plato_cantidad integer NOT NULL
);


ALTER TABLE public.detalles_ordenes_platos OWNER TO user_admin;

--
-- Name: detalles_ordenes_platos_detalle_orden_plato_id_seq; Type: SEQUENCE; Schema: public; Owner: user_admin
--

CREATE SEQUENCE public.detalles_ordenes_platos_detalle_orden_plato_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.detalles_ordenes_platos_detalle_orden_plato_id_seq OWNER TO user_admin;

--
-- Name: detalles_ordenes_platos_detalle_orden_plato_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_admin
--

ALTER SEQUENCE public.detalles_ordenes_platos_detalle_orden_plato_id_seq OWNED BY public.detalles_ordenes_platos.detalle_orden_plato_id;


--
-- Name: divisas; Type: TABLE; Schema: public; Owner: user_admin
--

CREATE TABLE public.divisas (
    divisa_id integer NOT NULL,
    divisa_nombre text NOT NULL,
    divisa_relacion double precision NOT NULL
);


ALTER TABLE public.divisas OWNER TO user_admin;

--
-- Name: divisas_divisa_id_seq; Type: SEQUENCE; Schema: public; Owner: user_admin
--

CREATE SEQUENCE public.divisas_divisa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.divisas_divisa_id_seq OWNER TO user_admin;

--
-- Name: divisas_divisa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_admin
--

ALTER SEQUENCE public.divisas_divisa_id_seq OWNED BY public.divisas.divisa_id;


--
-- Name: mesas; Type: TABLE; Schema: public; Owner: user_admin
--

CREATE TABLE public.mesas (
    mesa_id integer NOT NULL,
    mesa_descripcion text NOT NULL
);


ALTER TABLE public.mesas OWNER TO user_admin;

--
-- Name: mesas_mesa_id_seq; Type: SEQUENCE; Schema: public; Owner: user_admin
--

CREATE SEQUENCE public.mesas_mesa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mesas_mesa_id_seq OWNER TO user_admin;

--
-- Name: mesas_mesa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_admin
--

ALTER SEQUENCE public.mesas_mesa_id_seq OWNED BY public.mesas.mesa_id;


--
-- Name: mesas_ocupadas; Type: TABLE; Schema: public; Owner: user_admin
--

CREATE TABLE public.mesas_ocupadas (
    mesa_id integer NOT NULL,
    orden_id integer NOT NULL
);


ALTER TABLE public.mesas_ocupadas OWNER TO user_admin;

--
-- Name: ordenes; Type: TABLE; Schema: public; Owner: user_admin
--

CREATE TABLE public.ordenes (
    orden_id integer NOT NULL,
    orden_fecha timestamp without time zone NOT NULL,
    mesa_id integer NOT NULL,
    cliente_id integer
);


ALTER TABLE public.ordenes OWNER TO user_admin;

--
-- Name: ordenes_orden_id_seq; Type: SEQUENCE; Schema: public; Owner: user_admin
--

CREATE SEQUENCE public.ordenes_orden_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ordenes_orden_id_seq OWNER TO user_admin;

--
-- Name: ordenes_orden_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_admin
--

ALTER SEQUENCE public.ordenes_orden_id_seq OWNED BY public.ordenes.orden_id;


--
-- Name: platos; Type: TABLE; Schema: public; Owner: user_admin
--

CREATE TABLE public.platos (
    plato_id integer NOT NULL,
    plato_nombre text NOT NULL,
    plato_descripcion text NOT NULL,
    plato_precio double precision NOT NULL,
    tipo_plato_id integer NOT NULL
);


ALTER TABLE public.platos OWNER TO user_admin;

--
-- Name: platos_plato_id_seq; Type: SEQUENCE; Schema: public; Owner: user_admin
--

CREATE SEQUENCE public.platos_plato_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.platos_plato_id_seq OWNER TO user_admin;

--
-- Name: platos_plato_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_admin
--

ALTER SEQUENCE public.platos_plato_id_seq OWNED BY public.platos.plato_id;


--
-- Name: tipos_platos; Type: TABLE; Schema: public; Owner: user_admin
--

CREATE TABLE public.tipos_platos (
    tipo_plato_id integer NOT NULL,
    tipo_plato_nombre text NOT NULL,
    tipo_plato_icon text
);


ALTER TABLE public.tipos_platos OWNER TO user_admin;

--
-- Name: tipos_platos_tipo_plato_id_seq; Type: SEQUENCE; Schema: public; Owner: user_admin
--

CREATE SEQUENCE public.tipos_platos_tipo_plato_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipos_platos_tipo_plato_id_seq OWNER TO user_admin;

--
-- Name: tipos_platos_tipo_plato_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_admin
--

ALTER SEQUENCE public.tipos_platos_tipo_plato_id_seq OWNED BY public.tipos_platos.tipo_plato_id;


--
-- Name: vista_platos; Type: VIEW; Schema: public; Owner: user_admin
--

CREATE VIEW public.vista_platos AS
 SELECT p.plato_id,
    p.plato_nombre,
    p.plato_descripcion,
    p.plato_precio,
    tp.tipo_plato_id,
    tp.tipo_plato_nombre
   FROM (public.platos p
     JOIN public.tipos_platos tp ON ((p.tipo_plato_id = tp.tipo_plato_id)));


ALTER VIEW public.vista_platos OWNER TO user_admin;

--
-- Name: clientes cliente_id; Type: DEFAULT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.clientes ALTER COLUMN cliente_id SET DEFAULT nextval('public.clientes_cliente_id_seq'::regclass);


--
-- Name: detalles_ordenes_divisas detalle_orden_divisa; Type: DEFAULT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.detalles_ordenes_divisas ALTER COLUMN detalle_orden_divisa SET DEFAULT nextval('public.detalles_ordenes_divisas_detalle_orden_divisa_seq'::regclass);


--
-- Name: detalles_ordenes_platos detalle_orden_plato_id; Type: DEFAULT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.detalles_ordenes_platos ALTER COLUMN detalle_orden_plato_id SET DEFAULT nextval('public.detalles_ordenes_platos_detalle_orden_plato_id_seq'::regclass);


--
-- Name: divisas divisa_id; Type: DEFAULT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.divisas ALTER COLUMN divisa_id SET DEFAULT nextval('public.divisas_divisa_id_seq'::regclass);


--
-- Name: mesas mesa_id; Type: DEFAULT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.mesas ALTER COLUMN mesa_id SET DEFAULT nextval('public.mesas_mesa_id_seq'::regclass);


--
-- Name: ordenes orden_id; Type: DEFAULT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.ordenes ALTER COLUMN orden_id SET DEFAULT nextval('public.ordenes_orden_id_seq'::regclass);


--
-- Name: platos plato_id; Type: DEFAULT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.platos ALTER COLUMN plato_id SET DEFAULT nextval('public.platos_plato_id_seq'::regclass);


--
-- Name: tipos_platos tipo_plato_id; Type: DEFAULT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.tipos_platos ALTER COLUMN tipo_plato_id SET DEFAULT nextval('public.tipos_platos_tipo_plato_id_seq'::regclass);


--
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: user_admin
--

COPY public.clientes (cliente_id, cliente_nacionalidad, cliente_cedula, cliente_nombre, cliente_apellido, cliente_telefono, cliente_direccion) FROM stdin;
\.


--
-- Data for Name: detalles_ordenes_divisas; Type: TABLE DATA; Schema: public; Owner: user_admin
--

COPY public.detalles_ordenes_divisas (detalle_orden_divisa, orden_id, divisa_id, detalle_orden_divisa_cantidad) FROM stdin;
\.


--
-- Data for Name: detalles_ordenes_platos; Type: TABLE DATA; Schema: public; Owner: user_admin
--

COPY public.detalles_ordenes_platos (detalle_orden_plato_id, orden_id, plato_id, detalle_orden_plato_cantidad) FROM stdin;
\.


--
-- Data for Name: divisas; Type: TABLE DATA; Schema: public; Owner: user_admin
--

COPY public.divisas (divisa_id, divisa_nombre, divisa_relacion) FROM stdin;
1	Dolar	1
2	Bolivar	36
3	COP	3700
\.


--
-- Data for Name: mesas; Type: TABLE DATA; Schema: public; Owner: user_admin
--

COPY public.mesas (mesa_id, mesa_descripcion) FROM stdin;
7	MESA 1
8	MESA 2
9	MESA 3
10	MESA 4
11	MESA 5
12	MESA 6
\.


--
-- Data for Name: mesas_ocupadas; Type: TABLE DATA; Schema: public; Owner: user_admin
--

COPY public.mesas_ocupadas (mesa_id, orden_id) FROM stdin;
\.


--
-- Data for Name: ordenes; Type: TABLE DATA; Schema: public; Owner: user_admin
--

COPY public.ordenes (orden_id, orden_fecha, mesa_id, cliente_id) FROM stdin;
\.


--
-- Data for Name: platos; Type: TABLE DATA; Schema: public; Owner: user_admin
--

COPY public.platos (plato_id, plato_nombre, plato_descripcion, plato_precio, tipo_plato_id) FROM stdin;
5	Carne	Carne frita de las mas arrechisima	13	1
6	Pollo	Pollo frito vale	10	1
7	Agua Panela	Ta fria mrk	1	2
8	Agua	Agua de la llave (no esta fria)	0.3	2
\.


--
-- Data for Name: tipos_platos; Type: TABLE DATA; Schema: public; Owner: user_admin
--

COPY public.tipos_platos (tipo_plato_id, tipo_plato_nombre, tipo_plato_icon) FROM stdin;
2	BEBIDA	cup-outline
1	COMIDA	bowl-outline
\.


--
-- Name: clientes_cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_admin
--

SELECT pg_catalog.setval('public.clientes_cliente_id_seq', 1, false);


--
-- Name: detalles_ordenes_divisas_detalle_orden_divisa_seq; Type: SEQUENCE SET; Schema: public; Owner: user_admin
--

SELECT pg_catalog.setval('public.detalles_ordenes_divisas_detalle_orden_divisa_seq', 1, false);


--
-- Name: detalles_ordenes_platos_detalle_orden_plato_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_admin
--

SELECT pg_catalog.setval('public.detalles_ordenes_platos_detalle_orden_plato_id_seq', 1, false);


--
-- Name: divisas_divisa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_admin
--

SELECT pg_catalog.setval('public.divisas_divisa_id_seq', 6, true);


--
-- Name: mesas_mesa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_admin
--

SELECT pg_catalog.setval('public.mesas_mesa_id_seq', 12, true);


--
-- Name: ordenes_orden_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_admin
--

SELECT pg_catalog.setval('public.ordenes_orden_id_seq', 1, false);


--
-- Name: platos_plato_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_admin
--

SELECT pg_catalog.setval('public.platos_plato_id_seq', 8, true);


--
-- Name: tipos_platos_tipo_plato_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_admin
--

SELECT pg_catalog.setval('public.tipos_platos_tipo_plato_id_seq', 2, true);


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (cliente_id);


--
-- Name: detalles_ordenes_divisas detalles_ordenes_divisas_pkey; Type: CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.detalles_ordenes_divisas
    ADD CONSTRAINT detalles_ordenes_divisas_pkey PRIMARY KEY (detalle_orden_divisa);


--
-- Name: detalles_ordenes_platos detalles_ordenes_platos_pkey; Type: CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.detalles_ordenes_platos
    ADD CONSTRAINT detalles_ordenes_platos_pkey PRIMARY KEY (detalle_orden_plato_id);


--
-- Name: divisas divisas_pkey; Type: CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.divisas
    ADD CONSTRAINT divisas_pkey PRIMARY KEY (divisa_id);


--
-- Name: mesas mesas_pkey; Type: CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.mesas
    ADD CONSTRAINT mesas_pkey PRIMARY KEY (mesa_id);


--
-- Name: ordenes ordenes_pkey; Type: CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_pkey PRIMARY KEY (orden_id);


--
-- Name: platos platos_pkey; Type: CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.platos
    ADD CONSTRAINT platos_pkey PRIMARY KEY (plato_id);


--
-- Name: tipos_platos tipos_platos_pkey; Type: CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.tipos_platos
    ADD CONSTRAINT tipos_platos_pkey PRIMARY KEY (tipo_plato_id);


--
-- Name: fki_mesas_ocupadas_mesa_id_fkey; Type: INDEX; Schema: public; Owner: user_admin
--

CREATE INDEX fki_mesas_ocupadas_mesa_id_fkey ON public.mesas_ocupadas USING btree (orden_id);


--
-- Name: detalles_ordenes_divisas detalles_ordenes_divisas_divisa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.detalles_ordenes_divisas
    ADD CONSTRAINT detalles_ordenes_divisas_divisa_id_fkey FOREIGN KEY (divisa_id) REFERENCES public.divisas(divisa_id);


--
-- Name: detalles_ordenes_divisas detalles_ordenes_divisas_orden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.detalles_ordenes_divisas
    ADD CONSTRAINT detalles_ordenes_divisas_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.ordenes(orden_id);


--
-- Name: detalles_ordenes_platos detalles_ordenes_platos_orden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.detalles_ordenes_platos
    ADD CONSTRAINT detalles_ordenes_platos_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.ordenes(orden_id);


--
-- Name: detalles_ordenes_platos detalles_ordenes_platos_plato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.detalles_ordenes_platos
    ADD CONSTRAINT detalles_ordenes_platos_plato_id_fkey FOREIGN KEY (plato_id) REFERENCES public.platos(plato_id);


--
-- Name: mesas_ocupadas mesas_ocupadas_mesa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.mesas_ocupadas
    ADD CONSTRAINT mesas_ocupadas_mesa_id_fkey FOREIGN KEY (mesa_id) REFERENCES public.mesas(mesa_id);


--
-- Name: mesas_ocupadas mesas_ocupadas_orden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.mesas_ocupadas
    ADD CONSTRAINT mesas_ocupadas_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.ordenes(orden_id);


--
-- Name: ordenes ordenes_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.clientes(cliente_id);


--
-- Name: ordenes ordenes_mesa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.ordenes
    ADD CONSTRAINT ordenes_mesa_id_fkey FOREIGN KEY (mesa_id) REFERENCES public.mesas(mesa_id);


--
-- Name: platos platos_tipo_plato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_admin
--

ALTER TABLE ONLY public.platos
    ADD CONSTRAINT platos_tipo_plato_id_fkey FOREIGN KEY (tipo_plato_id) REFERENCES public.tipos_platos(tipo_plato_id) NOT VALID;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: user_admin
--

GRANT USAGE ON SCHEMA public TO user_simple;


--
-- Name: SEQUENCE clientes_cliente_id_seq; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT ON SEQUENCE public.clientes_cliente_id_seq TO user_simple;


--
-- Name: SEQUENCE detalles_ordenes_divisas_detalle_orden_divisa_seq; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT ON SEQUENCE public.detalles_ordenes_divisas_detalle_orden_divisa_seq TO user_simple;


--
-- Name: TABLE detalles_ordenes_platos; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT,INSERT ON TABLE public.detalles_ordenes_platos TO user_simple;


--
-- Name: SEQUENCE detalles_ordenes_platos_detalle_orden_plato_id_seq; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT ON SEQUENCE public.detalles_ordenes_platos_detalle_orden_plato_id_seq TO user_simple;


--
-- Name: TABLE divisas; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT ON TABLE public.divisas TO user_simple;


--
-- Name: SEQUENCE divisas_divisa_id_seq; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT ON SEQUENCE public.divisas_divisa_id_seq TO user_simple;


--
-- Name: TABLE mesas; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT ON TABLE public.mesas TO user_simple;


--
-- Name: SEQUENCE mesas_mesa_id_seq; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT ON SEQUENCE public.mesas_mesa_id_seq TO user_simple;


--
-- Name: TABLE mesas_ocupadas; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT,INSERT,UPDATE ON TABLE public.mesas_ocupadas TO user_simple;


--
-- Name: TABLE ordenes; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT,INSERT ON TABLE public.ordenes TO user_simple;


--
-- Name: SEQUENCE ordenes_orden_id_seq; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT ON SEQUENCE public.ordenes_orden_id_seq TO user_simple;


--
-- Name: TABLE platos; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT ON TABLE public.platos TO user_simple;


--
-- Name: SEQUENCE platos_plato_id_seq; Type: ACL; Schema: public; Owner: user_admin
--

GRANT SELECT ON SEQUENCE public.platos_plato_id_seq TO user_simple;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO user_admin;


--
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO user_admin;


--
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO user_admin;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO user_admin;


--
-- PostgreSQL database dump complete
--

