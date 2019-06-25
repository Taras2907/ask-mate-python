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
-- Name: answer; Type: TABLE; Schema: public; Owner: dmk
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text
);


ALTER TABLE public.answer OWNER TO dmk;

--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: dmk
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answer_id_seq OWNER TO dmk;

--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dmk
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: dmk
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer
);


ALTER TABLE public.comment OWNER TO dmk;

--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: dmk
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_id_seq OWNER TO dmk;

--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dmk
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: dmk
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text
);


ALTER TABLE public.question OWNER TO dmk;

--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: dmk
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_id_seq OWNER TO dmk;

--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dmk
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: question_tag; Type: TABLE; Schema: public; Owner: dmk
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.question_tag OWNER TO dmk;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: dmk
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


ALTER TABLE public.tag OWNER TO dmk;

--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: dmk
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO dmk;

--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dmk
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: dmk
--

CREATE TABLE public.users (
    username text,
    password text,
    reputation integer,
    "timestamp" timestamp with time zone DEFAULT now()
);


ALTER TABLE public.users OWNER TO dmk;

--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: dmk
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image) FROM stdin;
1	2019-06-24 11:24:26	0	1	 WAFEEW FWA FWAE FWA  FAW FEW F	
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: dmk
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count) FROM stdin;
1	1	\N	F SAF WAFEWA FWA FA GFWAF AWFW EAF	2019-06-24 11:24:22	\N
2	\N	1	 EWAF WAFWAF GRAG WAEGTF 23WEGA A	2019-06-24 11:24:31	\N
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: dmk
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image) FROM stdin;
4	2019-06-24 13:54:32	0	0	wqew  ewqea rw 	3r2q3 r13 r1 43t13 t3 2 	\N
5	2019-06-24 13:54:39	0	0	242 142 412 421 34 1324 324 4	2134 214 12423 42 4214 124 24	\N
6	2019-06-24 13:54:46	0	0	faffaasfsefewaffe ae fergdas	fdqas fwae fwaesrf aef ergfewa f	\N
7	2019-06-24 13:54:56	0	0	sd fsa f saf waesfesa fwaer	 asefasf wse<rfwasfw sfe	\N
1	2019-06-24 11:24:16	15	0	A FEWAEFW FEWAFEWA FWA	 FWAFE WAFWAFAW EFEWA AWEREWA AW RA REWERWEFR	\N
\.


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: dmk
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
1	8
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: dmk
--

COPY public.tag (id, name) FROM stdin;
1	python
2	sql
3	css
4	html
5	c++
6	java
7	javascript
8	ruby
9	pycharm
10	whatever
11	david
12	food
13	.NET
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dmk
--

COPY public.users (username, password, reputation, "timestamp") FROM stdin;
rafal	asdasdadasd	15	2019-06-25 11:24:15.204552+02
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dmk
--

SELECT pg_catalog.setval('public.answer_id_seq', 2, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dmk
--

SELECT pg_catalog.setval('public.comment_id_seq', 2, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dmk
--

SELECT pg_catalog.setval('public.question_id_seq', 2, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dmk
--

SELECT pg_catalog.setval('public.tag_id_seq', 5, true);


--
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id) ON DELETE CASCADE;


--
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id) ON DELETE CASCADE;


--
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: dmk
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- PostgreSQL database dump complete
--

