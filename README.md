# Ollama Blog Generator with CrewAI on Mesop

This project demonstrates how to use the `CrewAI` framework to automate the process of generating blog posts using a collaborative approach between two AI agents: a Tech Writer and a Tech Researcher. The agents leverage the `ChatOpenAI` language model to generate and iterate on content, managed within a Mesop web application.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Components](#components)
  - [Agents](#agents)
  - [Tasks](#tasks)
  - [Crew](#crew)
  - [Mesop Application](#mesop-application)
- [Customization](#customization)
- [Other](#other)

## Overview

This repository contains a Python project that creates a web application using Mesop, where users can generate short blog posts about a given topic. The application is powered by CrewAI, which manages the collaboration between two specialized agents: a Tech Writer and a Tech Researcher.

The Tech Researcher gathers key points, keywords, and trends on the given topic, while the Tech Writer crafts a blog post based on the research. The project uses the `llama3.1` model hosted locally.

## Requirements

- Python 3.11
- Mesop
- CrewAI
- langchain_openai
- Ollama LLM hosted locally

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rapidarchitect/ollama-crew-mesop.git
   cd ollama-crew-mesop
   ```
2. Install the required python packages
   ```bash
    pip install -r requirements.txt
    ```
3. Pull llama3.1 for ollama (NOTE: Ollama must already be installed, if not see https://ollama.ai)
   ```bash
    ollama pull llama3.1
    ```

## Usage
1. Run the mesop server:
   ```bash
   mesop ollama_crew.py
   ```
2. Open your browser to the link provided by mesop

3. Enter a topic to write a blog post about

## Components

### Agents
    Tech Writer: Responsible for writing and iterating a high-quality blog post.

    Tech Researcher: Focuses on gathering keywords, key points, and trends for the given topic.

### Tasks
    Task 1: The Researcher lists relevant keywords, key points, and trends.

    Task 2: The Writer creates a blog post based on the research.

### Crew
The Crew class manages the execution of tasks in a sequential process, ensuring the output from the researcher is used by the writer to generate a blog post.

## Mesop Application
The application uses the Mesop framework to create a web interface where users can input a topic and view the generated blog content. The state of agent messages is managed and displayed within the web interface.

## Customization
  - Agents: Modify the role, backstory, or goal attributes to adjust the behavior of the agents.
  - Tasks: Customize the task descriptions to change the focus of research or writing.
  - Model: Replace llama3.1 with another model supported by Ollama.

  ## Other
  Three additional scripts are included for educational purposes, an OpenAI version of the same app, a cli version and a simple crewAI example using a math professor