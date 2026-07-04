Title: AI-Powered Customer Support Chatbot
Date: 2026-07-04
Tags: python, ai, streamlit
Summary: A customer support assistant with sentiment detection and automatic human hand-off, running on a free local AI model.

A customer support chatbot with a real persona, sentiment detection on every
message, and automatic hand-off to a human agent when a conversation needs
one -- available as both a web chat and a terminal channel.

## How it works

- A local AI model (Ollama, `llama3.2:3b`) drives the conversation -- no
  account, no API key, no cost
- Structured outputs return a reply, a sentiment classification, and a
  handoff recommendation from a single model call
- Personalizes responses using consented customer account data, never
  invented specifics
- Escalates to a human on anger, explicit requests for a person, or
  repeated unresolved issues, logging a full transcript for review
- One conversation engine powers two channels -- web chat and terminal --
  proving the bot logic isn't tied to a single interface

## Stack

Python, Ollama, Streamlit, Pydantic.
