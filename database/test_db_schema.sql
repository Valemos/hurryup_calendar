--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.4

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Event; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Event" (
    id integer NOT NULL,
    user_id integer,
    time_start timestamp without time zone NOT NULL,
    time_end timestamp without time zone NOT NULL,
    name character varying(64) NOT NULL,
    description text,
    event_group_id integer,
    done boolean
);


ALTER TABLE public."Event" OWNER TO postgres;

--
-- Name: EventGroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."EventGroup" (
    id integer NOT NULL,
    user_id integer,
    name character varying(64) NOT NULL,
    description text,
    done boolean
);


ALTER TABLE public."EventGroup" OWNER TO postgres;

--
-- Name: EventGroup_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."EventGroup_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."EventGroup_id_seq" OWNER TO postgres;

--
-- Name: EventGroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."EventGroup_id_seq" OWNED BY public."EventGroup".id;


--
-- Name: EventParametric; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."EventParametric" (
    id integer NOT NULL,
    user_id integer,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    description text,
    patern_id integer
);


ALTER TABLE public."EventParametric" OWNER TO postgres;

--
-- Name: EventParametric_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."EventParametric_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."EventParametric_id_seq" OWNER TO postgres;

--
-- Name: EventParametric_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."EventParametric_id_seq" OWNED BY public."EventParametric".id;


--
-- Name: EventParticipants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."EventParticipants" (
    event_id integer,
    user_id integer
);


ALTER TABLE public."EventParticipants" OWNER TO postgres;

--
-- Name: EventPattern; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."EventPattern" (
    id integer NOT NULL,
    user_id integer,
    name character varying(64) NOT NULL,
    description text
);


ALTER TABLE public."EventPattern" OWNER TO postgres;

--
-- Name: EventPattern_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."EventPattern_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."EventPattern_id_seq" OWNER TO postgres;

--
-- Name: EventPattern_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."EventPattern_id_seq" OWNED BY public."EventPattern".id;


--
-- Name: Event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Event_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Event_id_seq" OWNER TO postgres;

--
-- Name: Event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Event_id_seq" OWNED BY public."Event".id;


--
-- Name: User; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."User" (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    login character varying(128) NOT NULL,
    email character varying(128) NOT NULL,
    password_hash character varying(256) NOT NULL,
    account_type integer DEFAULT 0,
    image_url text
);


ALTER TABLE public."User" OWNER TO postgres;

--
-- Name: User_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."User_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."User_id_seq" OWNER TO postgres;

--
-- Name: User_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."User_id_seq" OWNED BY public."User".id;


--
-- Name: Event id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event" ALTER COLUMN id SET DEFAULT nextval('public."Event_id_seq"'::regclass);


--
-- Name: EventGroup id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventGroup" ALTER COLUMN id SET DEFAULT nextval('public."EventGroup_id_seq"'::regclass);


--
-- Name: EventParametric id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventParametric" ALTER COLUMN id SET DEFAULT nextval('public."EventParametric_id_seq"'::regclass);


--
-- Name: EventPattern id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventPattern" ALTER COLUMN id SET DEFAULT nextval('public."EventPattern_id_seq"'::regclass);


--
-- Name: User id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User" ALTER COLUMN id SET DEFAULT nextval('public."User_id_seq"'::regclass);


--
-- Name: EventGroup EventGroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventGroup"
    ADD CONSTRAINT "EventGroup_pkey" PRIMARY KEY (id);


--
-- Name: EventParametric EventParametric_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventParametric"
    ADD CONSTRAINT "EventParametric_pkey" PRIMARY KEY (id);


--
-- Name: EventPattern EventPattern_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventPattern"
    ADD CONSTRAINT "EventPattern_pkey" PRIMARY KEY (id);


--
-- Name: Event Event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_pkey" PRIMARY KEY (id);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- Name: EventGroup EventGroup_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventGroup"
    ADD CONSTRAINT "EventGroup_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id);


--
-- Name: EventParametric EventParametric_patern_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventParametric"
    ADD CONSTRAINT "EventParametric_patern_id_fkey" FOREIGN KEY (patern_id) REFERENCES public."EventPattern"(id);


--
-- Name: EventParametric EventParametric_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventParametric"
    ADD CONSTRAINT "EventParametric_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id);


--
-- Name: EventParticipants EventParticipants_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventParticipants"
    ADD CONSTRAINT "EventParticipants_event_id_fkey" FOREIGN KEY (event_id) REFERENCES public."Event"(id);


--
-- Name: EventParticipants EventParticipants_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventParticipants"
    ADD CONSTRAINT "EventParticipants_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id);


--
-- Name: EventPattern EventPattern_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."EventPattern"
    ADD CONSTRAINT "EventPattern_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id);


--
-- Name: Event Event_event_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_event_group_id_fkey" FOREIGN KEY (event_group_id) REFERENCES public."EventGroup"(id);


--
-- Name: Event Event_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Event"
    ADD CONSTRAINT "Event_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id);


--
-- PostgreSQL database dump complete
--

