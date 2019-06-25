--
-- PostgreSQL database dump
--

-- Dumped from database version 10.8 (Ubuntu 10.8-0ubuntu0.18.10.1)
-- Dumped by pg_dump version 10.8 (Ubuntu 10.8-0ubuntu0.18.10.1)

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: applicants; Type: TABLE; Schema: public; Owner: dmk
--

CREATE TABLE public.applicants (
    id integer NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    phone_number character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    application_code integer NOT NULL
);


ALTER TABLE public.applicants OWNER TO dmk;

--
-- Name: applicants_id_seq; Type: SEQUENCE; Schema: public; Owner: dmk
--

CREATE SEQUENCE public.applicants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.applicants_id_seq OWNER TO dmk;

--
-- Name: applicants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dmk
--

ALTER SEQUENCE public.applicants_id_seq OWNED BY public.applicants.id;


--
-- Name: mentors; Type: TABLE; Schema: public; Owner: dmk
--

CREATE TABLE public.mentors (
    id integer NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    nick_name character varying(255),
    phone_number character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    city character varying(255) NOT NULL,
    favourite_number integer
);


ALTER TABLE public.mentors OWNER TO dmk;

--
-- Name: mentors_id_seq; Type: SEQUENCE; Schema: public; Owner: dmk
--

CREATE SEQUENCE public.mentors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mentors_id_seq OWNER TO dmk;

--
-- Name: mentors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dmk
--

ALTER SEQUENCE public.mentors_id_seq OWNED BY public.mentors.id;


--
-- Name: test; Type: TABLE; Schema: public; Owner: dmk
--

CREATE TABLE public.test (
    id integer NOT NULL,
    num integer,
    data character varying
);


ALTER TABLE public.test OWNER TO dmk;

--
-- Name: test_id_seq; Type: SEQUENCE; Schema: public; Owner: dmk
--

CREATE SEQUENCE public.test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_id_seq OWNER TO dmk;

--
-- Name: test_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dmk
--

ALTER SEQUENCE public.test_id_seq OWNED BY public.test.id;


--
-- Name: applicants id; Type: DEFAULT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.applicants ALTER COLUMN id SET DEFAULT nextval('public.applicants_id_seq'::regclass);


--
-- Name: mentors id; Type: DEFAULT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.mentors ALTER COLUMN id SET DEFAULT nextval('public.mentors_id_seq'::regclass);


--
-- Name: test id; Type: DEFAULT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.test ALTER COLUMN id SET DEFAULT nextval('public.test_id_seq'::regclass);


--
-- Data for Name: applicants; Type: TABLE DATA; Schema: public; Owner: dmk
--

COPY public.applicants (id, first_name, last_name, phone_number, email, application_code) FROM stdin;
1	Dominique	Williams	003630/734-4926	dolor@laoreet.co.uk	61823
2	Jemima	Foreman	003620/834-6898	magna@etultrices.net	58324
3	Zeph	Massey	003630/216-5351	a.feugiat.tellus@montesnasceturridiculus.co.uk	61349
4	Joseph	Crawford	003670/923-2669	lacinia.mattis@arcu.co.uk	12916
5	Ifeoma	Bird	003630/465-8994	diam.duis.mi@orcitinciduntadipiscing.com	65603
6	Arsenio	Matthews	003620/804-1652	semper.pretium.neque@mauriseu.net	39220
7	Jemima	Cantu	003620/423-4261	et.risus.quisque@mollis.co.uk	10384
8	Carol	Arnold	003630/179-1827	dapibus.rutrum@litoratorquent.com	70730
9	Jane	Forbes	003670/653-5392	janiebaby@adipiscingenimmi.edu	56882
10	Ursa	William	003620/496-7064	malesuada@mauriseu.net	91220
\.


--
-- Data for Name: mentors; Type: TABLE DATA; Schema: public; Owner: dmk
--

COPY public.mentors (id, first_name, last_name, nick_name, phone_number, email, city, favourite_number) FROM stdin;
2	Pál	Monoczki	Pali	003630/327-2663	pal.monoczki@codecool.com	Miskolc	\N
3	Sándor	Szodoray	Szodi	003620/519-9152	sandor.szodoray@codecool.com	Miskolc	7
4	Dániel	Salamon	Dani	003620/508-0706	daniel.salamon@codecool.com	Budapest	4
5	Miklós	Beöthy	Miki	003630/256-8118	miklos.beothy@codecool.com	Budapest	42
6	Tamás	Tompa	Tomi	003630/370-0748	tamas.tompa@codecool.com	Budapest	42
7	Mateusz	Ostafil	Mateusz	003648/518-664-923	mateusz.ostafil@codecool.com	Krakow	13
8	Anikó	Fenyvesi	Anikó	003670/111-2222	aniko.fenyvesi@codecool.com	Budapest	11
9	Immánuel	Fodor	Immi	003620/123-6234	immanuel.fodor@codecool.com	Budapest	3
10	László	Molnár	Laci	003620/222-5566	laszlo.molnar@codecool.com	Budapest	5
11	Mátyás	Forián Szabó	Matyi	003630/111-5532	matyas.forian.szabo@codecool.com	Budapest	90
12	Zoltán	Sallay	Zozi	003670/898-3122	zoltan.sallay@codecool.com	Budapest	5
13	Szilveszter	Erdős	Sly	003620/444-5555	szilveszter.erdos@codecool.com	Budapest	13
14	László	Terray	Laci	003670/402-2435	laszlo.terray@codecool.com	Budapest	8
15	Árpád	Törzsök	Árpád	003630/222-1221	arpad.torzsok@codecool.com	Budapest	9
16	Imre	Lindi	Imi	003670/222-1233	imre.lindi@codecool.com	Miskolc	3
17	Róbert	Kohányi	Robi	003630/123-5553	robert.kohanyi@codecool.com	Miskolc	\N
18	Przemysław	Ciąćka	Przemek	003670/222-4554	przemyslaw.ciacka@codecool.com	Krakow	55
19	Marcin	Izworski	Marcin	003670/999-2323	marcin.izworski@codecool.com	Krakow	55
20	Rafał	Stępień	Rafal	003630/323-5343	rafal.stepien@codecool.com	Krakow	3
21	Agnieszka	Koszany	Agi	003630/111-5343	agnieszka.koszany@codecool.com	Krakow	77
22	Mateusz	Steliga	Mateusz	003630/123-5343	mateusz.steliga@codecool.com	Krakow	5
23	Bence	Fábián	Benec	003620/123-7654	bence.fabian@codecool.com	Budapest	\N
1	Attila	Molnár	Atesz	003670/630-0539	attila.molnar@codecool.com	Budapest	23
\.


--
-- Data for Name: test; Type: TABLE DATA; Schema: public; Owner: dmk
--

COPY public.test (id, num, data) FROM stdin;
1	100	First row
2	100	Second row
\.


--
-- Name: applicants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dmk
--

SELECT pg_catalog.setval('public.applicants_id_seq', 10, true);


--
-- Name: mentors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dmk
--

SELECT pg_catalog.setval('public.mentors_id_seq', 22, true);


--
-- Name: test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dmk
--

SELECT pg_catalog.setval('public.test_id_seq', 2, true);


--
-- Name: applicants applicants_application_code_key; Type: CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.applicants
    ADD CONSTRAINT applicants_application_code_key UNIQUE (application_code);


--
-- Name: applicants applicants_pkey; Type: CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.applicants
    ADD CONSTRAINT applicants_pkey PRIMARY KEY (id);


--
-- Name: mentors mentors_pkey; Type: CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.mentors
    ADD CONSTRAINT mentors_pkey PRIMARY KEY (id);


--
-- Name: test test_pkey; Type: CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.test
    ADD CONSTRAINT test_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

